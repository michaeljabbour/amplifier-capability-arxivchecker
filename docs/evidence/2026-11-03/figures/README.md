# Figure and crop smoke evidence

All inputs and values in this folder are **fictional test fixtures**, not study
findings or performance evidence. Generated locally on 2026-11-03.

The existing `/opt/homebrew/bin/python3.14` environment supplied matplotlib and
Pillow; no software was installed. The default `python3` environment lacks these
optional rendering dependencies. With Python 3.14, all nine `test_figures.py`
tests passed, including PDF/PNG rendering and lossless crop verification.

The three explicitly selected series include zero, partial and full success
counts to exercise Wilson interval endpoints. `pdffonts fictional-metrics.pdf`
reported one font, `STIXGeneral-Regular`, as embedded CID TrueType; no Type 3
font appeared. The provenance sidecar records every selected series and input
and output hashes.

Visual inspection of `fictional-metrics.png` found all three series, legible
labels, visible confidence intervals and one stated unit without collisions.
Inspection of `crops/design-with-footnote.png` confirmed that both panels and
the full fictional footnote survived the preview-coordinate crop. The original
artboard was unchanged. The scripts intentionally leave their review fields as
pending: this dated record is separate human-readable evidence of this local
inspection, not automatic approval of any future figure.

Reproduce in a new output location (the helpers refuse to overwrite):

```sh
MPLCONFIGDIR=/tmp/arxivchecker-mpl PYTHONDONTWRITEBYTECODE=1 \
  /opt/homebrew/bin/python3.14 -m unittest discover -s tests -p test_figures.py -v

MPLCONFIGDIR=/tmp/arxivchecker-mpl /opt/homebrew/bin/python3.14 \
  skills/arxivchecker/scripts/make_figures.py \
  --input docs/evidence/2026-11-03/figures/fictional-metrics.json \
  --series 'Empty control' --series 'Illustrative approach' \
  --series 'Ceiling control' --output /tmp/new-fictional-metrics.pdf

/opt/homebrew/bin/python3.14 skills/arxivchecker/scripts/crop_artboards.py \
  --input docs/evidence/2026-11-03/figures/fictional-artboard.png \
  --boxes docs/evidence/2026-11-03/figures/fictional-boxes.json \
  --output /tmp/new-fictional-crops
```

These checks establish rendering and preservation behavior on this fixture.
They cannot establish that a real study chose an appropriate metric, denominator,
confidence interval, comparison, crop, or scientific conclusion.
