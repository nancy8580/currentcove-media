import asyncio, subprocess, sys, os, json
from playwright.async_api import async_playwright
H=os.path.abspath('bhawal.html'); OUT=sys.argv[1]; FPS=30; tj=json.load(open('vo/timing.json'))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--allow-file-access-from-files"])
        pg=await b.new_page(viewport={"width":1080,"height":1920}); pg.on("pageerror",lambda e:print("ERR",e)); pg.on("console",lambda m:print("CON",m.text) if m.type=="error" else None)
        await pg.goto("file://"+H); await pg.wait_for_function("window.go===true",timeout=30000)
        await pg.evaluate(f"setT({json.dumps(tj['SC'])},{tj['TOTAL']})"); T=tj['TOTAL']
        json.dump(await pg.evaluate("getSFX()"),open("vo/sfx.json","w"))
        if "--stills" in sys.argv:
            ts=[float(x) for x in sys.argv[3].split(',')]
            for i,t in enumerate(ts):
                try: await pg.evaluate(f"frame({t})")
                except Exception as e: print("FAIL",t,str(e)[:300])
                await pg.screenshot(path=f"{OUT}_{i:02d}.jpg",type="jpeg",quality=70)
        else:
            v=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-","-c:v","libx264","-preset","veryfast","-crf","16","-pix_fmt","yuv420p",OUT],stdin=subprocess.PIPE)
            for fr in range(int(T*FPS)):
                await pg.evaluate(f"frame({fr/FPS:.4f})"); v.stdin.write(await pg.screenshot(type="jpeg",quality=92))
            v.stdin.close(); v.wait()
        await b.close()
asyncio.run(main())
