#!/usr/bin/env python3
"""Bounded Google Scholar structured lookup with a Node-first transport.

The launcher intentionally owns only transport selection and safe parsing.  It
does not decide which candidate is the requested paper.  By default it makes
one request and emits one JSON record; it never rotates transports after an
explicit access restriction.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import os
import re
import subprocess
import tempfile
import time
from functools import lru_cache
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple
from urllib.parse import quote_plus, urljoin, urlparse


ROOT = "https://scholar.google.com"
DEFAULT_TIMEOUT_MS = 20_000
ACCESS_STATUSES = {401, 403, 407, 429, 503}
MAX_RESPONSE_BYTES = 8 * 1024 * 1024


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def clean_text(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None
    text = str(value)
    text = re.sub(r"<[^>]*>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def safe_link(value: Any) -> Optional[str]:
    """Resolve Scholar relative links, rejecting executable/non-web schemes."""
    if not isinstance(value, str) or not value.strip():
        return None
    value = html.unescape(value.strip())
    try:
        parsed = urlparse(value)
    except ValueError:
        return None
    if parsed.scheme and parsed.scheme.lower() not in {"http", "https"}:
        return None
    if value.startswith("//"):
        value = "https:" + value
    elif value.startswith("/"):
        value = urljoin(ROOT, value)
    elif not parsed.scheme:
        return None
    try:
        parsed = urlparse(value)
    except ValueError:
        return None
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc or parsed.username or parsed.password:
        return None
    return value


def valid_citing_link(value: Any) -> Optional[str]:
    link = safe_link(value)
    if not link:
        return None
    parsed = urlparse(link)
    from urllib.parse import parse_qs

    if parsed.netloc.lower() != "scholar.google.com" or parsed.path != "/scholar":
        return None
    cites = parse_qs(parsed.query).get("cites", [])
    if len(cites) != 1 or not re.fullmatch(r"[0-9]+", cites[0]):
        return None
    return link


def looks_like_captcha(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in ("captcha", "unusual traffic", "not a robot", "verify you are human", "recaptcha"))


def parse_charset(content_type: str) -> str:
    match = re.search(r"charset\s*=\s*[\"']?([^;\s\"']+)", content_type or "", re.I)
    charset = (match.group(1) if match else "utf-8").strip()
    # Keep declared encoding failures explicit instead of silently corrupting
    # author names and identity evidence.
    if charset.lower() in {"iso-8859-1", "latin1", "latin-1"}:
        return "iso-8859-1"
    return charset


def decode_body(body: bytes, content_type: str = "") -> Tuple[str, str]:
    charset = parse_charset(content_type)
    try:
        return body.decode(charset, errors="strict"), charset
    except LookupError as exc:
        raise ValueError(f"Unsupported response charset: {charset}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"Response cannot be decoded as {charset}: {exc}") from exc


def parse_citation(label: Optional[str]) -> Optional[int]:
    if not label:
        return None
    text = clean_text(label) or ""
    patterns = (
        r"^Cited\s+by\s+([0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)$",
        r"^被引用次数\s*[:：]?\s*([0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)$",
    )
    for pattern in patterns:
        match = re.match(pattern, text, re.I)
        if match:
            return int(match.group(1).replace(",", ""))
    return None


def _link_object(value: Any) -> Dict[str, Optional[str]]:
    if not isinstance(value, dict):
        return {"label": None, "url": None}
    return {"label": clean_text(value.get("l")), "url": safe_link(value.get("u"))}


def extract_candidates(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("r"), list):
        raise ValueError("Scholar response has no validated result array 'r'")
    candidates = []
    for row in payload["r"]:
        if not isinstance(row, dict):
            continue
        links = row.get("l") if isinstance(row.get("l"), dict) else {}
        citation = _link_object(links.get("c"))
        paper_link = safe_link(row.get("u"))
        citing_url = valid_citing_link(citation["url"])
        cluster_id = None
        if citing_url:
            from urllib.parse import parse_qs
            cluster_id = parse_qs(urlparse(citing_url).query).get("cites", [None])[0]
        full_text = _link_object(links.get("g"))
        candidates.append(
            {
                "title": clean_text(row.get("t")),
                "metadata": clean_text(row.get("m")),
                "snippet": clean_text(row.get("s")),
                "paper_url": paper_link,
                "citation_count": parse_citation(citation["label"]) if citing_url else None,
                "citation_label": citation["label"],
                "citing_url": citing_url,
                "cluster_id": str(cluster_id) if cluster_id is not None else None,
                "full_text": full_text,
                "related": _link_object(links.get("r")),
                "versions": _link_object(links.get("v")),
            }
        )
    return candidates


def parse_response(body: bytes, content_type: str = "") -> Tuple[list[dict[str, Any]], str]:
    if len(body) > MAX_RESPONSE_BYTES:
        raise ValueError("Scholar response exceeds the 8 MiB parsing limit")
    text, charset = decode_body(body, content_type)
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        if looks_like_captcha(text):
            raise PermissionError("Scholar response appears to be a CAPTCHA or access-verification page") from exc
        raise ValueError(f"Scholar response is not JSON: {exc.msg}") from exc
    return extract_candidates(payload), charset


def query_url(title: str, language: str) -> str:
    return f"{ROOT}/scholar?oi=gsr&q={quote_plus(title)}&output=gsb&hl={quote_plus(language)}"


def result_base(title: str, url: str, transport: str, started: str, elapsed_ms: int) -> dict[str, Any]:
    return {
        "status": "ok",
        "identity_status": "pending",
        "transport": transport,
        "query": title,
        "requested_url": url,
        "fetched_at": started,
        "elapsed_ms": elapsed_ms,
        "candidates": [],
    }


def error_result(title: str, url: str, status: str, message: str, transport: Optional[str] = None, **extra: Any) -> dict[str, Any]:
    result: dict[str, Any] = {"status": status, "query": title, "requested_url": url, "error": message}
    if transport:
        result["transport"] = transport
    result.update(extra)
    return result


def run_node(node: str, helper: Path, url: str, timeout_ms: int, fixture: Optional[Path], content_type: str = "") -> Tuple[dict[str, Any], int]:
    command = [node]
    supported, proxy_supported = preflight_node(node)
    if not supported:
        return error_result("", url, "tool_unavailable", "Node capabilities are unavailable", "node-fetch"), 1
    if proxy_supported:
        command.append("--use-env-proxy")
    command += [str(helper), "--url", url, "--timeout-ms", str(timeout_ms)]
    if fixture:
        command += ["--input-file", str(fixture)]
        if content_type:
            command += ["--input-content-type", content_type]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=(timeout_ms / 1000) + 5)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return error_result("", url, "transport_error", f"Node fetch launcher failed: {exc}", "node-fetch"), 1
    try:
        result = json.loads(completed.stdout)
        if not isinstance(result, dict):
            raise ValueError("Expected one JSON object")
    except ValueError:
        return error_result("", url, "transport_error", "Node helper did not emit one JSON result", "node-fetch"), 1
    if result.get("status") != "raw_ok":
        return result, completed.returncode
    try:
        body = base64.b64decode(result.pop("body_base64"), validate=True)
        candidates, charset = parse_response(body, result.get("content_type", ""))
    except PermissionError as exc:
        result.update({"status": "access_restricted", "error": str(exc)})
        result.pop("body_base64", None)
        return result, 1
    except (ValueError, KeyError, TypeError) as exc:
        result.update({"status": "invalid_response", "error": str(exc)})
        result.pop("body_base64", None)
        return result, 1
    result.update({"status": "ok", "identity_status": "pending", "charset": charset, "candidates": candidates})
    return result, 0


def run_curl(curl: str, title: str, url: str, timeout_ms: int, fixture: Optional[Path], content_type: str = "") -> Tuple[dict[str, Any], int]:
    started = now_iso()
    begin = time.monotonic()
    if fixture:
        try:
            body = fixture.read_bytes()
            candidates, charset = parse_response(body, content_type)
            result = result_base(title, url, "curl", started, int((time.monotonic() - begin) * 1000))
            result.update({"charset": charset, "http_status": 200, "content_type": "fixture", "candidates": candidates})
            return result, 0
        except PermissionError as exc:
            return error_result(title, url, "access_restricted", str(exc), "curl", http_status=200), 1
        except (OSError, ValueError) as exc:
            return error_result(title, url, "invalid_response", str(exc), "curl"), 1

    temp_name: Optional[str] = None
    header_name: Optional[str] = None
    http_status = 0
    try:
        with tempfile.NamedTemporaryFile(prefix="scholar-", suffix=".body", delete=False) as handle:
            temp_name = handle.name
        with tempfile.NamedTemporaryFile(prefix="scholar-", suffix=".headers", delete=False) as handle:
            header_name = handle.name
        seconds = max(1, int((timeout_ms + 999) / 1000))
        command = [
            curl, "-q", "-L", "--max-redirs", "5", "--proto", "=https", "--proto-redir", "=https",
            "--silent", "--show-error", "--compressed", "--connect-timeout", "8", "--max-filesize", str(MAX_RESPONSE_BYTES),
            "--max-time", str(seconds), "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "-H", "Accept: application/json,text/plain,*/*", "-H", "Accept-Language: en-US,en;q=0.9",
            "-D", header_name, "-o", temp_name, "-w", "%{http_code}", url,
        ]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=(timeout_ms / 1000) + 5)
        code_text = completed.stdout.strip().splitlines()[-1] if completed.stdout.strip() else "000"
        http_status = int(code_text) if code_text.isdigit() else 0
        if http_status in ACCESS_STATUSES:
            return error_result(title, url, "access_restricted", f"Scholar returned HTTP {http_status}; no transport retry", "curl", http_status=http_status), 1
        if completed.returncode != 0:
            status = "timeout" if completed.returncode == 28 else "transport_error"
            return error_result(title, url, status, "curl request failed", "curl", http_status=http_status, transport_exit_code=completed.returncode), 1
        if http_status != 200:
            return error_result(title, url, "http_error", f"Scholar returned HTTP {http_status}", "curl", http_status=http_status), 1
        response_headers = Path(header_name).read_text(encoding="latin-1", errors="replace") if header_name else ""
        content_type = ""
        for line in response_headers.splitlines():
            if line.upper().startswith("HTTP/"):
                content_type = ""
            if line.lower().startswith("content-type:"):
                content_type = line.split(":", 1)[1].strip()
        with open(temp_name, "rb") as response_file:
            body = response_file.read(MAX_RESPONSE_BYTES + 1)
        candidates, charset = parse_response(body, content_type)
        result = result_base(title, url, "curl", started, int((time.monotonic() - begin) * 1000))
        result.update({"charset": charset, "http_status": http_status, "content_type": content_type, "candidates": candidates})
        return result, 0
    except PermissionError as exc:
        return error_result(title, url, "access_restricted", str(exc), "curl", http_status=200), 1
    except ValueError as exc:
        return error_result(title, url, "invalid_response", str(exc), "curl", http_status=http_status), 1
    except FileNotFoundError:
        return error_result(title, url, "tool_unavailable", "curl executable is unavailable", "curl"), 1
    except (OSError, subprocess.TimeoutExpired) as exc:
        return error_result(title, url, "transport_error", str(exc), "curl"), 1
    finally:
        if temp_name:
            try:
                Path(temp_name).unlink()
            except OSError:
                pass
        if header_name:
            try:
                Path(header_name).unlink()
            except OSError:
                pass


@lru_cache(maxsize=8)
def preflight_node(node: str) -> Tuple[bool, bool]:
    """One local check per executable per launcher process; never a network probe."""
    script = """
const ok = typeof fetch === 'function' && typeof AbortSignal !== 'undefined' && typeof AbortSignal.timeout === 'function' && typeof TextDecoder === 'function';
console.log(JSON.stringify({ok, proxy: process.allowedNodeEnvironmentFlags.has('--use-env-proxy')}));
"""
    try:
        completed = subprocess.run([node, "-e", script], capture_output=True, text=True, timeout=5)
        data = json.loads(completed.stdout)
        return completed.returncode == 0 and data.get("ok") is True, data.get("proxy") is True
    except (OSError, subprocess.TimeoutExpired, ValueError, AttributeError):
        return False, False


def cache_key(title: str, language: str) -> str:
    return hashlib.sha256(f"{language}\n{title.strip()}".encode("utf-8")).hexdigest()


def cache_read(cache_dir: Path, key: str, title: str) -> Optional[dict[str, Any]]:
    path = cache_dir / f"{key}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("status") != "ok" or data.get("query") != title or not data.get("fetched_at") or not isinstance(data.get("candidates"), list):
        return None
    try:
        stamp = datetime.fromisoformat(str(data["fetched_at"]).replace("Z", "+00:00"))
        if stamp.tzinfo is None or data.get("source_kind") != "live" or data.get("schema_version") != 1:
            return None
        if any(not isinstance(candidate, dict) or not isinstance(candidate.get("title"), str) for candidate in data["candidates"]):
            return None
    except (TypeError, ValueError):
        return None
    original_transport = data.get("transport")
    data["transport"] = "cache"
    data["served_at"] = now_iso()
    data["cache"] = {"hit": True, "original_fetched_at": data.get("fetched_at"), "original_transport": original_transport, "served_at": data["served_at"]}
    return data


def cache_write(cache_dir: Path, key: str, data: dict[str, Any]) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{key}.json"
    fd, temp_name = tempfile.mkstemp(prefix=f".{key}-", suffix=".tmp", dir=str(cache_dir))
    os.close(fd)
    try:
        Path(temp_name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temp_name, path)
    finally:
        try:
            Path(temp_name).unlink()
        except OSError:
            pass


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Query Google Scholar's observed structured paper endpoint.")
    parser.add_argument("--title", required=True, help="Public paper title to search")
    parser.add_argument("--language", default="en", help="Scholar UI language (default: en)")
    parser.add_argument("--timeout-ms", type=int, default=DEFAULT_TIMEOUT_MS)
    parser.add_argument("--cache-dir", type=Path, help="Opt-in directory for paper-only JSON records")
    parser.add_argument("--refresh", action="store_true", help="Ignore and replace an opt-in cache record")
    parser.add_argument("--input-file", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--input-content-type", default="", help=argparse.SUPPRESS)
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.timeout_ms < 1000 or args.timeout_ms > 120000:
        parser.error("--timeout-ms must be between 1000 and 120000")
    if not args.title.strip():
        parser.error("--title must not be blank")
    url = query_url(args.title, args.language)
    key = cache_key(args.title, args.language)
    if args.cache_dir and not args.refresh and not args.input_file:
        cached = cache_read(args.cache_dir, key, args.title)
        if cached:
            print(json.dumps(cached, ensure_ascii=False))
            return 0

    node = os.environ.get("SCHOLAR_LOOKUP_NODE", "node")
    disable_node = os.environ.get("SCHOLAR_LOOKUP_DISABLE_NODE") == "1"
    helper = Path(__file__).with_name("scholar_fetch.mjs")
    result: dict[str, Any]
    code: int
    if not disable_node and helper.exists():
        supported, proxy_supported = preflight_node(node)
        proxy_configured = any(os.environ.get(key) for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"))
        only_all_proxy = any(os.environ.get(key) for key in ("ALL_PROXY", "all_proxy")) and not any(os.environ.get(key) for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"))
        if (proxy_configured and not proxy_supported or only_all_proxy) and not args.input_file:
            supported = False
    else:
        supported = False
    if supported:
        result, code = run_node(node, helper, url, args.timeout_ms, args.input_file, args.input_content_type)
    else:
        curl = os.environ.get("SCHOLAR_LOOKUP_CURL", "curl")
        result, code = run_curl(curl, args.title, url, args.timeout_ms, args.input_file, args.input_content_type)
    if result.get("query") in {None, ""}:
        result["query"] = args.title
    result.setdefault("requested_url", url)
    result["schema_version"] = 1
    result["source_kind"] = "fixture" if args.input_file else "live"
    if args.input_file:
        result["parsed_at"] = now_iso()
        result["fetched_at"] = None
        result["http_status"] = None
    if result.get("status") == "ok" and args.cache_dir and not args.input_file:
        try:
            cache_write(args.cache_dir, key, result)
            result["cache"] = {"hit": False, "written": True, "original_fetched_at": result.get("fetched_at")}
        except OSError:
            result["cache"] = {"hit": False, "written": False, "error": "Could not write cache"}
    print(json.dumps(result, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
