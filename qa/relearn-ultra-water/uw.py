# Stills + a short floater-impact clip from Humpalumps/Ultra-Water (MIT, read-only clone), SwiftShader.
import asyncio, os, subprocess
from playwright.async_api import async_playwright
URL = "http://127.0.0.1:15199/?desktop"
D = "/workspace/ink-fish/qa/relearn-ultra-water"
INIT = """(()=>{let t=1000;const q=[];let id=0;performance.now=()=>t;
window.requestAnimationFrame=cb=>{q.push([++id,cb]);return id};
window.__step=ms=>{t+=ms;const c=q.splice(0);c.forEach(e=>{try{e[1](t)}catch(x){console.error(x&&x.stack||x)}});};
let s=777;Math.random=()=>{s=(s*16807)%2147483647;return (s-1)/2147483646;};})();"""
HIDE = "document.querySelectorAll('.lil-gui, #hud, [id*=hud], .hud').forEach(e=>e.style.display='none')"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist","--hide-scrollbars"])
        pg = await b.new_page(viewport={"width": 800, "height": 500})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.add_init_script(INIT)
        await pg.goto(URL); await pg.wait_for_timeout(8000); await pg.evaluate(HIDE)
        for view, tag in (("Golden hour", "dark-ish-golden-hour"), ("Lagoon", "light-ish-lagoon")):
            await pg.evaluate(f"app.views[{view!r}]()")
            for i in range(3): await pg.evaluate("__step(1000/30)")
            await pg.screenshot(path=f"{D}/uw-{tag}.png", timeout=600000); print("still", tag, flush=True)
        await pg.evaluate("app.views['Flotsam']()")
        os.makedirs(f"{D}/frames-uw-flotsam", exist_ok=True)
        for i in range(48):            # 1.6 s at 30 fps: props fall, hit, ring out
            await pg.evaluate("__step(1000/30)")
            await pg.screenshot(path=f"{D}/frames-uw-flotsam/f{i:04d}.png", timeout=600000)
            print("flotsam", i, flush=True)
        print("errors:", errs, flush=True)
        await b.close()
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",f"{D}/frames-uw-flotsam/f%04d.png","-c:v","libx264","-pix_fmt","yuv420p","-crf","18",f"{D}/uw-flotsam-impacts.mp4"], check=True)
asyncio.run(main())
