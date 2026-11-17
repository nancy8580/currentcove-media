import asyncio,sys,subprocess
from playwright.async_api import async_playwright
OUT=sys.argv[1];D='/home/claude/currentcove/cactus/';N=1416
async def main(st):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--allow-file-access-from-files"])
        pg=await b.new_page(viewport={"width":1080,"height":1920});pg.on("pageerror",lambda e:print("ERR",e))
        await pg.goto("file://"+D+"ov.html");await pg.wait_for_function("window.go===true",timeout=60000)
        if st:
            for k,t in enumerate(st):
                await pg.evaluate(f"frame({t})");await pg.screenshot(path=f"{D}ovs_{k}.png",omit_background=True)
                subprocess.run(["ffmpeg","-loglevel","error","-y","-ss",str(t),"-i",D+"orig.mp4","-i",f"{D}ovs_{k}.png","-filter_complex","[0:v][1:v]overlay,scale=270:-1","-frames:v","1",f"{D}chk_{k}.jpg"])
        else:
            f=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-i",D+"orig.mp4","-f","image2pipe","-framerate","30","-c:v","png","-i","-","-filter_complex","[0:v][1:v]overlay=eof_action=pass[v]","-map","[v]","-map","0:a","-c:v","libx264","-preset","veryfast","-crf","17","-pix_fmt","yuv420p","-c:a","copy",OUT],stdin=subprocess.PIPE)
            for i in range(N):
                await pg.evaluate(f"frame({i/30:.4f})");f.stdin.write(await pg.screenshot(type="png",omit_background=True))
            f.stdin.close();f.wait()
        await b.close()
asyncio.run(main([float(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else None))
