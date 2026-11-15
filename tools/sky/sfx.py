import numpy as np, wave, json
SR=48000; tj=json.load(open('vo/timing.json')); T=tj['TOTAL']; S={s[0]:s[1] for s in tj['SC']}
out=np.zeros(int((T+1)*SR)); rng=np.random.default_rng(1115)
def add(sig,t,g):
    i=int(t*SR); j=min(len(out),i+len(sig)); out[i:j]+=g*sig[:j-i]
def whoosh(d=.5):
    n=int(d*SR); x=rng.standard_normal(n); t=np.arange(n)/SR
    # sweep a simple one-pole lowpass
    y=np.zeros(n); a=0
    for k in range(n):
        c=.02+.25*np.sin(np.pi*k/n); a+=c*(x[k]-a); y[k]=a
    return y*np.sin(np.pi*t/d)**2
def pop(f=900): t=np.arange(int(.12*SR))/SR; return np.sin(2*np.pi*f*t*(1+2*np.exp(-t*40)))*np.exp(-t*35)
def tick(): t=np.arange(int(.03*SR))/SR; return np.sin(2*np.pi*2400*t)*np.exp(-t*200)
def hit(): t=np.arange(int(1.2*SR))/SR; return np.sin(2*np.pi*(48+40*np.exp(-t*8))*t)*np.exp(-t*3.5)
w=whoosh()
for k in ['white','scatter','sky','violet','sunset','loop']: add(w,S[k]-.25,.5)
for t0 in [S['hook']+.0, S['white']+2.0, S['scatter']+2.6, S['scatter']+3.2, S['sky']+2.6, S['violet']+4.4, S['sunset']+4.4, S['loop']+2.2, S['loop']+3.0, S['loop']+3.8]: add(pop(),t0,.35)
for i in range(16): add(tick(), S['scatter']+5.6+i*.1, .25)
for i in range(20): add(tick(), S['sunset']+1.6+i*.12, .25)
add(hit(), S['scatter']+7.6, .8); add(hit(), S['sunset']+4.0, .8)
out=out/ max(1e-9,np.abs(out).max())*.5
y=(out*32767).astype(np.int16); f=wave.open('sfx.wav','wb'); f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(y.tobytes())
