#!/usr/bin/env python3
"""Offline diagnostic ASR and independent sample/timing checks; no listening claim."""
from array import array
from datetime import datetime, timezone
from difflib import SequenceMatcher
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import wave

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
MODEL = Path.home() / '.local/share/whisper-cpp/models/ggml-base.bin'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(text):
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())


def distance(expected, actual):
    previous = list(range(len(actual) + 1))
    for i, a in enumerate(expected, 1):
        row = [i]
        for j, b in enumerate(actual, 1):
            row.append(min(row[-1] + 1, previous[j] + 1, previous[j - 1] + (a != b)))
        previous = row
    return previous[-1]


def main():
    result_path = OUT / 'independent-audio-review.json'
    if result_path.exists():
        raise SystemExit('Refusing to overwrite an independent result')
    binary = shutil.which('whisper-cli')
    if not binary or not MODEL.is_file():
        raise SystemExit('Existing whisper-cli and cached ggml model required; no downloads allowed')
    plan_path = ROOT / 'site/film-source/narration.json'
    plan = json.loads(plan_path.read_text())
    voice_path = OUT / 'source-audio/voice-manifest.json'
    voice = json.loads(voice_path.read_text())
    assert sha(plan_path) == voice['plan_sha256']
    clip_checks = []
    for clip in voice['clips']:
        path = voice_path.parent / f"{clip['cut']}-{clip['scene']}.aiff"
        assert sha(path) == clip['sha256']
        end = .35 + clip['duration_seconds']
        clip_checks.append({'cut': clip['cut'], 'scene': clip['scene'] + 1,
                            'source_hash_matches': True, 'speech_source_end_in_scene_seconds': round(end, 6),
                            'remaining_scene_seconds': round(clip['scene_seconds'] - end, 6)})
    version = subprocess.run([binary, '--version'], capture_output=True, text=True, check=True)
    record = {'observed_at': datetime.now(timezone.utc).isoformat(),
              'scope': 'Independent offline diagnostic ASR and decoded sample/timing checks. ASR is not human listening, a pronunciation guarantee, or proof of subjective pacing.',
              'asr_engine': {'binary': '<HOMEBREW>/bin/whisper-cli', 'version': version.stdout.strip() or version.stderr.strip(),
                             'cached_model': 'ggml-base.bin', 'model_bytes': MODEL.stat().st_size, 'model_sha256': sha(MODEL),
                             'device': 'CPU', 'language': 'en', 'script_prompt': None,
                             'network_downloads_installations_provider_calls': False},
              'source_clip_checks': clip_checks, 'cuts': []}
    for cut, name, seconds, scene_seconds in [('full', 'arxivchecker-film.mp4', 48, 8), ('short', 'arxivchecker-film-15s.mp4', 15, 5)]:
        source = ROOT / 'site/assets' / name
        wav = OUT / f'independent-{cut}-16khz.wav'
        if wav.exists(): raise ValueError('Diagnostic WAV already exists')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-i', str(source), '-map', '0:a:0', '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', str(wav)], check=True)
        with wave.open(str(wav)) as reader:
            assert reader.getnchannels() == 1 and reader.getframerate() == 16000
            samples = array('h', reader.readframes(reader.getnframes()))
        if sys.byteorder != 'little': samples.byteswap()
        scene_activity = []
        for index in range(seconds // scene_seconds):
            scene = samples[index * scene_seconds * 16000:(index + 1) * scene_seconds * 16000]
            active = []
            for offset in range(0, len(scene), 320):
                frame = scene[offset:offset+320]
                rms = math.sqrt(sum((s/32768)**2 for s in frame)/len(frame))
                if rms >= 10**(-45/20): active.append(offset/16000)
            scene_activity.append({'scene':index+1,'threshold_dbfs':-45,'window_ms':20,
                                   'first_active_in_scene_seconds':active[0] if active else None,
                                   'last_active_in_scene_seconds':round(active[-1]+.02,3) if active else None,
                                   'silent_tail_at_threshold_seconds':round(scene_seconds-active[-1]-.02,3) if active else None})
        prefix = OUT / f'independent-{cut}-asr'
        command = [binary, '-m', str(MODEL), '-f', str(wav), '-l', 'en', '-ng', '-t', '8', '-ojf', '-otxt', '-of', str(prefix)]
        run = subprocess.run(command, capture_output=True, text=True)
        diagnostic = (run.stdout + '\n' + run.stderr).replace(str(Path.home()), '<HOME>').replace(str(ROOT), '<CHECKOUT>')
        (OUT/f'independent-{cut}-asr-log.txt').write_text(diagnostic)
        if run.returncode: raise RuntimeError(f'{cut} ASR exited {run.returncode}; inspect its independent log')
        asr = json.loads(prefix.with_suffix('.json').read_text())
        # Remove machine-specific model/input paths from the public diagnostic output.
        sanitized = json.dumps(asr, indent=2).replace(str(ROOT), '<CHECKOUT>').replace(str(Path.home()), '<HOME>')
        prefix.with_suffix('.json').write_text(sanitized+'\n')
        actual = ' '.join(item['text'].strip() for item in asr['transcription'])
        expected = ' '.join(plan[cut])
        for brand, spoken in plan.get('pronunciation', {}).items(): expected = expected.replace(brand, spoken)
        a, b = words(expected), words(actual)
        edits = distance(a,b)
        differences = [{'operation':op,'expected':' '.join(a[i:j]),'recognized':' '.join(b[k:l])}
                       for op,i,j,k,l in SequenceMatcher(None,a,b,autojunk=False).get_opcodes() if op != 'equal']
        recognized_duration = len(samples)/16000
        record['cuts'].append({'asset':source.relative_to(ROOT).as_posix(),'asset_sha256':sha(source),
                               'decoded_duration_seconds':recognized_duration,'expected_seconds':seconds,
                               'decoded_sample_peak_dbfs':round(20*math.log10(max(abs(x) for x in samples)/32768),3),
                               'decoded_samples_at_full_scale':sum(abs(x)>=32767 for x in samples),
                               'expected_spoken_text':expected,'asr_text':actual,'expected_words':len(a),
                               'recognized_words':len(b),'word_edit_distance':edits,
                               'word_error_rate':round(edits/len(a),6),'differences':differences,
                               'scene_activity':scene_activity,'asr_json':prefix.with_suffix('.json').name})
        print(json.dumps({'cut':cut,'expected_words':len(a),'recognized_words':len(b),'word_error_rate':round(edits/len(a),6),'differences':differences}),flush=True)
    result_path.write_text(json.dumps(record,indent=2)+'\n')
    print('Wrote', result_path.name)


if __name__ == '__main__':
    main()
