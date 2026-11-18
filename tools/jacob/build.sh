python3 -c "s=open('jacob.src.html').read();s=s.replace('__TIMING__',open('vo/timing.json').read());open('jacob.html','w').write(s)"
