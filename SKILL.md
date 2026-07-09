---
name: paper-close-reading
description: Guide rigorous close reading of academic papers, technical reports, PDFs, paper sections, figures, tables, or appendices. Use when the user asks to 精读/read closely a paper, continue to the next section, explain selected paper text, build a reading order, summarize with source locations, critique experiments, or turn paper reading into reusable research notes with citations, methods, metrics, limitations, and transfer to the user's research question.
---

# Paper Close Reading

## Overview

Use this skill to read papers with source-grounded interpretation and reusable research outputs. Do not give generic summaries. Rebuild context from the relevant paper pages before explaining, cite section/page/table/figure locations, quote only short source fragments, immediately explain each fragment in Chinese by default, distinguish paper claims from inference or critique, and connect the paper to the user's research question.

## Core Workflow

1. Identify the requested scope: whole-paper triage, current section, next section, selected text, method, result table, figure, appendix, related work, or whole-paper synthesis.
2. For a newly introduced paper, look up current external metadata before close reading: citation count when reliably available, publication venue/status, official paper page, arXiv/preprint page, version date, and visible code/data/project links. Prefer Google Scholar for citation count when accessible; otherwise use Semantic Scholar, OpenReview, DBLP, Crossref, publisher/conference pages, or arXiv and state the lookup source/date. If no reliable citation count is accessible, say so rather than guessing.
3. Re-read the relevant source before answering. For PDFs, extract or reopen the target pages; do not rely only on memory from earlier turns.
4. Locate evidence precisely: section title, page number, table/figure number, appendix subsection, or paragraph context.
5. Explain in source-adjacent blocks: show a short original fragment, then immediately explain that fragment in Chinese before moving to the next fragment.
6. Separate what the paper explicitly says from what can be inferred; label critiques and task transfers as your interpretation.
7. End with what to read next and why.

## Reading Depth

Choose the reading depth explicitly when useful:

- **Fast triage**: Read title, abstract, introduction, figure/table captions, conclusion, and reference signals. Use for weakly related papers, surveys, or deciding whether to continue.
- **Standard close reading**: Read introduction, method, main experiments, core figures/tables, limitations, and conclusion. Use for most related work.
- **Replication-oriented reading**: Also inspect appendix, prompts, data construction, metrics, hyperparameters, code/data links, and evaluation scripts. Use for papers whose method or benchmark may shape the user's own experiments.

## First-Pass 5C Triage

For a first pass over a paper, answer:

- **Category**: method, benchmark, dataset, survey, analysis, theory, position, or application paper.
- **Context**: what prior work or research gap it responds to.
- **Correctness**: whether the assumptions and evaluation design appear plausible.
- **Contributions**: the paper's claimed contributions, not your embellished version.
- **Clarity**: whether terms, setup, and evidence are clear enough to trust or reuse.

Also produce a one-sentence positioning note:

```text
这篇论文解决的问题是：...
它对当前研究最可能有用的地方是：...
```

## Source-Adjacent Explanation Pattern

For section-level close reading, use this structure:

- **外部元信息**: report venue/status, citation count if reliably available, official/arXiv page, version date, code/data links when visible, and lookup date/source.
- **位置**: name the section and page, plus table/figure/appendix if relevant.
- Then read in repeated blocks:
  - `原文`: quote one short phrase or sentence fragment from the relevant location.
  - `解释`: explain that exact fragment in Chinese, including terms, method, claim, implication, and whether it is explicit or inferred.
- **为什么重要**: connect the section to the paper's argument, method, experiment, or evaluation design.
- **批判性阅读**: identify assumptions, metric caveats, baseline issues, limitations, missing controls, or overclaiming.
- **迁移到用户课题**: state how the idea can or cannot transfer to the user's concrete research question.
- **下一步**: suggest the next section, table, figure, appendix, or paper to inspect.

For selected text explanations, keep it tighter: give the location if known, quote the shortest relevant fragment, paraphrase/translate it, define terms in context, and explain why the authors wrote it there.

## Concept Tracking

Build a lightweight terminology map while reading. Track each important term's definition, first location, and whether another paper uses it differently. Prioritize terms that define the task, label space, evidence standard, measurement target, uncertainty or confidence notion, failure mode, distribution shift, ground truth, baseline, and evaluation metric.

Use a table when it helps:

| 术语 | 论文定义 | 位置 | 可迁移性 |
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

For important figures or tables, explain:

1. Figure/table number and page.
2. What the rows, columns, axes, colors, or curves represent.
3. What comparison is being made.
4. Which metric changes, by how much when visible, and whether the pattern is stable.
5. What conclusion the authors draw.
6. Whether the figure/table actually supports that conclusion.

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

When the user is building research notes, end each paper or major section with a compact note containing:

- 一句话定位
- 研究问题
- 核心术语
- 方法拆解
- 关键图表
- 主要结论
- 局限和反例
- 对用户课题的启发
- 可写进 related work 的句子
- 可复用实验设计
- 下一步阅读建议

For a group of papers, organize reading order by dependency rather than chronology: problem definition, benchmark/dataset, method/metric, analysis/critique, then latest extensions.

## Evidence Rules

- Never present remembered detail as newly verified. If wording, page, or figure location matters, re-open or re-extract the source.
- When the user asks "where is this in the paper?" or challenges a claim, verify against the source and state whether it is explicit, implied, or your explanation.
- If PDF extraction is noisy, use page/section context and say when the citation is approximate.
- Keep quotes short and relevant. Do not reproduce long paper passages.
- Do not separate all quotes into one section and all explanations into another; interleave quote and explanation.
- Citation counts, venue status, version dates, and code/data availability are current external facts. Browse for them when starting a new paper or when asked; do not rely on memory.
- If the paper is old and the user asks whether a result is still current, separate paper-era conclusions from current-day claims.

## Tone And Granularity

Be precise, patient, and source-grounded. Prefer compact explanations that teach the user how to read the paper's logic. Avoid generic praise, unsupported claims, and vague summaries such as "the method works well" without evidence.
