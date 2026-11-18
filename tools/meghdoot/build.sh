python3 -c "s=open('meghdoot.src.html').read();s=s.replace('__TIMING__',open('vo/timing.json').read());open('meghdoot.html','w').write(s)"
