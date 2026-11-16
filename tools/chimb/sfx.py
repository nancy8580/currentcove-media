import numpy as np, wave, json
SR=48000; tj=json.load(open('vo/timing.json')); T=tj['TOTAL']; S={s[0]:s[1] for s in tj['SC']}
out=np.zeros(int((T+1)*SR)); rng=np.random.default_rng(1116)
def add(sig,t,g):
    i=int(t*SR); j=min(len(out),i+len(sig)); out[i:j]+=g*sig[:j-i]
def whoosh(d=.4):
    n=int(d*SR); x=rng.standard_normal(n); y=np.zeros(n); a=0
    for k in range(n):
        c=.02+.25*np.sin(np.pi*k/n); a+=c*(x[k]-a); y[k]=a
    return y*np.sin(np.pi*np.arange(n)/n)**2
def pop(f=900): t=np.arange(int(.12*SR))/SR; return np.sin(2*np.pi*f*t*(1+2*np.exp(-t*40)))*np.exp(-t*35)
def tick(f=2400): t=np.arange(int(.03*SR))/SR; return np.sin(2*np.pi*f*t)*np.exp(-t*200)
def hit(): t=np.arange(int(1.2*SR))/SR; return np.sin(2*np.pi*(48+40*np.exp(-t*8))*t)*np.exp(-t*3.5)
def stampS(): t=np.arange(int(.3*SR))/SR; return (np.sin(2*np.pi*(110+150*np.exp(-t*30))*t)+.4*rng.standard_normal(len(t))*np.exp(-t*50))*np.exp(-t*14)
def chime(f=1320): t=np.arange(int(1.0*SR))/SR; return (np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*2.01*t))*np.exp(-t*4)
w=whoosh()
for k in ['everest','bulge','chimb','reveal','history','loop']: add(w,S[k]-.2,.5)
add(chime(),S['hook']+.1,.35); add(stampS(),S['hook']+1.9,.6)
for i in range(26): add(tick(2000+i*30),S['everest']+.2+i*.1,.1)
add(stampS(),S['everest']+2.9,.7); add(w,S['everest']+3.8,.5); add(pop(700),S['everest']+5.8,.35); add(hit(),S['everest']+6.2,.4)
add(pop(900),S['bulge']+.3,.3); add(pop(1100),S['bulge']+1.5,.3); add(hit(),S['bulge']+3.0,.7)
add(pop(800),S['chimb']+.9,.3); add(chime(1560),S['chimb']+2.0,.35); add(pop(1000),S['chimb']+3.0,.35); add(w,S['chimb']+4.2,.5); add(stampS(),S['chimb']+6.3,.7)
add(pop(800),S['reveal']+1.0,.3); add(pop(1000),S['reveal']+1.9,.3); add(chime(1760),S['reveal']+3.0,.35); add(hit(),S['reveal']+3.6,.8)
add(stampS(),S['history']+.6,.6)
for i in range(26): add(tick(1800+i*25),S['history']+3.4+i*.1,.1)
add(stampS(),S['history']+6.1,.7)
add(chime(1320),S['loop']+.1,.3); add(pop(900),S['loop']+1.2,.35); add(pop(700),S['loop']+3.4,.3); add(w,S['loop']+5.4,.5); add(stampS(),S['loop']+7.5,.4)
out=out/max(1e-9,np.abs(out).max())*.5
y=(out*32767).astype(np.int16); f=wave.open('sfx.wav','wb'); f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(y.tobytes())
