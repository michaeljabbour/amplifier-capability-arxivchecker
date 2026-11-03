# ArxivChecker

Turn a finished study into a paper you can trace, rebuild and review.

ArxivChecker helps an assistant carry a study from source data and design notes to a LaTeX paper, checked figures and a reviewable submission package. It makes the problem, what was built, the harness, the tests and the answer visible in order. Every headline needs its source, denominator, unit and limits.

This is an Amplifier capability delivered as a portable skill, deterministic local helpers, a working mode, a staged recipe and a static explanatory website. It prepares work for human review. It does not submit to arXiv or certify scientific validity, reference accuracy, licensing or acceptance.

## Start locally

Python 3.11 or later is enough to install the skill and run the core checks. From this checkout:

```sh
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

Use `~/.claude/skills` for Claude Code or your assistant's supported skills parent. The installed skill is named `arxivchecker`; the original `arxiv-paper-from-study` skill stays in place. Start a new assistant session and ask:

> Use ArxivChecker on this study folder. Inventory the design, harness, raw results and draft first. Recompute each claim from the data, prepare the paper and show me the evidence and remaining human decisions.

For Amplifier, add the local behavior to your existing host as described in [INSTALL](docs/INSTALL.md). The `/arxiv` mode supports ongoing work; `recipes/arxivchecker-paper.yaml` sequences evidence review, preparation and handoff.

## What comes with it

| Part | What it does |
| --- | --- |
| [Canonical skill](skills/arxivchecker/SKILL.md) | A ten-step study-to-paper process with writing and reporting safeguards |
| [Core checker](skills/arxivchecker/scripts/arxivcheck.py) | File inventory and hashes, strict JSON-pointer extraction, binomial Wilson intervals, explicit source allowlists, clean local pdflatex builds and deterministic source packages |
| [Figure builder](skills/arxivchecker/scripts/make_figures.py) | Vector PDF plus PNG preview from explicitly named series; fails if data is missing |
| [Artboard cropper](skills/arxivchecker/scripts/crop_artboards.py) | Explicit, bounded crops with provenance and a visual-review record |
| [Templates](skills/arxivchecker/templates/) | Neutral LaTeX, extraction and package specifications; no inherited study results |
| [Amplifier bundle](bundle.md) | Skill discovery, mode and a staged recipe with review checkpoints |
| [Website](site/README.md) | Guide, fictional claim demonstration, self-review checklist, downloads and narrated films with captions and transcripts |

The current main reel is the [v2 MP4](https://github.com/michaeljabbour/amplifier-capability-arxivchecker/blob/main/site/assets/arxivchecker-film-v2.mp4), with a matching WebM, captions and short cut. See [video verification and limits](docs/VIDEO-UPDATE.md).

The core helper's interfaces are deliberately small:

```sh
python3 skills/arxivchecker/scripts/arxivcheck.py inventory /path/to/study
python3 skills/arxivchecker/scripts/arxivcheck.py extract /path/to/study --spec extraction.json --output metrics.json
python3 skills/arxivchecker/scripts/arxivcheck.py check /path/to/study --manifest manifest.json
python3 skills/arxivchecker/scripts/arxivcheck.py preflight /path/to/study --manifest manifest.json --output /tmp/new-arxiv-build
python3 skills/arxivchecker/scripts/arxivcheck.py package /path/to/study --manifest manifest.json --output submission.tar.gz
```

Outputs must be new files or directories. The preflight directory must be outside the study. It uses three pdflatex passes with shell escape disabled; supply a generated `.bbl` when bibliography processing is needed. This is a conservative local portability check, not a statement that arXiv requires this engine or forbids bibliography tools. Other engines and bibliography workflows are not rejected by generic checking/packaging; unsupported local preflight routes are reported as not run, with arXiv eligibility unassessed. Compile only trusted TeX: these flags are not an operating-system sandbox.

The figure and crop helpers need matplotlib and Pillow respectively. LaTeX preflight needs `pdflatex`, `pdffonts`, `pdfinfo` and `pdftotext`. The skill remains useful when a dependency is unavailable; report the unchecked step instead of inventing a pass. Installation never downloads these tools.

## Grounded in official arXiv documentation

The dated [format and file requirements](docs/ARXIV-REQUIREMENTS.md) and [submission-policy map](docs/ARXIV-SUBMISSION.md) distinguish stated requirements, conditional routes, recommendations and local preferences. They link directly to current official arXiv documentation, verified on 2026-11-03. Recheck before submitting: toolchains and policies change, and a local check never establishes acceptance.

The [verification record](docs/ATTACHMENT-VERIFICATION.md) checks the supplied secondary guidance against official sources without redistributing the private attachment.

## The reporting standard

MJ’s house default is visible page numbers, including the title page. Follow explicit author instructions or applicable venue requirements when they differ. This preference is separate from arXiv’s rules.

Tell the full story: problem, design, related work, question and decision rules, apparatus, methods, results and limits. A results-only summary misses what was built and why. Keep predeclared analyses distinct from exploratory ones.

Use [MJ's writing guide](skills/arxivchecker/references/writing.md) for pedagogical prose, explained jargon and visuals that help the reader understand. It is house style, separate from arXiv policy.

Check the denominator without hiding the full population or changing the question after the run. State the unit next to the measure. A model-call estimate is not the total study cost; disclose pricing assumptions, excluded calls, synthetic data, human work and agent usage. Record AI assistance accurately and let the authors approve the wording.

A numeric extraction does not establish that a cohort was chosen fairly. A passing build does not mean labels are readable. A packaged archive does not imply permission to publish. The handoff lists the reference checks, visual inspections and author decisions still needed.

## Build and verify

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m unittest discover -s tests -v
node --check site/site.js
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open `http://127.0.0.1:8000`. The site uses local assets and system fonts, with no analytics, backend or runtime network requests. Generated `_site/` contains the portable downloads. The Pages workflow is available for an owner to run later; nothing is published by this local build.

See [VALIDATION](docs/VALIDATION.md) for actual results and their limits, [BENCHMARK](docs/BENCHMARK.md) for the broader evaluation plan, and [PROVENANCE](docs/PROVENANCE.md) for the source skill and policy corrections. All demonstration studies and numbers shipped in this capability are fictional.

## Provenance and status

Adapted from the locally installed `arxiv-paper-from-study` skill and its paper-production lessons. The capability and web structure follow Right Shape. The original paper and its executable study-specific scripts are retained at their source, not redistributed as generic results. Source hashes and reuse decisions are recorded in the provenance document.

Source and skill are published in [the GitHub repository](https://github.com/michaeljabbour/amplifier-capability-arxivchecker) after a [privacy review](docs/PUBLIC-REVIEW.md). The website remains a local build; no separate hosted deployment or arXiv submission occurs automatically.

MIT for the new capability code and documentation; the copied family theme retains its own notice. `ArxivChecker` is an independent project name and does not imply affiliation with or approval by arXiv.
