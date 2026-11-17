import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','where','iss','use','count','name','end']
txt=["The nearest humans to this spot are often in *space.*",
"This is *Point* *Nemo,* in the South Pacific. The closest land is *2,688* *km* away, in every direction.",
"The Space Station orbits about *400* *km* up. So when it passes overhead, *astronauts* are your closest neighbours.",
"And all that emptiness makes it useful. Space agencies steer dying spacecraft to *crash* right here.",
"More than *260* of them since *1971,* including Russia's entire *Mir* space station, in 2001.",
"No ships, no people, nothing to hit. Even the name *Nemo* is Latin for *no* *one.*",
"And around *2030,* the Space Station itself is planned to fall here too. Fitting, because..."]
out=[];SC=[];t=0.0;lead=.12
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/f{i}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    l=0.02 if i==0 else lead
    d=l+vd+.7+(1.6 if i==len(ids)-1 else 0)
    if i==len(ids)-1: d-=1.0   # keep loop tight into the hook
    seg=np.zeros(int(d*sr)); seg[int(l*sr):int(l*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+l,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));print(json.dumps(SC,indent=0),t)
