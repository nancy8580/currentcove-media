import sys,json,wave,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','everest','bulge','chimb','reveal','history','loop']
txt=["Which mountain is closest to space? It's not Everest.",
"Everest is the tallest above sea level, nearly nine kilometres up. But Earth isn't a perfect ball. It spins, and that spin makes it bulge at the middle.",
"So the ground at the equator sits about twenty-one kilometres farther from Earth's centre than the poles.",
"Now meet Chimborazo, a volcano in Ecuador, just one degree south of the equator. It's about two and a half kilometres shorter than Everest.",
"But it stands right on top of the bulge. So its summit is over two kilometres farther from Earth's centre than Everest's.",
"People once thought it was the highest mountain in the world. In 1802, Humboldt climbed to about five thousand nine hundred metres, a record back then.",
"So the peak nearest the stars isn't the tallest one. Next time someone says Everest, just ask them:"]
out=[];SC=[];t=0.15;sr=None
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/v{i+1}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    if i==0: out.append(np.zeros(int(.15*sr)))
    d=vd+.7+(1.6 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[:len(a)]=a; out.append(seg)
    SC.append([k,round(t if i else 0,3),round(t+d,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));print(json.dumps(SC,indent=0),t,sr)
