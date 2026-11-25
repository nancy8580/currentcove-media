import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','caught','night','dunes','codes','boom','end']
txt=["India hid a nuke from US spy *satellites.*",
"Years earlier, US satellites had caught India preparing a test, and Washington made it *stop.*",
"So this time, the army's 58th Engineer Regiment dug only at night, and parked every machine back before *dawn.*",
"Dug-out sand was shaped like natural dunes. Scientists wore army uniforms, and used fake *names.*",
"Even the bomb shafts got code names. White House. And Taj *Mahal.*",
"On the eleventh of May, at 3:45 PM, three bombs went off under the Thar desert. The CIA had issued no *warning.*",
"US officials admitted they had blundered. American intelligence was humiliated. Because..."]
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
