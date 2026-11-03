# Narration revision evidence

Revised 2026-11-03. This adds intelligible local synthetic voiceover to the
existing six-scene, 48-second study-to-paper film and its existing three-scene,
15-second cut. The story and empirical limits are unchanged. The poster and
frames now use the Amplifier family paper, ink, gold and green palette.

The production script is `site/film-source/narration.json`. It was reviewed by
the coordinating agent before synthesis. Samantha, an installed US English
macOS voice, speaks at 165 words per minute. ArxivChecker is pronounced
“Archive Checker.” No external voice service, provider credits, software
installation, music, microphone or human voice recording was used.
No font or voice-model files are distributed. This local, unpublished revision
does not assign the repository's MIT license to Apple's synthetic voice or model.
Public release remains a separate owner decision, including any applicable
voice-use terms.

The first sandboxed `say` smoke test returned exit code zero but an empty AIFF
with no audio samples. A local unsandboxed `say` test produced valid samples,
then the approved narration was generated into `source-audio/`. Those original
speech clips and their hashes remain available. This was a local speech-service
access requirement, not a remote generation request. No failed empty test file
was used in the film.

Full speech clips last 5.58–7.14 seconds in eight-second scenes. Short speech
clips last 2.95–3.56 seconds in five-second scenes. The mix gives each clip
350 ms of silence before speech and fills the remaining scene with silence.
No sentence was rushed, time-compressed or truncated. Captions reproduce the
spoken script, with cue ends based on the measured clip durations; separate
transcripts describe both narration and on-screen text for each cut.

`audio-check.json` records complete ffmpeg decoding, stream format, duration,
decoded RMS/sample peaks, clipped sample count, integrated loudness and true
peaks. Results before listening review:

| Asset | Audio | LUFS | True peak | Clipped samples |
| --- | --- | ---: | ---: | ---: |
| Full MP4, 48 seconds | AAC, 48 kHz mono | −18.02 | −2.72 dBTP | 0 |
| Full WebM, 48.008 seconds | Opus, 48 kHz mono | −17.99 | −2.66 dBTP | 0 |
| Short MP4, 15 seconds | AAC, 48 kHz mono | −18.01 | −3.28 dBTP | 0 |

These checks establish that usable speech samples exist, the entire media
decodes, audio levels are appropriate, and the measured clips fit their scenes.
They cannot establish intelligibility by themselves. Browser playback and
listening review are recorded separately by the coordinating agent.

The original silent media was retained in the original local repository while
this revision was produced in a separate staging directory. Its filenames,
sizes and hashes are in `original-media-manifest.json`.

Reproduce with an existing Python environment containing Pillow and installed
`say`, ffmpeg and ffprobe:

```sh
python3 site/film-source/synthesize_voice.py --output /tmp/new-arxivchecker-voice
python3 site/film-source/make_film.py --audio-source /tmp/new-arxivchecker-voice
python3 site/film-source/check_audio.py --output /tmp/arxivchecker-audio-check.json
```

The voice output directory must be new. Synthesis may require local permission
to reach the installed macOS speech service; it performs no network request.
