# Paper Citation Counts

Use for citation counts (引用量/被引用次数), refreshing paper metadata, or the initial metadata check in close reading. Load [google-scholar-browser.md](google-scholar-browser.md) for all shared browser mechanics. Citation-only requests do not require choosing a reading mode or starting the three passes. Preserve reading progress; unavailable metadata must not block reading the paper.

## Workflow

For terminal Scholar requests, first apply the [sandbox and proxy requirements](google-scholar-json.md#sandbox-and-proxy-requirements): known sandbox network restrictions require host-authorized sandbox-external execution, and network failures or suspicious 404 responses require checking existing proxy settings before abandoning the request.

1. Establish full title, authors, year, and DOI/arXiv ID from the requested paper, its local manifest, or PDF first page. Read only what identity matching needs; do not download papers again or expand the requested collection.
2. Reuse cached evidence with its original timestamp unless a refresh is needed. For a new paper lookup, use the opt-in Python launcher in [google-scholar-json.md](google-scholar-json.md), unless the user requests browser-only operation. It selects Node native fetch after a local capability preflight, then tries curl only when Node is unavailable; explicit access restrictions stop automated requests rather than triggering a transport rotation. If the helper is unavailable or disabled after a failure in this session, reuse the normal Scholar tab and search the quoted full title using the search box and Enter. Ensure a previous citing-articles restriction is not narrowing the search.
3. Match title, authors, year, source, and available identifiers. Open a candidate's source page when identity remains ambiguous. The first result, highest count, or matching title alone does not establish identity: same-title slides, blogs, and citation-only records can appear.
4. Extract the matched result's `Cited by N` or `被引用次数：N` text and observed citation-list URL. Parse only that link's number, not arbitrary numbers from the whole result. Never invent a cluster ID. A missing count is unknown, not zero.
5. Keep the matched title, identity evidence, paper URL, count or null, raw count text, citation URL, lookup time with timezone, transport, and status. Distinguish helper `status: ok` from `identity_status: pending` or `verified`; also distinguish not found, count not shown, ambiguous, CAPTCHA pending, and tool error.
6. If an exact-title query cannot identify the paper, make at most two targeted fallback attempts: unquoted title, then distinctive title terms plus first author. Record the query that succeeded. Do not loop through speculative variations.

For multiple papers, process the selected list using the same tab and retain successful results; only revisit incomplete items. Do not equate preprint/publication/citation-only clusters without checking identity, and never sum their counts. When the main record is uncertain, report alternatives and the ambiguity. Citation counts do not prove quality, venue, or acceptance; verify publication claims against official sources separately.

## Output and caching

Provide a compact table in the user's language: paper, Scholar count, lookup time, source link, status/version notes. Retain raw evidence for explaining matches. Label reused data with its original time; do not present it as freshly checked. Refresh when requested, missing, or materially time-sensitive, not at each reading unit.

Follow the main skill's note rules: guided reading creates no persistent citation files unless requested; requested organization or autonomous reading may add metadata to the existing paper notes/manifest, preserving source and date. For citing-paper exploration continue with [google-scholar-citing.md](google-scholar-citing.md), rather than confusing the count with the citing list.
