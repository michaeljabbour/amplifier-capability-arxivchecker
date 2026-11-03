# Working on ArxivChecker

- Read `skills/arxivchecker/SKILL.md`, `skills/arxivchecker/references/workflow.md` and `skills/arxivchecker/references/policy.md` before changing the method. Record substantive changes in `CHANGELOG.md`.
- Keep one canonical `SKILL.md`. Modes and recipes stay short and point to the method instead of copying it.
- Never fabricate study results, authors, affiliations, references, preregistration or human approval. Templates and demonstrations are neutral or explicitly synthetic.
- Do not copy the originating paper's names, numbers, model catalogue, result schema, bibliography or artboard coordinates. Preserve provenance hashes in `docs/PROVENANCE.md`.
- Keep denominators tied to the research question and prior rules. Report full-population context, exclusions, missingness, units, cost scope and exploratory analyses.
- Reject missing keys/series, non-finite numbers, unsafe paths and out-of-bounds crops visibly. Never silently drop data or silently clamp crops.
- Treat generated figures and compiled PDFs as unreviewed until visually inspected. Report exactly what automated checks and human reviews ran.
- Distinguish style defaults from current arXiv policy and cite official documentation with a check date. A local preflight is not acceptance or peer review.
- Use explicit package file allowlists. Do not include private datasets, credentials, drafts, logs, unrelated caches or other unrelated files by directory glob. Preserve required build inputs, including compatible frozen minted caches and needed index/glossary outputs, through an explicit allowlist.
- Preserve originals and existing work. Keep tests in isolated temporary folders; never write into shared/production systems.
- Keep the site static and local-first, with no analytics, remote fonts or backend dependency. Include visible labels, keyboard controls and reduced-motion support.
- Run the documented build, repository checks, script tests and JavaScript syntax checks after changes. Inspect desktop and phone layouts after UI changes.
- Never claim users, measured savings, benchmark success, publication or deployment without dated evidence.
- Do not add remotes, push, publish, deploy, submit to arXiv or contact anyone unless asked.
