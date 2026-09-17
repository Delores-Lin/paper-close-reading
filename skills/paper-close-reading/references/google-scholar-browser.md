# Shared Google Scholar Browser Operations

Load this reference when executing either Scholar workflow. Use the current browser tool documentation as the API contract; The `cua`, `browser.tabs`, and `tab.playwright` examples below apply only when the current runtime documents those APIs. Otherwise translate the workflow to the host-provided browser tools; do not assume these objects exist. These are browser-runtime snippets, not standalone Node.js or Python scripts.

## Connection and recovery

- For sandbox-external terminal execution and proxy diagnosis, follow [sandbox and proxy requirements](google-scholar-json.md#sandbox-and-proxy-requirements). A working browser and failing CLI can use different network routes; compare known configuration rather than assuming the browser exports its proxy settings to Node/curl. Change browser proxy settings only through documented supported controls and within the user's authorization.

- Use the browser tools provided by the current host for browser workflows and citing lists, honoring any browser explicitly selected by the user. Paper search/counts may use the tested CLI recipe in [google-scholar-json.md](google-scholar-json.md), subject to user transport preferences and execution permissions. Earlier plain CLI requests returned 429/403; later browser-like CLI requests succeeded. Neither result establishes a usable parallel retrieval path. Do not replace a user-selected browser or citation database without authorization. Use only documented host capabilities.
- On first use or a runtime reset, follow the tool's initialization protocol, e.g. one `await cua.getState()` call, then read the returned documentation. Discover actual browser/tab IDs; honor explicit tab mentions and reuse an existing suitable Scholar tab.
- Where documented, connect with `browser.tabs.get(tabId)` separately from reading the DOM. Combined connection-and-read calls have timed out. Do not reacquire the browser merely because a tab handle is stale; rediscover its tabs. After a reset, rebuild discarded bindings.
- Navigate only when needed. On navigation or submission timeout, inspect current URL/state before repeating: the action may have completed. Never assume a timeout means the page failed to open.
- Retain a tab with the documented handoff/deliverable API when the user needs it. Marks may be turn-scoped.
- Only set visibility or viewport through supported capabilities when appropriate to the user's request. Do not claim unsupported user-agent, proxy, or context-locale settings. `hl=en`/`hl=zh-CN` selects website language, not browser locale. Browser success does not establish a specific proxy path.

## Empty inventory fallback

An empty browser or tab list is a recoverable state, not by itself a terminal error. Do not report retrieval failure until one bounded fresh-start attempt has been made, unless the tool explicitly denies access or requires user action.

1. Distinguish an empty browser inventory from an existing browser with no tabs. A subagent must discover its own runtime state; do not assume it shares the parent's handles, tab IDs, or session. An empty list alone does not prove session isolation.
2. If the selected browser exists but has no usable Scholar tab, retain the browser handle and create one tab through the documented API, then open `https://scholar.google.com/`. Do not reset or reselect a healthy browser merely because its tab list is empty.
3. If there is no browser handle and discovery remains empty, follow the current tool's initialization protocol from the beginning. When supported, use the host's explicit browser creation entry point, for example, only in a runtime documenting this API, `cua.createBrowserTab("iab", "https://scholar.google.com/", {visible:true})` for a user-visible test. This does not require inventing a discovered browser ID. If a runtime reset is needed for a broken connection, use the documented reset tool and then its required first-call initialization. Do not reset a healthy runtime or clear cookies, sign out, change proxies, or switch browsers.
4. If creation or navigation times out, rediscover the actual tabs before trying to create another: the page may already exist. Reuse a successfully created tab. Connect and inspect the page in separate outer calls where supported. Do not create duplicate tabs in a recovery loop.
5. Resume from the visible state. If the intended title is already filled, submit it once in a separate call; if results are already visible, extract them. Otherwise fill, inspect, submit, and inspect in separate calls. Preserve successful metadata and the original requested query across recovery.
6. Allow one fresh-start recovery cycle per lookup after ordinary connection recovery fails or yields an empty inventory. Only if this cycle also fails, report the exact failed stage and what was attempted. CAPTCHA, explicit permission denials, and missing tool capabilities retain their own handling; do not attempt to bypass them. In delegated lookup, send the blocker or verified result to the parent without making citation availability a prerequisite for close reading.

This fallback is a user-required recovery rule. Its end-to-end success in a subagent has not yet been verified; do not label it tested solely because the instructions were added.

## Structured lookup recovery

For paper metadata and counts, [google-scholar-json.md](google-scholar-json.md) describes the observed JSON endpoint and its bounded fallback. Navigation completion, page content availability, and tool-state retrieval are separate signals. In testing, navigation and automatic accessibility reads timed out while a later standalone `tab.playwright.domSnapshot()` returned valid JSON. Separate tab acquisition from content reads, inspect the existing page before reissuing a query, and parse an obtained snapshot locally to avoid another slow browser call. Do not call a tool timeout a Scholar failure, and do not assume a successful read proves a particular underlying timeout cause.

## Timeouts

| Layer | Setting | Rule |
| --- | --- | --- |
| Outer browser tool call | `timeout_ms: 60000` | Upper bound, not a fixed delay; short outer limits have reset the runtime |
| Element visibility | `waitFor({state:'visible', timeoutMs:2000})` | Initial attempt plus at most two retries for explicit element-wait timeouts |
| Enter submission / clicks | `timeoutMs:15000` | Check state before retrying a timed-out mutation |
| DOM snapshot / navigation / connection | Only documented options | Do not invent inner timeout arguments |

Read snapshots at decision points, rather than repeatedly polling full pages. Retry a failed snapshot at most twice; recover a reset session before using bindings. Stop and report a persistent blocker instead of looping. Do not treat CAPTCHA, permissions, or stale-session errors as element timeouts. Avoid fixed sleeps, overlapping calls on one tab, and `Promise.race` that leaves requests running. Observed end-to-end latency exceeded inner limits; do not promise two-second reads or assert an unverified root cause.

## English and Simplified Chinese locators

Use current DOM language, not the language of the paper title, to select a dictionary. Reuse these semantic locators when the observed UI matches; refresh local DOM on mismatch. Do not hard-code coordinates, tab IDs, iframe IDs, or a particular paper's cluster ID. Other languages require discovery.

```javascript
const labels = {
  en: {
    year:'Year', any:'Any time', range:'Custom range',
    relevance:'Sort by relevance', date:'Sort by date',
    dialog:'Citations per year', start:'Start year', end:'End year',
    search:'Search', next:'Next', previous:'Previous',
    cancel:'Cancel', clear:'Clear', within:'Search within citing articles'
  },
  'zh-CN': {
    year:'年份', any:'时间不限', range:'自定义范围',
    relevance:'按相关性排序', date:'按日期排序',
    dialog:'每年引用数', start:'开始年份', end:'结束年份',
    search:'搜索', next:'下一页', previous:'上一页',
    cancel:'取消', clear:'清除', within:'在引用文章中搜索'
  }
};
const L = labels[language]; // language established from current DOM
```

### Title search

Run slow actions in separate outer calls. Read state after submission before deciding the next action. If multiple search boxes exist, scope to the observed page region.

```javascript
await tab.playwright.getByRole('textbox', {name:L.search, exact:true})
  .waitFor({state:'visible', timeoutMs:2000});
await tab.playwright.getByRole('textbox', {name:L.search, exact:true})
  .fill('"' + paperTitle + '"');
await tab.playwright.getByRole('textbox', {name:L.search, exact:true})
  .press('Enter', {timeoutMs:15000});
nodeRepl.write(await tab.playwright.domSnapshot());
```

### Menus, year input, and pagination

These are conditional steps, not one script to run end-to-end blindly. After a menu-changing action, inspect state before choosing another action.

```javascript
await tab.playwright.getByRole('button', {name:L.year, exact:true})
  .click({timeoutMs:15000});
// With the menu observed open, select ONE appropriate item:
await tab.playwright.getByRole('menuitemradio', {name:L.range, exact:true})
  .click({timeoutMs:15000});
// Alternatives use L.any, L.relevance, or L.date, after reopening the menu.
```

In the observed year dialog, `fill()` returned success but did not apply the range; keyboard input succeeded. Prefer `pressSequentially()` into verified empty fields. If nonempty, clear with documented keyboard selection/deletion and verify before typing; do not append to old years or mutate DOM with evaluate.

```javascript
await tab.playwright.getByRole('textbox', {name:L.start, exact:true})
  .pressSequentially(String(startYear), {timeoutMs:15000});
await tab.playwright.getByRole('textbox', {name:L.end, exact:true})
  .pressSequentially(String(endYear), {timeoutMs:15000});
// Read the actual values before submitting. Scope the duplicate Search button:
await tab.playwright.getByRole('dialog', {name:L.dialog, exact:true})
  .getByRole('button', {name:L.search, exact:true}).click({timeoutMs:15000});
// On a results page with an observed enabled Next control:
await tab.playwright.getByRole('button', {name:L.next, exact:true})
  .click({timeoutMs:15000});
```

Use full result content for collection. A short snapshot excerpt is sufficient only for a specific menu/filter check, not for declaring a page fully collected.

## CAPTCHA and access limits

Normally preserve the tab and ask the user to complete CAPTCHA, then inspect the same page to resume. An assistant attempt requires explicit confirmation for the current CAPTCHA at action time under the current tool policy; previous confirmation is not permanent permission. Do not bypass verification, rotate proxies, or repeatedly refresh. If verification has already disappeared, do not claim to have solved it. Stop retrieval on a persistent access restriction and retain the completed scope.

## Validation boundary

English and Simplified Chinese labels above were observed in September 2026. English search, year submission, clearing range, date sorting, and pagination were exercised. Chinese year menu, custom range, keyboard input, scoped submission, relevance switching, and pagination were exercised; Chinese date/any-time labels and state were observed but not independently clicked in that test. Retry branches and other languages were not exhaustively tested. Locator reuse saves discovery work, not browser-bridge latency.
