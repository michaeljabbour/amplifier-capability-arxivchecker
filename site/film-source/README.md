# ArxivChecker text film

Original six-scene, silent film. The on-screen text contains the full message;
WebVTT captions and a plain-text transcript provide alternatives. The chart in
scene three is an illustration with no empirical values.

The main film is 48 seconds; the short cut is 15 seconds. Playback is user initiated.
Frames use the site palette and installed system fonts; there are no third-party
images, voice samples, stock footage, music, external services or measured claims.

To regenerate with an existing Python environment containing Pillow and local ffmpeg:

```sh
python3 site/film-source/make_film.py
```

The default font paths are macOS Georgia and Arial. On other platforms, pass
`--serif-font /path/to/serif.ttf --sans-font /path/to/sans.ttf`. Use `--skip-webm`
if the local ffmpeg does not support VP9. These optional production tools are not
website, installation or runtime requirements. The source script uses only Pillow
and Python's standard library and invokes ffmpeg without a shell.

Font files are not redistributed. Generated frames, film and captions are original
project assets under the repository license. Video encoding may vary across local
ffmpeg versions; all text is fixed in the source script.
