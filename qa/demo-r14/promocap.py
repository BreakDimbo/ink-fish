# r14: the promo capture script (inkfish-promo/scripts/cap.py) with the output dir and host made configurable; nothing else changed
# deterministic frame-by-frame capture (virtual clock + seeded Math.random), after ink-fish/qa/demo-r7/cap.py
import asyncio, sys, os, math, subprocess, shutil, json, importlib.util, time
from playwright.async_api import async_playwright
spec = importlib.util.spec_from_file_location("shots", os.environ.get("SHOTSPY", "/workspace/inkfish-promo/scripts/shots.py"))
S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
name = sys.argv[1]; shot = dict(S.SHOTS[name]); shot["url"] = shot["url"].replace("127.0.0.1:8765", os.environ["HOSTPORT"])
FPS = shot.get("fps", 30); N = int(shot["dur"] * FPS); vw, vh = shot["vp"]; dsf = shot.get("dsf", 2)
N = int(os.environ.get("NMAX", N))
OUT = os.environ["OUTDIR"] + "/" + name
INIT = """(()=>{let t=1000;const q=[];let id=0;
performance.now=()=>t;
window.requestAnimationFrame=cb=>{q.push([++id,cb]);return id};
window.cancelAnimationFrame=i=>{const k=q.findIndex(e=>e[0]===i);if(k>=0)q.splice(k,1)};
window.__step=ms=>{t+=ms;const c=q.splice(0);c.forEach(e=>{try{e[1](t)}catch(x){console.error(x&&x.stack||x)}});};
let s=%d;Math.random=()=>{s=(s*16807)%%2147483647;return (s-1)/2147483646;};
window.__errs=[];window.addEventListener('error',e=>__errs.push(String(e.message)));
})();""" % shot.get("seed", 12345)
async def main():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist","--hide-scrollbars"])
        ctx = await b.new_context(viewport={"width": vw, "height": vh}, device_scale_factor=dsf, color_scheme=shot.get("scheme", "light"))
        pg = await ctx.new_page()
        errs = []
        pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
        await pg.add_init_script(INIT)
        for pat, rep in shot.get("patch", []):
            def mk(rep):
                async def route(r):
                    resp = await r.fetch(); body = await resp.text()
                    for a, z in rep:
                        if a not in body: errs.append("PATCH MISS: " + a[:40])
                        body = body.replace(a, z)
                    await r.fulfill(response=resp, body=body)
                return route
            await pg.route(pat, mk(rep))
        await pg.goto(shot["url"]); await pg.wait_for_timeout(800)
        if shot.get("css"): await pg.add_style_tag(content=shot["css"])
        if shot.get("js"): await pg.evaluate(shot["js"])
        path = shot["path"]; x, y = path(-1)
        await pg.mouse.move(x, y)
        for i in range(shot.get("warm", 150)): await pg.evaluate("__step(1000/30)")
        await pg.wait_for_timeout(2600)  # CSS fade-in of canvases is wall-clock
        down = False; t0 = time.time()
        for i in range(N):
            t = i / FPS
            st = path(t); x, y = st[0], st[1]; want = len(st) > 2 and st[2]
            await pg.mouse.move(x, y)
            if want and not down: await pg.mouse.down(); down = True
            if not want and down: await pg.mouse.up(); down = False
            for ev in shot.get("events", []):
                if ev[0] == i: await pg.evaluate(ev[1])
            await pg.evaluate(f"__step(1000/{FPS})")
            await pg.screenshot(path=f"{OUT}/f{i:04d}.png", timeout=300000)
            if i == 4: print(name, "s/frame", round((time.time() - t0) / 5, 2), flush=True)
        print(name, "errors:", (errs + await pg.evaluate("__errs"))[:8], "time", round(time.time() - t0))
        await b.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{OUT}/f%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "12", "-preset", "slow", "-tune", "grain", os.environ["OUTDIR"] + f"/{name}.mp4"], check=True)
asyncio.run(main())
