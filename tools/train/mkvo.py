import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','cash','roof','cut','throw','twist','end']
txt=["Thieves robbed a moving Indian train. Through the *roof.*",
"Inside one parcel van: ₹342 crore in old notes, on their way to the RBI in Chennai, to be *burned.*",
"Police guarded the next coach. So five men climbed onto the roof, in the *dark.*",
"On a long stretch with no stops, they cut a hole in the roof, and dropped *inside.*",
"They broke open the boxes, and threw ₹5.78 crore down to friends waiting by the *tracks.*",
"But exactly three months later, India cancelled those notes. *Overnight.*",
"Police said the loot became almost useless. And the gang? Caught two years later, for robbing a moving *train...*"]
import os
SPS=[float(x) for x in os.environ.get('SPS','1.1,1.2,1.16,1.18,1.2,1.12,1.14').split(',')]
out=[];SC=[];t=0.0;lead=.05
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/b{i}.wav'); a=tighten(a,sr,cap=.14,thr=-36)
    w=wave.open('vo/_t.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(a.clip(-32768,32767).astype(np.int16).tobytes());w.close()
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i','vo/_t.wav','-filter:a',f'atempo={SPS[i]}','vo/_t2.wav']);a,sr=load('vo/_t2.wav')
    vd=len(a)/sr
    d=lead+vd+(.18 if i==0 else .3)+(1.7 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
