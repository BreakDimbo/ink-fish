# adaptive fallback trigger time on the real clock (SwiftShader, default options, adaptive on), v1.3.1 vs v1.4 interleaved
import asyncio, json, os, sys
from playwright.async_api import async_playwright
BASE = "http://127.0.0.1:8733/"
BUILDS = {"v1.3.1": "qa/demo-r9/base/index.html", "v1.4": "index.html"}
POLL = """(()=>{window.__jt=[];const t0=performance.now();let k='';(function f(){const a=document.body.__inkFish;if(a){const s=a.water+'/q'+(a.stats.wq||0);if(s!==k){k=s;__jt.push([Math.round(performance.now()-t0),s])}}if(performance.now()-t0<14000)setTimeout(f,50)})()})()"""
async def run(b, ver, w, h, cpu):
    ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
    pg = await ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    cdp = await ctx.new_cdp_session(pg)
    await cdp.send("Emulation.setCPUThrottlingRate", {"rate": cpu})
    await pg.goto(BASE + "qa/demo-r9/blank.html"); await pg.evaluate("sessionStorage.clear()")
    await pg.add_init_script("addEventListener('DOMContentLoaded',()=>{" + POLL + "})")
    await pg.goto(BASE + BUILDS[ver]); await pg.wait_for_timeout(14500)
    tr = await pg.evaluate("__jt"); await ctx.close()
    fb = next((t for t, s in tr if s.startswith("fallback")), None)
    return {"ver": ver, "size": w, "cpu": cpu, "fallback_ms": fb, "trace": tr, "errs": errs}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--hide-scrollbars"])
        for (w, h) in [(1440, 900), (390, 844)] if os.environ.get("SIZES", "1440,390") == "1440,390" else [(int(x), 900 if x == "1440" else 844) for x in os.environ["SIZES"].split(",")]:
            for cpu in [int(c) for c in os.environ.get("CPUS", "1,4").split(",")]:
                for rep in range(int(os.environ.get("REPS", "3"))):
                    for ver in BUILDS:
                        r = await asyncio.wait_for(run(b, ver, w, h, cpu), 90)
                        print(json.dumps(r), flush=True)
        await b.close()
asyncio.run(main())
