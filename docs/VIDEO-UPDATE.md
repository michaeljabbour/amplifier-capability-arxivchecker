# Supplied v2 reel integration — 2026-11-03

**House-style correction:** MJ now prefers visible page numbers, including the title page, with author/venue exceptions. The unchanged video’s contrary 46–49 second example is historical and awaits correction; see the [Claude prompt and exact edit targets](VIDEO-PAGE-NUMBERS.md).

The main player now uses the owner's supplied 71.14-second MP4, with the matching
WebM, timed English speech captions, descriptive transcript and poster. The
14.5-second cut and its captions/transcript remain available. All v1 assets are
preserved. The supplied MP4 SHA-256 is
`b449db7981ec99e201cd951823f11dcf15105b1a51aa9d8c0c71442e53af22c7`.

## What was checked

The supplied file and prepared local MP4 have identical encoded streams and
decoded audio/video despite different container bytes. The exact supplied file
is the main public MP4. All three delivery formats decode without errors and
have stereo 48 kHz audio; full/short dimensions are 1920×1080 at 30 fps. The full
MP4 has 2,134 video frames; its container lasts 71.14 s. No conversion of its
picture or audio was needed.

Independent offline recognition matches all 132 full-caption words and 29
short-caption words, ignoring case/punctuation and declared brand
pronunciations. WebVTT/SRT cue content, sequence, bounds and non-overlap were
checked against the source timeline and actual speech. Full/short tracks have
17/4 cues. Approximate timing supports their placement; exact perceptual
synchronization and subjective listening remain separate. No human-listening
approval is invented.

| Asset | Integrated loudness | True peak |
| --- | ---: | ---: |
| Supplied full MP4 | −16.06 LUFS | −3.85 dBTP |
| Full WebM | −16.02 LUFS | −3.94 dBTP |
| 14.5 s MP4 | −14.04 LUFS | −2.05 dBTP |

Sixteen keyframes were visually inspected. The illustrative cost sentence,
results file and chart are fictional. The transcript's on-screen AI-use label
was corrected to the actual final image, “How you disclose AI use.” Narration
was not changed. Media metadata contains only generic encoder/container tags.
See [independent evidence](evidence/2026-11-03/video-update/README.md) and the
[asset hash manifest](evidence/2026-11-03/video-update/media-manifest.json).

## Guidance boundaries

The film's one-inch-margin wording follows arXiv's format guidance, which uses
“should”; figure descriptions/alt text follow its recommendations. The film’s omission of
page numbers reflects the former house preference, superseded by visible page
numbers; neither choice is an arXiv mandate. Reporting significant AI assistance is required
consistent with the subject's methodology standards; the on-screen wording does
not remove that condition or the authors' responsibility. Official pages were
rechecked on 2026-11-03: [format policy](https://info.arxiv.org/help/policies/format_requirements.html),
[LaTeX best practices](https://info.arxiv.org/help/submit_latex_best_practices.html)
and [moderation/AI policy](https://info.arxiv.org/help/moderation/index.html).

The depicted source files are an illustration, not an executable manifest for
every paper. Include every dependency for the chosen processor and bibliography
route. The local helper's conservative three-pass pdflatex profile requires a
prepared matching `.bbl` when bibliography commands are used; arXiv also accepts
`.bib` processing and other supported routes. See the [canonical requirements](ARXIV-REQUIREMENTS.md),
[official bibliography instructions](https://info.arxiv.org/help/submit_tex.html)
and [processor guide](https://info.arxiv.org/help/faq/texlive.html). A clean local
build is not arXiv's final rendering or an acceptance decision.

## Preservation and release scope

The owner's prepared files and original production notes were preserved
privately before integration. The public notes omit internal flow identifiers,
workspace paths and unrelated project references. Archival scripts are labelled
as requiring omitted production inputs; their rebuild was not claimed. Supplied
production metrics and approvals retain their historical scope, separate from
the independent review above. No raw voice takes, stems, fonts, credentials or
private paper files are added. The owner authorized publication of the supplied
video to the existing public repository. This record does not independently
establish provider licence entitlement or human listening approval.

GitHub publication and a separately hosted website are different operations.
The Pages workflow remains manual-only; this update does not enable or dispatch
it. Local software/browser checks and the eventual repository CI result are
reported with the actual published commit.

## Local software and browser validation

All 50 regression tests passed with the existing Python 3.14 environment,
including optional figure/crop rendering. [Test log](evidence/2026-11-03/video-update/tests-python314.txt).
The site build/integrity checks and JavaScript syntax check passed; all six
v1/v2 delivery audio streams were inspected. The portable skill ZIP is unchanged.
The v2 production Python sources parse, but their archived generation/render
pipeline was not executed without its omitted inputs.

Edge played the integrated 1920×1080 reel with English captions enabled, sound
unmuted and no video error; playback advanced beyond 28 seconds. The owner
subsequently confirmed that the video works and requested no further browser
interaction. That request was followed. [Browser observations](evidence/2026-11-03/video-update/browser-review.json).
No subjective audio-quality or exact caption-sync approval is inferred.
