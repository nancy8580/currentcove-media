import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','ad','taj','raid','inside','gone','end']
txt=["In 1987, a *fake* CBI team robbed a Mumbai jeweller in broad daylight.",
"It began with a newspaper job ad: graduates wanted, for *intelligence* officer posts.",
"A man calling himself Mohan Singh hired *twenty-six* of them at the Taj, for a 'mock raid'.",
"On 19th March, they marched into a jeweller at Opera House, carrying a search *warrant.*",
"Cameras off. Phones banned. Jewels sealed as *evidence.* Then the boss left, for 'another raid'.",
"He *vanished* with lakhs in jewels and cash. Bollywood later made it Special 26.",
"But police think he'd tested the same ad months earlier. And the real Mohan Singh? *Never* found."]
out=[];SC=[];t=0.0;lead=.06
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/b{i}.wav'); a=tighten(a,sr,cap=.24); vd=len(a)/sr
    d=lead+vd+(.25 if i==0 else .38)+(1.3 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
