import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','attack','call','india','land','twist','navy','end']
txt=["In 1988, gunmen tried to steal an entire *country,* in one night.",
"4 a.m., the Maldives. Around 150 *mercenaries* storm the capital, and seize the key buildings.",
"The President hides, and calls for help. America says it needs *two to three days.*",
"India says: *tonight.* Paratroopers take off from Agra in two IL-76 jets, non-stop.",
"Nine hours after the call, they land, seize the airport, and reach the *President.*",
"But the gunmen *escape* on a hijacked ship, with hostages.",
"Indian warships hunt it down. Shells land around it. Navy *commandos* board. It's over.",
"Britain's Prime Minister reportedly said: *Thank God for India.*"]
out=[];SC=[];t=0.0;lead=.1
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/a{i}.wav'); a=tighten(a,sr,cap=.22); vd=len(a)/sr
    d=lead+vd+.55+(1.5 if i==len(ids)-1 else 0)
    if i==0: d=lead+vd+.35
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
