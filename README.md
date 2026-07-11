# Paper Close Reading

Paper Close Reading is a skills-only Codex plugin for rigorous, source-grounded reading of academic papers. It supports whole-paper triage, section-by-section explanation, figure and table analysis, experiment critique, replication-oriented reading, and reusable research notes.

## What it does

- Reopens the relevant paper pages before making source-specific claims.
- Binds important statements to sections, pages, figures, tables, equations, or appendices.
- Separates author claims, observed evidence, inference, and critique.
- Explains short source fragments adjacent to their interpretation.
- Produces structured method, experiment, limitation, and transfer notes.
- Refuses to invent quotations, page numbers, metrics, citations, or metadata.

## Plugin contents

```text
.codex-plugin/plugin.json
skills/paper-close-reading/
  SKILL.md
  agents/openai.yaml
  references/
assets/
evals/submission-tests.json
PRIVACY.md
TERMS.md
SUPPORT.md
```

## Example prompts

- “Read this paper section by section with cited source locations.”
- “Explain Figure 3 and Table 2 and test whether they support the authors' claim.”
- “Read this paper for replication and list every missing implementation detail.”
- “精读这篇论文，并判断它的方法能否迁移到我的研究课题。”

## Local validation

Run the official plugin and skill validators before packaging:

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
python3 /path/to/skill-creator/scripts/quick_validate.py skills/paper-close-reading
```

## Public submission

Submit this as a **Skills only** plugin through the OpenAI Plugin Submission Portal. Use `evals/submission-tests.json` for the required five positive and three negative tests. See `SUBMISSION.md` for the remaining account-level steps.

## License

MIT. See `LICENSE`.
