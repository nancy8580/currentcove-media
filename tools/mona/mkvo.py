import sys,json,wave,numpy as np,subprocess
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','heist','suspects','thief','trunk','florence','end']
txt=["In 1911, someone stole the Mona Lisa, and nobody noticed for a *day.*",
"The Louvre was closed that Monday. A man in a white worker's *smock* lifted her off the wall, dumped the frame on a stairway, and walked out.",
"Police even questioned *Picasso.* And thousands queued, just to stare at the empty wall.",
"The thief was Vincenzo Peruggia, a former Louvre worker who had helped build her glass case. He even left a *thumbprint* on it.",
"For 28 months, she was gone, hidden in a *trunk* in his room in Paris.",
"In 1913, he took her to Florence and asked a dealer for 500,000 lire. The dealer called the *police.*",
"And here's the twist. The theft is what made her the most *famous* painting on Earth."]
AT=float(sys.argv[1]) if len(sys.argv)>1 else 1.12
out=[];SC=[];t=0.0;sr=24000;lead=.12
for i,(k,s) in enumerate(zip(ids,txt)):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'vo/f{i}.wav','-af',f'atempo={AT*(1.13 if i==0 else 1)}','-ar','24000','-ac','1',f'vo/t{i}.wav'])
    a,sr=load(f'vo/t{i}.wav'); a=tighten(a,sr,cap=.35); vd=len(a)/sr
    d=lead+vd+.6+(1.6 if i==len(ids)-1 else 0)
    if i==0: d=lead+vd+.45
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
