# Corrected launch film v3 — 2026-11-03

The main player uses the exact owner-supplied **73.14-second v3 MP4**, with a
derived WebM, refreshed poster, updated English speech captions and descriptive
transcript. All earlier film and cut assets are preserved byte for byte. The
six removed landing-page links remain absent; native captions and the transcript
inside the unavailable-video fallback remain available.

The replacement MP4 SHA-256 is
`11a775d3eecb0c5b6f71ba16b84ca196547c20819f6ef639938934e482a59fb4`.
It contains 2,194 video frames at 1920×1080, 30 fps, with stereo 48 kHz AAC audio.
The supplied picture and audio were not edited or re-encoded in the main MP4.
The WebM is a VP9/Opus derivative; neither it nor the poster is represented as an
original supplied production asset. V3 source takes and the production project
were not supplied, so a production rebuild is not claimed. The historical v2
source archive describes that version only.

## Verified correction

The narration now says: “And your house style keeps page numbers, unless a
venue says otherwise.” The matching caption spans **46.100–50.730 seconds**.
At 47.0 and 47.5 seconds, decoded frames show **HOUSE STYLE / Visible page
numbers** and footer **1**. By 48.0 seconds, “Unless a venue says otherwise”
is visible. The number remains through the scene fade at 50.800 and 50.833
seconds; the scene is absent at 50.866667 seconds. It is no longer replaced
by an empty dashed footer.

Visible page numbers, including the title page, remain MJ’s publishing default,
with explicit author instructions or applicable venue requirements allowed to
differ. This is house style, not an arXiv page-number mandate. See the
[canonical writing guidance](../skills/arxivchecker/references/writing.md) and
[official arXiv format policy](https://info.arxiv.org/help/policies/format_requirements.html).
The film’s margin wording retains its prior scope: the policy uses “should.”
Figure descriptions follow arXiv’s
[LaTeX recommendations](https://info.arxiv.org/help/submit_latex_best_practices.html).
This media correction makes no new submission or acceptance claim.

## Audio, captions and timing

Existing local ffmpeg/ffprobe and offline whisper.cpp with its cached base model
were used; no provider request, model download, installation or recording was
needed. Recognition matches **135/135 normalized speech-caption words** after
case, punctuation and documented brand-pronunciation normalization. There are
17 non-overlapping WebVTT cues, at most two lines per cue and at most 42
characters per line. The final cue ends at 62.350 seconds.

Waveform comparisons confirm unchanged early narration at zero shift and
later narration shifted **+2.000 seconds**. Only cue 13 was replaced/extended;
cues 14–17 moved by two seconds. Earlier captions remain unchanged. Visual
chapter boundaries in the descriptive transcript were adjusted consistently.
The retained v2 short cut excludes the changed scene and remains a historical
asset; no newly produced short cut is claimed.

The MP4 decodes without errors and measures −16.06 LUFS integrated loudness,
−3.62 dBTP true peak. Detailed checks for both delivery formats and caption
correspondence are in the [media review](evidence/2026-11-03/video-v3/media-review.json).
These software and sampled-frame checks do not establish subjective listening
quality or exact perceptual caption synchronization. Browser/playback interaction
was deliberately omitted at the owner’s request.

## Privacy, preservation and validation

Review covered generic container metadata, 19 story frames from 0 to 72 seconds,
17 frames from 44 to 52 seconds at half-second intervals, additional full-size
page-number frames, all recognized speech and the new public text/manifest.
No PII, secrets, private study content, confidential markings or unrelated
material was identified within that scope. It is a sampled visual review, not
an inspection of every frame or a guarantee about all content. No Library
identifiers, signed download URLs, private filesystem paths, raw voice takes,
fonts or unrelated incoming files are included in this revision.

The [asset manifest](evidence/2026-11-03/video-v3/media-manifest.json) records
all five v3 delivery files and preservation hashes for earlier assets. The
[validation record](evidence/2026-11-03/video-v3/validation.json) records actual
local checks. The portable skill files and ZIP are unchanged by this video
revision. The existing manual-only Pages workflow was neither changed nor run;
GitHub repository publication does not deploy a separate website.
