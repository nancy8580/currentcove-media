import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','climb','six','prints','army','front','end']
txt=["In 1999, a lost yak exposed a secret invasion of *India.*",
"May 1999, Ladakh. A shepherd climbs the Batalik ridges with binoculars, hunting for his missing *yak.*",
"Instead, he spots six strangers in Pathani clothes, breaking stone and clearing snow on the *ridge.*",
"And there are no footprints in the snow from India's side. They came from across the *border.*",
"He rushes to an Army unit. Days later, at Yaldor, soldiers find about forty *intruders.*",
"Pakistani troops had quietly taken peaks along a 168 kilometre front, posts left empty every *winter.*",
"His tip set off the Kargil War, which India won that July. And the yak that started it all? No one ever said if he found *it.*"]
import os
SPS=[float(x) for x in os.environ.get('SPS','1.26,1.2,1.2,1.2,1.18,1.16,1.16').split(',')]
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
