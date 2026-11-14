import numpy as np, wave, sys
def load(p):
    w=wave.open(p); sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float); return a,sr
def tighten(a,sr,cap=.25,thr=-40):
    hop=int(sr*.01); n=len(a)//hop
    rms=np.array([np.sqrt(np.mean(a[i*hop:(i+1)*hop]**2)) for i in range(n)]); sil=rms<32768*10**(thr/20)
    idx=np.where(~sil)[0]
    if len(idx)==0: return a
    s0,s1=max(0,idx[0]-3),min(n,idx[-1]+6)
    out=[];i=s0;c=int(cap/.01)
    while i<s1:
        j=i
        while j<s1 and sil[j]==sil[i]: j+=1
        seg=a[i*hop:j*hop]
        if sil[i] and j-i>c: k=c*hop; seg=np.concatenate([seg[:k//2],seg[-k//2:]])
        out.append(seg); i=j
    return np.concatenate(out)
if __name__=="__main__":
    for p in sys.argv[1:]:
        a,sr=load(p); t=tighten(a,sr); print(p, round(len(a)/sr,2), round(len(t)/sr,2))
