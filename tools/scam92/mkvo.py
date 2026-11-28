import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','slip','fake','boom','bull','crash','end']
txt=["In 1992, one man drained 4,000 crore rupees from India's banks, with *paper.*",
"Banks lent each other cash through brokers, against government bonds. The proof was a slip called a bank *receipt.*",
"But a few small banks would issue those receipts with no bonds behind them. Fake paper, real *money.*",
"The money poured into shares. ACC jumped from about 200 rupees to nearly 9,000 in three *months.*",
"They called Harshad Mehta the Big Bull. Then, in April 1992, journalist Sucheta Dalal exposed the *trick.*",
"Banks asked for their bonds. There were none. The market crashed from 4,500 to *2,500.*",
"He was convicted, and died in custody in 2001. And it all began with a slip of *paper.*"]
import os
SPS=[float(x) for x in os.environ.get('SPS','1.25,1.32,1.32,1.32,1.32,1.3,1.25').split(',')]
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
