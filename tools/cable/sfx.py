import numpy as np, wave, json
SR=48000; tj=json.load(open('vo/timing.json')); T=tj['TOTAL']; S={s[0]:s[1] for s in tj['SC']}
out=np.zeros(int((T+1)*SR)); rng=np.random.default_rng(3317)
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
for k in ['share','length','hose','india','faults','loop']: add(w,S[k]-.2,.5)
def sonar(): t=np.arange(int(1.0*SR))/SR; return np.sin(2*np.pi*1150*t)*np.exp(-t*4)
add(sonar(),S['hook']+.1,.5); add(hit(),S['hook']+.6,.5)
for i in range(30): add(tick(2400),S['share']+.6+i*.073,.13)
add(hit(),S['share']+2.8,.7); add(pop(900),S['share']+2.8,.35); add(pop(700),S['share']+4.6,.3)
for i in range(30): add(tick(2200),S['length']+.3+i*.08,.12)
add(pop(1000),S['length']+2.7,.4)
for i in range(37): add(tick(1600+i*20),S['length']+3.0+i*.07,.1)
add(hit(),S['length']+5.6,.6)
for i in range(5): add(pop(600+i*150),S['hose']+.2+i*.25,.3)
add(pop(900),S['hose']+1.4,.35); add(w,S['hose']+3.2,.6); add(pop(1200),S['hose']+4.0,.35)
add(sonar(),S['india']+.3,.4); add(sonar(),S['india']+.9,.4); add(hit(),S['india']+1.6,.6)
for i in range(20): add(tick(2000),S['faults']+.4+i*.1,.12)
add(thud(),S['faults']+1.9,.9); add(hit(),S['faults']+1.9,.7); add(pop(800),S['faults']+2.4,.35)
add(w,S['faults']+4.2,.5); add(pop(500),S['faults']+5.8,.45)
add(hit(),S['loop']+.1,.5); add(w,S['loop']+1.2,.5); add(sonar(),S['loop']+4.6,.4)
out=out/max(1e-9,np.abs(out).max())*.5
y=(out*32767).astype(np.int16); f=wave.open('sfx.wav','wb'); f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(y.tobytes())
