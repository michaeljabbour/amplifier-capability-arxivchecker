#!/usr/bin/env python3
"""Captions from the measured voice timeline (edit/edit.json): WebVTT and SRT, at most two lines of 42 characters.
Long lines split at a sentence or clause boundary, timed by the word clock. Usage: make_captions.py OUTDIR [cut.json]"""
import json, sys, textwrap
from pathlib import Path
ROOT = Path(__file__).resolve().parent
E = json.loads((ROOT / 'edit/edit.json').read_text())
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
# Optional remap for a cut-down: list of [src_a, src_b, dst_a]
CUT = json.loads(Path(sys.argv[2]).read_text()) if len(sys.argv) > 2 and sys.argv[2] != '-' else None
SPLIT = {'L2': 'starts with', 'L3': 'and adds', 'L4': 'If a result', 'L7': 'from only', 'L8': 'how AI'}

cues = []
for v in E['vo']:
    words, text = v['words'], v['text']
    parts = [text]
    if v['id'] in SPLIT:
        k = text.index(SPLIT[v['id']]); parts = [text[:k].strip(), text[k:].strip()]
    # time each part by its first and last word
    n0 = 0
    for part in parts:
        nw = len(part.split()); ws = words[n0:n0 + nw] or words[-1:]
        a = v['start'] + ws[0][0] - 0.08; b = v['start'] + ws[-1][1] + 0.25
        cues.append([a, b, part]); n0 += nw
# no overlaps; a short gap stays a gap
for i in range(len(cues) - 1):
    cues[i][1] = min(cues[i][1], cues[i + 1][0] - 0.04)

def remap(a, b):
    if not CUT: return a, b
    for sa, sb, da in CUT:
        if b > sa and a < sb: return da + max(a, sa) - sa, da + min(b, sb) - sa
    return None
def ts(x, sep='.'):
    x = max(0, x); h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{s:06.3f}'.replace('.', sep)
vtt, srt, n = ['WEBVTT', ''], [], 0
for a, b, part in cues:
    r = remap(a, b)
    if not r or r[1] - r[0] < 0.3: continue
    n += 1
    if len(part) <= 42: lines = [part]
    else:
        ws = part.split(); best = min(range(1, len(ws)), key=lambda k: max(len(' '.join(ws[:k])), len(' '.join(ws[k:]))))
        lines = [' '.join(ws[:best]), ' '.join(ws[best:])]
    vtt += [f'{ts(r[0])} --> {ts(r[1])}', *lines, '']
    srt += [str(n), f'{ts(r[0], ",")} --> {ts(r[1], ",")}', *lines, '']
name = sys.argv[3] if len(sys.argv) > 3 else 'captions'
(out / f'{name}.vtt').write_text('\n'.join(vtt)); (out / f'{name}.srt').write_text('\n'.join(srt))
print(n, 'cues ->', out / f'{name}.vtt')
