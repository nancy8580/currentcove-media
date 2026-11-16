import sys,json,wave,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','rate','laser','tides','push','days','loop']
txt=["The Moon is running away from us.",
"Every year, it drifts about three point eight centimetres farther away. That's roughly as fast as your fingernails grow.",
"We know because Apollo astronauts left mirrors on the Moon. Scientists still fire lasers at them, and the light comes back in about two and a half seconds.",
"The culprit is tides. The Moon pulls Earth's oceans into a bulge, but Earth spins so fast it drags that bulge slightly ahead.",
"That bulge tugs the Moon forward, nudging it into a wider orbit, while Earth's spin slowly brakes.",
"So our days keep getting longer. One point four billion years ago, a whole day lasted just over eighteen hours.",
"Since Apollo 11 landed, it's slipped about two metres further. And right now, while you watch this..."]
out=[];SC=[];t=0.15;sr=None
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/v{i+1}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    if i==0: out.append(np.zeros(int(.15*sr)))
    d=vd+.7+(1.6 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[:len(a)]=a; out.append(seg)
    SC.append([k,round(t if i else 0,3),round(t+d,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));print(json.dumps(SC,indent=0),t,sr)
