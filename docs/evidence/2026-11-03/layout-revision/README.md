# Revised starter layout check — 2026-11-03

This is a fictional typesetting fixture generated from the actual neutral starter,
with one real 10 pt footnote and one vector workflow illustration. No study
results or real author details are used. The current starter uses 11 pt body type
and 1.05-inch geometry as house choices. The extra margin is a local buffer;
arXiv's cited format guidance says at least one inch, not 1.05 inches.

The local checker completed three pdflatex passes and font inspection. Both
rendered pages were visually inspected: the byline is centred, the workflow
figure and caption follow the Results introduction, and the footnote and its
marker are on page 1. No clipped text, colliding labels or mismatched panel type
was observed in this fixture. All extracted word bounds lie more than 74 points
from each page edge. The measured record covers words, not every PDF object;
visual review and actual submission-preview review remain separate.

An earlier fixture inserted the float immediately after the Results heading,
before its introductory sentence; its note moved to the next page despite a
successful build. Moving that fixture figure after the paragraph corrected the
observed layout. This is why a compile alone cannot establish good placement.
The source starter's instruction already says to discuss a visual first and
inspect its final float position.

Reproduce from the checkout with existing pdflatex and Poppler tools:

```sh
python3 scripts/smoke_template.py --output /tmp/new-arxivchecker-layout
```

The output directory must be new. TeX is trusted local source; this is not an OS
sandbox. These records do not certify arXiv policy compliance, accessibility,
science, rights or the final rendering on arXiv.

The repository's `pdfinfo.txt` normalizes trailing whitespace only. Its original
console output is preserved privately; the PDF and all measurement records are
unchanged.
