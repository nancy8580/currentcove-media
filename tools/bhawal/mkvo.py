import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','death','pyre','ghat','wife','court','end']
txt=["In 1909, a prince of Bengal was declared dead. Eleven years later, he came *back.*",
"Kumar Ramendra Narayan Roy, of the rich Bhawal estate, fell ill in Darjeeling, and was reported dead at just *25.*",
"His story? A hailstorm hit the funeral pyre, the mourners ran for shelter, and his body *vanished.*",
"In 1920, an ash-covered holy man sat by the river in Dhaka. People swore it was the *prince.*",
"His own wife called him an *impostor.* So in 1930, he went to court to prove who he was.",
"After hundreds of witnesses, a Dhaka judge ruled in 1936: he is the *prince.* The High Court agreed.",
"In July 1946, the Privy Council in London gave the final yes. Two days later, he was *dead.* And his wife never believed him."]
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
