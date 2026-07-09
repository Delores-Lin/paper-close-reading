---
name: paper-close-reading
description: Guide a rigorous close reading of academic papers, technical reports, PDFs, or paper sections. Use when the user asks to 精读/read closely a paper, continue to the next section, explain selected paper text, summarize a section with source locations, or turn paper-reading behavior into a cited step-by-step interpretation workflow.
---

# Paper Close Reading

## Overview

Use this skill to guide a user through a paper section by section with source-grounded interpretation. Always rebuild context from the relevant paper pages before explaining, cite the section/page/table/figure location, quote a short source fragment immediately before explaining that fragment, distinguish paper claims from your own interpretation or critique, and check current paper metadata before starting a new paper.

## Core Workflow

1. Identify the requested scope: selected text, current section, next section, table, figure, appendix, or whole-paper synthesis.
2. For a newly introduced paper, look up current external metadata before the close reading: citation count, publication venue/status, official paper page, arXiv/preprint page if relevant, and code/data links when visible. Prefer Google Scholar for citation count when accessible; if unavailable or blocked, use Semantic Scholar, OpenReview, DBLP, Crossref, publisher/conference pages, or arXiv and state the source and lookup date.
3. Re-read the relevant source before answering. For PDFs, extract the target pages or reopen the page text; do not rely only on memory from earlier turns.
4. Locate evidence precisely: section title, page number, table/figure number, appendix subsection, or paragraph context.
5. Explain in source-adjacent blocks: show a short original fragment, then immediately explain that fragment in Chinese before moving to the next fragment.
6. Quote only the shortest useful original phrases. Prefer paraphrase for the rest.
7. Explain in Chinese by default when the user is reading in Chinese.
8. Separate what the paper explicitly says from what can be inferred, and label critiques as your interpretation.
9. End with the next useful reading step when continuing a guided reading.

## Answer Pattern

For a section-level close reading, use this structure:

- **外部元信息**: for a new paper, report citation count and publication venue/status with source and lookup date.
- **位置**: name the section and page, plus table/figure/appendix if relevant.
- Then read in repeated source-adjacent blocks:
  - `原文`: quote one short phrase/sentence fragment from the relevant location.
  - `解释`: immediately explain that exact fragment in Chinese, including terms, method, claim, or implication.
- **为什么重要**: connect the section to the paper's argument, experiment, or evaluation design.
- **批判性阅读**: mention assumptions, limitations, metric caveats, or unstated implications when useful.
- **下一步**: suggest the next section or question to inspect.

For selected text explanations, keep it tighter:

1. Give the location if known.
2. Quote the selected sentence fragment or the relevant part of it.
3. Immediately translate/paraphrase and define technical terms in context.
4. Explain why the authors wrote it at that point in the argument.

## Evidence Rules

- Never present a remembered detail as newly verified. If exact wording or page location matters, re-open/re-extract the source.
- When the user asks "where is this in the paper?" or challenges a claim, verify against the source and state whether it is explicit, implied, or your own explanation.
- If a PDF extraction is noisy, use page/section context and say when the citation is approximate.
- Keep quotes short and relevant. Do not reproduce long paper passages.
- Do not separate all quotes into one section and all explanation into another for close reading; interleave quote and explanation so each explanation is anchored to the exact source fragment.
- Citation counts, publication status, and venue information are current external facts. Browse for them when starting a new paper or when the user asks for them; do not rely on memory.
- If the paper is old and the user asks whether a result is still current, separate paper-era conclusions from current-day claims.

## Common Reading Moves

- **Method section**: extract task formulation, assumptions, inputs/outputs, metrics, and what is controlled or uncontrolled.
- **Experiment section**: read tables by row/column, explain what each metric means, and identify whether the result supports the stated claim.
- **Analysis section**: distinguish measured failure modes from author speculation about causes.
- **Related work**: explain what gap the paper claims and whether the comparison is fair.
- **Conclusion**: separate contribution summary from limitations and future work.

## Tone And Granularity

Be precise, patient, and source-grounded. Avoid turning close reading into a generic summary. Prefer compact explanations that teach the user how to read the paper's logic.
