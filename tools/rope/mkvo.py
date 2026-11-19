import sys,json,wave,numpy as np
sys.path.insert(0,'/root/ccm/tools'); from tight import load,tighten
ids=['hook','rope','byline','hoax','reward','end']
txt=["India's most famous magic trick was invented in a Chicago *newsroom.*",
"August 1890. The Chicago Tribune reports a magician who throws a rope into the sky. A boy climbs it, and *vanishes.*",
"The writer's name? Fred S. Ellmore. Say it fast: *sell* *more.*",
"Papers across America and Europe reprinted it. Four months later, the Tribune admitted it was a *hoax.* Hardly anyone noticed.",
"By 1934, London's Magic Circle offered a reward for one outdoor performance. Nobody ever *claimed* it.",
"And the reporter who made it up, John Wilkie? He went on to run the U.S. *Secret* *Service.*"]
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
