import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','call','voice','code','hand','caught','end']
txt=["In 1971, one phone call made a bank hand over sixty lakh *rupees.*",
"Delhi, May 24th. The chief cashier of State Bank picks up the *phone.*",
"A voice says the Prime Minister needs sixty lakh rupees, for work that is very highly *secret.*",
"The password? A man will say, 'Bangladesh ka babu.' You answer: *Bar-at-Law.*",
"He hands the cash to a stranger, then asks the PM's house for a receipt. Nobody had *called.*",
"Within a day, police caught Rustom Nagarwala at the airport. He confessed: he had faked the *voice.*",
"A ten-minute trial. He died in custody. Then an inquiry said his confession should have been rejected. So whose voice was *it?*"]
import os
SPS=[float(x) for x in os.environ.get('SPS','1.26,1.2,1.2,1.2,1.18,1.16,1.16').split(',')]
out=[];SC=[];t=0.0;lead=.05
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/b{i}.wav'); a=tighten(a,sr,cap=.2)
    w=wave.open('vo/_t.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(a.clip(-32768,32767).astype(np.int16).tobytes());w.close()
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i','vo/_t.wav','-filter:a',f'atempo={SPS[i]}','vo/_t2.wav']);a,sr=load('vo/_t2.wav')
    vd=len(a)/sr
    d=lead+vd+(.18 if i==0 else .3)+(1.7 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
