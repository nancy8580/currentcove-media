"""Slow, smooth storytelling bed — a NEW original piece every run.
Usage: python3 gen_story.py <mood: dark|warm|reflective|wonder> <seconds> <out.wav> <unique-seed-text>
The seed text (e.g. "2026-11-09-reel2-nvidia") picks key, chord progression, piano pattern, melody and sounds,
so every Reel gets a different track. One chord per slide (5.9 s) = slow, cinematic changes that line up with cuts."""
import numpy as np, wave, sys, subprocess, os, hashlib, json
SR = 44100; PH = 5.9; beat = PH / 8          # 8 slow beats per slide (~81 BPM felt as half-time)
mood, secs, outp, seedtxt = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
seed = int(hashlib.sha256(seedtxt.encode()).hexdigest()[:12], 16)
R = np.random.default_rng(seed)
n2f = lambda n: 440 * 2 ** ((n - 69) / 12)
SCALES = {"minor": [0, 2, 3, 5, 7, 8, 10], "major": [0, 2, 4, 5, 7, 9, 11], "dorian": [0, 2, 3, 5, 7, 9, 10], "lydian": [0, 2, 4, 6, 7, 9, 11]}
MODE = {"dark": ["minor", "dorian"], "warm": ["major"], "reflective": ["minor", "dorian", "major"], "wonder": ["lydian", "major"]}[mood]
PROGS = {  # scale-degree progressions (0-based), one chord per slide
 "minor": [[0, 5, 2, 6], [0, 3, 5, 4], [0, 5, 3, 4], [5, 3, 0, 6], [0, 2, 5, 4], [0, 6, 5, 6]],
 "dorian": [[0, 3, 0, 6], [0, 1, 3, 0], [0, 6, 3, 4], [0, 3, 6, 4]],
 "major": [[0, 4, 5, 3], [5, 3, 0, 4], [0, 5, 3, 4], [3, 0, 4, 5], [0, 2, 5, 3], [3, 4, 2, 5]],
 "lydian": [[0, 1, 0, 6], [0, 1, 4, 5], [3, 1, 0, 4]],
}
mode = R.choice(MODE); sc = SCALES[mode]; prog = PROGS[mode][R.integers(len(PROGS[mode]))]
root = 48 + int(R.integers(0, 12))           # random key
if root > 54: root -= 12
def deg(d, octv=0):
    o, i = divmod(d, 7); return root + 12 * (o + octv) + sc[i]
def chord(d, extra=False):
    c = [deg(d), deg(d + 2), deg(d + 4)]
    if extra: c.append(deg(d + 6))            # add 7th for colour
    return c
# --- per-track "sound design" choices ---
bright = R.uniform(0.15, 0.45)               # piano brightness
pad_kind = R.choice(["strings", "choir", "glass"])
lead_kind = R.choice(["piano", "bell", "flute"])
arp_pat = [list(R.permutation([0, 1, 2, 1, 2, 0, 3, 2])) for _ in range(2)]
use7 = R.random() < 0.6
L = int(secs * SR); out = np.zeros((L + SR * 6, 2))
def add(sig, t0, g=1.0, pan=0.0):
    i = int(t0 * SR); j = min(i + len(sig), len(out))
    if i >= len(out): return
    l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
    out[i:j, 0] += g * l * sig[: j - i]; out[i:j, 1] += g * r * sig[: j - i]
T = lambda d: np.arange(int(d * SR)) / SR
def env(n, a, r):
    e = np.ones(n); A = max(1, int(a * SR)); Rr = max(1, int(r * SR)); e[:A] = np.linspace(0, 1, A) ** 2; e[-Rr:] *= np.linspace(1, 0, Rr) ** 1.5; return e
def piano(f, d=3.0, vel=1.0):
    t = T(d); s = np.zeros_like(t)
    for k in range(1, 7):
        s += (bright ** (k - 1)) * np.sin(2 * np.pi * f * k * (1 + 0.0004 * k * k) * t) * np.exp(-t * (1.2 + 0.9 * k))
    s += 0.15 * np.sin(2 * np.pi * f * t) * np.exp(-t * 0.6)
    return vel * s * env(len(t), 0.004, 0.8)
def bell(f, d=3.0, vel=1.0):
    t = T(d); return vel * (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2.0 * f * t) * np.exp(-t * 3)) * np.exp(-t * 1.6) * env(len(t), .01, .6)
def flute(f, d=1.6, vel=1.0):
    t = T(d); vib = 1 + 0.004 * np.sin(2 * np.pi * 5 * t) * np.clip(t / 0.4, 0, 1)
    s = np.sin(2 * np.pi * f * np.cumsum(vib) / SR) + 0.12 * np.sin(4 * np.pi * f * t)
    return vel * s * env(len(t), 0.18, 0.5)
LEAD = {"piano": piano, "bell": bell, "flute": flute}[lead_kind]
def pad(ch, d):
    t = T(d); s = np.zeros_like(t)
    for m in ch:
        f = n2f(m + 12)
        for dt in (-0.003, 0.0, 0.003):
            if pad_kind == "strings": s += sum(np.sin(2 * np.pi * f * (1 + dt) * k * t) / k ** 1.6 for k in range(1, 6))
            elif pad_kind == "choir": s += np.sin(2 * np.pi * f * (1 + dt) * t) + 0.3 * np.sin(2 * np.pi * 2 * f * (1 + dt) * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t)
            else: s += np.sin(2 * np.pi * f * (1 + dt) * t) + 0.2 * np.sin(2 * np.pi * 4 * f * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t))
    s *= 0.5 + 0.5 * np.sin(2 * np.pi * (0.08 + R.uniform(0, .05)) * t + R.uniform(0, 6))   # slow breathing
    return s * env(len(t), 1.8, 2.0) / (len(ch) * 3)
def sub(f, d):
    t = T(d); return np.sin(2 * np.pi * f * t) * env(len(t), 0.25, 1.2)
def swell(d=1.6):  # soft airy rise into the next slide
    t = T(d); n = R.standard_normal(len(t)); k = 40; n = np.convolve(n, np.ones(k) / k, "same")
    return n * (t / d) ** 3 * np.exp(-((t - d) * 8) ** 2 * 0) * 0.6
nphr = int(np.ceil(secs / PH)) + 1
mel_note = 4                                   # melody random-walk position (scale degree)
for p in range(nphr):
    t0 = p * PH; d = prog[p % 4]; ch = chord(d, use7)
    add(pad(ch, PH + 2.5), t0, 0.55, R.uniform(-.3, .3))
    add(sub(n2f(deg(d, -1)), PH + 0.5), t0, 0.22)
    # piano: low root on the downbeat, then a slow broken chord (quarter notes)
    add(piano(n2f(deg(d, -1)), 4.0, 0.9), t0, 0.16, -0.2)
    if p >= 1 or mood != "dark":
        pat = arp_pat[p % 2]
        for s in range(8):
            if R.random() < 0.18: continue    # breathe: leave gaps
            note = (ch + [ch[0] + 12])[pat[s] % (len(ch) + 1)]
            add(piano(n2f(note + 12), 2.6, R.uniform(.55, .9)), t0 + s * beat + R.uniform(0, .02), 0.075, R.uniform(-.5, .5))
    # melody from slide 3: sparse, singable, follows the chord
    if p >= 2 and p < nphr - 1:
        slots = sorted(R.choice(8, size=int(R.integers(2, 5)), replace=False))
        for s in slots:
            mel_note += int(R.choice([-2, -1, -1, 0, 1, 1, 2]))
            mel_note = int(np.clip(mel_note, 2, 9))
            if R.random() < 0.5:                # snap to a chord tone half the time
                mel_note = min([d, d + 2, d + 4, d + 7], key=lambda x: abs(x - mel_note))
            add(LEAD(n2f(deg(mel_note, 1)), 2.4), t0 + s * beat, 0.10, R.uniform(-.25, .25))
    if p >= 1 and not os.environ.get("NO_SWELL"): add(swell(), t0 - 1.6, 0.05)
out = out[:L]
# --- simple stereo reverb (decaying-noise impulse) for a smooth, cinematic space ---
ir_len = int(2.8 * SR); ti = np.arange(ir_len) / SR
for c in range(2):
    ir = R.standard_normal(ir_len) * np.exp(-ti * 2.2); ir[0] = 0; ir /= np.sqrt(np.sum(ir ** 2))
    n = 1 << int(np.ceil(np.log2(L + ir_len)))
    wet = np.fft.irfft(np.fft.rfft(out[:, c], n) * np.fft.rfft(ir, n), n)[:L]
    out[:, c] = 0.72 * out[:, c] + 0.38 * wet
fi, fo = int(1.2 * SR), int(3.5 * SR); out[:fi] *= np.linspace(0, 1, fi)[:, None]; out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
out = np.tanh(out * 1.2); out /= np.abs(out).max() * 1.05
raw = outp + ".raw.wav"
with wave.open(raw, "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
    "lowpass=f=9500,highpass=f=35,loudnorm=I=-16:TP=-1.5", "-ar", "48000", outp], check=True)
os.remove(raw)
sig = {"seed": seedtxt, "mode": str(mode), "key_midi": root, "prog": [int(x) for x in prog], "pad": str(pad_kind), "lead": str(lead_kind)}
print(json.dumps(sig))
