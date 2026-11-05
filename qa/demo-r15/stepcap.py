# r15 · device-equivalent capture: the page's clock is stepped by exactly 1000/HZ ms per frame and the frames are
# encoded at HZ fps, so the video plays at true wall-clock speed for a HZ display (each library frame sees dt = 1/HZ s,
# as on a device that keeps up). Validated against the box's wall-clock capture (livecap.py ÷ its sim/wall ratio).
# usage: stepcap.py URL light|dark NAME KIND DUR [HZ]   KIND: jclick | moveclick | drag | hold | still
import asyncio, sys, os, json, subprocess, math
from playwright.async_api import async_playwright
url, theme, name, kind = sys.argv[1:5]; DUR = float(sys.argv[5]); HZ = int(sys.argv[6]) if len(sys.argv) > 6 else 60
OUT = f"/workspace/r15tmp/step/{name}"; os.makedirs(OUT, exist_ok=True)
INIT = """(()=>{let t=1000;const q=[];let id=0;performance.now=()=>t;
window.requestAnimationFrame=cb=>{q.push([++id,cb]);return id};
window.cancelAnimationFrame=i=>{const k=q.findIndex(e=>e[0]===i);if(k>=0)q.splice(k,1)};
window.__step=ms=>{t+=ms;const c=q.splice(0);c.forEach(e=>{try{e[1](t)}catch(x){console.error(x&&x.stack||x)}});};
const _st=window.setTimeout;window.setTimeout=(f,ms,...a)=>_st(f,0,...a);
let s=12345;Math.random=()=>{s=(s*16807)%2147483647;return (s-1)/2147483646;};})();"""
X, Y = 700, 330; PRE = 0.5
def path(t):  # t from the press (s); None = pointer untouched
    if kind == "jclick": return None if t < 0 else (X, Y, t < 0.12)
    if kind == "moveclick":
        if t < -0.6: return (X - 300, Y + 150, False)
        if t < 0: u = (t + 0.6) / 0.6; return (X - 300 + 300 * u, Y + 150 - 150 * u, False)
        return (X, Y, t < 0.12)
    if kind == "hold": return None if t < 0 else (X, Y, t < 1.0)
    if kind == "drag":  # press, then a slow stroke ~200 px/s for 2 s, lift
        if t < 0: return None
        if t < 0.15: return (X - 300, Y, True)
        if t < 2.15: return (X - 300 + 400 * (t - 0.15) / 2, Y, True)
        return (X + 100, Y, False)
    if kind == "flick":  # press, a fast 1200 px/s stroke, lift
        if t < 0: return None
        if t < 0.1: return (X - 400, Y + 100, True)
        if t < 0.8: u = (t - 0.1) / 0.7; return (X - 400 + 840 * u, Y + 100 - 140 * u, True)
        return (X + 440, Y - 40, False)
    return None
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist","--hide-scrollbars"])
        pg = await b.new_page(viewport={"width": int(os.environ.get("VW", 1440)), "height": int(os.environ.get("VH", 900))}, color_scheme=theme)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.add_init_script(INIT)
        async def route(r):
            resp = await r.fetch(); body = await resp.text()
            body = body.replace('water: "real",', 'water: "real", adaptive: false,')
            if os.environ.get("MEASURE"): body = body.replace("koi: true,", "koi: false, opacity: 0, shadow: 0,")
            await r.fulfill(response=resp, body=body)
        await pg.route("**/index.html", route)
        await pg.goto(url); await pg.wait_for_timeout(600)
        for i in range(int(3 * HZ)): await pg.evaluate("__step(%f)" % (1000 / HZ))
        await pg.wait_for_timeout(2500)  # idle callbacks (the promo kernel table)
        n0 = int(-PRE * HZ); down = False; k = 0
        if kind == "moveclick": n0 = int(-1.0 * HZ)
        for i in range(n0, int(DUR * HZ)):
            t = i / HZ; q = path(t)
            if q:
                x, y, pr = q; await pg.mouse.move(x, y)
                if pr and not down: await pg.mouse.down(); down = True
                if not pr and down: await pg.mouse.up(); down = False
            await pg.evaluate("__step(%f)" % (1000 / HZ))
            await pg.screenshot(path=f"{OUT}/f{k:04d}.png", type="png"); k += 1
        json.dump(dict(hz=HZ, t0=n0 / HZ, n=k, errors=errs, water=await pg.evaluate("document.body.__inkFish.water")), open(f"{OUT}/meta.json", "w"))
        print(name, "frames", k, "t0", n0 / HZ, "errors", errs, "water", await pg.evaluate("document.body.__inkFish.water"))
        await b.close()
    if os.environ.get("VIDEO"):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(HZ), "-i", f"{OUT}/f%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", f"{OUT}.mp4"], check=True)
asyncio.run(main())
