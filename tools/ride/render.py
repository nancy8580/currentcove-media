import asyncio, subprocess, sys, os
from playwright.async_api import async_playwright
H=os.path.abspath(os.path.join(os.path.dirname(__file__),'anim.html')); OUT=sys.argv[1]; FPS=30
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--allow-file-access-from-files"])
        pg=await b.new_page(viewport={"width":1080,"height":1920}); pg.on("pageerror",lambda e:print("ERR",e))
        await pg.goto("file://"+H); await pg.wait_for_function("window.go===true")
        if os.path.exists(os.path.join(os.path.dirname(H),"vo/timing.json")):
            import json; tj=json.load(open(os.path.join(os.path.dirname(H),"vo/timing.json"))); await pg.evaluate(f"SC={json.dumps(tj['SC'])}; window.TOTAL={tj['TOTAL']}")
        T=await pg.evaluate("window.TOTAL")
        if "--stills" in sys.argv:
            for i,t in enumerate([4,11,14,19,22,26,30,32,37,40,45,47,50]):
                await pg.evaluate(f"frame({t})"); await pg.screenshot(path=f"{OUT}_{i:02d}.jpg",type="jpeg",quality=70)
        else:
            v=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-","-c:v","libx264","-preset","veryfast","-crf","16","-pix_fmt","yuv420p",OUT],stdin=subprocess.PIPE)
            for fr in range(int(T*FPS)):
                await pg.evaluate(f"frame({fr/FPS:.4f})"); v.stdin.write(await pg.screenshot(type="jpeg",quality=92))
            v.stdin.close(); v.wait()
        await b.close()
asyncio.run(main())
