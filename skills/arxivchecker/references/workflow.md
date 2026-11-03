# Study to submission: the ten-step procedure

Use this procedure for a completed study or to identify why a draft is not yet ready. Keep a dated evidence ledger and a list of unresolved issues throughout. The neutral templates contain prompts, not scientific findings.

## 1. Inventory the evidence

Read the study README, design document, harness README/source, methods log, draft, dataset documentation and result files before writing. Identify the question, what was actually built, what was run and what the design merely proposes. Record file paths, revisions or hashes and who supplied author names, affiliations and release decisions. Check whether there are corrected, partial, failed or superseded runs. Preserve the original kit.

Before calling the work submission-ready, identify its content type and intended category. Use the [submission map](submission.md#content-type-and-account-checks) for special CS review/position-paper conditions and submitter quotas. Original-study, review and position-paper routes must not be silently substituted for one another. Account conditions require the submitter's actual status; the local helper cannot infer it.

Run `arxivcheck.py inventory` to obtain a local file/hash inventory. It does not infer which results are valid. Inspect executable scripts before running them. Work on copies in a private output directory and never insert test records into shared or production stores.

## 2. Derive the numbers once

Write one study-specific extraction script, or use the declarative extraction helper for simple JSON metrics. Read original result files; do not copy numeric claims from draft prose. Produce a machine-readable metrics file and human-readable ledger covering counts, rates, denominators, units, missing values, uncertainty, tests, cost and latency. Record source hashes so later changes are visible. Require every expected series/key and reject non-finite values instead of silently skipping them.

Use integer counts when available; do not reconstruct them by rounding a percentage. Check `0 ≤ successes ≤ denominator`, nonzero denominators and whether the observations are independent. Report what each denominator includes and excludes and why. Do not choose a subgroup after seeing its result without labelling that analysis exploratory; report the full population too. Keep per-call, per-attempt and per-problem quantities separate. Repeated samples are not independent problems.

For each cost figure, record currency, price source/date, measured usage versus estimated prices, pricing assumptions, and coverage. List excluded preparation, synthetic data, failed/unpriced calls, agent usage, hardware, labour and overhead where relevant. Never call a partial model-call estimate total study cost. State whether latency is wall-clock, provider latency, sum of attempts or elapsed human time. Preserve preregistered tests; disclose exploratory tests, multiplicity and uncertainty.

## 3. Build and inspect data figures

Build charts from extracted metrics, preferably as vector PDF, with stable category colours and publication-sized text. The figure template uses an explicit generic schema; change the schema or study adapter deliberately rather than hiding missing series. Matplotlib's `pdf.fonttype = 42`, STIX serif type and Okabe–Ito colours are useful defaults, not mandatory policy. Do not infer confidence intervals from averages. Wilson intervals suit binomial proportions only when the statistical assumptions fit; consult a qualified reviewer for dependent observations or complex designs.

Export a PNG preview of every chart and inspect it at intended printed size. Look for clipped labels, overlap, obscured data, misleading axes, lost series, accidental defaults and inconsistent units. Use leader lines or a label column for clusters. Suppress confusing minor-tick labels on log axes. Preserve a shared natural scale across paired panels so equal font settings do not render at different sizes. Captions state unit, population, sample size, uncertainty and source.

## 4. Include the design visuals

Identify which proposal/design panels explain the system under test. Put explanatory figures in the main text and additional relevant figures in an appendix. Do not insert entire slides or posters as article pages; the official format guidance directs those to ancillary files, subject to the submission route’s ancillary rules. See [requirements](requirements.md). Preserve source attribution and confirm rights to include them. Vector source is preferable. If a design PDF contains raster artboards, inspect it with `pdfimages -list`, extract images losslessly where possible and crop from an explicit preview-coordinate manifest. Preserve footnotes, legends and context. Reject out-of-bounds boxes; do not silently clamp them. Inspect every full-resolution crop, including the edges. Document any resize or compression.

## 5. Verify every reference

For each cited work, check title, complete author list/order, year, version, venue and identifier against an authoritative publisher, DOI record or arXiv abstract page. Record the checked URL/date, any correction and unresolved discrepancy in a reference ledger. If an arXiv API request fails, use the abstract page and its citation metadata; a failed request is not evidence that a citation is false. Check software URLs against the actual repository/release and record versions used. Add references for statistical methods and datasets actually used; do not add citations solely because they appeared in the originating paper. Reading metadata does not establish that a paper supports the scientific claim: inspect the cited passage/method too.

## 6. Write the paper as an argument

Explain the problem and stakes, then the design/system with visuals, related work, question and decision rules fixed before the run, harness/apparatus, methods, results, discussion, limitations and conclusion. Finish with availability, significant AI use, references and appendices. Keep proposed capabilities, implemented features and measured results distinct. Explain how the harness generated and verified the evidence. Include negative and inconclusive findings. Use exact author-provided names and affiliations in a balanced byline. Never infer institutional approval from an affiliation.

Apply the [house writing guide](writing.md): teach the argument, remove unnecessary jargon or explain needed terms, and use visuals when they improve understanding. These are the owner's editorial preferences, not submission-policy gates. Follow arXiv's [recommended semantic markup](requirements.md#latex-source-and-typesetting-recommendations): use structural headings and frontmatter, meaningful emphasis and helpful image alternatives with a compatible package version. Check converted structure as well as visual appearance; a heading painted with font commands is not the same as a semantic section.

Use `templates/main.tex` as a neutral structural starter. Keep the no-page-numbers preference unless the user or venue asks otherwise; no page-number prohibition was found in the checked format policy. Letter paper, exact 11 pt and 1.05-inch geometry, newtx, numeric natbib, microtype and booktabs are local styling choices within the official single-spacing, 10–14 point and minimum one-inch margin guidance; see [requirements](requirements.md). The small geometry buffer leaves room for ink protrusion and footnotes; inspect rendered margins rather than trusting a declaration. Adapt these defaults for the study's field or publisher requirements. Significant AI use belongs in a specific statement (code, experiments, analysis, synthetic labels/data, figures, drafting or editing as applicable); do not assert author review has happened before it has. Tools are not authors.

## 7. Compile and inspect all pages

Build using the declared engine and bibliography workflow. Inspect the complete log for errors, undefined references/citations, overfull boxes, rerun requests and PDF-bookmark/hyperref warnings. Wrap mathematical section titles with a plain-text bookmark alternative such as `\texorpdfstring{...}{...}`. Put figure/table source immediately after its first discussion and verify where the float landed. Check title-page affiliation alignment and consistent panel typography after every material edit. Verify scripted edits by reading the resulting file.

Render all pages into contact sheets, then inspect the title page, every figure/table page and suspicious pages at readable resolution. A successful compile does not demonstrate legibility, correct science or correct float placement. Record what was visually reviewed and any defects remaining.

## 8. Run a clean preflight

Create an explicit allowlist of the minimal files required to build the paper: main TeX, included source/style files, referenced figures and the chosen bibliography inputs. Avoid unrelated caches, drafts, logs, credentials, unused assets and the output main PDF in the source archive. Retain required pre-generated build inputs, including a compatible frozen minted cache if that route requires it. Keep optional ancillary research files deliberately selected, documented and cleared for release.

Run the helper's checks and a build in a new empty directory from exactly the allowlisted files. The conservative default is three `pdflatex` passes with a pre-generated `.bbl`; it tests source portability without bibliography regeneration. Current arXiv also supports `.bib` processing, so this is not a claim that BibTeX/Biber is forbidden. Use a supported engine and bibliography workflow when another one is required, record it and test it explicitly.

Inspect the fresh log. Use `pdfinfo`, `pdffonts` and `pdftotext` to check page count, embedded outline fonts and extracted text; reject Type 3 fonts for this capability's PDF quality gate. If a reference PDF is supplied, the helper compares page counts and exact `pdftotext -layout` output; investigate differences. Agreement cannot establish visual identity; review rendered pages too. Use portable relative filenames and the helper's deliberately conservative safe-name rule; local caps are not arXiv limits. Distinguish explanatory design figures from entire slides/posters, which the official format guidance directs to ancillary files rather than the article body. A local build does not reproduce arXiv's environment exactly: the submitter must still inspect arXiv's generated PDF.

## 9. Package for two purposes

For the TeX-source route, deliver a clearly named review PDF and a minimal `arxiv-submission.tar.gz` with explicit source contents. Other accepted routes and archive formats are described in [requirements](requirements.md); the helper does not implement every route. Include an unpacked source folder, evidence/claim ledger, source hashes, reference ledger, figure/crop review notes and build commands in a review package. Keep the larger study kit, design originals, datasets/datasheets and scripts separate from the minimal submission source. If a ZIP of the review package is requested, exclude unrelated caches and obsolete renders and list its contents. Retain required build inputs such as the documented frozen minted cache when that route needs it; do not apply a blanket cache ban. Never bundle sensitive or unlicensed data just because it was present in the study directory.

Write a README describing the study's contents, what changed from the draft, prerequisites, exact rebuild commands, known limitations and remaining submission decisions. Archive success means files were packaged; it does not mean a clean build or review passed. Link each claimed verification to its log/result.

## 10. Hand off the human decisions

Report the state accurately: draft prepared, checks passed/failed, visual review completed/not completed, and unresolved evidence. Ask the responsible authors to review labels, scientific interpretation, authorship and affiliations, significant AI-use wording, release rights, public code/data URLs, category, licence, endorsement and the final arXiv-rendered PDF. Do not invent their approvals. Publish or submit only if explicitly asked. For a brief colleague update, tell the story in the user's voice: what we ran, the answer and the surprise, with one or two important numbers.

Include any unresolved content-type evidence or account-capacity decision in that handoff. Do not claim an available monthly or active-submission slot without the responsible submitter checking their account.
