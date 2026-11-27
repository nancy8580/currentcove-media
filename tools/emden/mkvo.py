import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','anchor','lights','fire','court','panic','end']
txt=["In 1914, a German warship crept up to Madras at night and shelled the *city.*",
"It was the SMS Emden. She dropped anchor just 2,500 metres off the harbour, and nobody *noticed.*",
"At about 9:20 pm, her searchlights found the giant oil tanks of Burmah Oil. Then she opened *fire.*",
"Around 130 shells later, almost 350,000 gallons of fuel were *burning.*",
"One shell hit the wall of the Madras High Court. A plaque still marks the *spot.*",
"Panic spread. One account says nearly 20,000 people fled the city every *day.*",
"Seven weeks later, the Emden was a wreck. But her name never left Madras. In Tamil, an Emden still means a daring *person.*"]
import os
SPS=[float(x) for x in os.environ.get('SPS','1.22,1.2,1.2,1.18,1.18,1.16,1.18').split(',')]
out=[];SC=[];t=0.0;lead=.05
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/b{i}.wav'); a=tighten(a,sr,cap=.2)
    w=wave.open('vo/_t.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(a.clip(-32768,32767).astype(np.int16).tobytes());w.close()
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i','vo/_t.wav','-filter:a',f'atempo={SPS[i]}','vo/_t2.wav']);a,sr=load('vo/_t2.wav')
    vd=len(a)/sr
    d=lead+vd+(.15 if i==0 else .22)+(1.3 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
