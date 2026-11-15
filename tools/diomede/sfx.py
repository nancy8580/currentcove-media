import numpy as np, wave, json
SR=48000; tj=json.load(open('vo/timing.json')); T=tj['TOTAL']; S={s[0]:s[1] for s in tj['SC']}
out=np.zeros(int((T+1)*SR)); rng=np.random.default_rng(2611)
def add(sig,t,g):
    i=int(t*SR); j=min(len(out),i+len(sig)); out[i:j]+=g*sig[:j-i]
def whoosh(d=.5):
    n=int(d*SR); x=rng.standard_normal(n); t=np.arange(n)/SR
    X=np.fft.rfft(x); f=np.fft.rfftfreq(n,1/SR); X*=1/(1+(f/900)**2); y=np.fft.irfft(X,n)
    return y/np.abs(y).max()*np.sin(np.pi*t/d)**2
def pop(f=880): t=np.arange(int(.12*SR))/SR; return np.sin(2*np.pi*f*t*(1+2*np.exp(-t*40)))*np.exp(-t*35)
def tick(): t=np.arange(int(.03*SR))/SR; return np.sin(2*np.pi*2400*t)*np.exp(-t*200)
def hit(): t=np.arange(int(1.2*SR))/SR; return np.sin(2*np.pi*(48+40*np.exp(-t*8))*t)*np.exp(-t*3.5)
def chime(f=1320): t=np.arange(int(.8*SR))/SR; return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.01*t))*np.exp(-t*5)
w=whoosh()
for k in ['meet','line','clocks','zigzag','samoa','loop']: add(w,S[k]-.25,.5)
for t0 in [S['hook']+1.4,S['meet']+3.4,S['meet']+4.7,S['clocks']+4.4,S['clocks']+5.6,S['samoa']+.3,S['samoa']+2.4,S['samoa']+6.6,S['samoa']+7.0]: add(pop(),t0,.35)
for i in range(12): add(tick(),S['clocks']+2.8+i*.1,.25)
add(hit(),S['zigzag']+4.4,.8); add(hit(),S['samoa']+5.4,.7); add(chime(),S['samoa']+4.6,.3); add(chime(990),S['loop']+.8,.3)
out=out/max(1e-9,np.abs(out).max())*.5
y=(out*32767).astype(np.int16); f=wave.open('sfx.wav','wb'); f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(y.tobytes())
