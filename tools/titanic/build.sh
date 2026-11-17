python3 -c "s=open('titanic.src.html').read();s=s.replace('__TIMING__',open('vo/timing.json').read());open('titanic.html','w').write(s)"
