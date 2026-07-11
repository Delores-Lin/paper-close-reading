---
name: paper-close-reading
description: Guide rigorous, source-grounded close reading of academic papers, technical reports, PDFs, selected sections, figures, tables, equations, or appendices. Use when the user asks to 精读/read closely a paper, explain selected text, continue section by section, critique methods or experiments, locate support for a claim, assess reproducibility, or create reusable research notes. Do not use for ordinary news, blog posts, or generic document summaries unless the user explicitly wants the academic-paper workflow.
---

# Paper Close Reading

Read papers as evidence-bearing arguments rather than summary material. Reopen the relevant source before answering, bind important statements to precise source locations, distinguish author claims from inference, and connect the paper to the user's research goal.

## Scope first

Identify the requested depth and scope:

- fast triage of the whole paper;
- standard close reading of the main argument, method, and evidence;
- replication-oriented reading including appendices, prompts, data, metrics, hyperparameters, and code;
- one section, paragraph, figure, table, equation, or appendix;
- whole-paper synthesis or reusable notes.

If the user's goal is unclear but reading can begin safely, start with fast triage and state the assumed goal. Ask only for information that cannot be recovered from the paper or public sources.

## Core workflow

1. Obtain or reopen the actual paper content. Do not rely on an abstract when the question concerns methods, figures, numbers, limitations, or wording.
2. For a newly introduced paper, verify current metadata when useful: official page, venue/status, version date, visible code/data links, and a reliably sourced citation count if available. Never guess current metadata.
3. Locate evidence precisely using section title, printed or PDF page, figure/table/equation number, appendix subsection, or paragraph context.
4. Explain in source-adjacent blocks: give the location, quote only the shortest useful fragment, then immediately explain it in Chinese by default unless the user requests another language.
5. When text invokes a figure, table, equation, or appendix, inspect that artifact before moving on. Address every cited artifact needed for the claim.
6. Separate four layers explicitly when relevant: what the paper states, what the evidence shows, what can be inferred, and your critique.
7. End with the next best reading target and why.

## First-pass triage

Use the 5C frame:

- Category: method, benchmark, dataset, survey, analysis, theory, position, or application.
- Context: the prior work or gap the paper responds to.
- Correctness: whether assumptions and evaluation design appear plausible.
- Contributions: the authors' claimed contributions without embellishment.
- Clarity: whether definitions, setup, and evidence are sufficiently clear.

Also provide:

```text
这篇论文解决的问题是：...
它对当前研究最可能有用的地方是：...
```

## Method and experiment reading

Before judging a result, extract:

| Item | What to identify |
|---|---|
| Task | What is measured or optimized |
| Input/output | What the system receives and produces |
| Ground truth | Who or what decides correctness |
| Data | Splits, filtering, distribution, and leakage risks |
| Method | Minimal operational description |
| Baselines | Comparisons and controls |
| Metrics | Exact definition and blind spots |
| Main claim | The conclusion being advanced |
| Evidence | Supporting figure, table, result, or proof |

Load `references/critical-reading.md` for detailed validity, reproducibility, and transfer checks.

## Figures, tables, and equations

Treat artifacts as part of the argument, not decoration. For each important artifact explain:

1. its number and page;
2. the surrounding claim that invokes it;
3. rows, columns, axes, colors, curves, variables, or assumptions;
4. the comparison being made;
5. visible metric changes and stability;
6. the authors' conclusion;
7. whether the artifact supports that conclusion and remaining caveats.

Load `references/artifact-reading.md` when figures, tables, equations, or appendices are central.

## Output and evidence rules

- Never invent quotations, page numbers, citations, metrics, code links, or metadata.
- If access is partial, say exactly which sections or pages were available and limit conclusions accordingly.
- If extraction is noisy, label locations as approximate and prefer page images or a cleaner source.
- Keep quotations short and interleave each quotation with its explanation.
- State whether a conclusion is explicit, implied, or your interpretation.
- Do not claim a result is current merely because it appeared in the paper; separate paper-era findings from current evidence.
- Do not degrade a close-reading request into an abstract summary.

For reusable notes, load `references/note-template.md` and fill only fields supported by the available evidence.

## Negative routing

- For a non-academic article, do not force this workflow; use ordinary document analysis unless the user explicitly requests the same framework.
- For an inaccessible or missing paper, do not simulate reading it. Request the source or explain what can be assessed from available metadata alone.
- For requests to fabricate support, refuse the fabrication and offer a verifiable alternative.
