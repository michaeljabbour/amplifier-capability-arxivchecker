# Provenance and adaptation

ArxivChecker was adapted on 2026-11-03 from the user's installed `arxiv-paper-from-study` Claude Code skill and its accompanying figure, artboard and LaTeX examples. The original files were inspected locally and left unchanged. They came from one specific study; this repository does not redistribute that paper's names, results, bibliography, model catalogue or artboard coordinates.

## Source fingerprints

Source root: `~/.claude/skills/arxiv-paper-from-study/`.

| File | SHA-256 at inspection |
| --- | --- |
| `SKILL.md` | `acfbee3ce81bbd1c06c776de1ed6ce6c40a79b27ddb1ccb1a1fab6aedc0d153d` |
| `scripts/make_figures.py` | `ca6218edd2b5b7135845caed857bad45313dfd29a1be79b304b818a88ee1de29` |
| `scripts/crop_artboards.py` | `02209e7b02bd7ab0c1a2e4d55ca04751504c6bce995688f6445c24cf62daff5b` |
| `scripts/example_main.tex` | `9fbdf4798584b54b0573c66cfac12c7a09b65a446ec9a51ece881262e698c8c5` |

No separate licence file was present in the inspected source folder. The user requested this adaptation. The original research material is not represented as third-party licensed training/example data for general redistribution. Any future decision to include it requires a separate rights and disclosure review.

## What carries forward

The study-to-paper sequence; the requirement to explain the design and harness; exact author-provided bylines; reproducible extraction; explicit denominators, units, cost assumptions and exclusions; fail-visible figure data; visual inspection of charts/crops/pages; matched panel typography; checked references; AI-use transparency; clean builds and fonts; deliberate packaging; and an honest human handoff.

## What changed

- One canonical reusable skill replaces the paper-specific playbook, with detailed workflow and policy references and neutral templates.
- Generic data extraction, chart and crop interfaces replace model names, original schemas, sample sizes, result values and fixed page coordinates.
- Denominator guidance explicitly prevents post-hoc cherry-picking and requires full-population context, subgroup disclosure and exploratory labels.
- The submission archive is a deliberate file allowlist; the full study kit is a separate deliverable.
- Style preferences are distinguished from official policy. MJ now prefers visible page numbers on the title and subsequent pages, with explicit author/venue exceptions; this supersedes the source playbook’s earlier omission preference and is not an arXiv requirement. A three-pass `pdflatex` build with a prepared `.bbl` is a conservative portability check; current arXiv also supports BibTeX/Biber input processing.
- Source integrity, review completion and external acceptance are separate claims. Local checks do not prove the science, author approval or arXiv acceptance.

## Capability and web reference

The local `~/dev/amplifier-skill-right-shape` repository supplied the capability structure and web-delivery reference: capability identity, a portable skill, Amplifier composition, installation and checks, a static site and associated downloadable assets. ArxivChecker adapts the delivery pattern for a different task. It does not copy Right Shape's rubric, fictional placements or claims.

Official policy sources and the check date are recorded in [`policy.md`](../skills/arxivchecker/references/policy.md). Local memory was consulted for context only; it is not evidence of current build, deployment, publication or acceptance.
