import sys,json,wave,numpy as np,subprocess
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','gift','study','beam','inside','found','end']
txt=["For seven years, a wooden gift *spied* on America's ambassador.",
"Moscow, 1945. A Soviet children's group, the Young Pioneers, gives the US ambassador a hand-carved *Great Seal.*",
"He hangs it in his study. No battery. No wires. *Nothing* for a bug sweep to find.",
"But when the Soviets beamed radio waves at the house, the carving woke up, and *broadcast* every word.",
"Inside was a tiny metal capsule, just 31 grams, designed by Léon *Theremin,* the inventor of an eerie electronic instrument.",
"In 1952, American security finally *found* it. In 1960, the US held it up at the United Nations.",
"They called it, *The* *Thing.* So next time someone hands you a gift, remember:"]
AT=float(sys.argv[1]) if len(sys.argv)>1 else 1.1
out=[];SC=[];t=0.0;sr=24000;lead=.12
for i,(k,s) in enumerate(zip(ids,txt)):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'vo/f{i}.wav','-af',f'atempo={AT*(1.08 if i==0 else 1)}','-ar','24000','-ac','1',f'vo/t{i}.wav'])
    a,sr=load(f'vo/t{i}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    d=lead+vd+.6+(1.6 if i==len(ids)-1 else 0)
    if i==0: d=lead+vd+.45
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
