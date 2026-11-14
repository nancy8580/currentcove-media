"""Elegy: slow solo cello over sparse piano, minor key, no percussion, no noise.
Usage: python3 gen_elegy.py <seconds> <out.wav> <seed-text>   (each seed = different melody/key)"""
import sys, hashlib, wave, json
import numpy as np
secs, outp, seedtxt = float(sys.argv[1]), sys.argv[2], sys.argv[3]
rng = np.random.default_rng(int(hashlib.md5(seedtxt.encode()).hexdigest()[:8], 16))
SR = 44100; N = int(secs * SR); t_all = np.arange(N) / SR
key = int(rng.choice([45, 47, 48, 50, 52]))          # A2, B2, C3, D3, E3 (natural minor)
MINOR = [0, 2, 3, 5, 7, 8, 10]
progs = [[0, 5, 3, 4], [0, 3, 5, 4], [0, 5, 2, 4], [0, 6, 5, 4]]
prog = progs[int(rng.integers(len(progs)))]
bpm = float(rng.uniform(52, 60)); beat = 60 / bpm; bar = beat * 4
f = lambda m: 440 * 2 ** ((m - 69) / 12)
def deg(d, octave=0):  # scale degree -> midi
    return key + 12 * (octave + d // 7) + MINOR[d % 7]
out = np.zeros(N)

def piano(m, start, dur, vel):
    i0 = int(start * SR); n = min(int((dur + 2.5) * SR), N - i0)
    if n <= 0: return
    t = np.arange(n) / SR; fr = f(m); s = np.zeros(n)
    for k in range(1, 7):
        fk = fr * k * (1 + 0.0004 * k * k)
        s += np.sin(2 * np.pi * fk * t) * (0.6 ** (k - 1)) * np.exp(-t * (1.2 + 0.9 * k))
    s *= np.minimum(1, t / 0.004) * vel
    out[i0:i0 + n] += s

def cello(m, start, dur, vel):
    i0 = int(start * SR); n = min(int((dur + 0.6) * SR), N - i0)
    if n <= 0: return
    t = np.arange(n) / SR; fr = f(m)
    vib = 1 + 0.0045 * np.sin(2 * np.pi * 5.2 * t) * np.minimum(1, t / 0.8)
    ph = 2 * np.pi * fr * np.cumsum(vib) / SR
    s = sum(np.sin(k * ph) / k ** 1.25 * (1 if k < 4 else .6) for k in range(1, 9))
    env = np.minimum(1, t / 0.45) * np.clip((dur + 0.6 - t) / 0.6, 0, 1)
    env *= 1 + 0.15 * np.sin(np.pi * np.clip(t / max(dur, .1), 0, 1))     # swell inside the bow
    out[i0:i0 + n] += s * env * vel

# structure: 2 bars piano alone, then cello enters; last bar resolves to tonic
nbars = int(secs / bar) + 1
mel = 4  # start on 5th degree
for b in range(nbars):
    t0 = b * bar; root = prog[b % 4]
    if t0 > secs - 1: break
    # piano: low root + slow broken chord
    piano(deg(root, -1), t0, bar, .32)
    for j, d in enumerate([root, root + 2, root + 4, root + 2]):
        if rng.random() < .85: piano(deg(d, 1), t0 + j * beat + rng.uniform(0, .03), beat, .16 + .04 * rng.random())
    # cello melody from bar 2: long notes (1–2 beats), stepwise
    if b >= 2 and t0 < secs - bar:
        pos = 0.0
        while pos < 4 - 1e-6:
            L = float(rng.choice([1, 2, 2, 3])); L = min(L, 4 - pos)
            chord = {root % 7, (root + 2) % 7, (root + 4) % 7}
            step = int(rng.choice([-2, -1, -1, 0, 1, 1, 2]))
            mel = int(np.clip(mel + step, 0, 9))
            if pos == 0 and mel % 7 not in chord: mel = min(chord, key=lambda c: abs(c - mel % 7)) + 7 * (mel // 7)
            cello(deg(mel, 1) - 12, t0 + pos * beat, L * beat * .98, .085)
            pos += L
# simple reverb: decaying multi-tap echoes (no noise)
rev = np.zeros(N)
for d, g in [(.031, .35), (.047, .3), (.071, .26), (.113, .22), (.167, .18), (.241, .14), (.353, .1), (.509, .07)]:
    k = int(d * SR); rev[k:] += out[:-k] * g
mix = out + rev * .8
fi, fo = int(2.5 * SR), int(3 * SR)
mix[:fi] *= np.linspace(0, 1, fi); mix[-fo:] *= np.linspace(1, 0, fo)
mix = np.tanh(mix / (np.abs(mix).max() + 1e-9) * 1.2) * .9
st = np.stack([mix, np.roll(mix, int(.012 * SR)) * .97], 1)
with wave.open(outp, "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print(json.dumps({"engine": "elegy", "seed": seedtxt, "key_midi": key, "prog": prog, "bpm": round(bpm, 1)}))
