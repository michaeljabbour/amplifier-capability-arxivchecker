# ArxivChecker launch film, v2

This preserved film uses an earlier page-number preference. MJ now defaults to visible page numbers; the main player uses the corrected v3 film. This preserved v2 film’s contrary 46–49 second example is historical. See [the exact edit targets and Claude prompt](../../../docs/VIDEO-PAGE-NUMBERS.md). This archive describes v2, not current instructions for a new paper.

A 71-second narrated launch film and a 14.5-second cut, made with the Sizzle skill on 2026-11-03. It replaces the 48-second six-card explainer as the site's main film. The v1 film and every v1 asset are unchanged in `site/assets/`.

## What the film says

One fictional sentence, "The system saved half the cost.", hangs from a loose gold thread. "Half of what?" The thread pulls taut into the results file, and the sentence rebuilds as the site's own corrected example, with its comparison and exclusions stitched in from the fields they came from. Then, in order:

- the figures are drawn from the data, and a renamed result stops the build;
- the paper tells the story in order;
- LaTeX, and the rules sorted into three kinds: arXiv policy (margins of at least one inch), arXiv recommends (describe each figure) and house style (no page numbers);
- a rebuild in an empty folder from only the files you send, shown as "a local check, not arXiv's decision";
- a hand-over sheet of the decisions that stay with the authors, with "No promise of acceptance.";
- "A stronger claim has clearer limits.", the end card and the README's first request.

## What changed after review

- **Creative gate on storyboard v1.** It failed 5 of 15 points; all five were fixed before MJ saw v2.
- **Voice.** All four first takes whispered on the same line-final words, so three lines were reworded.
- **Second critic.** In response, the narration now says "a skill for your AI assistant", "arXiv advises" (not "It advises") and "your house style". The figure scene shows why D comes back. The AI item reads "How you disclose AI use". The rebuild plays on the charcoal stage.

The supplied production measurements are in `verification.txt`; they were not all independently rerun here. The subsequent publication review is in [VIDEO-UPDATE](../../../docs/VIDEO-UPDATE.md).

## Production

- **Voice:** Veda Sky, ElevenLabs eleven_v4.
- **Score and effects:** generated with ElevenLabs.
- **Picture:** one HTML canvas page (`index.src.html`), rendered frame by frame.
- **Fonts used to render, not shipped:** Gelasio, Liberation Sans, Latin Modern.
- **Archived production sequence:** `make_edit.py` → `build.py` → `render.py` (three frame ranges) → `mix.py` → `deliver.py` → `make_transcripts.py`. This is a source archive, not a turnkey rebuild. The original `audio/`, `edit/`, `web/`, audit `tools/` and render-font inputs are not all supplied. Rebuilding requires the original licensed production inputs and the documented dependencies; do not assume these scripts run from this checkout.

Every file, number and chart in the film is fictional. The voice is synthetic. Any public release is the owner's decision, including a review of the applicable voice and music terms.
