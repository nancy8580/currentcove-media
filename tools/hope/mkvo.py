import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','india','theft','london','curse','mail','end']
txt=["A diamond from India was once sent by post. Postage: two dollars, forty-four *cents.*",
"Mined in India, it was sold to King Louis XIV of *France.*",
"Recut as the French Blue, it vanished in 1792, when thieves looted the French crown *jewels.*",
"Twenty years later, a 45-carat blue diamond surfaced in London. Cut, experts believe, from the *same* stone.",
"It took a banker's name, Hope, and collected stories of a *curse.*",
"In 1958, jeweller Harry Winston gave it to the Smithsonian. And he sent it by registered *mail.*",
"Insured for one million dollars, it arrived safely. And it's still there *today.*"]
import os
SPS=[float(x) for x in os.environ.get('SPS','1.12,1.1,1.1,1.1,1.08,1.1,1.1').split(',')]
out=[];SC=[];t=0.0;lead=.05
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/b{i}.wav'); a=tighten(a,sr,cap=.2)
    w=wave.open('vo/_t.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(a.clip(-32768,32767).astype(np.int16).tobytes());w.close()
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i','vo/_t.wav','-filter:a',f'atempo={SPS[i]}','vo/_t2.wav']);a,sr=load('vo/_t2.wav')
    vd=len(a)/sr
    d=lead+vd+(.18 if i==0 else .3)+(1.7 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
