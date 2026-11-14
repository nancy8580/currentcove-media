"""Dread score: dissonant low drone + heartbeat + creepy music-box motif + eerie high tones. No noise.
Usage: python3 gen_dread.py <seconds> <out.wav> <seed-text> [comma-separated boom times]"""
import sys, hashlib, wave, json, os
NO_HEART = os.environ.get('NO_HEART') == '1'; NO_BELL = os.environ.get('NO_BELL') == '1'
import numpy as np
secs, outp, seedtxt = float(sys.argv[1]), sys.argv[2], sys.argv[3]
booms = [float(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 and sys.argv[4] else []
rng = np.random.default_rng(int(hashlib.md5(seedtxt.encode()).hexdigest()[:8], 16))
SR = 44100; N = int(secs * SR); t = np.arange(N) / SR
f = lambda m: 440 * 2 ** ((m - 69) / 12)
key = int(rng.choice([38, 39, 40, 41]))           # D2..F2
out = np.zeros(N)
arc = np.clip(t / (secs * .85), 0, 1)              # tension rises over the piece
# 1) low dissonant drone: root + minor 2nd, harmonic-rich, slow swell
for m, g in [(key, .5), (key + 1, .32), (key + 12, .22), (key + 18, .12)]:   # + tritone above
    fr = f(m) * (1 + .002 * np.sin(2 * np.pi * .05 * t + rng.random() * 6))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    s = sum(np.sin(k * ph) / k ** 1.5 for k in range(1, 10))
    out += s * g * (.55 + .45 * np.sin(2 * np.pi * t / 17 + rng.random() * 6) ** 2) * (.6 + .4 * arc)
out *= .22
# 2) heartbeat: lub-dub, slowly quickening (tonal thumps with audible overtone)
def thump(at, g):
    n = int(.35 * SR); i0 = int(at * SR)
    if i0 >= N: return
    n = min(n, N - i0); tt = np.arange(n) / SR
    fr = 70 * np.exp(-tt * 6) + 42
    ph = 2 * np.pi * np.cumsum(fr) / SR
    out[i0:i0 + n] += (np.sin(ph) + .45 * np.sin(2 * ph) + .2 * np.sin(3 * ph)) * np.exp(-tt * 11) * g
hb = 3.0
while hb < secs - 2 and not NO_HEART:
    k = hb / secs; thump(hb, .55); thump(hb + .28, .38); hb += 1.35 - .45 * k
# 3) music-box motif: high, thin, slightly out of tune, minor/chromatic, sparse
motif = [0, 3, 7, 6, 3, 2, 0, -1]
def bell(m, at, g):
    n = int(2.2 * SR); i0 = int(at * SR)
    if i0 >= N: return
    n = min(n, N - i0); tt = np.arange(n) / SR; fr = f(m) * (1 + .006 * rng.standard_normal())
    s = np.sin(2 * np.pi * fr * tt) + .35 * np.sin(2 * np.pi * fr * 2.76 * tt) * np.exp(-tt * 6) + .2 * np.sin(2 * np.pi * fr * 5.4 * tt) * np.exp(-tt * 9)
    out[i0:i0 + n] += s * np.exp(-tt * 2.6) * np.minimum(1, tt / .003) * g
step = .42; at = 6.0
while at < secs - 6 and not NO_BELL:
    for j, d in enumerate(motif):
        bell(key + 48 + d, at + j * step * (1 + .05 * rng.standard_normal()), .07 + .03 * rng.random())
    at += len(motif) * step + float(rng.uniform(5, 9))
# 4) eerie high glass tone: slow bends, fades in and out
for _ in range(int(secs / 14)):
    st = float(rng.uniform(4, secs - 8)); d = float(rng.uniform(5, 9)); i0 = int(st * SR); n = min(int(d * SR), N - i0)
    tt = np.arange(n) / SR; m0 = key + 50 + int(rng.choice([0, 1, 6, 7]))
    fr = f(m0) * 2 ** ((np.sin(2 * np.pi * tt / d) * .5) / 12) * (1 + .004 * np.sin(2 * np.pi * 4.5 * tt))
    out[i0:i0 + n] += np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * tt / d) ** 2 * .05
# 5) low hits (scene markers)
for b in booms:
    i0 = int(b * SR); n = min(int(3 * SR), N - i0)
    if n <= 0: continue
    tt = np.arange(n) / SR; fr = f(key) * (1 - .25 * tt / 3)
    ph = 2 * np.pi * np.cumsum(fr) / SR
    out[i0:i0 + n] += sum(np.sin(k * ph) / k for k in range(1, 7)) * np.exp(-tt * 1.6) * .35
# reverb (multi-tap, no noise), fades, normalise
rev = np.zeros(N)
for d, g in [(.043, .32), (.067, .28), (.109, .22), (.163, .18), (.251, .13), (.383, .09), (.577, .06)]:
    k = int(d * SR); rev[k:] += out[:-k] * g
mix = out + .7 * rev
fi, fo = int(1.5 * SR), int(2.5 * SR); mix[:fi] *= np.linspace(0, 1, fi); mix[-fo:] *= np.linspace(1, 0, fo)
mix = np.tanh(mix / (np.abs(mix).max() + 1e-9) * 1.4) * .9
st = np.stack([mix, np.roll(mix, int(.015 * SR)) * .96], 1)
with wave.open(outp, "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print(json.dumps({"engine": "dread", "seed": seedtxt, "key_midi": key}))
