import numpy as np, wave, json
SR=48000; tj=json.load(open('vo/timing.json')); T=tj['TOTAL']; S={s[0]:s[1] for s in tj['SC']}
out=np.zeros(int((T+1)*SR)); rng=np.random.default_rng(1116)
def add(sig,t,g):
    i=int(t*SR); j=min(len(out),i+len(sig)); out[i:j]+=g*sig[:j-i]
def whoosh(d=.45):
    n=int(d*SR); x=rng.standard_normal(n); t=np.arange(n)/SR; y=np.zeros(n); a=0
    for k in range(n):
        c=.02+.25*np.sin(np.pi*k/n); a+=c*(x[k]-a); y[k]=a
    return y*np.sin(np.pi*t/d)**2
def pop(f=900): t=np.arange(int(.12*SR))/SR; return np.sin(2*np.pi*f*t*(1+2*np.exp(-t*40)))*np.exp(-t*35)
def tick(f=2400): t=np.arange(int(.03*SR))/SR; return np.sin(2*np.pi*f*t)*np.exp(-t*200)
def hit(): t=np.arange(int(1.2*SR))/SR; return np.sin(2*np.pi*(48+40*np.exp(-t*8))*t)*np.exp(-t*3.5)
def thud(): t=np.arange(int(.25*SR))/SR; return (np.sin(2*np.pi*(90+120*np.exp(-t*30))*t)+.3*rng.standard_normal(len(t))*np.exp(-t*60))*np.exp(-t*18)
w=whoosh()
for k in ['rain','rock','river','sun','pile','loop']: add(w,S[k]-.2,.5)
def drip(f=1400): t=np.arange(int(.08*SR))/SR; return np.sin(2*np.pi*f*t*(1+1.5*np.exp(-t*60)))*np.exp(-t*50)
for i in range(8): add(drip(1200+i*90),S['hook']+.1+i*.3,.18)
add(hit(),S['hook']+1.2,.5)
add(pop(800),S['rain']+1.6,.4); add(pop(1000),S['rain']+3.4,.35); add(pop(1200),S['rain']+4.4,.35)
for i in range(7): add(pop(1300+i*60),S['rain']+.6+i*.25,.15)
for i in range(12): add(thud(),S['rock']+.4+i*.35,.18)
add(pop(900),S['rock']+2.2,.4); add(w,S['rock']+3.0,.3)
for i in range(30): add(tick(2400),S['river']+.9+i*.08,.15)
add(hit(),S['river']+3.3,.6); add(pop(800),S['river']+4.0,.4); add(pop(1000),S['river']+4.5,.3)
add(pop(700),S['sun']+.15,.35); add(pop(1100),S['sun']+1.3,.3); add(pop(900),S['sun']+3.0,.4); add(pop(900),S['sun']+4.4,.35)
for i in range(20): add(tick(2000),S['sun']+4.4+i*.14,.12)
for i in range(18): add(tick(2600),S['pile']+1.0+i*.09,.14)
add(pop(800),S['pile']+2.8,.4); add(w,S['pile']+4.0,.45)
for i in range(10): add(thud(),S['pile']+5.0+i*.22,.15)
add(hit(),S['pile']+7.1,.8)
for i in range(6): add(pop(900+i*80),S['loop']+.3+i*.2,.25)
add(w,S['loop']+2.4,.4)
out=out/max(1e-9,np.abs(out).max())*.5
y=(out*32767).astype(np.int16); f=wave.open('sfx.wav','wb'); f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(y.tobytes())
