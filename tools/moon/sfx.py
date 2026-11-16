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
for k in ['rate','laser','tides','push','days','loop']: add(w,S[k]-.2,.5); add(hit(),S[k]+.02,.35)
add(hit(),S['hook']+.0,.5); add(stampS(),S['hook']+.05,.5)
add(stampS(),S['rate']+.02,.6)
for i in range(22): add(tick(2000+i*30),S['rate']+.2+i*.1,.1)
add(stampS(),S['rate']+2.62,.6); add(stampS(),S['rate']+3.92,.6); add(stampS(),S['rate']+4.27,.6)
add(stampS(),S['laser']+.02,.6); add(pop(900),S['laser']+1.4,.35)
for n in range(5): add(pop(1500),S['laser']+.8+n*1.3,.25)
for i in range(18): add(tick(2200+i*30),S['laser']+4.3+i*.1,.1)
add(chime(1560),S['laser']+6.1,.35)
add(stampS(),S['tides']+.02,.7); add(stampS(),S['tides']+1.62,.6); add(stampS(),S['tides']+3.62,.6)
add(stampS(),S['push']+.02,.6); add(stampS(),S['push']+.37,.6); add(hit(),S['push']+3.42,.6); add(stampS(),S['push']+3.42,.6)
add(stampS(),S['days']+.02,.6); add(w,S['days']+2.2,.6); add(stampS(),S['days']+2.22,.5); add(hit(),S['days']+4.12,.7); add(stampS(),S['days']+4.12,.6)
add(stampS(),S['loop']+.02,.6); add(stampS(),S['loop']+.42,.6)
for i in range(22): add(tick(1800+i*25),S['loop']+.5+i*.1,.1)
add(stampS(),S['loop']+3.62,.6); add(chime(1320),S['loop']+6.4,.3)
out=out/max(1e-9,np.abs(out).max())*.5
y=(out*32767).astype(np.int16); f=wave.open('sfx.wav','wb'); f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(y.tobytes())
