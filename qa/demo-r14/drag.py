# r14 copy of demo-r13/drag.py (output to demo-r14; + kind jclick)
# deterministic press-and-drag capture (virtual clock, seeded random, 30 fps = real time)
# usage: drag.py URL light|dark NAME KIND [N]   KIND: slow | fast | combo | full | tap | measure | still
#   MEASURE=1 → no fish/koi (water only), for diffing against a 'still' baseline
import asyncio, sys, os, math, subprocess, shutil
from playwright.async_api import async_playwright
url, theme, name, kind = sys.argv[1:5]
N = int(sys.argv[5]) if len(sys.argv) > 5 else 300
OUT = f"/workspace/ink-fish-r14/qa/demo-r14/frames/{name}"
INIT = """(()=>{let t=1000;const q=[];let id=0;
performance.now=()=>t;
window.requestAnimationFrame=cb=>{q.push([++id,cb]);return id};
window.cancelAnimationFrame=i=>{const k=q.findIndex(e=>e[0]===i);if(k>=0)q.splice(k,1)};
window.__step=ms=>{t+=ms;const c=q.splice(0);c.forEach(e=>{try{e[1](t)}catch(x){console.error(x&&x.stack||x)}});};
const _st=window.setTimeout;window.setTimeout=(f,ms,...a)=>_st(f,0,...a);
let s=12345;Math.random=()=>{s=(s*16807)%2147483647;return (s-1)/2147483646;};
window.__errs=[];window.addEventListener('error',e=>__errs.push(String(e.message)));
})();"""
def ss(u): return u * u * (3 - 2 * u)
# returns (x, y, pressed) at t seconds
def path(t):
    if kind == "slow":   # ~200 px/s (≈12 cm/s at 16.7 px/cm: below the 23 cm/s minimum phase speed)
        if t < 0.5: return (300, 430, False)
        if t < 4.5: u = (t - 0.5) / 4; return (300 + 800 * u, 430 - 50 * math.sin(u * math.pi), True)
        return (1100, 430, False)
    if kind == "fast":   # ~1200 px/s (≈70 cm/s: a Kelvin-type wedge regime)
        if t < 0.5: return (280, 470, False)
        if t < 1.2: u = (t - 0.5) / 0.7; return (280 + 860 * u, 470 - 140 * u, True)
        return (1140, 330, False)
    if kind == "combo":  # slow stroke, then a fast flick (10 s)
        if t < 0.5: return (300, 380, False)
        if t < 4.5: u = (t - 0.5) / 4; return (300 + 800 * u, 380 - 50 * math.sin(u * math.pi), True)
        if t < 5.5: u = (t - 4.5); return (1100 - 820 * ss(u), 380 + 160 * ss(u), False)
        if t < 6.0: return (280, 540, False)
        if t < 6.7: u = (t - 6.0) / 0.7; return (280 + 860 * u, 540 - 120 * u, True)
        return (1140, 420, False)
    if kind == "full":  # press+hold, slow drag, lift; hover; press, fast flick, lift (10 s)
        if t < 0.5: return (320, 400, False)
        if t < 1.3: return (320, 400, True)
        if t < 4.0: u = (t - 1.3) / 2.7; return (320 + 560 * u, 400 - 40 * math.sin(u * math.pi), True)
        if t < 5.2: u = (t - 4.0) / 1.2; return (880 - 600 * ss(u), 400 + 150 * ss(u), False)
        if t < 5.7: return (280, 550, False)
        if t < 5.9: return (280, 550, True)
        if t < 6.6: u = (t - 5.9) / 0.7; return (280 + 860 * u, 550 - 120 * u, True)
        return (1140, 430, False)
    if kind == "click":  # a click (0.12 s) at one spot, then a still press-and-hold (1 s) at another (6 s)
        return (700, 330, 0.5 <= t < 0.62 or 2.6 <= t < 3.6)  # one spot: no hover rings from travel
    if kind == "jclick":  # promo-style: the pointer jumps onto the spot as it clicks (as in the film), then a 1 s hold there
        return None if t < 0.5 else (700, 330, 0.5 <= t < 0.62 or 2.6 <= t < 3.6)
    if kind == "tap":   # press and hold 1.9 s at one spot (press packet, then the dimple alone), lift (release packet)
        return (700, 290, t < 2.0)
    if kind == "measure":  # a straight horizontal stroke at 1600 px/s, y = 450
        if t < 0.3: return (200, 450, False)
        if t < 0.8: u = (t - 0.3) / 0.5; return (200 + 800 * u, 450, True)
        return (1000, 450, False)
    return None  # still: the pointer never enters
async def main():
    os.makedirs(OUT, exist_ok=True)  # frames are overwritten in place, never removed
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist","--hide-scrollbars"])
        pg = await b.new_page(viewport={"width": 1440, "height": 900}, color_scheme=theme)
        errs = []
        pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
        await pg.add_init_script(INIT)
        async def route(r):
            resp = await r.fetch(); body = await resp.text()
            body = body.replace('water: "real",', 'water: "real", adaptive: false,')
            if os.environ.get("FLAT"): body = body.replace('water: "real", adaptive: false,', 'water: "flat",')
            if os.environ.get("MEASURE"): body = body.replace("koi: true,", "koi: false, opacity: 0, shadow: 0,")
            await r.fulfill(response=resp, body=body)
        await pg.route("**/index.html", route)
        if os.environ.get("PATCHJS"):  # JSON [[from, to], ...] applied to src/ink-fish.js (diagnostic variants)
            import json
            PJ = json.loads(os.environ["PATCHJS"])
            async def rjs(r):
                resp = await r.fetch(); body = await resp.text()
                for x, y in PJ:
                    assert x in body, x
                    body = body.replace(x, y)
                await r.fulfill(response=resp, body=body)
            await pg.route("**/src/ink-fish.js*", rjs)
        await pg.goto(url); await pg.wait_for_timeout(600)
        if kind == "click":  # park the pointer first; its hover ring dies out during the warm-up
            q0 = path(0); await pg.mouse.move(q0[0], q0[1])
        for i in range(150): await pg.evaluate("__step(1000/30)")
        await pg.wait_for_timeout(2600)
        down = False
        for i in range(N):
            t = i / 30; q = path(t)
            if q:
                x, y, pr = q
                await pg.mouse.move(x, y)
                if pr and not down: await pg.mouse.down(); down = True
                if not pr and down: await pg.mouse.up(); down = False
            await pg.evaluate("__step(1000/30)")
            await pg.screenshot(path=f"{OUT}/f{i:04d}.png", timeout=180000)
        print(name, "errors:", errs + await pg.evaluate("__errs"), "water:", await pg.evaluate("document.body.__inkFish.water"))
        await b.close()
    if not os.environ.get("NOVIDEO"):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", f"{OUT}/f%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "slow", f"/workspace/ink-fish-r14/qa/demo-r14/{name}.mp4"], check=True)
asyncio.run(main())
