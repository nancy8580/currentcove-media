import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','sats','shout','delay','circles','clock','loop']
txt=["Your phone never talks to GPS satellites.",
"It only listens. Twenty thousand kilometres up, at least twenty-four GPS satellites circle the Earth, each one twice a day.",
"Each one keeps broadcasting two things: the exact time, and exactly where it is.",
"Your phone checks how late each message arrives. Radio moves at the speed of light, so that tiny delay is really a distance.",
"One distance gives a circle of places you could be. Three circles cross at just one point: you. A fourth satellite fixes your phone's clock.",
"Timing is everything. Thanks to Einstein's relativity, those satellite clocks run thirty-eight microseconds a day fast. Left uncorrected, your map would drift over ten kilometres every day.",
"And it finds you without sending a single signal back, because..."]
out=[];SC=[];t=0;sr=24000
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/v{i+1}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    pre=.15 if i==0 else 0
    d=pre+vd+(.45 if i==0 else .7)+(.6 if i==6 else 0)
    seg=np.zeros(int(d*sr)); seg[int(pre*sr):int(pre*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(x[:4]) for x in SC];print(t)
