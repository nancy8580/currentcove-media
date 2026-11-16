import sys,json,wave,numpy as np
sys.path.insert(0,'/home/claude/currentcove-media/tools'); from tight import load,tighten
ids=['hook','rain','rock','river','sun','pile','loop']
txt=["The sea is salty because of the rain.",
"As rain falls, it picks up carbon dioxide from the air, which makes it very slightly acidic.",
"That weak acid slowly eats away at rocks, dissolving tiny bits of salt and minerals.",
"Rivers carry those salts to the sea, about four billion tonnes every year. In a river, it's far too little to taste.",
"But when the sun evaporates seawater, only the water rises. The salt stays behind, and over millions of years, it piled up.",
"Today, every litre of seawater holds about thirty-five grams of salt. Spread all of it over the land, and the pile would be taller than a forty-storey building.",
"So who salted the ocean? The answer falls from the sky."]
out=[];SC=[];t=0.15;sr=24000;out.append(np.zeros(int(.15*sr)))
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/v{i+1}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    d=vd+.7+(1.6 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[:len(a)]=a; out.append(seg)
    SC.append([k,round(t if i else 0,3),round(t+d,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));print(json.dumps(SC,indent=0),t)
