import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','s1','s2','s3','s4','s5','end']
txt=["How do just *six* *digits* find your post office?",
"Step one: chop India into *eight* *zones.* The first digit tells you which. One is Delhi and the north. Six is Tamil Nadu and Kerala.",
"Step two: keep a ninth zone just for the *Army* Postal Service. Yes, nine means the army.",
"Step three: the second digit narrows it to a *region,* usually a state. The third picks the *sorting* *district.*",
"Step four: the last three digits name the *exact* *post* *office* that delivers your letter. Out of about 1.65 lakh.",
"Step five: make it impossible to confuse. Many towns share the *same* *name,* and addresses come in many languages and spellings. *Numbers* don't.",
"It launched on *15* *August* *1972,* and it still works. So next time you write a PIN, ask yourself:"]
out=[];SC=[];t=0.0;sr=24000;lead=.12
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/v{i}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    d=lead+vd+.7+(1.6 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));print(json.dumps(SC,indent=0),t)
