import asyncio,sys,subprocess,json,time
from playwright.async_api import async_playwright
OUT=sys.argv[1];FPS=30;TOTAL=json.load(open('/root/ccm/tools/meghdoot/vo/timing_ig.json'))['TOTAL']
async def main(stills):
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--allow-file-access-from-files","--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
        pg=await b.new_page(viewport={"width":1080,"height":1920});pg.on("pageerror",lambda e:print("PAGEERR",e,flush=True));pg.on("console",lambda m:print("C",m.text,flush=True) if m.type=="error" else None)
        await pg.goto("file:///root/ccm/tools/meghdoot/meghdoot_ig.html");await pg.wait_for_function("window.go===true",timeout=60000)
        json.dump(await pg.evaluate("window.SFXL()"),open("/root/ccm/tools/meghdoot/vo/sfx_ig.json","w"))
        if stills:
            for k,tt in enumerate(stills):
                await pg.evaluate(f"window.frame({tt})");await pg.screenshot(path=f"{OUT}_{k:02d}.jpg",type="jpeg",quality=80)
        else:
            vid=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-","-c:v","libx264","-preset","veryfast","-crf","16","-pix_fmt","yuv420p",OUT],stdin=subprocess.PIPE)
            n=int(TOTAL*FPS);t0=time.time()
            for fr in range(n):
                await pg.evaluate(f"window.frame({fr/FPS:.4f})");vid.stdin.write(await pg.screenshot(type="jpeg",quality=90))
                if fr%150==0:print("frame",fr,n,round(time.time()-t0),flush=True)
            vid.stdin.close();vid.wait()
        await b.close()
st=[float(x) for x in sys.argv[2].split(",")] if len(sys.argv)>2 else None
asyncio.run(main(st))
