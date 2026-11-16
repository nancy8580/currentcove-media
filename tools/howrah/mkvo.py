import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','s1','s2','s3','s4','s5','end']
txt=["Kolkata's Howrah Bridge has *no* *nuts* and *no* *bolts.*",
"Step one: leave the river alone. Ships needed the Hooghly clear, so the bridge leaps across in one *457-metre* *span.*",
"Step two: dig deep. Its two towers stand on giant boxes sunk up to *31* *metres* into the soft riverbank.",
"Step three: find steel during a world war. Britain could send only 3,000 tonnes, so *Tata* *Steel* made the other *23,000.*",
"Step four: skip the nuts and bolts. Every joint was *riveted,* so the whole thing holds together like one giant piece of steel.",
"Step five: open it quietly. Fearing air raids, there was *no* *ceremony* in 1943. The first vehicle across was a lone *tram.*",
"Today it carries about a *lakh* vehicles a day. Its worst enemy? *Paan* *spit,* which ate *half* the thickness of its steel guards. So next time you cross it, remember:"]
out=[];SC=[];t=0.0;sr=24000;lead=.12
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/f{i}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    d=lead+vd+.7+(1.6 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));print(json.dumps(SC,indent=0),t)
