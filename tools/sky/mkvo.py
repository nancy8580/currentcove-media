import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','white','scatter','sky','violet','sunset','loop']
txt=["Why is the sky blue, but sunsets orange?",
"Sunlight looks white, but it's actually every colour of the rainbow, mixed together.",
"When it hits our air, tiny nitrogen and oxygen molecules scatter it in every direction. And short blue waves get scattered about six times more than long red ones.",
"So blue light bounces all over the sky, and wherever you look, blue reaches your eyes.",
"Why not violet? The sun sends less of it, and our eyes are much less sensitive to it.",
"But at sunset, sunlight crosses up to thirty-eight times more air to reach you. Most of the blue is scattered away on the journey.",
"Only the oranges and reds survive. Same sunlight, same air, just a longer road. That's why the sky is blue, but sunsets glow orange."]
out=[];SC=[];t=0.15;sr=24000;out.append(np.zeros(int(.15*sr)))
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/v{i+1}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    d=vd+.7+(1.6 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[:len(a)]=a; out.append(seg)
    SC.append([k,round(t if i else 0,3),round(t+d,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));print(json.dumps(SC,indent=0),t)
