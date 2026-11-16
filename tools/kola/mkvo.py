import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','kola','depth','fossil','heat','plastic','end']
txt=["Why did humanity's deepest hole stop at just *12* *kilometres?*",
"In 1970, Soviet scientists began drilling into the Arctic rock of Russia's *Kola* *Peninsula.* The hole was just *23* *centimetres* wide.",
"Nineteen years later, they hit *12,262* *metres.* That's deeper than the ocean's *deepest* *point.*",
"At 6.7 kilometres down, they found tiny plankton *fossils,* about *two* *billion* years old, still intact.",
"Then came the heat. They expected *100* *degrees* down there. They measured *180.*",
"The rock got so hot it behaved like *plastic,* creeping back into the hole as they drilled. The *15-kilometre* target was *never* reached.",
"All that effort, and we got just *0.2%* of the way to Earth's centre. So think about it:"]
out=[];SC=[];t=0.0;sr=24000;lead=.12
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/f{i}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    d=lead+vd+.7+(1.6 if i==len(ids)-1 else 0)
    if i==0: d=lead+vd+.45
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
