import sys,json,wave,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','share','length','hose','india','faults','loop']
txt=["Your message to America never goes to space.",
"Over ninety-nine percent of the data moving between continents travels through cables lying on the ocean floor. Satellites carry only a tiny fraction.",
"There are more than one and a half million kilometres of them. That's enough to wrap around the Earth about thirty-seven times.",
"Most are only as thick as a garden hose. Inside, your data races as pulses of light, through glass fibres as thin as a human hair.",
"And India's international internet comes ashore mainly in just two cities: Mumbai and Chennai.",
"About two hundred cables get damaged every year. Two-thirds of the time, it's fishing boats and dragging anchors. Sharks? Almost never.",
"So the internet isn't in the sky. It's at the bottom of the sea. And every time you hit send,"]
out=[];SC=[];t=0.15;sr=24000;out.append(np.zeros(int(.15*sr)))
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/v{i+1}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    d=vd+.7+(1.6 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[:len(a)]=a; out.append(seg)
    SC.append([k,round(t if i else 0,3),round(t+d,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));print(json.dumps(SC,indent=0),t)
