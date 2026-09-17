# Changelog

## v1.5 — 2026-09-17

### Paper discovery and metadata

- Added a unified Python Scholar lookup helper with a local Node capability
  check, native fetch transport, and curl fallback for unsupported environments.
- Added structured candidates, citation counts, source links, acquisition times,
  opt-in caching, and explicit paper-identity matching requirements.
- Added bounded, on-request PDF downloads with file validation; paper identity
  and reading-version verification remain separate checks.
- Expanded initial metadata to include main authors and principal institutions
  from the paper or official source.
- Documented host-authorized sandbox recovery and existing-proxy diagnosis.
- Kept background literature and citing-paper exploration optional and driven
  by the user's request.

### Reading experience and documentation

- Refined paper-map metadata and the connection to optional discovery workflows.
- Added English and Chinese READMEs, quick-start prompts, and reading-flow diagrams.
- Added real Switch Transformers map-building demos and source/figure-reading
  screenshots, with historical citation counts clearly distinguished from live data.
- Added the editorial logo and README header artwork.

The public version label is **v1.5**; the plugin manifest uses **1.5.0**.


## 1.0.0 — 2026-07-11

- Packaged Paper Close Reading as a skills-only Codex plugin.
- Added progressive-disclosure references for critical reading, artifacts, and reusable notes.
- Added plugin discovery metadata and starter prompts.
- Added five positive and three negative submission tests.
- Added public privacy, terms, support, and submission documentation.
