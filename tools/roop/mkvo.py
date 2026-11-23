import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','found','hail','dna','twist','end']
txt=["There's a lake in the Himalayas filled with human *skeletons.*",
"In 1942, a forest ranger found hundreds of bones at Roopkund, five thousand metres up. Some feared they were Japanese *soldiers.*",
"For decades, the answer seemed simple: pilgrims, killed in one freak *hailstorm.*",
"Then in 2019, scientists read the DNA of 38 skeletons. Twenty-three were South Asian, and died around *800* *AD.*",
"But fourteen had roots in the eastern Mediterranean, like Greece and Crete. And they died around *1800.*",
"A thousand years apart, in the same frozen lake. And nobody knows how they got *there.*"]
SP=float(sys.argv[1]) if len(sys.argv)>1 else 1.0
out=[];SC=[];t=0.0;lead=.06
for i,(k,s) in enumerate(zip(ids,txt)):
    a,sr=load(f'vo/b{i}.wav'); a=tighten(a,sr,cap=.22)
    if SP!=1.0:
        import subprocess,tempfile
        wave_tmp='vo/_t.wav';w=wave.open(wave_tmp,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(a.clip(-32768,32767).astype(np.int16).tobytes());w.close()
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',wave_tmp,'-filter:a',f'atempo={SP}','vo/_t2.wav']);a,sr=load('vo/_t2.wav')
    vd=len(a)/sr
    d=lead+vd+(.22 if i==0 else .34)+(1.3 if i==len(ids)-1 else 0)
    seg=np.zeros(int(d*sr)); seg[int(lead*sr):int(lead*sr)+len(a)]=a; out.append(seg)
    SC.append([k,round(t,3),round(t+d,3),round(t+lead,3),round(vd,3),s]); t+=d
y=np.concatenate(out).clip(-32768,32767).astype(np.int16)
w=wave.open('vo/voice.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes())
json.dump({'SC':SC,'TOTAL':round(t,3)},open('vo/timing.json','w'));[print(s[:5]) for s in SC];print(t)
