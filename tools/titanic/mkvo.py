import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','blair','key','ask','berg','inquiry','end']
txt=["The Titanic may have sunk because of a key in one man's *pocket.*",
"Southampton, April 1912. Second Officer David Blair is pulled off the ship in a last-minute *reshuffle.*",
"When he walks off, the key to the crow's nest locker walks off with him. The lookouts sail with *no binoculars.*",
"They ask for a pair. They're told: there are *none.*",
"April 14th, 11:40 at night. Lookout Fred Fleet sees a black shape dead ahead. An *iceberg.* Too late.",
"At the inquiry, a US senator asked him: with binoculars, how much sooner? His answer: Enough to get *out of the way.*",
"In 2007, that forgotten little key sold at auction for ninety thousand *pounds.*"]
tempo=[1.22,1.12,1.12,1.08,1.1,1.08,1.08]
out=[];SC=[];t=0.0;lead=.1
for i,(k,s) in enumerate(zip(ids,txt)):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'vo/a{i}.wav','-af',f'atempo={tempo[i]}','-ar','24000',f'vo/f{i}.wav'])
    a,sr=load(f'vo/f{i}.wav'); a=tighten(a,sr,cap=.22); vd=len(a)/sr
    d=lead+vd+.6+(1.6 if i==len(ids)-1 else 0)
    if i==0: d=lead+vd+.35
    if k=='berg': d+=0.6
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
