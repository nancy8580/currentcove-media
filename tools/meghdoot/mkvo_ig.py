import sys,json,wave,subprocess,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','order','leak','line','race','heli','hold','end']
src=[0,1,2,7,3,4,5,6]
txt=["A supplier in London accidentally gave away Pakistan's *secret* mountain plan.",
"In 1983, Pakistan ordered Arctic gear there, to seize the *Siachen* glacier.",
"But the same supplier also kitted out the Indian Army. And word reached *India.*",
"Why was it up for grabs? In 1949, the ceasefire line simply stopped, and said: thence north to the *glaciers.*",
"Pakistan's troops would move by April 17th. So India struck first: on the 13th, *Baisakhi.*",
"Tiny Cheetah helicopters couldn't land on the snow. So soldiers *jumped* from a hover.",
"By nightfall, about *300* Indian troops were dug into the high passes.",
"When Pakistan's troops finally climbed up, India was already on top. All because of an order for *winter gear.*"]
tempo=[1.22,1.16,1.16,1.14,1.16,1.16,1.14,1.14]
out=[];SC=[];t=0.0;lead=.08
for i,(k,s) in enumerate(zip(ids,txt)):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'vo/a{src[i]}.wav','-af',f'atempo={tempo[i]}','-ar','24000',f'vo/g{i}.wav'])
    a,sr=load(f'vo/g{i}.wav'); a=tighten(a,sr,cap=.2); vd=len(a)/sr
    d=lead+vd+.45+(1.5 if i==len(ids)-1 else 0)
    if i==0: d=lead+vd+.3
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice_ig.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing_ig.json','w'));[print(s[:5]) for s in SC];print(t)
