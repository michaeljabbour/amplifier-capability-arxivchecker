# Original ArxivChecker narrated film (v1)

This page documents the retained v1 assets. The main page now uses the [v2 launch film](v2/README.md).

The original six-scene story has local synthetic US English narration.
WebVTT captions match the spoken lines, with separate full and 15-second
transcripts that also describe the on-screen text. The chart in scene three is
an illustration with no empirical values.

The main film is 48 seconds; the short cut is 15 seconds. Playback is user initiated.
Frames use the site palette and installed system fonts; there are no third-party
images, human voice recordings, stock footage, music, external services or measured
claims. Samantha is an installed macOS synthetic voice, used at 165 words per
minute. The existing story and its limits are preserved.

To regenerate with an existing Python environment containing Pillow and local ffmpeg:

```sh
python3 site/film-source/synthesize_voice.py --output /tmp/new-arxivchecker-voice
python3 site/film-source/make_film.py --audio-source /tmp/new-arxivchecker-voice
python3 site/film-source/check_audio.py --output /tmp/arxivchecker-audio-check.json
```

Use a trusted installed Python environment with Pillow (the local production
environment used Python 3.14). `synthesize_voice.py` requires the installed macOS
`say` utility; speech-service access may need an unsandboxed local command. It
rejects the empty audio that some sandboxes produce despite exit code zero.
The voice output directory must be new. Existing source audio is preserved.
There is no external voice provider or API key.

`narration.json` is the reviewed script. Only the brand pronunciation is expanded
from ArxivChecker to “Archive Checker” for speech; captions preserve the brand.
Full speech clips are 5.58–7.14 seconds within eight-second scenes; short clips
are 2.95–3.56 seconds within five-second scenes. Each clip has a 350 ms lead-in
and the remaining time is a pause. The generator rejects overflow rather than
speeding up or truncating a sentence. Two-pass loudness normalization targets
−18 LUFS and a −1.5 dB true-peak ceiling. MP4 uses 48 kHz mono AAC; WebM uses
48 kHz mono Opus. `check_audio.py` verifies full decode, sample/RMS levels,
loudness and peaks. Listening review is still separate.

The default font paths are macOS Georgia and Arial. On other platforms, pass
`--serif-font /path/to/serif.ttf --sans-font /path/to/sans.ttf`. Use `--skip-webm`
if the local ffmpeg does not support VP9. These optional production tools are not
website, installation or runtime requirements. The source scripts use Pillow
and Python's standard library and invoke local tools without a shell.

No font files, voice-model files or human voice recordings are redistributed.
The project code, written script and original visual design follow the repository
license; that statement does not relicense Apple's installed synthetic voice or
its model. This voiceover revision is local and unpublished. Any public release
requires the owner's release decision, including review of applicable voice-use
terms. Video encoding may vary across local ffmpeg versions; all text is fixed
in the source script.
