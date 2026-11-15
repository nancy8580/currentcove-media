"""Usage: python3 sfx.py vo/sfx.json TOTAL out/sfx.wav  -- synthesises whoosh/thud/stamp/paper/tick/pop/swing/type/marker/rise events."""
import json,sys,numpy as np,wave
SR=48000;T=float(sys.argv[2])+.5;A=np.zeros(int(T*SR));rng=np.random.default_rng(3)
def env(n,a,d):e=np.exp(-np.arange(n)/(d*SR));e[:int(a*SR)]*=np.linspace(0,1,int(a*SR));return e
def lp(x,k):return np.convolve(x,np.ones(k)/k,'same')
def snd(k):
    if k=='whoosh':n=int(.35*SR);x=rng.standard_normal(n);x=lp(x,6)-lp(x,40);return x*np.sin(np.linspace(0,np.pi,n))**2*.5
    if k=='thud':n=int(.4*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*(70-30*t/.4)*t)*env(n,.002,.12)+lp(rng.standard_normal(n),20)*env(n,.001,.03)*.6)*.9
    if k=='stamp':n=int(.35*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*55*t)*env(n,.001,.09)*.9+lp(rng.standard_normal(n),3)*env(n,.0005,.025)*.8)
    if k=='paper':n=int(.25*SR);x=rng.standard_normal(n);x=x-lp(x,8);return x*env(n,.02,.08)*.35
    if k=='tick':n=int(.05*SR);t=np.arange(n)/SR;return np.sin(2*np.pi*2200*t)*env(n,.0005,.008)*.4
    if k=='pop':n=int(.12*SR);t=np.arange(n)/SR;return np.sin(2*np.pi*(900+1400*t/.12)*t)*env(n,.001,.03)*.5
    if k=='swing':n=int(.5*SR);t=np.arange(n)/SR;return np.sin(2*np.pi*3200*t)*env(n,.001,.25)*.12+np.sin(2*np.pi*4100*t)*env(n,.001,.2)*.08
    if k=='type':
        out=np.zeros(int(1.3*SR))
        for i in range(20):
            s=snd('tick')*1.2;i0=int(i*.062*SR);out[i0:i0+len(s)]+=s[:len(out)-i0]
        return out
    if k=='marker':n=int(.45*SR);x=rng.standard_normal(n);x=lp(x,3)-lp(x,12);return x*.2*np.sin(np.linspace(0,np.pi,n))
    if k=='rise':n=int(1.4*SR);t=np.arange(n)/SR;return np.sin(2*np.pi*(200+500*t/1.4)*t)*np.linspace(0,1,n)**2*.18
    return np.zeros(10)
for t,k in json.load(open(sys.argv[1])):
    s=snd(k);i=int(t*SR);A[i:i+len(s)]+=s[:max(0,len(A)-i)]
A=A/max(1e-9,np.max(np.abs(A)))*.8
w=wave.open(sys.argv[3],'w');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((A*32767).astype(np.int16).tobytes());w.close()
