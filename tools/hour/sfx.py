import numpy as np, wave, json
SR=48000; tj=json.load(open('vo/timing.json')); T=tj['TOTAL']; S={s[0]:s[1] for s in tj['SC']}
out=np.zeros(int((T+1)*SR)); rng=np.random.default_rng(1640)
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
for k in ['base60','why60','hands','egypt','ptolemy','france','loop']: add(w,S[k]-.2,.5)
# hook clock ticks
for i in range(6): add(tick(1800),S['hook']+.1+i*.5,.3)
# wedges stamping
for i in range(30): add(thud(),S['base60']+.2+i*.09,.12)
add(hit(),S['base60']+3.1,.7)
for i in range(5): add(pop(700+i*120),S['why60']+.3+i*.8,.35)
add(pop(400),S['why60']+5.2,.4)
for i in range(60): add(tick(2200+(i%12)*40),S['hands']+.6+i*5.6/60,.16)
add(hit(),S['hands']+6.2,.8)
for i in range(12): add(pop(1100),S['egypt']+.2+i*2.6/12,.15)
add(pop(800),S['egypt']+2.6,.35); add(pop(800),S['egypt']+4.6,.35); add(hit(),S['egypt']+5.0,.7)
add(pop(900),S['ptolemy']+3.4,.35); add(w,S['ptolemy']+4.3,.35); add(pop(900),S['ptolemy']+7.0,.35); add(pop(1200),S['ptolemy']+7.8,.3); add(pop(1200),S['ptolemy']+8.4,.3)
add(pop(800),S['france']+.2,.3); add(thud(),S['france']+4.4,.9); add(hit(),S['france']+4.4,.8)
for i in range(5): add(pop(900),S['loop']+.3+i*.15,.2)
out=out/max(1e-9,np.abs(out).max())*.5
y=(out*32767).astype(np.int16); f=wave.open('sfx.wav','wb'); f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(y.tobytes())
