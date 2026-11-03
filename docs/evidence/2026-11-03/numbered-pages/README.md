# Numbered starter validation — 2026-11-03

The actual current starter was filled with fictional author/method text and a
vector illustration using `scripts/smoke_template.py`. Three clean pdflatex
passes and font inspection succeeded. Both rendered pages were inspected:
page numbers 1 and 2 are visible, including the first/title page, and the
footnote marker and text remain on page 1. No new collision or clipped text
was observed in these two pages.

The smoke procedure now checks the actual centred footer digit against each
PDF page index. Both digits have bounding boxes y=709.025–718.767 on a 792-point
page, leaving 73.233 points at the bottom. All measured word bounds remain
inside a 72-point/one-inch text envelope. The geometry includes the footer and
uses a 24-point footskip. These are local template measurements, not a claim
that arXiv requires this page style or layout mechanism.

Visible first and subsequent numbers are MJ's house default. Explicit author
instructions or applicable venue requirements may change the treatment. The
local generic checker does not turn a different legitimate page style into an
arXiv eligibility failure.

All 50 regression tests passed with the existing Python 3.14 environment,
including the optional figure/crop checks. No software was installed. The site
build/check and JavaScript syntax checks were also run. No browser interaction
was performed because the owner had asked us to stop clicking the video.
The site checks inspect the generated markup, hidden fallback versus visible
anchors, retained caption track, canonical guidance and complete skill ZIP.

Reproduce the template check with existing TeX/Poppler tools and a new output:

```sh
python3 scripts/smoke_template.py --output /tmp/new-numbered-template-review
```

Source/PDF evidence is fictional. Word bounds do not inspect every graphic or
prove accessibility, scientific validity, licensing or arXiv acceptance. Every
actual manuscript and the final arXiv rendering still need review. The previous
layout-revision evidence is retained as a historical, superseded snapshot.
