# OpenAI public submission checklist

The plugin bundle is prepared as a skills-only plugin. The following account-level actions must be completed by the publisher in the OpenAI Platform.

## Publisher setup

- [ ] Sign in to the OpenAI Platform organization that will own the plugin.
- [ ] Verify the individual or business developer identity.
- [ ] Ensure the submitter has **Apps Management: Write** permission.
- [ ] Confirm the displayed publisher name matches the verified identity and public project pages.

## Listing

- Plugin name: `Paper Close Reading`
- Submission type: `Skills only`
- Category: choose the closest available Education or Productivity category.
- Website: `https://github.com/Delores-Lin/paper-close-reading`
- Support: `https://github.com/Delores-Lin/paper-close-reading/issues`
- Privacy: `https://github.com/Delores-Lin/paper-close-reading/blob/main/PRIVACY.md`
- Terms: `https://github.com/Delores-Lin/paper-close-reading/blob/main/TERMS.md`
- Repository: `https://github.com/Delores-Lin/paper-close-reading`

Suggested short description:

> Read academic papers with traceable source locations.

Suggested long description:

> Guide rigorous close reading of academic papers, methods, experiments, figures, tables, and appendices. Explanations stay grounded in source locations and can be turned into reusable research notes.

## Upload and tests

- [ ] Push `PRIVACY.md`, `TERMS.md`, and `SUPPORT.md` so all listing URLs are public.
- [ ] Upload the final plugin ZIP without repository metadata or local caches.
- [ ] Enter the three starter prompts from `.codex-plugin/plugin.json`.
- [ ] Enter exactly five positive and three negative tests from `evals/submission-tests.json`.
- [ ] Select only countries or regions where the publisher is ready to provide the listing and support.
- [ ] Confirm policy attestations after reviewing the final package.
- [ ] Submit for review.
- [ ] After approval, return to the Portal and publish the approved version.

## Suggested release notes

> Initial public submission of Paper Close Reading 1.0.0, a skills-only plugin for source-grounded academic paper reading. The package includes whole-paper triage, section-level explanation, figure and table analysis, replication checks, reusable note templates, and explicit safeguards against fabricated evidence.
