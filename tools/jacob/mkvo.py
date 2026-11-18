import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','offer','nope','court','shoe','desk','vault']
txt=["A diamond bigger than the Kohinoor was once used as a *paperweight.*",
"In 1891, a jeweller named Jacob offered it to the Nizam of Hyderabad, for *50 lakh* rupees.",
"The Nizam paid a huge deposit, held the stone, and said: *na pasand.* Not liked.",
"Jacob refused to refund him. The fraud case reached *Calcutta.* Jacob was acquitted, but it ruined him.",
"The Nizam kept the diamond, wrapped it in a rag, and pushed it into an old *shoe.*",
"Years later, his son found it in the toe, and put it on his desk, as a *paperweight.*",
"In 1995, India bought it. Today, that paperweight sits in a *Reserve Bank* vault in Mumbai."]
tempo=[1.24,1.2,1.2,1.2,1.18,1.18,1.16]
out=[];SC=[];t=0.0;lead=.08
for i,(k,s) in enumerate(zip(ids,txt)):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'vo/a{i}.wav','-af',f'atempo={tempo[i]}','-ar','24000',f'vo/f{i}.wav'])
    a,sr=load(f'vo/f{i}.wav'); a=tighten(a,sr,cap=.2); vd=len(a)/sr
    d=lead+vd+.42+(1.5 if i==len(ids)-1 else 0)
    if i==0: d=lead+vd+.3
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
