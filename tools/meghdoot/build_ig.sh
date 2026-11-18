python3 -c "s=open('meghdoot.src.html').read();s=s.replace('__TIMING__',open('vo/timing_ig.json').read());open('meghdoot_ig.html','w').write(s)"
