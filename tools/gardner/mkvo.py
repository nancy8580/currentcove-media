import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','door','cuffs','loot','tape','reward','end']
txt=["Two fake cops stole half a billion dollars of art. In one *night.*",
"Boston, 1990. At 1:24 a.m., two men in police uniforms buzzed the Gardner Museum's side door. The guard let them *in.*",
"Minutes later, both guards were handcuffed in the *basement.*",
"For eighty-one minutes, the thieves took their pick. A Rembrandt. A Vermeer. Thirteen works in *all.*",
"On the way out, they even took the security camera's *tape.*",
"Today the reward is ten million dollars. Not one painting has ever come *back.*",
"Their empty frames still hang on the walls, waiting for the two fake cops who stole half a billion dollars of *art...*"]
import os
SPS=[float(x) for x in os.environ.get('SPS','1.22,1.16,1.12,1.14,1.12,1.12,1.1').split(',')]
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
