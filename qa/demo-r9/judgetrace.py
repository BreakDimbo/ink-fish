# frame-by-frame trace of the first seconds (real clock, SwiftShader, adaptive on): gap, library ms, water state, for both builds
import asyncio, json, sys
from playwright.async_api import async_playwright
BASE = "http://127.0.0.1:8733/"
BUILDS = {"v1.3.1": "qa/demo-r9/base/index.html", "v1.4": "index.html"}
PROBE = """addEventListener('DOMContentLoaded',()=>{window.__fr=[];const t0=performance.now();let l=0,k=0;(function f(t){const a=document.body.__inkFish;
if(a){const n=a.stats.n;if(n!==k){k=n;__fr.push([Math.round(t-t0),Math.round(t-l),+a.stats.ring[(n-1)%600].toFixed(1),a.water[0]+(a.stats.wq||0),a.stats.gw.prof])}}l=t;if(t-t0<9000)requestAnimationFrame(f)})(performance.now())})"""
async def main():
    w = int(sys.argv[1]) if len(sys.argv) > 1 else 1440; cpu = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--hide-scrollbars"])
        for ver, path in BUILDS.items():
            ctx = await b.new_context(viewport={"width": w, "height": 900 if w == 1440 else 844}, device_scale_factor=1); pg = await ctx.new_page()
            cdp = await ctx.new_cdp_session(pg); await cdp.send("Emulation.setCPUThrottlingRate", {"rate": cpu})
            await pg.goto(BASE + "qa/demo-r9/blank.html"); await pg.evaluate("sessionStorage.clear()")
            await pg.add_init_script(PROBE); await pg.goto(BASE + path); await pg.wait_for_timeout(9500)
            fr = await pg.evaluate("__fr"); await ctx.close()
            print(ver, len(fr), "frames"); out = []; pp = 0
            for t, g, m, s, pr in fr[:160]: out.append(f"{t}:{g}/{m}{s}" + ("P" if pr != pp else "")); pp = pr
            print("  " + " ".join(out), flush=True)
        await b.close()
asyncio.run(main())
