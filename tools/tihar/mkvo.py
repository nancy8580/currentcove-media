import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','who','sweets','gates','goa','twist','end']
txt=["In 1986, a prisoner drugged his guards and walked out of Tihar *Jail.*",
"He was Charles Sobhraj, a notorious con man. And Thailand was waiting to try him for *murder.*",
"In March 1986, boxes of sweets arrived for the guards, for a so-called birthday. They were laced with sleeping *pills.*",
"As the guards passed out, he walked straight out of the front *gates.*",
"Days later, Mumbai inspector Madhukar Zende walked into a Goa restaurant and said: Hello, *Charles.*",
"But reports say that was the plan. Escaping added years to his sentence in *India.*",
"By the time India freed him in 1997, Thailand's case had run out of time, and he flew to France. Getting caught was the *escape.*"]
import os
SPS=[float(x) for x in os.environ.get('SPS','1.22,1.2,1.2,1.18,1.18,1.16,1.18').split(',')]
out=[];SC=[];t=0.0;lead=.05
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/b{i}.wav'); a=tighten(a,sr,cap=.2)
    w=wave.open('vo/_t.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(a.clip(-32768,32767).astype(np.int16).tobytes());w.close()
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i','vo/_t.wav','-filter:a',f'atempo={SPS[i]}','vo/_t2.wav']);a,sr=load('vo/_t2.wav')
    vd=len(a)/sr
    d=lead+vd+(.15 if i==0 else .22)+(1.3 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
