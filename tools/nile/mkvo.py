import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','people','strip','rain','source','green','loop']
txt=["Why do almost all Egyptians live on one thin line?",
"Egypt covers over a million square kilometres. Yet about 95% of its 113 million people live within 20 km of one river: the Nile.",
"Add that strip up, and it's only about 4% of the country. Roughly the size of Kerala.",
"The rest is the Sahara. Egypt averages about 18 millimetres of rain a year. That's less than two centimetres!",
"So the water comes from far away. Rain over Ethiopia and around Lake Victoria flows thousands of kilometres north.",
"Wherever that water reaches, fields turn green. A few steps past the farms, it's pure sand.",
"About 2,500 years ago, Herodotus called Egypt the gift of the Nile. From space at night, it still looks like one glowing line."]
out=[];SC=[];t=0;sr=24000
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/v{i+1}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    pre=.1 if i==0 else 0
    d=pre+vd+(.45 if i==0 else .7)+(.9 if i==6 else 0)
    seg=np.zeros(int(d*sr)); seg[int(pre*sr):int(pre*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+pre,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(x[:5]) for x in SC];print(t)
