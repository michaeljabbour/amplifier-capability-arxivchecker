# Page-number correction for Claude

MJ's current default is **visible page numbers on the title page and subsequent
pages**. Follow explicit author instructions or applicable venue requirements
when they differ. This is MJ's publishing style, not an arXiv requirement.
The reviewed [arXiv format policy](https://info.arxiv.org/help/policies/format_requirements.html)
discusses line numbers, which are a separate feature; no universal page-number
requirement or prohibition was identified in the reviewed policy.

## Resolved in the supplied v3 reel

The [v3 verification record](VIDEO-V3.md) documents the replacement narration, visible footer and retimed captions. The prompt and exact v2 edit targets below are preserved as history; they do not describe a remaining conflict in the current player.

## Historical v2 conflict

The unchanged v2 MP4 SHA-256 is
`b449db7981ec99e201cd951823f11dcf15105b1a51aa9d8c0c71442e53af22c7`.
Times below are in the full 71.14-second master. Spoken bounds come from the
production alignment; visual animation-clock bounds were checked against
selected actual 30 fps frames. They are edit targets, not subframe perceptual
measurements.

| Element | Master time | Current content requiring correction |
| --- | --- | --- |
| L6d source audio cut | 46.140–48.890 s | “And your house style leaves off the page numbers.” |
| Aligned spoken words | 46.180–48.480 s | “leaves off” spans 47.100–47.780 s |
| Full VTT/SRT cue | 46.100–48.730 s | Same obsolete narration |
| HOUSE STYLE chip | Fade-in 46.410–46.710 s | Keep the classification as house style |
| Main visual label | Reveal 46.610–46.960 s | “No page numbers” must become “Visible page numbers” |
| Footer digit 1 | Appears 46.560–46.810 s; fades away 48.130–48.480 s | Keep the digit visible rather than removing it |
| Empty dashed footer | Appears 48.180–48.480 s | Remove this representation of an empty footer |
| Scene transition | Fades out 48.490–48.840 s | Preserve the scene's transition or report any necessary retiming |

The 14.5-second cut excludes this segment. Its master ranges are
2.05–4.75, 9.30–12.95, 13.14–19.04 and 65.89–68.14 seconds; its narration,
captions and transcript have no page-number conflict. Recheck mappings if the
master's timing changes.

## Copy this prompt into Claude

```text
Use the Sizzle skill to correct the existing ArxivChecker v2 film's page-number
example. Read ~/dev/amplifier-skill-sizzle/SKILL.md and the current capability
in ~/dev/amplifier-capability-arxivchecker first. Work in the original production
workspace with its licensed source audio/alignment inputs, fonts and tools;
the public site/film-source/v2 archive is not a turnkey rebuild.

MJ's default is visible page numbers, including the title and subsequent pages,
with explicit author instructions or applicable venue requirements allowed to
change the treatment. This is MJ's house style, not an arXiv requirement.

Correct only the house-style segment around 00:46–00:49:
- Replace “And your house style leaves off the page numbers.” with
  “And your house style includes visible page numbers.”
- Keep the HOUSE STYLE chip. Change “No page numbers” to “Visible page numbers”.
- Reveal and retain the footer page number. Remove the animation that fades it
  away and replaces it with an empty dashed footer.
- Keep the arXiv margin rule and figure-description recommendation unchanged,
  with their existing classifications.

The current L6d cut is 46.140–48.890 s; its spoken words occupy 46.180–48.480 s.
The matching caption is 46.100–48.730 s. Treat these as current edit targets,
then remeasure the new take. Do not rush or truncate speech to fit old timings.

Show the replacement line and changed storyboard frame for approval before
new generation/rendering, as Sizzle requires. Make a new version; preserve v2.
Keep the rest of the story, voice casting, score, palette and motion unchanged
except where the correction requires a documented timing adjustment.

Update L6d's actual take, text and word alignment; the edit.json snapshot;
scene 6's label/footer logic in index.src.html; lint copy; full captions/SRT and
the descriptive transcript. The existing code uses T.house and T.numbers from
L6d word anchors: recompute those timings from the new voice. If wording changes
again, update all anchor lookups so missing words cannot silently mis-time it.
Refresh the production brief/README/verification record to describe the new
version while retaining earlier reports as historical evidence.

Render the corrected full MP4 and WebM. The current 14.5-second cut excludes
this scene; preserve it if its source/timing remains valid, otherwise remap it.
Verify caption wording against the new audio, review the actual footer frames,
check loudness/decoding and compare changed frame ranges with v2. State exactly
what was seen, measured and left for human listening; do not invent approval.
Do not re-add the removed homepage link row or publish/deploy anything unless
separately asked. Return the new files and verification notes.
```

## Preserved historical v2 material

The film, captions and transcripts continue to describe the existing v2 media
accurately; changing those words alone would make them inaccurate. The v2
composition, alignment, storyboard and generation notes are archival records of
that version, not the current publishing default. Old unnumbered PDF/TeX layout
evidence is retained as a superseded snapshot. Current skill guidance,
examples, starter and new numbered-template evidence govern new papers.
