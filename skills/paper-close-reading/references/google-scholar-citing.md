# Citing Papers, Year Filters, and Recent Additions

Use for “who cites this paper,” 被引, 某年被引, 最新被引, or highly cited follow-up literature. Load [google-scholar-browser.md](google-scholar-browser.md). Resolve the target via [google-scholar-citations.md](google-scholar-citations.md) only when its identity and entry link are not already verified. Preserve the close-reading position; do not start the three-pass workflow.

## Direction and scope

For target A, a citing paper B cites A. The count used to rank B is B's own citation count, not A's count. A's References list is the opposite direction and is outside this subfunction.

For “take a look,” announce a first-three-pages preview. Follow an explicit count, page limit, year range, or request for all accessible results. A partial sample cannot establish global top-cited papers. Even all accessible pages do not establish all real-world citations or complete database coverage.

## Workflow

1. Confirm A's identity and follow its observed citation-list link. Verify the target heading and cluster; do not accidentally enter a citing paper's own citing list.
2. Set the requested mode below. Record year range and sort mode separately. After a filter change, inspect page position: the year dialog has retained `start=20` in testing. Use an observed page-1 link to return to the filtered first page; do not navigate back to an unfiltered historical page.
3. Collect each result's title, visible authors/year, paper URL, own count or null, raw count text, citation URL/cluster when present, source page URL/number, target identity, filter/sort mode, and lookup time/timezone. Preserve raw visible metadata; do not infer missing authors or years.
4. Use the actual enabled Next control. Check target, filters, page number, and first item after navigation. Track visited pages and record identities. Stop at the requested limit, an accessible last page, repeated page/no new items, CAPTCHA, or persistent access restriction. Report why collection stopped.
5. Deduplicate identical Scholar clusters first; otherwise use a verified DOI/arXiv ID or canonical paper URL. Similar title/author/year combinations are candidates for review, not automatic merges. Keep ambiguous versions separate and do not add their counts. Preserve provenance and timestamps when duplicate observations disagree.
6. For impact ranking, sort collected known counts numerically descending and list unknown counts separately; use year descending only as an optional tie-breaker. For recency requests preserve Scholar date order and visible relative dates. Do not silently replace recency with impact ranking.
7. Report raw/unique totals, pages covered, filters, missing values, source links, and lookup date. Label partial rankings “among N collected papers.” A displayed result estimate is not an exact completeness guarantee. Follow the main skill's persistence rules.

Only claim “Scholar lists B as citing A” from the list. Classifying B as an extension, application, baseline comparison, or criticism requires inspecting its citation context. Keep research relevance and recommended reading priority separate from citation-count order.

## Specific year or range

First exit date-sorted mode by selecting relevance sorting. In the Chinese test, submitting a custom range while date sorting was active did not apply the year filter; returning to relevance mode before entering the range succeeded. Do not promise arbitrary combinations of these modes.

Open Year → Custom range. For year Y set both fields to Y; for an interval set distinct bounds. Since Y includes later years and is not equivalent to only Y. Use the shared keyboard-input recipe and verify both field values before scoped submission.

After submission verify the visible range label and results. Observed `as_ylo`/`as_yhi` URL parameters can corroborate the range but do not establish success while a CAPTCHA is displayed. Check and reset pagination to the filtered first page.

This uses Scholar's document-year classification, not an exact timestamp of a citation event. B's displayed citation count is its current overall count, not citations B received during the selected year.

## Latest additions

For an unrestricted recency request, clear an old range with Any time, reopen Year, then select Sort by date. Inspect the actual result-page description and retain it in the explanation.

In the verified UI the page says `Articles added in the last year, sorted by date` / `过去一年中添加的文章，按日期排序`, with labels such as `3 days ago` / `3 天前`. Describe this as Scholar's recently added citing results, not all citing papers sorted by exact publication time or exact citation-event time. The observed `scisbd=1` parameter corroborates this mode; do not guess other parameters to force untested combinations.

If the user asks for the newest papers within an exact year, explain the observed combination limitation. A possible alternative is collecting that year's results and verifying publication dates from paper sources; do not present that alternative as already implemented or tested.

## Tested behavior and limits

On 2026-09-16, Mixtral citing pages 1–3 yielded 10 items each, 30 distinct records. Replaying the first page produced 40 inputs and 30 unique outputs. Numeric ranking worked. No natural cross-page duplicate occurred; replay testing does not validate cross-version identity resolution.

English single-year filtering, clearing a range, and recent-additions sorting succeeded. Chinese 2025–2025 filtering and Next-to-page-2 succeeded with target and range retained. A year query made directly from date mode failed to apply; returning to relevance mode fixed it. See the shared browser reference for precise per-control validation. All accessible last-page behavior, every language, and cross-version merging remain unexhaustively tested. Historical counts are evidence of tests, never default current values.
