# Fictional examples

Every case here is invented to illustrate the workflow. None is a measured
ArxivChecker result, a published paper, a real deployment, or evidence of time
saved. Use the current study's files and author metadata in a real run.

## A promising headline with the wrong denominator

A fictional routing study ran 20 tasks. Twelve of 14 tasks in a prespecified
subset met its criterion; the other six belonged to a different question. A
rough draft says only “12 of 20.” ArxivChecker should reconstruct both
denominators from task-level evidence and explain the subset rule. It should
report 12/14 for the prespecified question alongside 12/20 overall, disclose all
exclusions and retain failures. It must not choose the flattering denominator
after seeing outcomes.

The useful output is a claim ledger with the source file, extraction command,
unit, numerator, denominator, exclusion rule and scope. A caption can then say
what was actually counted. If the subset rule has no earlier record, label the
analysis exploratory instead of inventing preregistration.

## A renamed series makes a chart look stronger

A fictional results JSON renames one condition, but the plotting code silently
skips missing keys. The figure now shows three of four conditions. The correct
response is to fail the expected-series assertion, verify the schema change and
rebuild the figure. After plotting, compare plotted IDs with the full data
inventory, render the PDF, inspect labels and legends, and record the fix.

The correct first output is a failure, not a chart. A later passing check should
retain that failure history. A readable image alone cannot prove data coverage.

## A clean PDF with a package that cannot rebuild

A fictional draft PDF looks finished, but its source refers to an image outside
the package and has no generated bibliography. The handoff remains blocked
until the dependencies are explicit, the bibliography is included as needed,
and the submission source builds in an empty directory without shell escape or
network retrieval. Missing TeX tools are a skipped check with a concrete next
action, not a successful arXiv preflight.

Even a clean local build leaves author approval, rights, AI-use wording,
category, license and endorsement to people. It does not establish arXiv
acceptance.

## A short note to a colleague

An illustrative summary might read:

> We ran the routing comparison across the full task set and checked the
> prespecified subset separately. The pattern held in that subset, although the
> small sample still limits the claim. The surprise was that one missing chart
> series changed how strong the result looked, so we rebuilt the figure from the
> complete data before packaging the paper.

The words must change with the real evidence. Do not reuse fictional counts,
names, systems, outcomes, or this conclusion in a paper.
