#!/usr/bin/env python3
"""Join the picture parts, mux the master, encode web copies, cut the 15 s version, captions, posters, transcripts.
Usage: deliver.py v1   (reads out/v1/parts/*.mp4 and out/v1/mix.wav)"""
import json, subprocess, sys
from pathlib import Path
import numpy as np, soundfile as sf
ROOT = Path(__file__).resolve().parent
V = sys.argv[1] if len(sys.argv) > 1 else 'v1'
OUT = ROOT / 'out' / V; E = json.loads((ROOT / 'edit/edit.json').read_text()); DUR = E['duration']
NAME = 'arxivchecker-film-v2'
run = lambda *a: subprocess.run(list(a), check=True, capture_output=True, text=True)
SR = 48000

# 1. picture: concat parts losslessly, then mux the master with the mix, exact length
parts = sorted((OUT / 'parts').glob('p*.mp4'), key=lambda p: int(p.stem[1:]))
(OUT / 'parts/list.txt').write_text(''.join(f"file '{p.name}'\n" for p in parts))
if not (OUT / f'{NAME}.webm').exists(): run('ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(OUT / 'parts/list.txt'), '-c', 'copy', str(OUT / 'picture.mp4'))
if not (OUT / f'{NAME}.webm').exists(): run('ffmpeg', '-y', '-v', 'error', '-i', str(OUT / 'picture.mp4'), '-i', str(OUT / 'mix.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
    '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-t', str(DUR), str(OUT / f'{NAME}-master.mp4'))
# web copies: H.264 (faststart) and VP9/Opus
if not (OUT / f'{NAME}.webm').exists(): run('ffmpeg', '-y', '-v', 'error', '-i', str(OUT / f'{NAME}-master.mp4'), '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-fps_mode', 'passthrough', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(DUR), str(OUT / f'{NAME}.mp4'))
if not (OUT / f'{NAME}.webm').exists(): run('ffmpeg', '-y', '-v', 'error', '-i', str(OUT / f'{NAME}-master.mp4'), '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '33', '-row-mt', '1', '-deadline', 'good', '-cpu-used', '2',
    '-c:a', 'libopus', '-b:a', '128k', '-t', str(DUR), str(OUT / f'{NAME}.webm'))

# 2. the 15 s cut: master frames and the master mix, joined with 25 ms crossfades, -14 LUFS
CUT = [[2.05, 4.75], [9.3, 12.95], [13.14, 19.04], [65.89, 68.14]]
mix, _ = sf.read(OUT / 'mix.wav', dtype='float64'); xf = int(0.025 * SR); pieces = []
for a, b in CUT:
    seg = mix[int(a * SR):int(b * SR) + xf].copy()
    seg[:xf] *= np.linspace(0, 1, xf)[:, None] ** 0.5; seg[-xf:] *= np.linspace(1, 0, xf)[:, None] ** 0.5
    pieces.append(seg)
L = sum(int((b - a) * SR) for a, b in CUT) + xf; short = np.zeros((L, 2)); pos = 0
for (a, b), seg in zip(CUT, pieces): short[pos:pos + len(seg)] += seg; pos += int((b - a) * SR)
sdur = round(sum(b - a for a, b in CUT), 3)
sf.write(OUT / 'short-pre.wav', short[:int(sdur * SR)], SR, subtype='FLOAT')
p1 = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(OUT / 'short-pre.wav'), '-af', 'loudnorm=I=-14:TP=-1:LRA=20:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
js = json.loads(p1[p1.rindex('{'):p1.rindex('}') + 1])
af = f"loudnorm=I=-14:TP=-1:LRA=20:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true:print_format=json"
p2 = subprocess.run(['ffmpeg', '-hide_banner', '-y', '-i', str(OUT / 'short-pre.wav'), '-af', af, '-ar', '48000', '-c:a', 'pcm_f32le', str(OUT / 'short-mix.wav')], capture_output=True, text=True).stderr
j2 = json.loads(p2[p2.rindex('{'):p2.rindex('}') + 1])
segs = []
for i, (a, b) in enumerate(CUT):
    sp = OUT / f'cutseg{i}.mp4'
    run('ffmpeg', '-y', '-v', 'error', '-ss', str(a), '-i', str(OUT / 'picture.mp4'), '-t', str(round(b - a, 3)), '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', str(sp))
    segs.append(sp)
(OUT / 'cutlist.txt').write_text(''.join(f"file '{p.name}'\n" for p in segs))
run('ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(OUT / 'cutlist.txt'), '-i', str(OUT / 'short-mix.wav'), '-map', '0:v', '-map', '1:a',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(sdur), str(OUT / f'{NAME}-15s.mp4'))
cutmap = []; d = 0.0
for a, b in CUT: cutmap.append([a, b, round(d, 3)]); d += b - a
(OUT / 'cut-15s.json').write_text(json.dumps(cutmap))

# 3. captions for both
run('python3', str(ROOT / 'make_captions.py'), str(OUT), '-', NAME)
run('python3', str(ROOT / 'make_captions.py'), str(OUT), str(OUT / 'cut-15s.json'), NAME + '-15s')
print('full', DUR, 's; short', sdur, 's; short loudness', j2['output_i'], 'TP', j2['output_tp'], j2['normalization_type'])
