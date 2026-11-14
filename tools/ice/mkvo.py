import sys,json,wave,numpy as np
sys.path.insert(0,'..'); from tight import load,tighten
ids=['hook','dense','liquid','hex','berg','lake']
txt=["Ice is just frozen water. So why doesn't it sink in water?",
"Most things get denser when they freeze. Water does the opposite. Ice is about nine percent less dense than liquid water.",
"Here's why. In liquid water, the molecules tumble around and pack in close together.",
"But when water freezes, hydrogen bonds lock every molecule into a hexagon, with empty space in the middle. Same molecules, more room.",
"That's why about ninety percent of an iceberg hides below the waterline.",
"And it's why lakes freeze from the top down, so fish can survive the winter underneath. Follow Current Cove for more everyday science."]
out=[];SC=[];t=0.3;sr=24000;out.append(np.zeros(int(.3*sr)))
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/v{i+1}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    d=vd+.85+(1.8 if i==5 else 0)
    seg=np.zeros(int(d*sr)); seg[:len(a)]=a; out.append(seg)
    SC.append([k,round(t if i else 0,3),round(t+d,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));print(SC,t)
