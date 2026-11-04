# Captures evanw/webgl-water (MIT, read-only clone) with deterministic frames: a press, then a drag.
import asyncio, sys, os, math, subprocess
from playwright.async_api import async_playwright
view = sys.argv[1]            # "oblique" (demo default) or "top" (top-down, closest to ink-fish)
URL = "http://127.0.0.1:18761/index.html"
OUT = f"/workspace/ink-fish/qa/relearn-ultra-water/frames-evw-{view}"
INIT = """(()=>{let t=1e12;const q=[];let id=0;
performance.now=()=>t; Date.prototype.getTime=function(){return t}; Date.now=()=>t;
window.requestAnimationFrame=cb=>{q.push([++id,cb]);return id};
window.__step=ms=>{t+=ms;const c=q.splice(0);c.forEach(e=>{try{e[1](t)}catch(x){console.error(x&&x.stack||x)}});};
let s=12345;Math.random=()=>{s=(s*16807)%2147483647;return (s-1)/2147483646;};})();"""
N = 90
def path(t, W, H):
    cx, cy = (W * 0.5, H * 0.55) if view == 'top' else (600, 215)
    if t < 0.2: return None
    if t < 0.5: return (cx - 120, cy, True)                 # press and hold
    if t < 0.8: return (cx - 120, cy, False)
    if t < 1.6: u = (t - 0.8) / 0.8; return (cx - 200 + 400 * u, cy + 60 - 120 * u, True) if view == 'top' else (cx - 260 + 300 * u, cy + 30 - 40 * u, True)  # drag ~560 px/s
    return (cx + 200, cy - 60, False)
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist","--hide-scrollbars"])
        pg = await b.new_page(viewport={"width": 960, "height": 600})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.add_init_script(INIT)
        await pg.goto(URL); await pg.wait_for_timeout(1500)
        await pg.evaluate("document.getElementById('help').style.display='none'; dispatchEvent(new Event('resize'))")
        if view == "top": await pg.evaluate("angleX=-89.9; angleY=-180")
        W, H = 960, 600
        for i in range(20): await pg.evaluate("__step(1000/30)")
        down = False
        for i in range(N):
            q = path(i / 30, W, H)
            if q:
                x, y, pr = q
                if pr and not down: await pg.mouse.move(x, y); await pg.mouse.down(); down = True
                elif pr: await pg.mouse.move(x, y)
                if not pr and down: await pg.mouse.up(); down = False
            await pg.evaluate("__step(1000/30)")
            await pg.screenshot(path=f"{OUT}/f{i:04d}.png", timeout=180000)
            if i % 10 == 0: print(view, i, flush=True)
        print(view, "errors:", errs, flush=True)
        await b.close()
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",f"{OUT}/f%04d.png","-c:v","libx264","-pix_fmt","yuv420p","-crf","18",f"/workspace/ink-fish/qa/relearn-ultra-water/evanw-{view}-press-drag.mp4"], check=True)
asyncio.run(main())
