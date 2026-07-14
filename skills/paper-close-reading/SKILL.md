---
name: paper-close-reading
description: Guide rigorous, source-grounded close reading of academic papers, technical reports, PDFs, sections, figures, tables, and appendices through either guided interactive reading or autonomous full-paper analysis. Use when the user asks to read a paper closely, continue to the next section, explain selected text, follow a three-pass reading process, inspect cited visual evidence, critique experiments, resume a multi-turn reading, or produce reusable research notes with precise source locations, methods, metrics, limitations, and task transfer.
---

# Paper Close Reading

## Overview

Read papers through a source-grounded three-pass process and produce reusable research outputs. Support guided interactive reading and autonomous full-paper analysis without silently choosing between them. Match the user's language unless the user requests another language. Do not give generic summaries. Rebuild context from the relevant pages before explaining, cite precise locations, interleave short source fragments with explanation in the user's language, integrate cited figures and tables with the surrounding argument, distinguish paper claims from inference or critique, and preserve progress during sustained multi-turn reading.

## Core Workflow

1. Identify the requested scope: one-off explanation, whole-paper triage, sustained close reading, current or next section, individual paragraph, method, experiment, visual artifact, appendix, related work, or whole-paper synthesis.
2. For sustained reading, use the interaction mode explicitly selected in the current conversation. If the user has not selected one, ask whether to use Guided or Autonomous mode and stop before beginning Pass 1. Do not choose a default. Keep one-off explanations in the conversation without requiring mode selection or creating files.
3. For a newly introduced paper, look up external metadata once: venue/status, official or arXiv page, version date, reliable citation count when available, and visible code/data/project links. Record the source and lookup date in the conversation and include it in final notes when notes are requested; do not repeat it in every section.
4. After the interaction mode is known, apply the mandatory three-pass workflow at the selected effort level. A triage-only request may stop after Pass 1; a selected-text request may use the local source-adjacent pattern without processing the whole paper.
5. Re-read or re-extract the relevant source pages before every close-reading answer. Never rely only on earlier-turn memory when wording, location, or evidence matters.
6. Locate evidence precisely and explain it in source-adjacent blocks. When text cites figures, tables, equations, or appendices, resolve every cited artifact in citation order before continuing.
7. Separate explicit paper claims from inference, critique, and transfer. Label each clearly.
8. In Guided mode, end each unit by stating the exact next section or artifact and why it comes next. In Autonomous mode, complete the requested outputs before reporting completion.

## Interaction Mode

Require an explicit mode for sustained whole-paper close reading. Neither mode is the default.

- **Guided mode**: Teach the paper interactively, one bounded unit at a time, and wait for the user between units.
- **Autonomous mode**: Complete the requested passes independently and deliver the resulting notes and synthesis.

Treat requests to start a close reading or be guided through a paper as ambiguous unless they explicitly specify the interaction style. Ask one concise question in the user's language before starting. The question must present both options clearly:

```text
Which mode should I use for this paper: Guided, where we read one unit at a time and pause for you, or Autonomous, where I complete all three passes and deliver the full notes?
```

Do not ask when the user requests only a selected passage, term, figure, table, or other one-off explanation. Do not ask again when a mode is already established in the current conversation. In a new conversation where the intended mode is unclear, ask again. Change modes only when the user explicitly requests the change.

### Guided Mode Rules

- Complete Pass 1, present the paper map to the user, and stop. Do not enter Pass 2 automatically.
- Before Pass 2, establish whether the user wants unit-level or paragraph-level reading. Ask if the user has not already made the desired granularity clear. Retain that choice for the current conversation, but let the user change it explicitly at any time.
- In unit-level reading, handle at most one section or one coherent natural unit per user turn.
- In paragraph-level reading, handle exactly one source paragraph per user turn. Do not merge adjacent paragraphs merely because they discuss the same topic.
- Interpret any brief continuation request, such as "next," "continue," or "next section," as authorization for exactly one next unit, not the rest of the paper.
- Resolve and display every figure, table, equation, and appendix cited by the current unit before stopping, but do not use those references as permission to enter the next unit.
- Ask for confirmation before entering Pass 3 after Pass 2 is complete.
- Treat a section as complete only after its close reading and visual evidence have been delivered in the user-facing conversation.
- Do not create or update `close-reading.md` during Guided mode unless the user explicitly asks to take notes while reading.
- After Pass 3 has been delivered, ask whether the user wants the guided reading consolidated into `close-reading.md`. Create it only after confirmation, and never present a note link before the file exists and the user has requested it.
- Treat notes as an optional record of the guided session, never as a substitute for showing the explanation to the user.
- End each unit with the exact proposed next unit and wait for the user.

### Guided Reading Granularity

Offer these two Pass 2 granularities in the user's language:

- **Unit-level**: Read one section or coherent argumentative unit per turn. Use this for efficient coverage while preserving source-grounded explanation.
- **Paragraph-level**: Read exactly one source paragraph per turn. Use this when the user wants the original text and evidence examined line by line.

For paragraph-level reading, use this sequence:

1. Give the exact section, printed page when available, PDF page, and enough opening words to identify the paragraph unambiguously.
2. Reproduce the complete source paragraph as one block when the source is locally available or supplied by the user. Preserve sentence order and do not replace the paragraph with selected fragments or a summary.
3. Explain every sentence in order, including terminology, references, logical connectors, assumptions, and its role in the paragraph's argument.
4. Retrieve, crop, display, and explain every figure, table, equation, or appendix cited in that paragraph. Place each visual immediately after the sentence that invokes it and process multiple citations in source order.
5. State the paragraph's main claim, its connection to the preceding argument, what evidence supports it, and any critical caveat.
6. Stop after that paragraph and its cited artifacts are fully resolved. Name the next paragraph by location or opening words and wait.

Do not let a broad section summary substitute for paragraph-level reading. If a paragraph is unusually long, still keep it as one reading unit unless the user explicitly permits sentence-level subdivision. If a complete quotation cannot be provided, state the constraint instead of silently presenting an excerpt as the full paragraph.

### Autonomous Mode Rules

- Enter this mode only after the user explicitly requests an independent, one-shot, or complete full-paper reading, or selects Autonomous mode when asked.
- Execute the requested passes without pausing between ordinary sections, while preserving the same evidence, figure, critique, and note-quality requirements.
- Deliver a concise completion summary and links to the self-contained notes. Do not claim the user was “guided through” material that was processed only autonomously.

## Mandatory Three-Pass Workflow

Use all three passes for sustained whole-paper close reading unless the user explicitly narrows the task. Apply the pass-transition rules of the selected interaction mode.

### Pass 1: Map the Paper

Read the title, abstract, introduction, conclusion, section structure, figure/table captions, and reference signals. Produce:

- First-Pass 5C triage and a one-sentence positioning note.
- The research question, claimed contributions, argument structure, and core terminology.
- A list of key figures, tables, appendices, and prerequisites.
- A dependency-based Pass 2 reading order.

Do not treat caption scanning as evidence sufficient to accept experimental claims.

### Pass 2: Close-Read the Evidence

Read the paper section by section. For each claim:

- Reopen the relevant pages and quote the shortest complete sentence or clause that preserves the claim in unit-level reading; quote the complete paragraph in paragraph-level reading.
- Explain terminology, method, assumptions, implication, and source location immediately after the quote.
- Decompose methods and experiments before judging results.
- Retrieve and explain every cited figure, table, equation, and appendix in context.
- Record conclusions, caveats, unresolved questions, and cross-section dependencies.

Do not mark a section complete while a cited artifact that materially supports its argument remains unresolved.

### Pass 3: Critique and Synthesize

After the intended main text and appendices are covered:

- Build a claim-evidence map and test whether each major conclusion is supported.
- Evaluate assumptions, datasets, metrics, baselines, controls, ablations, uncertainty, generalization, and reproducibility.
- Separate robust findings from suggestive evidence and speculation.
- Compare terminology and claims with relevant prior or later work when needed.
- Deliver the final critique and synthesis. Include task transfer, related-work language, experiment ideas, and open questions when relevant.

Do not declare a sustained whole-paper reading complete until Pass 3 has been delivered. In Guided mode, final notes are optional and require confirmation; in Autonomous mode, finish the requested notes before reporting completion.

## Effort Level

Choose how deeply to execute the applicable passes. Effort level does not replace pass order.

- **Fast**: Execute Pass 1 to decide relevance; continue only if requested or clearly required.
- **Standard**: Execute all three passes over the introduction, method, main experiments, core visual evidence, limitations, and conclusion.
- **Replication-oriented**: Execute all three passes and also inspect appendices, prompts, data construction, metrics, hyperparameters, code/data links, and evaluation scripts.

## First-Pass 5C Triage

For a first pass over a paper, answer:

- **Category**: method, benchmark, dataset, survey, analysis, theory, position, or application paper.
- **Context**: what prior work or research gap it responds to.
- **Correctness**: whether the assumptions and evaluation design appear plausible.
- **Contributions**: the paper's claimed contributions, not your embellished version.
- **Clarity**: whether terms, setup, and evidence are clear enough to trust or reuse.

Also produce a one-sentence positioning note:

```text
The problem this paper addresses is: ...
Its most likely value for the current research is: ...
```

Render these labels in the user's language.

## Source-Adjacent Explanation Pattern

For unit-level close reading, use this structure. Report external metadata only when first introducing the paper, when it changes, or when it is directly relevant to the current section.

- **Location**: name the section and page, plus table/figure/appendix if relevant.
- Then read in repeated blocks:
  - `Source (Section/Page/Figure/Table)`: quote the complete sentence whenever feasible, with the exact location in the label. If the sentence is too long or contains unrelated clauses, quote the shortest complete clause or sentence that preserves the claim.
  - `Explanation`: explain that exact sentence or clause in the user's language, including terms, method, claim, implication, and whether it is explicit or inferred.
- **Why it matters**: connect the section to the paper's argument, method, experiment, or evaluation design.
- **Critical reading**: identify assumptions, metric caveats, baseline issues, limitations, missing controls, or overclaiming.
- **Transfer to the user's research**: state how the idea can or cannot transfer to the user's concrete research question.
- **Next step**: suggest the next section, table, figure, appendix, or paper to inspect.

Translate these presentation labels into the user's language; do not force English labels into a non-English response.

For selected text explanations, keep it tighter: give the location if known, quote the shortest relevant fragment, paraphrase/translate it, define terms in context, and explain why the authors wrote it there.

For paragraph-level Guided reading, use the stricter sequence in Guided Reading Granularity instead of shortening the source to isolated claim fragments.

## Concept Tracking

Build a lightweight terminology map while reading. Track each important term's definition, first location, and whether another paper uses it differently. Prioritize terms that define the task, label space, evidence standard, measurement target, uncertainty or confidence notion, failure mode, distribution shift, ground truth, baseline, and evaluation metric.

Use a table when it helps:

| Term | Paper definition | Location | Transferability |
|---|---|---|---|

## Method And Experiment Decomposition

For method, benchmark, and experiment sections, extract the setup before judging the conclusion:

- Task formulation: what problem is being measured or optimized.
- Input and output: what the model receives and produces.
- Ground truth: who or what decides correctness.
- Data: training, validation, test, distribution shifts, and filtering.
- Model or algorithm: the minimal operational description, not every implementation detail unless needed.
- Baselines and controls: what comparisons make the claim meaningful.
- Metrics: exact definitions and what they do or do not measure.
- Evidence: which figure/table/result supports each claim.

Prefer a compact table:

| Item | Content |
|---|---|
| Task |  |
| Input |  |
| Output |  |
| Ground truth |  |
| Metric |  |
| Baseline/control |  |
| Main claim |  |
| Evidence |  |

## Figure And Table Reading

Read figures and tables as part of the paper's argument, not as isolated illustrations. When a paragraph says "as shown in Figure X" or a contribution cites a table, first explain the paragraph's claim, then inspect the figure/table to test how that evidence supports the claim. If the paragraph cites multiple figures/tables/appendices, handle them in citation order and state which part of the claim each one supports.

In paragraph-level reading, every visual artifact cited by the current paragraph is mandatory even when it appears in the appendix or on a distant page. Do not postpone it to a later figure-only unit.

When a local PDF and rendering tools are available, render and embed each cited figure or table that materially supports the current claim:

1. Render the source page at a readable resolution.
2. Crop the complete visual artifact, retaining its title or caption, axes, legend, labels, and essential footnotes when feasible.
3. Visually inspect the crop for clipping, unreadable text, blank output, or incorrect figure boundaries.
4. Save it in the current paper artifact directory's `images/` subdirectory with a stable descriptive name such as `figure_06_calibration_across_tasks.png`. Reuse an existing verified crop instead of regenerating it.
5. In the user-facing conversation, embed the image with its absolute filesystem path so the app can render it.
6. When `close-reading.md` is created, embed the same image with a path relative to the note, such as `images/figure_06_calibration_across_tasks.png`. Do not write absolute filesystem paths or `file://` URLs into persistent Markdown notes.
7. Embed the image immediately after the sentence or explanation that invokes it. Do not collect all screenshots in a detached gallery.
8. Inspect the image itself. If a Markdown note is created, also confirm that every relative image link resolves to an existing readable file.

If reliable cropping is unavailable, show the rendered full page or provide the precise page and explain the limitation. Typeset equations directly unless their visual layout is necessary to interpret them.

For important figures or tables, explain:

1. Figure/table number and page.
2. The exact sentence, claim, or contribution in the surrounding text that invokes it.
3. What the rows, columns, axes, colors, or curves represent.
4. What comparison is being made.
5. Which metric changes, by how much when visible, and whether the pattern is stable.
6. What conclusion the authors draw.
7. Whether the figure/table actually supports that conclusion, and what caveat remains.

Do not say only "performance improves"; specify dataset, metric, baseline, direction, and caveat.

## Critical Reading Checklist

Ask these questions before accepting a claim:

- Are the assumptions realistic for the target use case?
- Does the dataset cover the claimed phenomenon?
- Does the metric actually measure the claimed capability?
- Are baselines fair and strong enough?
- Are there missing controls, ablations, confidence intervals, or negative results?
- Could results come from leakage, prompt format, annotation artifacts, spurious correlations, or language priors?
- Is the conclusion explicit in the evidence, implied, or speculative?
- What cannot be transferred to the user's problem?

For the user's current research question, dynamically add domain-specific checks. Derive them from the user's target capability, task boundary, data distribution, failure modes, confounders, reliability requirements, and evaluation metrics. Do not hard-code checks for one domain unless the user explicitly asks for that domain.

Use this generic pattern:

- Does the paper actually measure the capability the user cares about?
- Does it distinguish major failure causes instead of collapsing them into one error rate?
- Does it allow uncertainty, abstention, boundary cases, or non-applicability when relevant?
- Does it cover the target deployment or research distribution?
- Does it report the reliability, generalization, cost, or risk metrics needed for the user's goal?

## Output Artifacts

Keep paper-specific visual artifacts self-contained when a writable local paper directory is available:

```text
<paper-directory>/notes/<paper-stem>/
├── close-reading.md   # only when requested in Guided mode; always for Autonomous delivery
└── images/            # created as needed for figure/table delivery
    ├── figure_01_<description>.png
    ├── table_01_<description>.png
    └── page_01.png
```

Keep rendered pages, cropped figures, cropped tables, and other note-specific visual evidence inside `images/`. Do not place them in a distant shared `figures/` directory unless the user explicitly requests shared assets. Preserve the whole note directory as a movable unit whose Markdown links remain valid after relocation.

In Guided mode, do not create `close-reading.md` by default. If the user requests note-taking during reading, build it incrementally; otherwise ask after Pass 3 whether to create it from the delivered reading and verified source. In Autonomous mode, create and consolidate `close-reading.md` as part of the requested delivery. Use this structure:

- One-sentence positioning
- Research question
- Core terminology
- Method decomposition
- Key figures and tables
- Main conclusions
- Limitations and counterexamples
- Implications for the user's research
- Reusable related-work language
- Reusable experiment designs
- Recommended next reading

Render these headings in the user's language.

Do not create persistent artifacts for a one-off excerpt explanation unless the user asks for notes.

For a group of papers, organize reading order by dependency rather than chronology: problem definition, benchmark/dataset, method/metric, analysis/critique, then latest extensions.

## Evidence Rules

- Never present remembered detail as newly verified. If wording, page, or figure location matters, re-open or re-extract the source.
- When the user asks "where is this in the paper?" or challenges a claim, verify against the source and state whether it is explicit, implied, or your explanation.
- If PDF extraction is noisy, use page/section context and say when the citation is approximate.
- Prefer quoting a complete sentence with an exact location label, while keeping quotes short and relevant in ordinary unit-level reading. In user-requested paragraph-level reading of a locally available or user-supplied paper, reproduce the complete current paragraph as required by that mode; do not extend the quotation into neighboring paragraphs.
- Do not separate all quotes into one section and all explanations into another; interleave quote and explanation.
- Citation counts, venue status, version dates, and code/data availability are current external facts. Browse for them when starting a new paper or when asked; do not rely on memory.
- Cache external metadata after the first lookup and do not repeat it section by section unless it changes or matters to the current argument.
- If the paper is old and the user asks whether a result is still current, separate paper-era conclusions from current-day claims.

## Tone And Granularity

Be precise, patient, and source-grounded. Prefer compact explanations that teach the user how to read the paper's logic. Avoid generic praise, unsupported claims, and vague summaries such as "the method works well" without evidence.
