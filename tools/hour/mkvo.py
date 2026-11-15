import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','base60','why60','hands','egypt','ptolemy','france','loop']
txt=["Your clock is still counting in ancient Babylonian.",
"About four thousand years ago, the Sumerians and Babylonians counted in sixties, not tens.",
"Because sixty splits perfectly into halves, thirds, quarters, fifths and sixths. Ten can't even make a clean third.",
"One theory: count the twelve finger joints of one hand with your thumb, and track each dozen on the other hand's five fingers. Twelve times five is sixty.",
"Egyptians split daylight into twelve parts and the night into twelve more. That's our twenty-four hours.",
"Then astronomers like Ptolemy cut each degree into sixty small parts, the first minute parts, and each of those into sixty again, the second. Minute. Second.",
"In 1793, France tried a ten-hour day, with a hundred minutes in every hour. Less than eighteen months later, it was quietly dropped.",
"Sixty just worked too well. So the next time you check the time, remember:"]
out=[];SC=[];t=0.15;sr=24000;out.append(np.zeros(int(.15*sr)))
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/v{i+1}.wav'); a=tighten(a,sr,cap=.4); vd=len(a)/sr
    d=vd+.7+(1.6 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[:len(a)]=a; out.append(seg)
    SC.append([k,round(t if i else 0,3),round(t+d,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));print(json.dumps(SC,indent=0),t)
