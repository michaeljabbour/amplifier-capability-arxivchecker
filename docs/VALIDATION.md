# Local validation — 2026-11-03

This record describes local checks of the capability and fictional fixtures. It does not establish scientific validity, model quality, arXiv acceptance, user savings or publication. The broader benchmark in `BENCHMARK.md` remains a plan.

## Completed checks

- Core regression suite: 35 tests, including real pdflatex clean builds, embedded-font checks, reference-PDF text/page-count comparison, missing series/data rejection, units and denominator rules, exact source-byte hashes, concurrent source-edit rejection, explicit source allowlists, deterministic packaging and overwrite protection.
- Figure/crop suite: 9 tests passed using the existing Python 3.14 environment with matplotlib and Pillow. Default Python lacks these two optional libraries and skips two rendering tests. No packages were installed.
- Fictional vector figure and lossless crop were produced and visually inspected. All requested series, intervals and labels are present; the crop retains its footnote. `pdffonts` reports embedded CID TrueType STIXGeneral, with no Type 3 fonts. See [figure evidence](evidence/2026-11-03/figures/README.md).
- Installed Amplifier runtime: offline bundle composition for both the root and behavior-only entry; actual skill discovery/loading and mode discovery; recipe validation returned valid with no warnings. No provider, paid session or global app configuration was changed. The recipe was validated, not executed through a model.

- Portable-release regression suite: 6 tests passed. Complete recursive installation is idempotent; edited copies are refused; explicit replacement preserves a backup; symlinks and overlapping destinations are rejected; ZIPs are deterministic and match source bytes. See [the 50-test run](evidence/2026-11-03/tests-python314.txt) and [the earlier portable smoke record](evidence/2026-11-03/integration/portable-smoke.json). That earlier record's ZIP hash applies to its observed snapshot, not later edits.
- [Amplifier runtime record](evidence/2026-11-03/integration/amplifier-smoke.json): root and behavior-only load, namespace resolution, real skill/mode discovery and recipe validation. The public record normalizes machine-specific path prefixes; the original is retained privately. `scripts/smoke_amplifier.py` makes this repeatable using an existing Amplifier environment and cached official dependencies.
- Static site build and checks passed: two HTML pages, 55 local links/assets/fragments, 54 Markdown destinations, 18 portable files, canonical workflow order, source/download/ZIP byte fidelity and SHA-256. JavaScript syntax check passed. The site uses relative links for repository-subpath hosting.
- Browser review passed at 1280×720 and 390×844. The landing page and mobile playbook have no horizontal overflow. Claim details expand, the checklist changes from 0 to 1 and resets to 0, and the 47.958-second film plays with visible captions. The responsive override was reset after testing. See [browser observations](evidence/2026-11-03/browser-review.json).

All **50 automated regression tests passed** with existing `/opt/homebrew/bin/python3.14`, including both optional rendering tests. No software was installed. These are local software and integration checks; no model-driven end-to-end study-to-paper benchmark was run.

## Official-source audit and template build

The portable [requirements map](../skills/arxivchecker/references/requirements.md) and [submission-policy map](../skills/arxivchecker/references/submission.md) record official sources accessed on 2026-11-03. They distinguish requirements, conditional rules, recommendations and local choices, and document conflicts or unverified limits. Boundary tests cover `.bib`-only and `.bbl`-only source, optional affiliations, ordinary TODO prose, braceless/macro/graphics search-path inputs, nested main files, required generated inputs, frozen caches and unsupported local engines. Local reports explicitly leave arXiv eligibility unassessed.

A fictional document generated from the actual neutral template compiled in three clean pdflatex passes to two pages, with no local errors and passing font inspection. This tests template structure and installed packages, not scientific or policy approval. See [template build report](evidence/2026-11-03/template/report.json).

## What still needs a person

Every actual study needs review of scientific claims and denominators, figure/page readability, references and support for cited claims, exact author information, AI-use disclosure, permissions, release rights, arXiv category, licence and endorsement. The helpers cannot confer those approvals.

The original source skill is preserved outside this repository. This capability is local and unpublished; no push, hosted deployment or arXiv submission has occurred.
