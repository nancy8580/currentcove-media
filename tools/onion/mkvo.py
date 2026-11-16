import sys,json,wave,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','cells','knife','eyes','why','tips','loop']
txt=["Your onion is fighting back when you cut it.",
"Inside every onion cell, an enzyme and a sulphur compound are kept apart, in separate little bags.",
"Your knife bursts those bags. They mix, and a second enzyme turns the result into a sneaky gas, called propanethial S-oxide.",
"The gas drifts up into your eyes and reacts with the water there, making a mild acid. Your nerves raise the alarm, and tears rush in to wash it away.",
"Scientists think it's a defence, to stop animals from eating the onion. And that second enzyme was only discovered in 2002, by researchers in Japan.",
"Want fewer tears? Chill the onion first, use a really sharp knife, or just wear swimming goggles.",
"Because those aren't sad tears. It's chemistry."]
out=[];SC=[];t=0.15;sr=24000;out.append(np.zeros(int(.15*sr)))
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/v{i+1}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    d=vd+.7+(1.6 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[:len(a)]=a; out.append(seg)
    SC.append([k,round(t if i else 0,3),round(t+d,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));print(json.dumps(SC,indent=0),t)
