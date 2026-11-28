import sys,json,wave,subprocess,numpy as np,os
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','boats','tow','fire','hits','end']
txt=["In 1971, India set Karachi's harbour on *fire,* with boats too small to even reach it.",
"Three tiny Soviet-built missile boats: Nipat, Nirghat and Veer. Built to guard the coast, their range was far too *short.*",
"So the Navy *towed* them from Bombay towards Karachi, with two bigger warships guarding them.",
"At 10:45 on the night of 4 December, the first Styx missile flew. A Pakistani destroyer thought it was a *plane,* and fired its anti-aircraft guns.",
"A destroyer, a minesweeper and a ship full of ammunition went down. Then a missile hit Karachi's oil *tanks.*",
"Not one Indian sailor was lost. That's why India celebrates Navy Day on 4 *December.* And three days later, they came back."]
SPS=[float(x) for x in os.environ.get('SPS','1.18,1.2,1.2,1.2,1.2,1.15').split(',')]
out=[];SC=[];t=0.0;lead=.05
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/b{i}.wav'); a=tighten(a,sr,cap=.2)
    w=wave.open('vo/_t.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(a.clip(-32768,32767).astype(np.int16).tobytes());w.close()
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i','vo/_t.wav','-filter:a',f'atempo={SPS[i]}','vo/_t2.wav']);a,sr=load('vo/_t2.wav')
    vd=len(a)/sr
    d=lead+vd+(.15 if i==0 else .22)+(1.4 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
