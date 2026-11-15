import numpy as np, wave, json
SR=48000; tj=json.load(open('vo/timing.json')); T=tj['TOTAL']; EV=json.load(open('vo/sfx.json'))
out=np.zeros(int((T+1)*SR)); rng=np.random.default_rng(1511)
def add(sig,t,g):
    i=max(0,int(t*SR)); j=min(len(out),i+len(sig)); out[i:j]+=g*sig[:j-i]
def noise_lp(n,fc):
    x=rng.standard_normal(n);X=np.fft.rfft(x);f=np.fft.rfftfreq(n,1/SR);X*=1/(1+(f/fc)**2);y=np.fft.irfft(X,n);return y/np.abs(y).max()
def whoosh(d=.45): n=int(d*SR);t=np.arange(n)/SR;return noise_lp(n,1100)*np.sin(np.pi*t/d)**2
def pop(f=760): t=np.arange(int(.12*SR))/SR; return np.sin(2*np.pi*f*t*(1+2*np.exp(-t*40)))*np.exp(-t*35)
def tick(): t=np.arange(int(.03*SR))/SR; return np.sin(2*np.pi*2600*t)*np.exp(-t*200)
def hit(): t=np.arange(int(1.2*SR))/SR; return np.sin(2*np.pi*(46+40*np.exp(-t*8))*t)*np.exp(-t*3.5)
def stamp(): n=int(.25*SR);t=np.arange(n)/SR;return .6*noise_lp(n,2500)*np.exp(-t*30)+np.sin(2*np.pi*90*t)*np.exp(-t*20)
def chime(f=1175): t=np.arange(int(.9*SR))/SR; return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.01*t))*np.exp(-t*5)
def rise(d=1.2): n=int(d*SR);t=np.arange(n)/SR;return np.sin(2*np.pi*(200*t+300*t*t/d))*np.sin(np.pi*t/d)**2*.6
F={'whoosh':(whoosh(),.5),'pop':(pop(),.35),'tick':(tick(),.22),'hit':(hit(),.8),'stamp':(stamp(),.6),'chime':(chime(),.3),'rise':(rise(),.25)}
for t0,k in EV: s,g=F[k]; add(s,t0,g)
out=out/max(1e-9,np.abs(out).max())*.5
y=(out*32767).astype(np.int16); f=wave.open('sfx.wav','wb'); f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(y.tobytes())
