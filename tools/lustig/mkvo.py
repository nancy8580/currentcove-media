import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','s1','s2','s3','paid','again','end']
txt=["In 1925, a con man *sold* the Eiffel Tower.",
"Step one: pose as a government official, and invite Paris scrap dealers to a secret meeting at a *luxury* *hotel.*",
"Step two: the lie. The tower costs too much to maintain, so Paris will scrap all *7,000* *tonnes.* Tell no one.",
"Step three: pick one dealer, André Poisson, and quietly ask him for a *bribe.* That's what made it feel real.",
"Poisson paid. The con man vanished with the cash, and Poisson was too *embarrassed* to go to the police.",
"So the con man came back... to sell it *again.* This time the police heard, and he fled to America.",
"He later fooled *Al* *Capone,* and died a prisoner of Alcatraz. The tower? Still standing."]
out=[];SC=[];t=0.0;lead=.1
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/a{i}.wav'); a=tighten(a,sr,cap=.3); vd=len(a)/sr
    d=lead+vd+(.35 if i==0 else .5)+(1.4 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
