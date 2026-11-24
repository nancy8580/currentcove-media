import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','drop','odds','stay','trap','never','end']
txt=["Britain's secret radio in Nazi Paris was an Indian *princess.*",
"June 1943. Noor Inayat Khan landed by night plane: Britain's first woman radio operator in occupied *France.*",
"Radio operators were expected to last six weeks. Within ten days, her whole network was *arrested.*",
"London offered to fly her home. She stayed, as German detector vans hunted her *signal.*",
"Then she was betrayed. The Germans used her own radio to trap three more *agents.*",
"She tried to escape twice, and never talked. Her last word, reportedly: *Liberté.*",
"In 1949: the George *Cross.* Because for months, Britain's secret radio in Nazi Paris..."]
import os
SPS=[float(x) for x in os.environ.get('SPS','1.26,1.2,1.2,1.2,1.18,1.16,1.16').split(',')]
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
