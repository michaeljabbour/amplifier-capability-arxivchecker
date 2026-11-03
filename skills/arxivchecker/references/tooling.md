# Tooling and template contract

All paths below are examples to replace. From the repository root, set the script path to `skills/arxivchecker/scripts/arxivcheck.py`; an installed skill keeps the same `scripts/` subdirectory. Use `--help` for exact options. The core helper needs Python 3.11+ and only the standard library. It reads local files and does not fetch references or send study data anywhere.

## Inventory

```sh
python3 skills/arxivchecker/scripts/arxivcheck.py inventory /path/to/study
```

This emits paths, byte sizes and SHA-256 hashes. Hidden files, common caches and credential filenames are excluded. Symlinks are not included as study data. Inventory is not classification of scientific evidence or a guarantee that the folder contains no sensitive data.

## Extract

Copy `templates/extraction-spec.json`, replace its prompts and run:

```sh
python3 skills/arxivchecker/scripts/arxivcheck.py extract /path/to/study --spec /path/to/spec.json --output /path/to/new-metrics.json
```

The extraction specification is a JSON object with `schema_version: 1` and a nonempty `metrics` array. Each metric has a unique alphanumeric/underscore/hyphen `id`, relative JSON `source`, RFC 6901 `pointer`, `kind` (`number` or `proportion`) and explicit `unit`. A proportion's pointer selects the integer numerator and its `denominator_pointer` selects an integer denominator. The helper requires `0 ≤ numerator ≤ denominator` and `denominator > 0`, and reports a rate and 95% Wilson interval. The user must still assess the binomial assumptions and study population. Number metrics can include a `cost_scope` string documenting assumptions, coverage and exclusions.

The helper rejects missing paths/keys, duplicate JSON keys, booleans used as numbers, non-finite values and invalid binomial counts. Binomial denominators are limited to 2**53 for exact floating-point integer conversion; this is a helper limit, not a study or arXiv rule. Each extracted metric records the source path/hash and pointer. There is no expression evaluator, inferred denominator or automatic statistical analysis beyond the stated interval. For complex data, write and review a study-specific extractor that produces a comparable evidence ledger. The output file must not already exist.

## Manifest and static check

Copy `templates/manifest.json`. Set `main_tex` and keep it in the explicit `files` allowlist; include every input, required custom style and figure. `engine` records the chosen route; the executable local preflight currently covers `pdflatex` only. Generic checking/packaging does not blacklist other engines or establish arXiv eligibility. `authors` is a nonempty list of author-provided name objects; `affiliation` is optional and must never be invented. This is a local provenance contract, not a universal full-name or affiliation rule. `human_review` lists remaining decisions; it is not approval and does not waive checks.

```sh
python3 skills/arxivchecker/scripts/arxivcheck.py check /path/to/study --manifest /path/to/manifest.json
```

The safe-path policy rejects traversal, absolute paths, symlinks, hidden/cache/credential paths and filenames outside the conservative portable character set. Files are an explicit list, not a directory glob. The local cap is 1,000 files / 100 MiB; it is not an arXiv quota claim. The static TeX scan finds explicit local template markers and some missing literal dependencies. Braceless/macro inputs, graphics search paths and ambiguous editing words are review findings; a clean build resolves what a regex cannot. The scan cannot fully interpret TeX macros, package imports, author identity, references or scientific claims. Check the recorder and examine a missing-file finding before changing a legitimate source. Review the report's limits.

The neutral main template deliberately contains explicit `REPLACE_ME` prompts and no research results. Ordinary TODO/FIXME prose is a review finding rather than proof of an unfinished or ineligible paper. It must fail readiness checks until completed. Both `.bib`-only and compatible prebuilt `.bbl`-only source routes are permitted by generic checking/packaging. This helper’s conservative no-bibliography-engine clean-build profile requires a generated `main.bbl` when bibliography commands are used. Generate that file using the verified bibliography before preflight. Current arXiv can also process `.bib` files; see [requirements](requirements.md). Unsupported local engines or bibliography builds return `not-run-unsupported-local-profile`, create no build directory and leave `arxiv_eligibility` as `not-assessed`. Test those routes separately; never infer rejection.

## Preflight and package

```sh
python3 skills/arxivchecker/scripts/arxivcheck.py preflight /path/to/study --manifest /path/to/manifest.json --output /path/to/new-clean-build --reference-pdf /path/to/reviewed.pdf
python3 skills/arxivchecker/scripts/arxivcheck.py package /path/to/study --manifest /path/to/manifest.json --output /path/to/new-submission.tar.gz
```

Preflight requires a **new output directory outside the study**, `pdflatex`, `pdfinfo`, `pdffonts` and `pdftotext`. It copies exactly the manifest files and performs three TeX passes without shell escape or bibliography regeneration. Compile trusted source only: disabling shell escape is not a complete TeX security sandbox. Inspect the supplied source and environment first. If a prerequisite is absent, report the missing tool and continue independent static/review work; do not claim the clean build passed. This compiler does not reproduce the arXiv toolchain or perform the human-only format, policy and rights review in the cited maps.

The optional reference PDF enables page-count and exact `pdftotext -layout` comparisons; without it the report must not claim a comparison. Extracted-text and page-count agreement do not establish pixel identity or correct layout. Font checks and log scans are mechanical gates; every page/figure still needs visual inspection. A new archive contains exactly the allowlisted source, and packaging does not run preflight. Its `packaged-unreviewed` result is an archive-creation statement only. The helper does not upload or submit anything.

## Figures and artboard crops

These helpers require optional dependencies: Matplotlib for figures and Pillow for crops. They are not installed by the capability. Use an existing trusted environment; inspect dependency availability before running them.

```sh
python3 skills/arxivchecker/scripts/make_figures.py --input /path/to/metrics.json --series METRIC_ID --output /path/to/new-figure.pdf
python3 skills/arxivchecker/scripts/crop_artboards.py --input /path/to/artboard.png --boxes /path/to/boxes.json --output /path/to/new-crops
```

Repeat `--series` for every expected metric. Selection is explicit; missing series fail. A chart emits vector PDF, PNG preview and a `.figure.json` record. Plot numeric series with compatible units together; plot proportions using their recorded intervals. The chart helper validates source-hash shape, count/rate consistency and Wilson intervals, but does not re-read original study data to independently certify the extracted file.

For crops, supply `{ "schema_version": 1, "preview_width": 750, "crops": [{ "name": "panel", "box": [0, 0, 100, 100] }] }` with coordinates measured on **your own** preview. Those numbers are a syntax example, not a recommended crop. The optional `preview_width` determines scaling; without it boxes use source pixels. Source input is a raster image. Extract raster images from a PDF separately when appropriate. Output must be new; invalid/out-of-bounds boxes fail rather than silently clamp. Crop records preserve source fingerprints. Inspect every preview/full-resolution output and mark review separately; helper output does not claim visual approval.
