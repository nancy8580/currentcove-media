import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','plat','press','mask','ground','turb','route','end']
txt=["There's a giant *hole* in the world's flight map.",
"It sits over *Tibet:* a plateau of *2.5 million* square km, averaging more than *4.5 km* high.",
"Now picture this. Your cabin *loses* *pressure* at *35,000* feet.",
"Your oxygen mask lasts only about *15* *minutes,* so pilots must dive to *10,000* *feet,* where the air is breathable.",
"But over Tibet, the *ground* itself is higher than that. In places, the safe altitude is over *20,000* *feet.*",
"Add violent mountain *turbulence,* and almost *no* *airports* to divert to.",
"So only a few special airways, like *L888,* cross it, with extra oxygen and planned escapes to *Chengdu* or *Kashgar.*",
"Next time you open a flight tracker, *look* *for* *it.*"]
out=[];SC=[];t=0.0;lead=.12
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/f{i}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    l=0.02 if i==0 else lead
    d=l+vd+.7+(1.6 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[int(l*sr):int(l*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+l,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));print(json.dumps(SC,indent=0),t)
