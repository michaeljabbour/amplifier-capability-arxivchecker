# ArxivChecker launch film: brief

Version: brief v2, storyboard v2 (2026-11-03; v1 revised after the creative gate, before showing MJ). Replaces the 48 s six-slide explainer as the site's main film. The current film and all its assets stay as they are; the new film ships as v2 beside them.

## Harness
- Eyes: yes. PNG frames open directly in the file reader (contact sheet of the current film viewed).
- Voice, music and sound: ElevenLabs connector. No keys were requested in chat.
- Tools: Playwright Chromium, ffmpeg/ffprobe, numpy, scipy, soundfile, librosa, pyloudnorm, faster-whisper, plus the existing Sizzle audit tools (audit hook, lint, motion, pops, ASR, voice-over-bed, voice words).
- Fonts (render only, never shipped): Gelasio (open stand-in for Georgia, the site's serif), Liberation Sans (stand-in for Arial), Latin Modern Roman and Mono (the real LaTeX faces, GUST licence) for the typeset page and source.
- Source: the ArxivChecker capability checkout. This archival brief describes the production session before GitHub publication; it does not describe current repository status.

## What to beat (the current film)
Six static cards, 8 s each, 1280x720, 24 fps. Body type about 14 px on a 720 frame. No motion, no score, a macOS system voice (Samantha). Each card restates a checklist. It reads as a slideshow with narration. The new film must move, teach and land.

## Idea
- **Purpose.** ArxivChecker helps an assistant carry a finished study to a LaTeX paper and a reviewable arXiv submission package: every claim traced to its source, figures built from the data, the whole story told in order, a clean rebuild from only the files you will send, and an explicit list of what people still decide. It prepares work for human review. It does not submit, and it does not certify science or acceptance.
- **Audience.** Researchers and builders (MJ's team, university labs, Amplifier adopters) who have finished a study, often an AI or agent experiment, and now have to write it up. They know research. They may not know arXiv's rules in detail, and they are wary of tools that promise to "write your paper". They watch on the capability's site, mostly with sound on, and on a feed with sound off.
- **Insight.** Your reader never sees your results folder. They only get sentences, and a sentence drifts a little further from its evidence every time it is polished.
- **Proposition.** ArxivChecker keeps every sentence in your paper tied to its evidence, all the way to the submission package, and leaves the final call with people.
- **Shape.** Scattered to assembled: a loose study folder becomes a typeset paper and a clean package. The opening sentence floats free of its evidence; the closing sentence carries its limits.
- **Turn.** "ArxivChecker starts with the evidence, not the draft." The loose thread snaps taut and pulls the camera down into the results file. Picture, voice and music all change on "evidence".
- **Hero line.** "A stronger claim has clearer limits." (already the site's own heading). Set big, in type, in near silence.
- **Ending.** The thread that hung loose from the first sentence ends as a blank signature line for the authors, then underlines the wordmark. Tagline: Trace. Rebuild. Review.
- **One breath.** We open on a polished sentence with nothing behind it, turn when the thread pulls us back into the evidence, and leave on a blank line that only a person can sign.

## Teaching device: three kinds of rule
The film teaches one distinction the repo cares about most, with three chips that keep their colour wherever they appear:
- **arXiv policy** (charcoal chip). Stated in arXiv's format policy or submission instructions. Examples used: single spacing, 10 to 14 pt type, margins of at least one inch; disclosing significant AI use.
- **arXiv recommends** (sage chip). arXiv's LaTeX best-practice advice for HTML and accessibility. Example used: alt text on figures.
- **House style** (gold chip). MJ's publishing style and the template's local choices. Examples used: no page numbers; the teaching order problem, what you built, how you tested it, what happened, limits; plain words with defined terms.
- **Local check** (outlined chip, one appearance): the clean rebuild in an empty folder. On screen with it: "A local check, not arXiv's decision."

## Claims ledger (what the film may say; source in the repo)
| Film statement | Source |
| --- | --- |
| Starts with the evidence, not the draft | SKILL.md: "Start with the study's files, never the old draft's numbers." |
| Traces each claim to its source; count, unit and what's left out go with it | SKILL.md evidence rules; README "Every headline needs its source, denominator, unit and limits."; claim-ledger template |
| Figures come straight from the data; a missing series stops the build | README: figure builder "fails if data is missing"; SKILL.md "Missing keys and expected series must fail visibly." |
| Tells the whole story in order: problem, built, tested, happened, limits | SKILL.md paper order; writing.md "Teach the reader the study". This order is house style, not an arXiv rule (requirements.md). |
| Sets the paper in LaTeX | templates/main.tex |
| 10 to 14 pt type, single spacing, margins at least one inch | requirements.md, official format requirement ("should"), format policy page |
| Alt text on figures is recommended | requirements.md, arXiv LaTeX best practices (recommendation) |
| No page numbers is a local preference | policy.md and requirements.md: "No page numbers preserves the user's preference" |
| Rebuilds in an empty folder from only the files you will send | README preflight: output must be new and outside the study; manifest allowlist; three pdflatex passes (local check) |
| Fonts embedded, filenames arXiv can read, no hidden files | requirements.md (PDF fonts check; filename rules; hidden files deleted on announcement) |
| Names, AI-use statement, license, category, final claims stay with people | SKILL.md "Leave category, licence, endorsement, authorship approval, release rights and final submission to the responsible person." |
| No promise of acceptance | README "does not ... certify ... acceptance"; policy.md |
| "A stronger claim has clearer limits." | site template heading |
| Fictional example claim and values | site.json claim_example (fictional teaching example) and docs/EXAMPLES.md. Labelled "Fictional example" on screen. |

## Never claim
Acceptance or likelihood of acceptance; that it submits for you; that a local build means arXiv will accept; time saved, users, adoption or benchmark results; any arXiv affiliation, endorsement or approval; that it verifies scientific validity, rights or references on its own; that the site is published. No private study material: every file name, number and chart is generic and fictional.

## Script v2 (for the ear; arXiv is voiced as "archive", ArxivChecker as "Archive Checker")
Emphasis word in **bold**. "/" marks a pause. 116 words, about 43 s of speech in a 68 s film (36 per cent free of voice).

1. Your study is **done**. / One result becomes a **sentence**.
2. ArxivChecker starts with the **evidence**, / not the draft.
3. It traces the claim to its **source**, / and adds the comparison / and what's left out.
4. Figures come straight from the **data**. / If a result goes missing, / the build **stops**.
5. The paper tells the story in **order**, / from the problem to its limits.
6. It sets the paper in LaTeX, / and **sorts** the rules. / Margins of at least an inch: / arXiv **asks**. / Describe each figure: / arXiv **advises**. / No page numbers: / house **style**.
7. Then it **rebuilds** the paper in an empty folder, / from only the files you'll send.
8. The names, how AI was used, the license / and the final **call** / stay with you.

In type only, in silence: "Half of what?" · "Then look at it." · "No promise of acceptance." · "A stronger claim has clearer limits." · the typed invitation "Use ArxivChecker on this study folder." and "Trace. Rebuild. Review."

Spelling: American (license), matching MJ.

## Script v2.1 (as recorded, 2026-11-03)
All four first takes went breathy on the same line-final words ("the draft", "arXiv asks", "house style", "with you"), confirmed on spectrograms. Three lines were reworded so the key word is not last; MJ was told, and the story is unchanged.
2. ArxivChecker starts with the evidence, not the old draft's numbers.
6. It sets the paper in LaTeX, and sorts the rules. arXiv asks for margins of at least an inch. It advises a description for every figure. And house style leaves off the page numbers.
8. You decide the names, how AI was used, the license and the final claims.
Recorded take: audio/v2/u2.mp3 (Veda Sky, eleven_v4). 124 words, about 46 s of speech in a 70 s film.

## Creative gate (fresh reviewer, 2026-11-03)
Verdict on storyboard v1: 10 of 15 passed. Failures and fixes:
- 4 (hook late): the polished sentence now writes on by 3.4 s over the soft-focus folder; "Half of what?" at 4.8 s.
- 7 (no invitation): the end card types the README's own first request, "Use ArxivChecker on this study folder."
- 10 (even scene lengths): scenes now run 7.8, 3.6, 10.6, 8.4, 5.2, 10.4, 6.4, 7.2, 3.4 and 5.0 s.
- 11 (scene 9 read as a slide): now a hand-over. The package slides across the desk to the viewer, and its cover sheet has blank decision lines and a signature line.
- 13 (unread callouts, insider labels): the rules scene now says every example aloud, with its chip seated on the phrase; the LaTeX source shows no template numbers (1.05in, 11pt); scene 8 thinned to four things; ".bbl", "Pass 1 2 3", "pt" and "Series" removed.
Precision fixes: the AI item reads "Disclose significant AI use" (a conditional official requirement, requirements.md line 94); the format items are voiced "arXiv asks", keeping the policy's "should" nuance; fonts and filenames dropped from the local-check scene so rule types do not mix; the rewrite now answers the question ("as much as the baseline"), and the before and after sentences are the site's own fictional example, verbatim (site.json).

## Beat sheet v2 (1920x1080, 30 fps, about 68 s; 120 BPM grid, 2 s bars)
| # | Time | Music | Picture and craft move | Voice | On screen | Thread (motif) | Sound | Job |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0-7.8 | Prepared, dry, close piano; dead stop at 4.6, silence to 7.8 | Five file cards drift in soft-focus 3D parallax; the polished sentence writes on huge in front of them; one sheen sweeps it; the thread hangs loose from its full stop; then the question, held in silence | 1 | "The system saved half the cost." · "Half of what?" (gold italic) · "Fictional example" | Loose end, swaying | Cards sliding; nib on paper; shimmer; silence | A polished sentence can lose its evidence |
| 2 | 7.8-11.4 | TURN: pizzicato pulse enters on "evidence" | The thread snaps taut and pulls; the camera dives along it into the results file, which opens like an aperture | 2 | "ArxivChecker" wordmark | Taut, pulling | Plucked-thread thrum | The method begins from evidence |
| 3 | 11.4-22.0 | Pulse, dampened mallets | Results file in large mono; the thread lands on the field; the sentence rebuilds itself as the evidence supplies each piece: the scope, what was counted, the comparison, the exclusions, each insertion arriving in gold on its spoken word; then held | 3 | results.json (fictional) · tags "Source", "vs baseline", "Left out" · final sentence "On this held-out task set, priced model calls cost half as much as the baseline. Setup, unpriced calls and human review are excluded." | Trace from the field into each insertion | Soft wooden clicks | A claim travels with its comparison and its exclusions |
| 4 | 22.0-30.4 | Build; drops out on "stops" (26.4-28.2) | Data rows stream into bars; row D's name changes in the file, so it never arrives; its slot stays empty; the thread snaps red and a stamp lands; hold; D restored and a lens passes over the labels | 4 | Rows A-D · "D is missing. Build stopped." · "Then look at it." (silent) · "Illustration, not study data" | Plotted stems; snaps on the empty slot | Wooden ticks; string snap; silence | A chart can look fine and still be missing data |
| 5 | 30.4-35.6 | Strings enter | Burst: the thread turns vertical; five section cards ripple down it and fold into a page's headings | 5 | Problem · What we built · How we tested it · What happened · Limits | The reading spine | Page flicks | The paper teaches in order |
| 6 | 35.6-46.0 | Lift | Four lines of LaTeX source type on, then compile into the page. Three examples, each said aloud: the thread measures the margin (chip "arXiv policy"), a figure gains its description (chip "arXiv recommends"), the page footer stays empty (chip "House style") | 6 | `\documentclass{article}` · `\includegraphics[alt=...]` · "Margins of at least 1 inch" · "Describe each figure" · "No page numbers" | Margin ruler, then sorting | Soft keys; a click per chip | Rules, advice and preference are different things |
| 7 | 46.0-52.4 | Drive | The page folds into its files; the thread stitches through the ones that ship and skips drafts and private data; an empty folder opens; the files drop in; the page rebuilds | 7 | main.tex · figures/ · references.bib · drafts/ (skipped) · private-data/ (skipped) · chip "Local check" · "A local check, not arXiv's decision." | Stitch | Archive latch; three soft ticks | Ready means it rebuilds from what you send |
| 8 | 52.4-59.6 | Breakdown: strings hold, piano alone | Hand-over: the package slides across the desk to the viewer; its cover sheet has four blank decision lines; the thread becomes the signature line; nothing gets ticked | 8 | Authors and affiliations · Disclose significant AI use (chip "arXiv policy") · License · Final claims · "No promise of acceptance." | Blank signature line | Paper slide; pen cap click | Some decisions only people make |
| 9 | 59.6-63.0 | Near silence, one piano note | Hero line in type; the thread underlines "clearer limits" | none | "A stronger claim has clearer limits." | Underline | One note | The takeaway |
| 10 | 63.0-68.0 | Warm resolve; sub drop under title | The underline becomes the wordmark rule; the first request types itself below | none | "ArxivChecker" · "Trace. Rebuild. Review." · "Use ArxivChecker on this study folder." | Wordmark rule | Sub drop; soft keys | Brand and invitation |

Held moments: 4.8-7.8 (the question), 16.5-22.0 (the rebuilt sentence), 26.6-28.2 (the empty slot), 59.6-63.0 (hero). Burst: scene 5.

Exception to the type rules: "Fictional example", "Illustration, not study data" and the chip labels at 24 px or more (each chip's phrase is spoken).

## Cut-downs
15 s cut: 2.2-5.2 (the polished sentence and its loose thread), 7.8-11.4 (the turn, with the name), 12.4-19.0 (the sentence gains its limits), 63.4-66.2 (end card). Brand on screen by about 3.2 s. Every beat reads with sound off. Captions remapped, -14 LUFS.

## Casting
US English, warm, thoughtful, peer to peer, early 30s to 40s, unhurried (about 150 wpm), never salesy. Recommendation: Veda Sky (ElevenLabs, eleven_v4), the selected voice for this production. Alternative: a calm US male voice from a fresh shortlist.

## Music brief
A research world, not a tech commercial: prepared piano, dry and close-miked (not soft inspirational felt), pizzicato strings, soft mallets (marimba or vibraphone, dampened), a warm cello, a light woodblock or clock-tick pulse, 120 BPM. Arc: curious, sparse opening; a dead stop for the question; the pulse enters on the turn; a steady build through the method with one drop at "the build stops"; a lift into the LaTeX scene; drive into the rebuild; a breakdown to strings and piano for the human decisions; near silence for the hero line; a warm, resolved final chord. Anti-references: no corporate electronica, stock tech arpeggios, glassy pads, generic inspirational piano, ukulele, or elevator and stock-video music.

## Sound palette
Paper cards sliding on a desk; a fountain-pen nib on paper; a taut thread plucked; small wooden clicks as tags seat; a string snapping; page flicks; soft mechanical keys; an archive latch; three soft ticks; a pen cap click; a sub drop under the title. Tactile, quiet, nothing decorative.

## Look
Elevated Amplifier Smart Tools family: paper #f6f4ee, ink #252823, muted #64685e, line #d8d8cc, gold #80642f (thread on cream; lifted to #b8924a on charcoal), sage #486b61, wash #e9ede5, proof red #8c473d for failure only. Charcoal stage for the turn and the LaTeX source. Static paper grain. Gelasio for display (96 to 140 px), Liberation Sans for labels (36 px and up), Latin Modern for the typeset page and the source. Motion typeset, not effects-driven: pushes of 3.5 per cent at most, eased moves, no spins or shake, one idea per beat.

## Questions for MJ
1. Length: about 67 s plus a 15 s cut. (Recommended.)
2. Voice: Veda Sky, or a new US voice? (Recommended: Veda Sky.)
3. Label for your style: "House style" on screen and in the voice, or "MJ's publishing style" as the site calls it? (Recommended: "House style" in the film, since the viewer reads it as the paper's house style; the site keeps the full name.)

## Storyboard approval
Version: storyboard v2 (10 frames, about 68 s)
Approved by: MJ, in chat, 2026-11-03 12:05 ("go! just make it clear")
Changes asked for: none to the story. Direction: clarity first. Big type, one idea per frame, every must-read word spoken or held, generous holds.
Answers: defaults accepted. About 68 s plus a 15 s cut; voice Veda Sky; label "House style".

Public copy: internal production identifiers, workspace paths and unrelated project references are omitted. The original supplied records are preserved privately. Storyboard/review entries below are supplied production history; independent publication checks are recorded separately.
