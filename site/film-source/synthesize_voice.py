#!/usr/bin/env python3
"""Synthesize the reviewed narration locally with an installed macOS voice.

Uses only /usr/bin/say and ffprobe, with no network, provider credits or microphone.
Some sandboxes return an empty AIFF despite exit 0; duration validation catches it.
Output must be a new directory. Audio is generated sentence-by-sentence so no line
is sped up or cut to fit a scene. make_film.py adds pauses and verifies the fit.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def duration(path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    return float(json.loads(result.stdout).get('format', {}).get('duration', 0))


def synthesize(plan_path, output):
    if output.exists() or output.is_symlink():
        raise ValueError('Voice output must be a new directory; existing audio is preserved.')
    plan = json.loads(plan_path.read_text())
    if plan['voice'] not in ('Samantha', 'Daniel') or not 150 <= plan['words_per_minute'] <= 175:
        raise ValueError('Use an installed reviewed voice and a normal 150–175 wpm rate.')
    if len(plan['full']) != 6 or len(plan['short']) != 3:
        raise ValueError('The existing film has six full scenes and three short scenes.')
    output.mkdir(parents=True)
    record = {'voice': plan['voice'], 'locale': plan['locale'], 'words_per_minute': plan['words_per_minute'], 'plan_sha256': sha256(plan_path), 'clips': []}
    for cut, scene_duration in [('full', 8), ('short', 5)]:
        for index, caption in enumerate(plan[cut]):
            text = caption
            for original, spoken in plan.get('pronunciation', {}).items():
                text = text.replace(original, spoken)
            target = output / f'{cut}-{index}.aiff'
            subprocess.run(['/usr/bin/say', '-v', plan['voice'], '-r', str(plan['words_per_minute']), '-o', str(target), text], check=True)
            seconds = duration(target)
            if seconds < 0.5:
                raise ValueError(f'{target.name}: no usable speech samples; local speech-service access may be blocked.')
            if seconds > scene_duration - 0.6:
                raise ValueError(f'{target.name}: speech {seconds:.3f}s exceeds a {scene_duration}s scene with pauses. Shorten the text; do not truncate or rush it.')
            record['clips'].append({'cut': cut, 'scene': index, 'caption': caption, 'tts_text': text, 'duration_seconds': seconds, 'scene_seconds': scene_duration, 'sha256': sha256(target)})
    (output / 'voice-manifest.json').write_text(json.dumps(record, indent=2) + '\n')
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('narration.json'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = synthesize(args.plan, args.output)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Voice generation stopped: {exc}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
