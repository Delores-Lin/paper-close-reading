#!/usr/bin/env python3
"""Opt-in Scholar full-text downloader with separate file and identity states."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from contextlib import closing
from pathlib import Path
from typing import Optional
from urllib.request import Request, HTTPRedirectHandler, build_opener
from urllib.parse import urlparse, parse_qs


def valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username and not parsed.password
    except ValueError:
        return False


class SafeRedirect(HTTPRedirectHandler):
    max_redirections = 5

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not valid_url(newurl):
            raise ValueError("Refusing a non-HTTPS or credential-bearing redirect")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def urlopen(request, timeout):
    """Local opener; never installs global handlers or exports browser cookies."""
    return build_opener(SafeRedirect()).open(request, timeout=timeout)


def resolve_full_text_url(url: str) -> str:
    """Unwrap the observed Scholar tracking URL, without executing its HTML/JS."""
    parsed = urlparse(url)
    if parsed.netloc == "scholar.google.com" and parsed.path == "/scholar_url":
        targets = parse_qs(parsed.query).get("url", [])
        if len(targets) != 1 or not valid_url(targets[0]):
            raise ValueError("Scholar full-text redirect has no single safe HTTPS target")
        return targets[0]
    return url


def emit(data: dict, code: int = 0) -> int:
    print(json.dumps(data, ensure_ascii=False))
    return code


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Download and validate a paper full-text link.")
    parser.add_argument("--url", required=True, help="Matched HTTPS full-text URL from Scholar")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--expected-sha256", help="Optional digest for the downloaded bytes")
    parser.add_argument("--expected-title", help="Optional title passed to a first-page extraction check")
    parser.add_argument("--max-bytes", type=int, default=50 * 1024 * 1024)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args(argv)
    if args.max_bytes <= 0 or args.timeout <= 0:
        return emit({"status": "invalid_limits", "file_status": "not_downloaded", "identity_status": "pending"}, 2)
    if not valid_url(args.url):
        return emit({"status": "invalid_url", "file_status": "not_downloaded", "identity_status": "pending", "error": "Only HTTPS URLs without embedded credentials are accepted"}, 2)
    if os.path.lexists(args.output):
        return emit({"status": "output_exists", "file_status": "not_downloaded", "identity_status": "pending", "output": str(args.output)}, 2)
    try:
        source_url = resolve_full_text_url(args.url)
    except ValueError as exc:
        return emit({"status": "invalid_url", "file_status": "not_downloaded", "identity_status": "pending", "error": str(exc)}, 2)
    started = time.monotonic()
    try:
        with closing(urlopen(Request(source_url, headers={"User-Agent": "PaperCloseReading/1.0"}), timeout=args.timeout)) as response:
            final_url = response.geturl()
            if not valid_url(final_url):
                raise ValueError("Refusing unsafe final URL")
            advertised = response.headers.get("Content-Length")
            if advertised and int(advertised) > args.max_bytes:
                return emit({"status": "too_large", "file_status": "not_downloaded", "identity_status": "pending", "bytes": int(advertised)}, 1)
            chunks: list[bytes] = []
            total = 0
            read_chunk = getattr(response, "read1", response.read)
            while True:
                if time.monotonic() - started > args.timeout:
                    raise TimeoutError("Download exceeded its time budget")
                chunk = read_chunk(min(64 * 1024, args.max_bytes - total + 1))
                if not chunk:
                    break
                chunks.append(chunk)
                total += len(chunk)
                if total > args.max_bytes:
                    return emit({"status": "too_large", "file_status": "not_downloaded", "identity_status": "pending", "bytes": total}, 1)
            body = b"".join(chunks)
            content_type = response.headers.get("Content-Type", "")
    except Exception as exc:
        return emit({"status": "download_error", "file_status": "not_downloaded", "identity_status": "pending", "error": str(exc)}, 1)
    digest = hashlib.sha256(body).hexdigest()
    final_parsed = urlparse(final_url)
    if final_parsed.scheme != "https":
        return emit({"status": "unsafe_redirect", "file_status": "invalid", "identity_status": "pending", "final_url": final_url}, 1)
    if not body.startswith(b"%PDF-"):
        return emit({"status": "not_pdf", "file_status": "invalid", "identity_status": "pending", "content_type": content_type, "final_url": final_url, "bytes": len(body)}, 1)
    if len(body) < 64 or b"%%EOF" not in body[-4096:]:
        return emit({"status": "truncated_pdf", "file_status": "invalid", "identity_status": "pending", "content_type": content_type, "bytes": len(body)}, 1)
    if args.expected_sha256 and digest.lower() != args.expected_sha256.lower():
        return emit({"status": "digest_mismatch", "file_status": "invalid", "identity_status": "pending", "sha256": digest}, 1)
    temp_name = ""
    parse_status = "not_attempted"
    first_page_text = None
    pdfinfo = shutil.which("pdfinfo")
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix=f".{args.output.name}-", dir=str(args.output.parent))
        os.close(fd)
        Path(temp_name).write_bytes(body)
        if pdfinfo:
            check = subprocess.run([pdfinfo, temp_name], capture_output=True, text=True, timeout=15)
            if check.returncode != 0:
                return emit({"status": "invalid_pdf", "file_status": "invalid", "identity_status": "pending", "parse_status": "parse_failed", "bytes": len(body), "error": check.stderr.strip()[-500:]}, 1)
            parse_status = "parsed"
        else:
            parse_status = "signature_only"
        if args.expected_title:
            pdftotext = shutil.which("pdftotext")
            if pdftotext:
                check = subprocess.run([pdftotext, "-f", "1", "-l", "1", temp_name, "-"], capture_output=True, text=True, timeout=15)
                if check.returncode == 0:
                    first_page_text = " ".join(check.stdout.split())[:1200]
        # A hard-link publish is atomic and fails if another process created
        # the requested output after the initial no-clobber check.  Both paths
        # are in the same output directory, so this does not cross devices.
        try:
            os.link(temp_name, args.output)
        except FileExistsError:
            return emit({"status": "output_exists", "file_status": "not_downloaded", "identity_status": "pending", "output": str(args.output)}, 2)
        except OSError as exc:
            return emit({"status": "publish_error", "file_status": "not_downloaded", "identity_status": "pending", "error": str(exc)}, 1)
        os.unlink(temp_name)
        temp_name = ""
    except subprocess.TimeoutExpired as exc:
        return emit({"status": "validation_timeout", "file_status": "invalid", "identity_status": "pending", "error": str(exc)}, 1)
    except OSError as exc:
        return emit({"status": "file_error", "file_status": "not_downloaded", "identity_status": "pending", "error": str(exc)}, 1)
    finally:
        try:
            if temp_name:
                Path(temp_name).unlink()
        except OSError:
            pass
    # A valid PDF proves only that the bytes look like a readable PDF.  Even
    # when a first-page excerpt is available, identity/version review remains
    # pending for the skill/user to confirm against the selected candidate.
    return emit({"status": "downloaded", "file_status": "valid_pdf" if parse_status == "parsed" else "signature_only", "parse_status": parse_status, "identity_status": "pending", "content_type": content_type, "requested_url": args.url, "resolved_source_url": source_url, "final_url": final_url, "output": str(args.output.resolve()), "bytes": len(body), "sha256": digest, "expected_title": args.expected_title, "first_page_text": first_page_text})


if __name__ == "__main__":
    raise SystemExit(main())
