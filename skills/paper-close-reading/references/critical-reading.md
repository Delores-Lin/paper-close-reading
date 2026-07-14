# Critical reading and transfer checks

Use only the checks relevant to the paper and the user's goal.

## Claim validity

- Are assumptions realistic for the stated use case?
- Does the dataset cover the phenomenon claimed?
- Does the metric measure the claimed capability?
- Are baselines fair, current enough for the paper's time, and implemented comparably?
- Are controls, ablations, confidence intervals, or negative results missing?
- Could gains arise from leakage, prompt format, annotation artifacts, spurious correlations, or language priors?
- Is the conclusion explicit in evidence, merely implied, or speculative?

## Reproducibility

- Is the task formulation operationally complete?
- Are data construction, filtering, and split rules available?
- Are prompts, hyperparameters, random seeds, model versions, and compute reported?
- Are evaluation scripts, code, checkpoints, and data accessible?
- Can the reported metric be reconstructed from the described procedure?
- Are sample sizes and uncertainty adequate for the claim?

## Transfer to the user's research

- Does the paper measure the capability the user actually cares about?
- Does its data distribution match the user's setting?
- Does it distinguish important failure causes rather than collapse them into one score?
- Does it handle uncertainty, abstention, boundary cases, or non-applicability when relevant?
- What components transfer directly, what require adaptation, and what should not transfer?
- Which experiment would most cheaply test transferability?

## Concept tracking

For important terminology, record:

| Term | Paper definition | Location | Difference from other literature | Transferability |
|---|---|---|---|---|
