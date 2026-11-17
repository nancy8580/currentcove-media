python3 -c "s=open('cactus.src.html').read();s=s.replace('__TIMING__',open('vo/timing.json').read());open('cactus.html','w').write(s)"
