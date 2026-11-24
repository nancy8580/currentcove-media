import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','nobel','gone','loot','probe','closed','end']
txt=["India's first Nobel Prize was stolen. And it was never *found.*",
"In 1913, Rabindranath Tagore became the first Asian to win a Nobel *Prize.*",
"His medal was kept in a museum at Santiniketan. On 25 March 2004, after a two-day break, the museum reopened. The medal was *gone.*",
"So were 47 other treasures, including his gold pocket *watch.*",
"The CBI took over within days. Investigators questioned at least a hundred staff. *Nothing.*",
"Sweden sent replica medals. And in 2010, the case was officially *closed.*",
"Reports said it was smuggled out of India. No one ever proved it. So where is the medal *today?*"]
import os
SPS=[float(x) for x in os.environ.get('SPS','1.12,1.1,1.12,1.1,1.1,1.1,1.08').split(',')]
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
