---
name: arxivchecker
description: Turn a completed study, results folder, design document, harness and draft into a checked LaTeX paper and a reviewable arXiv submission package. Use for study write-ups, paper cleanup, figure and claim audits, citation checks, arXiv preflight or packaging. Keeps measured evidence, narrative and human decisions distinct.
---

# ArxivChecker

Make the paper tell the full story of what was built, why it was tested and what the evidence supports. Start with the study's files, never the old draft's numbers. A local preflight is evidence about a build; it is not peer review or a guarantee of arXiv acceptance.

Apply [MJ's publishing style](references/writing.md) on top of the official requirements: teach the reader the study, remove unnecessary jargon, explain essential terms in context or a suitable footnote, and use visuals that help readers understand. This is substantive editorial guidance, not an arXiv rule.

## Start here

1. Read [workflow](references/workflow.md), [policy](references/policy.md), the dated [format/file requirement map](references/requirements.md) and [submission-policy map](references/submission.md). Recheck official sources before an actual submission. Distinguish stated requirements, conditional routes, recommendations and local checks; leave eligibility unassessed when a route is unsupported.
2. Inventory the study, preserve originals and identify the author-provided names, affiliations, decision rules, data and build instructions. Work in a separate output directory. Do not test against shared or production systems.
3. Agree the study question and reporting unit from the evidence. If essential data is missing, record the gap and continue independent work. Never invent results, authors, references, preregistration or consent.
4. Copy neutral files from `templates/` only as starting points. Replace every `REPLACE_ME` template marker and review editing notes in context. The originating paper's content, names, numbers, schema and artboard coordinates must never be transplanted into a different study.

## Evidence rules

- Extract counts, denominators, units, uncertainty and cost scope from source data with one reproducible script. Missing keys and expected series must fail visibly. Record source paths and hashes.
- Keep the primary population and denominator tied to the research question and rules fixed before the run. Explain exclusions and show the full population alongside any subgroup. A more flattering fraction is not a reason to change the denominator.
- Distinguish per-call, per-attempt, per-problem and per-participant measures. Report missingness, repeated measures and incomplete runs. Separate measured cost from estimates at assumed prices and list all exclusions.
- Check every figure against data, render it and inspect it. Check every reference against an authoritative record; record unresolved references as unresolved. A resolving URL does not verify a scientific claim.
- Preserve confirmatory decision rules as written; label later analyses exploratory. Describe negative findings, limitations and unmeasured quantities plainly.

## Local tools

Run the helper from this skill's folder, using absolute paths when the working directory differs:

```sh
python3 scripts/arxivcheck.py inventory /path/to/study
python3 scripts/arxivcheck.py extract /path/to/study --spec /path/to/spec.json --output /path/to/metrics.json
python3 scripts/arxivcheck.py check /path/to/study --manifest /path/to/manifest.json
python3 scripts/arxivcheck.py preflight /path/to/study --manifest /path/to/manifest.json --output /path/to/new-build
python3 scripts/arxivcheck.py package /path/to/study --manifest /path/to/manifest.json --output /path/to/arxiv-submission.tar.gz
```

Consult each command's `--help` and `references/tooling.md`. Inventory, extraction and checks use Python's standard library. Preflight needs the declared TeX toolchain and Poppler tools. Figure and crop templates require their explicitly documented optional dependencies. Do not install software or execute unfamiliar study scripts without inspecting them and the environment first.

## Paper and handoff

Use this order: problem → design and visuals → related work → question and prior decision rules → harness → methods → results → discussion and limitations → conclusion → availability → AI-use statement → references → appendices. Adapt to the field and venue when justified.

Prefer the supplied readable single-column template, exact author-provided names and affiliations, and no page numbers. These preferences do not replace arXiv’s official format guidance: single spacing, 10–14 point type, margins of at least one inch, machine readability, title/authorship and complete references. Check the prohibited-content guidance too. These facts and exceptions are sourced in the requirement map. Describe significant AI assistance accurately and leave authors responsible for review and final wording.

Deliver the manuscript/PDF, rebuild instructions, evidence ledger, figure and citation review notes, clean submission archive and explicit unresolved issues. Keep the full study kit separate from the minimal submission archive. State exactly which automatic checks and visual reviews ran. Leave category, licence, endorsement, authorship approval, release rights and final submission to the responsible person. Submit or publish only when explicitly asked.

For a colleague's short summary, use three or four plain sentences in the user's voice: what we ran, the answer, then the surprise. Include at most one or two decision-relevant numbers.
