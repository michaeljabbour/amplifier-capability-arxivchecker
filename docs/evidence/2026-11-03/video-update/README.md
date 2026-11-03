# Independent supplied-video review — 2026-11-03

These records describe the exact user-supplied v2 MP4, its retained WebM and
short cut, captions and transcripts. They supplement the originating production
record in `site/film-source/v2/verification.txt`; those earlier creative, layout,
motion, PSNR and voice-over-bed metrics were not all independently repeated.

Existing ffmpeg/ffprobe and offline whisper.cpp 1.9.5 with its already cached
base model were used. No provider call, model download, installation or
microphone recording was made. The ASR model hash and normalization are in the
independent record. Report word counts differ from the supplied production
record because tokenization/normalization differs.

All media decode cleanly. Word recognition exactly matches the full 132-word
and short 29-word caption sequences after case/punctuation and documented brand
pronunciation normalization. Full/short WebVTT have 17/4 non-overlapping cues,
matching their SRT counterparts and source word/cut mapping. These are speech
content and structural timing checks; coarse ASR timestamps cannot establish
subsecond perceptual synchronization. Human listening was not claimed.

The attachment and the previously prepared local MP4 have different container
hashes but identical encoded streams and decoded audio/video. The supplied
container bytes are the published main MP4. WebM has zero measured audio lag
and 0.9984 waveform correlation. Its 11 sampled decoded frames show no content
mismatch; lossy compression/texture causes small pixel differences. The 14.5 s
cut follows four master ranges and has zero measured audio lag. See the detailed
correspondence and frame records for the actual measured scope.

The coordinating agent visually inspected 16 supplied-video frames at 1.5,
6.9, 10.5, 16.8, 20.5, 25.5, 29, 33, 37, 41, 46, 50.8, 57.2, 60.5, 64.2 and
68.5 seconds. They show generic fictional study files, an illustrative chart,
format/style distinctions and author decisions. No private study material or
personal content was observed. This was sampled visual review, not inspection
of every frame.

Raw diagnostics remain private. Public JSON normalizes any machine-specific
path prefixes without changing hashes, measurements or recognized words.
Subjective listening, independent reproduction of every supplied Sizzle audit,
and provider rights/entitlement verification are outside this recorded check.
