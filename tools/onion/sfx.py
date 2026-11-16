import numpy as np, wave, json
SR=48000; tj=json.load(open('vo/timing.json')); T=tj['TOTAL']; S={s[0]:s[1] for s in tj['SC']}
out=np.zeros(int((T+1)*SR)); rng=np.random.default_rng(2211)
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
for k in ['cells','knife','eyes','why','tips','loop']: add(w,S[k]-.2,.5)
for i in range(5): add(thud(),S['hook']+.15+i*.63,.35)
add(hit(),S['hook']+1.0,.5)
for i in range(9): add(pop(700+i*50),S['cells']+.3+i*.12,.18)
add(pop(900),S['cells']+2.2,.4); add(pop(1000),S['cells']+3.0,.4); add(pop(800),S['cells']+4.2,.4)
add(w,S['knife']+.2,.7); add(hit(),S['knife']+.5,.6)
for i in range(9): add(pop(1300+i*40),S['knife']+.5+i*.08,.15)
add(pop(900),S['knife']+2.0,.4); add(pop(800),S['knife']+4.2,.45)
add(pop(900),S['eyes']+1.4,.4)
for i in range(6): add(tick(1800),S['eyes']+3.0+i*.17,.3)
add(hit(),S['eyes']+3.0,.6)
add(pop(900),S['why']+.6,.35); add(thud(),S['why']+2.2,.6); add(pop(600),S['why']+2.3,.4); add(w,S['why']+4.5,.4); add(hit(),S['why']+5.8,.8)
for st in [.5,1.8,3.2]: add(pop(900),S['tips']+st,.4); add(tick(2600),S['tips']+st+.5,.4)
add(pop(800),S['loop']+.0,.4); add(pop(1000),S['loop']+.4,.35); add(pop(1200),S['loop']+.9,.35); add(w,S['loop']+2.2,.4)
out=out/max(1e-9,np.abs(out).max())*.5
y=(out*32767).astype(np.int16); f=wave.open('sfx.wav','wb'); f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(y.tobytes())
