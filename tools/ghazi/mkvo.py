import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','target','slip','decoy','bait','blast','end']
txt=["In 1971, India trapped a Pakistani submarine with a fake *grocery* order.",
"Ghazi was sent to sink INS Vikrant, India's only aircraft *carrier.*",
"But Vikrant had secretly slipped away to the *Andamans.*",
"So an old destroyer, INS Rajput, posed as Vikrant. Fake radio signals. Huge *ration* orders.",
"Pakistan took the bait. Carrier in *port.*",
"Just after midnight on 4 December, a massive *blast* shook the sea off Vizag.",
"Ghazi never surfaced. India credits Rajput's depth charges; Pakistan, an explosion on board. Either way, it was hunting a ship that was never *there.*"]
SPS=[1.26,1.17,1.12,1.17,1.1,1.15,1.17]
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
