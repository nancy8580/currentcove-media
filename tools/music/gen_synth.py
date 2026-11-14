"""Smooth modern synth track for tech Reels: warm pumping pads, plucky delayed arpeggio, round bass, soft kick, bell lead.
No noise sources at all (no hiss). Unique per seed text.
Usage: python3 gen_synth.py <seconds> <out.wav> "<seed text>"   -> prints a JSON signature"""
import numpy as np, wave, sys, subprocess, os, hashlib, json
SR = 44100
secs, outp, seedtxt = float(sys.argv[1]), sys.argv[2], sys.argv[3]
R = np.random.default_rng(int(hashlib.sha256(seedtxt.encode()).hexdigest()[:12], 16))
BPM = float(R.choice([96, 100, 104])); beat = 60 / BPM; bar = 4 * beat
n2f = lambda m: 440 * 2 ** ((m - 69) / 12)
MODES = {"major": [0, 2, 4, 5, 7, 9, 11], "lydian": [0, 2, 4, 6, 7, 9, 11], "dorian": [0, 2, 3, 5, 7, 9, 10]}
mode = str(R.choice(["major", "lydian", "major", "dorian"])); sc = MODES[mode]
PROGS = [[0, 4, 5, 3], [5, 3, 0, 4], [0, 5, 3, 4], [3, 4, 5, 0], [0, 2, 3, 4], [5, 4, 3, 4]]
prog = PROGS[int(R.integers(len(PROGS)))]; root = 45 + int(R.integers(0, 10))
deg = lambda d, o=0: root + 12 * (d // 7 + o) + sc[d % 7]
L = int(secs * SR); out = np.zeros((L + SR * 4, 2))
def add(sig, t0, g=1., pan=0.):
    i = int(t0 * SR)
    if i >= len(out): return
    j = min(i + len(sig), len(out)); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan))
    out[i:j, 0] += g * l * sig[:j - i]; out[i:j, 1] += g * r * sig[:j - i]
T = lambda d: np.arange(int(d * SR)) / SR
def adsr(n, a, r):
    e = np.ones(n); A = max(1, int(a * SR)); Rr = max(1, int(r * SR)); e[:A] = np.linspace(0, 1, A); e[-Rr:] *= np.linspace(1, 0, Rr); return e
def saw(f, t, nh=10, tilt=1.4, det=(-.004, .0, .004)):
    s = np.zeros_like(t)
    for dd in det:
        for k in range(1, nh + 1): s += np.sin(2 * np.pi * f * (1 + dd) * k * t + k) / k ** tilt
    return s / len(det)
def pluck(f, d=.5):
    t = T(d); s = sum(np.sin(2 * np.pi * f * k * t) * np.exp(-t * (6 + 5 * k)) / k for k in range(1, 6)); return s * adsr(len(t), .003, .05)
def bell(f, d=1.8):
    t = T(d); return (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 5) + .2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 9)) * np.exp(-t * 2.2) * adsr(len(t), .004, .2)
def kick():
    t = T(.45); f = 52 + 70 * np.exp(-t * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * adsr(len(t), .001, .05)
def tick():
    t = T(.06); return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 90) * .5 + np.sin(2 * np.pi * 3600 * t) * np.exp(-t * 120) * .3
nb = int(np.ceil(secs / bar)) + 1
pump = np.ones(L + SR * 4)                       # sidechain envelope for the pad
arp_pat = [list(R.permutation([0, 1, 2, 3, 2, 1, 0, 2])) for _ in range(2)]
lead_on = int(R.integers(3, 5)); mel = int(R.integers(2, 6))
for b in range(nb):
    t0 = b * bar; d = prog[b % 4]; ch = [deg(d), deg(d + 2), deg(d + 4), deg(d + 6)]
    intro = b == 0
    # pad
    t = T(bar + .6); pad = sum(saw(n2f(m + 12), t, 8, 1.6) for m in ch[:3]) / 3
    add(pad * adsr(len(t), .25, .5), t0, .16 if not intro else .12, 0)
    # bass (8th pulse, round)
    if not intro:
        for k in range(8):
            tb = T(beat * .45); f = n2f(deg(d, -1)); bs = (np.sin(2 * np.pi * f * tb) + .25 * np.sin(4 * np.pi * f * tb)) * adsr(len(tb), .005, .08)
            add(bs, t0 + k * beat / 2, .30 if k % 2 == 0 else .2)
    # arp with dotted-8th echo
    pat = arp_pat[b % 2]
    for k in range(8):
        m = ch[pat[k] % 4] + 24; ts = t0 + k * beat / 2; p = (k % 2) * .4 - .2
        add(pluck(n2f(m)), ts, .11, p); add(pluck(n2f(m)), ts + beat * .75, .045, -p); add(pluck(n2f(m)), ts + beat * 1.5, .02, p)
    # drums: soft kick + tonal ticks (no noise)
    if not intro:
        for k in range(4):
            add(kick(), t0 + k * beat, .55); i0 = int((t0 + k * beat) * SR); n = int(.22 * SR)
            pump[i0:i0 + n] = np.minimum(pump[i0:i0 + n], .45 + .55 * np.linspace(0, 1, n) ** .6)
            add(tick(), t0 + k * beat + beat / 2, .10, .3)
    # bell lead melody
    if b >= lead_on and b < nb - 1:
        for k in sorted(R.choice(8, size=int(R.integers(3, 6)), replace=False)):
            mel = int(np.clip(mel + R.choice([-2, -1, 1, 1, 2, 0]), 1, 9))
            if R.random() < .5: mel = min([d, d + 2, d + 4, d + 7], key=lambda x: abs(x - mel))
            add(bell(n2f(deg(mel, 2))), t0 + k * beat / 2, .07, R.uniform(-.3, .3))
out[:, 0] *= pump[:len(out)] ** .5; out[:, 1] *= pump[:len(out)] ** .5
out = out[:L]
# short room reverb (decaying sine-sum impulse, not noise)
irl = int(1.2 * SR); ti = np.arange(irl) / SR
ir = sum(np.sin(2 * np.pi * f * ti + R.uniform(0, 6)) for f in R.uniform(300, 3000, 40)) * np.exp(-ti * 4.5); ir /= np.sqrt((ir ** 2).sum())
for c in range(2):
    n = 1 << int(np.ceil(np.log2(L + irl))); wet = np.fft.irfft(np.fft.rfft(out[:, c], n) * np.fft.rfft(np.roll(ir, c * 37), n), n)[:L]
    out[:, c] = .8 * out[:, c] + .25 * wet
fi, fo = int(.6 * SR), int(2.5 * SR); out[:fi] *= np.linspace(0, 1, fi)[:, None]; out[-fo:] *= np.linspace(1, 0, fo)[:, None]
out = np.tanh(out * 1.3); out /= np.abs(out).max() * 1.05
raw = outp + ".raw.wav"
with wave.open(raw, "w") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", "highpass=f=30,lowpass=f=12000,loudnorm=I=-14:TP=-1", "-ar", "48000", outp], check=True); os.remove(raw)
print(json.dumps({"seed": seedtxt, "style": "synth", "bpm": BPM, "mode": mode, "root": root, "prog": prog}))
