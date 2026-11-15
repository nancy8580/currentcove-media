import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','meet','line','clocks','zigzag','samoa','loop']
txt=["Four kilometres apart. Twenty-one hours apart.",
"These are the Diomede Islands, in the icy Bering Strait. The big one is Russian. The little one is American.",
"Right between them runs the International Date Line. Cross it, and the calendar jumps a whole day.",
"Big Diomede runs on Russia's far-east time, Little Diomede on Alaska time. So they're nicknamed Tomorrow Island and Yesterday Island.",
"And the line isn't straight. It roughly follows 180 degrees longitude, but it has no legal status, so it bends around countries.",
"Kiribati pushed it east in 1995. And Samoa skipped an entire Friday, 30 December 2011, to line up with Australia and New Zealand.",
"So from Yesterday Island, you can look straight across at tomorrow."]
out=[];SC=[];t=0;sr=24000
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/v{i+1}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    pre=.1 if i==0 else 0
    d=pre+vd+(.45 if i==0 else .7)+(.9 if i==6 else 0)
    seg=np.zeros(int(d*sr)); seg[int(pre*sr):int(pre*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(x[:4]) for x in SC];print(t)
