# Independent offline narration check — 2026-11-03

This is automated verification, **not a listening review**. Existing Homebrew
`whisper-cli` 1.9.5 and the already cached multilingual `ggml-base.bin` ran on CPU,
in English, without a script prompt, installation, network access, model
download or provider call. The model fingerprint and current media hashes are
recorded in `independent-audio-review.json`. The expected text applies only the
documented brand pronunciation, “Archive Checker”; punctuation and case are
ignored for word comparison.

| Cut | Expected / recognized words | Word edits | Diagnostic result |
| --- | ---: | ---: | --- |
| 48-second MP4 | 92 / 92 | 7 (7.61% word error rate) | No obvious missing ending; recognizer differences need listening |
| 15-second MP4 | 27 / 27 | 0 | All expected words recognized in order |

Full-cut differences were `raw` → `row`, `filenames` → `file names`, `AI use,
rights` → `AIUS writes`, and `acceptance` → `exceptions`. The filenames difference
is tokenization; the others are diagnostic uncertainties in this small ASR
model, not proof that the narrator spoke the wrong words. Listen particularly
to the final scene's “AI use, rights” and “cannot guarantee acceptance.” The
brand was recognized as “Archive Checker,” matching the intended expansion.

Independent decoding produced exactly 48.0 and 15.0 seconds of mono PCM. No
sample reached full scale; decoded peaks were −2.72 and −3.35 dBFS after 16 kHz
resampling. The separate producer's 48 kHz measurements report zero clipped
samples, integrated loudness near −18 LUFS and true peaks below −2.6 dBTP across
all three encoded assets. These signal checks do not establish intelligibility.

The current narration plan hash and all nine source-clip hashes match the voice
manifest. The production code inserts 350 ms before each source clip, pads each
scene, then normalizes the complete cut in two passes. It rejects overlong
source clips before applying the fixed scene trim. The longest full-cut source
ends 7.488 seconds into its eight-second scene, leaving 0.512 seconds; none needs
to be cut to fit.

A separate 20 ms RMS-envelope check at −45 dBFS found each scene's speech onset
at 0.34–0.36 seconds, consistent with that lead-in. Full-cut speech tails leave
0.56–2.12 seconds per scene; short-cut tails leave 1.12–1.74 seconds. No detected
speech reaches a scene boundary. These are threshold-based timing observations,
not a subjective pacing judgment or word-level synchronization measurement.

`independent-full-asr.json`, `independent-short-asr.json` and their text/log files
preserve the recognizer outputs. The diagnostic WAVs are decoded copies of the
generated narration, not microphone recordings. `independent_audio_review.py`
records how this check was run and refuses to overwrite an existing result.
Actual audible playback, pronunciation and natural pacing still require the
separate listening review.
