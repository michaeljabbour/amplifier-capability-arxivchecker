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

## Family, narration and publishing-style revision

The subsequent local revision passed all 50 regression tests again with the
existing Python 3.14 environment, including optional figure/crop rendering. See
[the revision test log](evidence/2026-11-03/tests-revision-python314.txt). The final
static check passed two HTML pages, 71 local links/assets/fragments, 90 Markdown
destinations and 19 byte-exact portable files; all three film audio streams were
inspected. ZIP SHA-256: `cba088815c8d0493c7ee4f910b94c09fabbbd03f1b207058b32926baa2a68869`.
JavaScript syntax passed. No new software was installed.

The revision keeps official rules, arXiv/LaTeX recommendations
and MJ's pedagogical style in three labelled layers. The canonical [writing
guide](../skills/arxivchecker/references/writing.md) is included in the installed
skill, ZIP and rendered playbook. [The supplied-guidance audit](ATTACHMENT-VERIFICATION.md)
records corrections checked against primary sources, without redistributing the
private attachment.

The family comparison uses actual Right Shape, Taste, Decisioncraft, Unfold and
Project Handoff sources, with live Right Shape/Taste browser inspection and
computed-colour evidence. The revised page matches the cream/charcoal/gold/sage
baseline and common masthead/product-title layout. See [site provenance](../site/README.md).
Desktop 1280×720 and mobile 390×844 views were inspected; both landing and guide
have no horizontal document overflow. Wide policy tables scroll within their
containers. The viewport override was reset. [Browser revision record](evidence/2026-11-03/browser-revision.json).

Full MP4/WebM and 15-second MP4 now contain locally generated synthetic narration,
matching English captions and separate transcripts. All three decode fully, have
zero clipped samples and measured loudness near −18 LUFS. Source clips fit their
scenes without time compression or truncation. The full film played to its
48-second end in the in-app browser without an error. Mac Edge also showed
unmuted playback and visible captions. Independent offline speech recognition
matched all 27 short-cut words; the full cut had seven diagnostic word edits,
including unresolved final-scene wording. These checks are **not a subjective
listening review**: the agent cannot hear tool audio in this environment. Human
pronunciation/pacing review remains pending, and the independent report preserves
the uncertainty. See [audio evidence](evidence/2026-11-03/audio-revision/README.md)
and [independent review](evidence/2026-11-03/audio-revision/independent-review.md).

The actual starter was rebuilt with a footnote and vector illustration, and both
pages were visually inspected. Rendered word bounds are inside a one-inch text
envelope. The 1.05-inch geometry buffer, 10 pt footnote and 10 pt chart defaults
are house readability choices. A fixture float-placement issue was corrected
before the final render; see [layout evidence](evidence/2026-11-03/layout-revision/README.md).
This is partial layout evidence for a fictional fixture, not arXiv certification.

No push, public repository creation, hosted deployment or arXiv submission was
performed. Reopening the final page visibly on the Mac requires the Mac to be
unlocked; the connection's native UI reported it locked during final review.

## Supplied v2 reel update

The subsequent [video integration record](VIDEO-UPDATE.md) describes the exact
owner-supplied MP4, independent full/short caption recognition, format/audio
checks, sampled visual review and preservation of all v1 asset bytes. All 50
local regressions passed again; the site and JavaScript checks passed. Browser
playback worked and was confirmed by the owner, who then requested no more
interaction. The source and skill have since been published to GitHub; historical
local/unpublished statements above describe the earlier snapshots. At the time of that review, the separate
website had not been deployed. See the video record for exact limitations.

## Visible-page-number default and landing-page cleanup

MJ's current house default is visible first and subsequent page numbers, with
author/venue exceptions. The canonical skill, policy/writing guides, examples
and starter now agree. The actual two-page starter was rebuilt, and both
renders were inspected: footers 1 and 2 are visible and their ink remains
73.233 PDF points from the bottom edge. See the [new numbered-template
evidence](evidence/2026-11-03/numbered-pages/README.md). All 50 local regressions
passed again, plus the generated-site and JavaScript checks. The six auxiliary
film links are absent from visible page markup; captions and all asset files
remain. No further browser interaction was performed at the owner's request.

The video was not edited. Its obsolete page-number line and animation are
identified in [the Claude correction prompt](VIDEO-PAGE-NUMBERS.md). Historical
film/transcript/source and unnumbered-layout records remain evidence of their
original versions, not current instructions. The new ZIP contains the current
canonical numbered starter and guidance.
