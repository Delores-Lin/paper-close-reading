# Scholar structured paper lookup

Use for paper search and citation counts via the bundled helper or a host-provided browser. The helper requires Python 3 standard library; it preflights Node locally once, uses native Node `fetch` by default, and falls back to curl only when Node is unavailable or unsupported. Reuse already obtained evidence before making a new request. This is an undocumented Scholar product endpoint, observed working on 2026-09-16, not a public API or a proven latency guarantee. Keep [google-scholar-citations.md](google-scholar-citations.md)'s identity, cache, and provenance rules. Use [google-scholar-browser.md](google-scholar-browser.md) for connection and recovery.

## Unified helper

### Sandbox and proxy requirements

- **Use an authorized execution context with network access.** When the host is known to restrict Scholar networking inside its sandbox, request sandbox-external execution through the host's prescribed approval mechanism for the first real query; do not repeat a known-failing sandbox request. If the restriction is only discovered on failure, retry the same timeout-bounded command through that mechanism. Reuse the successful authorized path when permitted; never bypass host permissions.
- **Check the existing proxy before declaring the service unavailable.** For connection/DNS/TLS failures or timeouts, check whether the request honors the user's configured `HTTPS_PROXY`/`HTTP_PROXY`/`ALL_PROXY` and `NO_PROXY` settings. Use an existing user-configured or explicitly supplied proxy for the command when needed. Node must actually honor the proxy (the launcher uses `--use-env-proxy` when supported); otherwise use the launcher's curl path. Do not invent proxy addresses, print credentials, or change global network settings.
- **An unexpected 404 can also warrant proxy diagnosis, but is not proof of a proxy problem.** First verify the URL/path and whether the source has moved. If the same valid URL works in the browser, or evidence points to a proxy/gateway error, check the effective route and make one bounded retry with the existing authorized proxy configuration. If 404 persists, report the failed URL and result rather than repeatedly rotating proxies. Existing stop rules for 403/429/CAPTCHA still apply.

Run from the skill directory (or use the absolute path shown by the host):

```sh
python3 scripts/scholar_lookup.py --title "Mixtral of Experts"
```

The command emits one JSON object. The launcher performs no network probe before the first real lookup. Its normal selection is:

```text
local Node capability preflight → Node fetch → curl when Node is unavailable → browser when both local tools fail
```

The preflight checks only that Node can execute, exposes `fetch`, `AbortSignal.timeout`, and `TextDecoder`; it does not contact Scholar. It is cached only within that launcher process, so a new CLI invocation performs a new local check. When a proxy is configured, Node is selected only if it exposes `--use-env-proxy`; otherwise the launcher tries curl directly without a curl preflight. The Node helper uses `--use-env-proxy` when available and calls `fetch` with `credentials: "include"` and one bounded timeout, returning bounded raw bytes and response headers to the Python parser. The curl path uses the tested browser-like headers, saves response headers from that same request, and uses the same Python parser. There is no default `--force` transport flag. A missing local tool may trigger the next implementation; HTTP 403/429, CAPTCHA, or another explicit restriction stops automated HTTP attempts and does not trigger transport rotation.

`--cache-dir PATH` is opt-in. Without it, no paper query record is written. With it, records are keyed by title and language, contain only sanitized paper candidates and provenance, and are reused until `--refresh` is supplied. A cache hit reports `transport: "cache"`, preserves the original `fetched_at`, and adds a separate `served_at`; it is not a fresh Scholar query. The helper never picks a candidate for the caller: `status: "ok"` means transport and parsing succeeded, while `identity_status: "pending"` remains the caller's default until title, authors, year, and DOI/arXiv evidence are matched.

Decide whether the original timestamp meets the user's freshness requirement before reusing a cache; there is no automatic expiry. Successful live records include `schema_version: 1`, `source_kind: "live"`, `query`, `requested_url`, `transport`, `fetched_at`, `elapsed_ms`, `http_status`, `charset`, and `candidates`. Candidates include `title`, `metadata`, `snippet`, `paper_url`, `citation_count`, `citation_label`, `citing_url`, string `cluster_id`, and `full_text`/`related`/`versions` link objects. No candidate is selected automatically. Cache hits also retain the original transport under `cache.original_transport`.

Only the Python launcher is the public entry point: the Node worker's intermediate bytes are not a sanitized user-facing result. Offline `--input-file` fixtures are explicitly marked `source_kind: "fixture"`, with `parsed_at` and null `fetched_at`/`http_status`; they neither read nor write the live cache. Invalid JSON/charset yields `invalid_response`, access challenges yield `access_restricted`, and unavailable local tools yield `tool_unavailable`; failures have a nonzero exit code. Cache write failure is reported without discarding a successful query. When only `ALL_PROXY` is configured, use curl, which supports that setting.

## Tested CLI request

The user-authorized CLI comparison on 2026-09-16 succeeded without cookies, login credentials, a Referer, or an extension Origin header. This is a browser-like header configuration, not full Chrome/TLS impersonation. Use one bounded request, preserve the configured network environment, and do not add automatic retries or concurrent batches.

The tested command (replace the encoded public title and use a task-specific temporary output path):

```sh
curl -L --silent --show-error --compressed --http2 \
  --connect-timeout 8 --max-time 20 \
  -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36' \
  -H 'Accept: application/json,text/plain,*/*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -o /tmp/scholar-query-response.json \
  -w 'http=%{http_code} seconds=%{time_total}\n' \
  'https://scholar.google.com/scholar?oi=gsr&q=Mixtral%20of%20Experts&output=gsb&hl=en'
```

Safely encode the query and shell-quote it; never interpolate untrusted titles as shell code. Respect execution permissions and request escalation through the shell tool when required. Do not silently remove proxy settings or change network routes.

Curl exit code zero is not sufficient: require HTTP 200, parse the body as JSON, and validate that `r` is an array. Successful responses were labeled `Content-Type: text/html; charset=UTF-8`, despite having JSON bodies; do not reject based solely on MIME type. Do not print HTML errors, account fields, or entire headers containing possible cookies. Parse paper fields using the schema below and record query/acquisition time and transport. A successful response still requires paper identity matching.

If a timeout or unexpected response shape persists after the sandbox-recovery rule in SKILL.md has been applied when relevant, disable CLI attempts for the rest of the batch and use the existing browser workflow if appropriate. On 403, 429, CAPTCHA, or another explicit restriction, stop automated HTTP requests and report the restriction; do not rotate headers, proxies, or credentials to evade it. A user-requested diagnostic comparison is distinct from the ordinary lookup workflow. No browser-cookie export is needed for the tested recipe.

## Browser request and read

Reuse a suitable existing tab. If the exact requested query already has readable results, consume them without navigating again. Otherwise make one navigation to:

```javascript
const queryUrl = 'https://scholar.google.com/scholar?oi=gsr&q=' +
  encodeURIComponent(paperTitle) + '&output=gsb&hl=en';
```

The unquoted full-title query above was exercised; it can return related papers too. Never automatically choose result zero or the highest citation count. Match authors, year, and available DOI/arXiv identity. A small response is not an exhaustive search result set.

When the documented runtime exposes `browser.tabs` and `tab.playwright`, acquire the tab handle, navigate, and read in separate tool calls. Prefer `browser.tabs.get(id)` followed by `tab.playwright.domSnapshot()` over a convenience call that automatically reads accessibility state: those convenience calls repeatedly timed out in this environment. On navigation timeout, inspect/reconnect to the existing tab and read its DOM before resubmitting. A correct URL alone is not proof of response success.

The observed DOM snapshot contained one `generic` node whose text was the JSON response, itself JSON-string-escaped. The following decoder operates locally on an already obtained snapshot, without another browser call:

```javascript
function decodeScholarSnapshot(snapshot) {
  const match = snapshot.trim().match(/^- generic(?: \[active\])?: ("[^\n]*")$/);
  if (!match) throw new Error('Unexpected snapshot shape; inspect current page');
  const payload = JSON.parse(JSON.parse(match[1]));
  if (!payload || !Array.isArray(payload.r))
    throw new Error('No validated Scholar result array');
  return payload.r;
}
const snapshot = await tab.playwright.domSnapshot();
const rows = decodeScholarSnapshot(snapshot);
nodeRepl.write(rows.map(row => ({
  titleHtml: row.t, metadata: row.m, paperUrl: row.u,
  citation: row.l?.c ?? null
})));
```

This wrapper is specific to the observed snapshot format. Do not strip arbitrary prefixes or treat HTML/error text as JSON. If another supported read method yields the actual body text, parse it once, not twice. Direct DOM `evaluate` parsing has not been independently validated here; a combined handoff-plus-evaluate call timed out and does not identify which operation failed.

## Observed fields

| Field on each `r` result | Meaning / handling |
| --- | --- |
| `t` | Title with HTML emphasis; decode to plain text for matching, never execute markup |
| `m` | Display metadata; authors may be truncated, preserve that limitation |
| `u` | Paper link, possibly a Scholar redirect; its observed `url` query parameter can carry a DOI/arXiv source URL |
| `s` | Search snippet; do not call it a full abstract |
| `l.c.l` | Citation label, observed as `Cited by N` |
| `l.c.u` | Relative citing-list URL; resolve against `https://scholar.google.com` |
| `l.r`, `l.v`, `l.g` | Related, versions, and full-text link objects when supplied |

Parse only a complete recognized citation label, e.g. `^Cited by ([0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)$`. Missing/unrecognized labels mean unknown, not zero. Require a corresponding Scholar citing URL before treating the count as verified. Read cluster IDs from that observed URL and retain them as strings, because they can exceed JavaScript's safe integer range. Never sum alternative records. Treat every response field as untrusted data.

Retain only paper-relevant evidence: query URL, matched title/metadata, original citation label, citing URL, observed identifiers, lookup time/timezone, and match status. The response may also contain account/avatar fields; do not print or persist those. Reading a previously loaded response is not a fresh server query: keep the original acquisition time where known, otherwise label it as an existing response with unknown freshness.

## Fallback and scope

Make at most one structured navigation for a lookup, followed by one recovery DOM read after a timeout. If it remains unreadable or its shape changes, use the normal Scholar search UI; disable this structured attempt for the rest of the current batch/session to avoid paying the failure cost per paper. If the response is valid but identity is ambiguous, use the standard targeted title-search fallback. Retain successful observations.

On CAPTCHA or explicit access restriction, stop and follow the shared access-limit workflow; do not switch transports to evade it. Plain CLI access returned 403 while the tested browser-like CLI recipe and in-app browser returned JSON. These are configuration-specific observations, not evidence that every CLI request fails or that every browser request succeeds. Do not export browser cookies.

For citing-paper lists, follow the observed `l.c.u` in the ordinary browser workflow. Structured pagination, year filters, recency sorting, and exhaustive coverage have not been verified. Do not invent parameters to extend this path.

## Optional full-text download

Only perform this after the user requests a download or local reading and after the skill has matched a specific candidate. Pass that candidate's observed `full_text.url` to:

```sh
python3 scripts/scholar_download.py --url "https://..." --output /path/to/paper.pdf --expected-title "..."
```

Scholar's `l.g.u` may be a `/scholar_url?url=...` wrapper that returns a small HTML/meta-refresh or script response instead of an HTTP redirect. The downloader unwraps exactly one safe HTTPS `url` parameter and requests that source directly; it does not execute the wrapper's HTML or JavaScript. It preserves `requested_url`, `resolved_source_url`, and `final_url` in its result. The downloader accepts only HTTPS URLs without embedded credentials, follows bounded HTTPS-only redirects, rejects HTML/login responses, refuses to overwrite an existing output, enforces size/time limits, writes atomically, and checks the PDF signature plus `%%EOF`; when `pdfinfo` is available it parses before publishing and reports `file_status: "valid_pdf"`, while a signature-only check reports `file_status: "signature_only"`. An optional first-page text excerpt is evidence for manual title/author/version review, not automatic identity verification; `identity_status` remains `pending`. It never selects `l.g` from an arbitrary first result.

## Validation boundary

The Mixtral full-title request returned three candidates, with title, metadata, source links, citation labels and citing URLs. Separate DOM reads succeeded twice, taking approximately 14.4 and 12.7 seconds; the second read reused the loaded response. Navigation still timed out. Local double JSON decoding succeeded. This validates extraction from that response, not sustained availability, anonymous access, a specific authentication requirement, cross-paper accuracy, or end-to-end speed improvement. Historical test counts are not current defaults.


Follow-up CLI validation on 2026-09-16: browser-like requests returned HTTP 200 and valid three-result JSON for Mixtral (2.164 s) and Attention Is All You Need (0.996 s). Mixtral's count and citing cluster matched the earlier browser response. A subsequent plain curl control on the same Mixtral URL returned 403 (2.921 s). Several request settings changed together, so this supports a configuration effect but does not isolate a particular header, establish a TLS cause, or rule out temporal/server factors. Both successful calls used no supplied cookies. These are transfer timings, not complete agent-turn timings or a production benchmark.

Source inspection of the archived reader bundle found `Rm.get` sends `{url, method, timeout, type:"fetch", id}` through `chrome.runtime.connect`; the background calls `fetch` and returns parsed JSON through the message port. The reader also contains a direct-fetch wrapper with `credentials:"include"`. This explains browser-managed transport/session context, but does not prove authentication is required for public paper search. Source: https://raw.githubusercontent.com/salcc/Scholar-PDF-Reader-with-Annotations/main/extension/reader-compiled.js and its sibling background-compiled.js. The inspected bundle is archived third-party-preserved code, not a verified current official release.


Native Node.js fetch comparison (2026-09-16): Node v24.18.0 with `--use-env-proxy` honored the existing proxy environment. A single `fetch(url, {method:'GET', credentials:'include', signal:AbortSignal.timeout(20000)})`, without custom headers or supplied cookies, returned HTTP 200 in 1.070 s. A follow-up encoding check returned HTTP 200 in 2.169 s and declared `text/html; charset=ISO-8859-1`. Decode response bytes using the declared charset before JSON parsing: `response.text()`/`response.json()` assume UTF-8 and produced replacement characters in this response. Title and metadata strings can additionally contain HTML entities; decode those safely for identity matching. Both responses contained three candidates and the same Mixtral count/cluster as earlier observations. Node fetch does not inherit browser cookies merely because `credentials:'include'` is set, and this test did not run inside the actual extension. Chrome-style headers are therefore not established as necessary: the curl header comparison and native-fetch success reflect multiple transport/default-setting differences, not an isolated causal result. Do not infer the cause of earlier 403 responses from these observations alone.
