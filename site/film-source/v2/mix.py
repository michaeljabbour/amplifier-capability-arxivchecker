#!/usr/bin/env python3
"""Mix voice, score and effects from edit/edit.json into stems and a mastered WAV (Sizzle 5.4, 7.2)."""
import json, subprocess, sys
from pathlib import Path
import numpy as np, librosa, soundfile as sf, pyloudnorm as pyln
from scipy.signal import butter, sosfilt, sosfiltfilt

ROOT = Path(__file__).resolve().parent
SR = 48000
E = json.loads((ROOT / 'edit/edit.json').read_text())
N = int(E['duration'] * SR)
OUT = ROOT / 'out' / (sys.argv[1] if len(sys.argv) > 1 else 'v1')
(OUT / 'stems').mkdir(parents=True, exist_ok=True)
meter = pyln.Meter(SR)

def load(path, mono=True):
    y, _ = librosa.load(ROOT / path, sr=SR, mono=mono)
    return y.astype(np.float64)
def fade(y, fin=0.008, fout=0.035):
    a, b = int(fin * SR), int(fout * SR)
    y = y.copy(); y[:a] *= np.linspace(0, 1, a); y[len(y) - b:] *= np.linspace(1, 0, b); return y
def place(bus, y, t):
    i = int(round(t * SR)); j = min(bus.shape[-1], i + y.shape[-1])
    if j > i: bus[..., i:j] += y[..., :j - i]

# ---------- voice: light compression, each line to -18 LUFS ----------
vo = np.zeros(N)
hp = butter(2, 70, 'hp', fs=SR, output='sos')
for line in E['vo']:
    y = load(line['src'])[int(line['in'] * SR):int(line['out'] * SR)]
    y = sosfilt(hp, y)
    env = np.sqrt(np.convolve(y ** 2, np.ones(480) / 480, 'same')) + 1e-9
    lvl = 20 * np.log10(env); over = np.maximum(0, lvl - (-26)); gain = 10 ** (-(over * (1 - 1 / 3)) / 20)
    y = y * gain
    y = y * 10 ** ((-18 - meter.integrated_loudness(np.pad(y, (0, SR)))) / 20)
    place(vo, fade(y), line['start'])

# ---------- score: segments, muffle, stops, ducking ----------
M = E['music']
s = load(M['src'], mono=False)
mus = np.zeros((2, N)); xf = int(0.025 * SR)
for a, b, src in M['segments']:
    piece = s[:, int(src * SR):int((src + b - a) * SR)].copy()
    f = min(int(0.025 * SR), piece.shape[1] // 2)
    piece[:, :f] *= np.linspace(0, 1, f) ** 0.5
    place(mus, piece, a)
for a, b in M.get('fades', []):
    i, j = int(a * SR), int(b * SR); mus[:, i:j] *= np.linspace(1, 0, j - i) ** 2; mus[:, j:int(M['segments'][1][0] * SR)] = 0
for a, b in M['stops']:
    i, j, f = int(a * SR), int(b * SR), int(0.012 * SR)
    mus[:, i:j] = 0; mus[:, i - f:i] *= np.linspace(1, 0, f); mus[:, j:j + f] *= np.linspace(0, 1, f)
# duck under the voice: 120 ms look-ahead attack, 450 ms release
venv = np.convolve(np.abs(vo), np.ones(int(0.03 * SR)) / int(0.03 * SR), 'same') > 10 ** (-40 / 20)
look = int(0.12 * SR); act = np.convolve(venv.astype(float), np.ones(look), 'full')[look - 1:look - 1 + N] > 0
duck = np.where(act, 10 ** (-10 / 20), 1.0)
rel = np.exp(-1 / (0.45 * SR)); att = np.exp(-1 / (0.06 * SR)); g = np.ones(N); cur = 1.0
for k in range(N):
    tgt = duck[k]; c = att if tgt < cur else rel; cur = tgt + (cur - tgt) * c; g[k] = cur
mus *= g

# ---------- effects ----------
fx = np.zeros(N)
def synth(name):
    t = np.arange(int(0.25 * SR)) / SR
    if name == 'tick': return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 60) * 0.5, 0.0
    if name == 'snap':
        rng = np.random.default_rng(5); n = rng.standard_normal(len(t)) * np.exp(-t * 45)
        return sosfilt(butter(2, [1500, 6000], 'bp', fs=SR, output='sos'), n) * 1.2, 0.0
    if name == 'impact':
        t = np.arange(int(1.6 * SR)) / SR
        sub = np.sin(2 * np.pi * np.cumsum(np.linspace(62, 34, len(t))) / SR) * np.exp(-t * 2.4)
        return sub * 0.9, 0.0
    if name == 'riser':
        t = np.arange(int(2.0 * SR)) / SR; rng = np.random.default_rng(9)
        n = sosfilt(butter(2, 1200, 'hp', fs=SR, output='sos'), rng.standard_normal(len(t)))
        return n * (t / 2.0) ** 2.5 * 0.35, 0.0
    return None, 0
for name, t0, gain in E['sfx']:
    y, peak = synth(name)
    if y is None:
        y = load(f'audio/sfx/{name}.mp3'); peak = int(np.argmax(np.abs(y))) / SR
        y = y / (np.max(np.abs(y)) + 1e-9) * 0.5
    start = t0 - peak if name not in ('riser',) else t0
    place(fx, fade(y * gain, 0.002, 0.05), max(0, start))
# ---------- stems, sum, limiter, loudness ----------
mus *= 1.1; fx *= 0.8
sf.write(OUT / 'stems/voice.wav', vo, SR, subtype='FLOAT')
sf.write(OUT / 'stems/music.wav', mus.T, SR, subtype='FLOAT')
sf.write(OUT / 'stems/fx.wav', fx, SR, subtype='FLOAT')
mix = mus + np.vstack([vo, vo]) + np.vstack([fx, fx])
mix = mix * 10 ** ((-16.6 - meter.integrated_loudness(mix.T)) / 20)
ceil = 10 ** (-5.0 / 20)
from scipy.ndimage import maximum_filter1d, uniform_filter1d
pk = maximum_filter1d(np.max(np.abs(mix), axis=0), size=int(0.010 * SR))   # 5 ms look-ahead and hold either side
need = np.minimum(1, ceil / (pk + 1e-9))
gmin = uniform_filter1d(maximum_filter1d(-need, size=int(0.010 * SR)) * -1, size=int(0.004 * SR))  # smooth, never above need's local min
gmin = np.minimum(gmin, need)
mix = mix * gmin
pre = OUT / 'stems/premaster.wav'; sf.write(pre, mix.T, SR, subtype='FLOAT')
# two-pass loudnorm to -16 LUFS, TP -1
p1 = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(pre), '-af', 'loudnorm=I=-16:TP=-1:LRA=30:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
js = json.loads(p1[p1.rindex('{'):p1.rindex('}') + 1])
af = f"loudnorm=I=-16:TP=-1:LRA=30:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true:print_format=json"
p2 = subprocess.run(['ffmpeg', '-hide_banner', '-y', '-i', str(pre), '-af', af, '-ar', str(SR), '-c:a', 'pcm_f32le', str(OUT / 'mix.wav')], capture_output=True, text=True).stderr
j2 = json.loads(p2[p2.rindex('{'):p2.rindex('}') + 1])
print('mix:', OUT / 'mix.wav', 'output I', j2['output_i'], 'TP', j2['output_tp'], 'type', j2['normalization_type'])
