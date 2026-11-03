#!/usr/bin/env python3
"""Place every voice line by rule and write edit/edit.json (Sizzle 0.5, 5.4, 6.3).
Source take: audio/v2/u2.mp3 (Veda Sky, eleven_v4). Word times from edit/takes-v2.json (Whisper),
first line from a separate Whisper pass on 0-4.6 s (it was dropped in the full-take pass)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
take = json.loads((ROOT / 'edit/takes-v2.json').read_text())['audio/v2/u2.mp3']
take3 = json.loads((ROOT / 'edit/takes-v3.json').read_text())['audio/v3/w1.mp3']
W3 = sorted(([w['a'], w['b'], w['w']] for w in take3['words']), key=lambda x: x[0])
W3 = [[a, b, 'arXiv' if w == 'Arxiv' else w] for a, b, w in W3]
WORDS = sorted(([w['a'], w['b'], w['w']] for w in take['words']), key=lambda x: x[0])
WORDS += [[0.0, 0.16, 'Your'], [0.16, 0.56, 'study'], [0.56, 0.92, 'is'], [0.92, 1.26, 'done.'],
          [1.90, 2.14, 'One'], [2.14, 2.52, 'result'], [2.52, 3.08, 'becomes'], [3.08, 3.30, 'a'], [3.30, 3.60, 'sentence.']]
WORDS.sort(key=lambda x: x[0])
# Whisper hears "house" as "how" and puts "Archive" 0.7 s early (energy island starts 28.39).
FIX = {(34.66, 'how'): 'house', (27.68, 'Arxiv'): 'arXiv'}
WORDS = [[a, b, FIX.get((round(a, 2), w), w)] for a, b, w in WORDS]
for w in WORDS:
    if w[2] == 'arXiv': w[0] = 28.40

FREEZE, SH = 5.35, 1.14   # visual time held at 5.35 s for 1.14 s of real time
def real(tv): return tv if tv < FREEZE else tv + SH
def vis(tr): return tr if tr < FREEZE else (FREEZE if tr < FREEZE + SH else tr - SH)
# id, source in, source out (cut in silence, from the energy islands), film start, caption text
LINES = [
    ('L1a', 0.00, 1.55, 0.35, 'Your study is done.'),
    ('L1b', 1.85, 4.15, 2.05, 'One result becomes a sentence.'),
    ('L2', 0.00, 6.95, 6.00, 'ArxivChecker, a skill for your AI assistant, starts with the evidence, not the old draft’s numbers.', 'v3'),
    ('L3', 9.05, 13.98, 13.14, 'It traces the claim to its source, and adds the comparison and what’s left out.'),
    ('L4', 14.20, 19.75, 22.84, 'Figures come straight from the data. If a result goes missing, the build stops.'),
    ('L5', 20.05, 24.45, 31.24, 'The paper tells the story in order, from the problem to its limits.'),
    ('L6a', 24.65, 28.05, 36.04, 'It sets the paper in LaTeX, and sorts the rules.'),
    ('L6b', 28.30, 31.40, 39.59, 'arXiv asks for margins of at least an inch.'),
    ('L6c', 10.75, 13.85, 42.89, 'arXiv advises a description for every figure.', 'v3'),
    ('L6d', 14.20, 16.95, 46.14, 'And your house style leaves off the page numbers.', 'v3'),
    ('L7', 37.25, 42.35, 49.04, 'Then it rebuilds the paper in an empty folder, from only the files you’ll send.'),
    ('L8', 42.50, 48.00, 55.04, 'You decide the names, how AI was used, the license and the final claims.'),
]
vo = []
for i, (lid, a, b, start, cap, *src) in enumerate(LINES):
    SRCW = W3 if src else WORDS
    ws = [[round(x - a, 3), round(y - a, 3), w] for x, y, w in SRCW if a <= x < b]
    if i:  # no overlap with the previous line
        p = vo[-1]; assert start >= p['start'] + (p['out'] - p['in']) + 0.15 - 1e-6, (lid, start)
    vo.append({'id': lid, 'src': 'audio/v3/w1.mp3' if src else 'audio/v2/u2.mp3', 'in': a, 'out': b, 'start': start, 'text': cap, 'words': ws})

def at(lid, word, nth=0):
    v = next(x for x in vo if x['id'] == lid)
    hits = [w for w in v['words'] if w[2].lower().strip('.,!’\'').startswith(word.lower())]
    return round(vis(v['start'] + hits[nth][0]), 3)

DUR = round(70.0 + SH, 3)
# m4 is 117.45 BPM; pulse enters on its downbeat 8.034 s. Put that on "evidence".
evid = at('L2', 'evidence'); evidR = real(evid); off = round(evidR - 8.034, 3)
stops = at('L4', 'stops')
music = {
    'src': 'audio/score/m4.wav', 'offset': off,
    # film a, film b, source start
    'segments': [[0.0, 4.6, 0.0], [evidR, DUR, 8.034]],
    'stops': [[round(real(stops) + 0.18, 3), round(28.026 + off, 3)]],   # drop out on "stops", back on the next downbeat
    'fades': [[4.45, 4.6]],
    'final_chord': round(63.8 + off, 3), 'final_chord_vis': round(vis(63.8 + off), 3),
}
T = {'name_real': 6.0, 'L1b_sentence': at('L1b', 'sentence'), 'evidence': evid, 'source': at('L3', 'source'), 'comparison': at('L3', 'comparison'),
     'left': at('L3', 'left'), 'data': at('L4', 'data'), 'missing': at('L4', 'missing'), 'stops': stops,
     'order': at('L5', 'order'), 'problem': at('L5', 'problem'), 'limits': at('L5', 'limits'), 'latex': at('L6a', 'latex'),
     'sorts': at('L6a', 'sorts'), 'asks': at('L6b', 'asks'), 'margins': at('L6b', 'margins'), 'inch': at('L6b', 'inch'),
     'advises': at('L6c', 'advises'), 'figure': at('L6c', 'figure'), 'house': at('L6d', 'house'), 'numbers': at('L6d', 'numbers'),
     'rebuilds': at('L7', 'rebuilds'), 'empty': at('L7', 'empty'), 'files': at('L7', 'files'), 'send': at('L7', 'send'),
     'decide': at('L8', 'decide'), 'names': at('L8', 'names'), 'ai': at('L8', 'ai'), 'license': at('L8', 'license'),
     'claims': at('L8', 'claims')}
SC = {'s1': 0.0, 's2': 7.2, 's3': 11.8, 's4': 21.5, 's5': 30.55, 's6': 34.7, 's7': 47.7, 's8': 53.6, 's9': 61.9,
      's10': 64.4, 'end': DUR}
edit = {'duration': DUR, 'vo': vo, 'music': music, 'T': T, 'SC': SC, 'sfx': [], 'copy': {}, 'freeze': [FREEZE, SH]}
old = ROOT / 'edit/edit.json'
if old.exists():
    prev = json.loads(old.read_text()); edit['copy'] = prev.get('copy', {})
old.write_text(json.dumps(edit, indent=1))
print('evidence', evid, 'offset', off, 'stops', stops, 'chord', music['final_chord'])
for v in vo: print(f"{v['id']:4} {v['start']:6.2f}-{v['start'] + v['out'] - v['in']:6.2f}  {v['text']}")
print({k: v for k, v in T.items()})
