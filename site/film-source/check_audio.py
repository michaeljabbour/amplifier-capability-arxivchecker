#!/usr/bin/env python3
"""Verify complete decode, audible samples, levels and expected film audio streams.

This is a signal and container check, not a substitute for listening to the film.
It uses existing ffmpeg/ffprobe and Python's standard library, with no network.
"""
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys


def db(value):
    return round(20 * math.log10(value), 3) if value > 0 else None


def check_captions(path, expected, scene_seconds):
    def seconds(text):
        hours, minutes, final = text.split(':')
        return int(hours) * 3600 + int(minutes) * 60 + float(final)
    blocks = re.split(r'\n\s*\n', path.read_text().strip())[1:]
    if len(blocks) != len(expected):
        raise ValueError(f'{path.name}: caption count differs from narration')
    cues = []
    for index, (block, narration) in enumerate(zip(blocks, expected)):
        timing, *lines = block.splitlines()
        start_text, end_text = timing.split(' --> ')
        start, end = seconds(start_text), seconds(end_text)
        if ' '.join(' '.join(lines).split()) != narration:
            raise ValueError(f'{path.name}: caption {index+1} differs from spoken script')
        if abs(start - (index * scene_seconds + 0.35)) > 0.001 or not start < end <= (index+1)*scene_seconds-0.25:
            raise ValueError(f'{path.name}: caption {index+1} exceeds its speech scene')
        cues.append({'scene': index+1, 'start_seconds': start, 'end_seconds': end, 'script_match': True})
    return {'file': path.name, 'spoken_script_matches': True, 'cues': cues}


def inspect(path, expected_duration):
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)
    audio = [stream for stream in info['streams'] if stream['codec_type'] == 'audio']
    video = [stream for stream in info['streams'] if stream['codec_type'] == 'video']
    if len(audio) != 1 or len(video) != 1:
        raise ValueError(f'{path.name}: expected exactly one video and one audio stream')
    if audio[0]['sample_rate'] != '48000' or audio[0]['channels'] != 1:
        raise ValueError(f'{path.name}: expected 48 kHz mono audio')
    expected_codec = 'opus' if path.suffix == '.webm' else 'aac'
    if audio[0]['codec_name'] != expected_codec:
        raise ValueError(f'{path.name}: expected {expected_codec} audio')
    actual_duration = float(info['format']['duration'])
    if abs(actual_duration - expected_duration) > 0.1:
        raise ValueError(f'{path.name}: unexpected duration {actual_duration}')
    subprocess.run(['ffmpeg', '-hide_banner', '-v', 'error', '-i', str(path), '-f', 'null', '-'], capture_output=True, check=True)
    raw = subprocess.run(['ffmpeg', '-hide_banner', '-v', 'error', '-i', str(path), '-vn', '-f', 'f32le', '-ac', '1', '-ar', '48000', '-'], capture_output=True, check=True).stdout
    samples = array('f')
    samples.frombytes(raw)
    if sys.byteorder != 'little':
        samples.byteswap()
    if not samples or not all(math.isfinite(value) for value in samples):
        raise ValueError(f'{path.name}: missing or non-finite decoded samples')
    peak = max(abs(value) for value in samples)
    rms = math.sqrt(sum(value * value for value in samples) / len(samples))
    clipped_samples = sum(abs(value) >= 1 for value in samples)
    if peak < 0.01 or rms < 0.001 or clipped_samples:
        raise ValueError(f'{path.name}: absent speech or clipped samples')
    measurement = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(path), '-vn', '-af', 'loudnorm=I=-18:TP=-1.5:LRA=7:print_format=json', '-f', 'null', '-'], capture_output=True, text=True, check=True)
    loudness, _end = json.JSONDecoder().raw_decode(measurement.stderr[measurement.stderr.rfind('{'):])
    if not -19 <= float(loudness['input_i']) <= -17 or float(loudness['input_tp']) > -1:
        raise ValueError(f'{path.name}: loudness or true peak outside reviewed limits')
    return {
        'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'duration_seconds': actual_duration, 'audio_codec': audio[0]['codec_name'],
        'sample_rate_hz': 48000, 'channels': 1, 'complete_decode': 'passed',
        'decoded_samples': len(samples), 'sample_peak_dbfs': db(peak), 'rms_dbfs': db(rms),
        'clipped_samples': clipped_samples,
        'integrated_loudness_lufs': float(loudness['input_i']),
        'true_peak_dbtp': float(loudness['input_tp']), 'loudness_range_lu': float(loudness['input_lra']),
        'listening_review': 'required separately: signal checks cannot establish spoken intelligibility or pacing',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path, default=Path(__file__).resolve().parents[1] / 'assets')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        plan = json.loads(Path(__file__).with_name('narration.json').read_text())
        result = {
            'schema_version': 1,
            'checks': [inspect(args.assets / name, seconds) for name, seconds in [('arxivchecker-film.mp4', 48), ('arxivchecker-film.webm', 48), ('arxivchecker-film-15s.mp4', 15)]],
            'captions': [check_captions(args.assets / 'arxivchecker-film.vtt', plan['full'], 8), check_captions(args.assets / 'arxivchecker-film-15s.vtt', plan['short'], 5)],
        }
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Audio verification failed: {exc}\n')
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
