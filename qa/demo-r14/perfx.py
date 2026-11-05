# r14 copy of demo-r13/perfx.py: v1.5.1 vs v1.5.2; CASES "w,cpu,mode,adaptive|forced"
import os
import asyncio, json, sys, statistics
from playwright.async_api import async_playwright
BASE = os.environ.get("BASE", "http://127.0.0.1:8733/")
F = ('water: "real",', 'water: "real", adaptive: false,')
BUILDS = {  # r14: live v1.5.1 vs the v1.5.2 candidate, each on its own server
  "v1.5.1 real (adaptive)": ("http://127.0.0.1:8842/ink-fish/index.html", None),
  "v1.5.1 real (forced)":   ("http://127.0.0.1:8842/ink-fish/index.html", F),
  "v1.5.2 real (adaptive)": ("http://127.0.0.1:8861/ink-fish/index.html", None),
  "v1.5.2 real (forced)":   ("http://127.0.0.1:8861/ink-fish/index.html", F),
}
PROBE = """(()=>{window.__iv=[];window.__lt=0;let l=0;function f(t){if(l)__iv.push(t-l);l=t;requestAnimationFrame(f)};requestAnimationFrame(f);
try{new PerformanceObserver(e=>{__lt+=e.getEntries().length}).observe({type:'longtask',buffered:false})}catch(e){}})()"""
if os.environ.get("ONLY"): BUILDS = {k: v for k, v in BUILDS.items() if os.environ["ONLY"] in k}
async def run(b, build, w, h, cpu, mode):
    path, rep = BUILDS[build]
    ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, color_scheme="light")
    pg = await ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    if rep:
        async def route(r):
            resp = await r.fetch(); body = await resp.text()
            await r.fulfill(response=resp, body=body.replace(rep[0], rep[1]))
        await pg.route("**/index.html", route)
    await pg.goto(path); await pg.evaluate("sessionStorage.clear()"); await pg.wait_for_timeout(3500)
    cdp = await ctx.new_cdp_session(pg)
    await cdp.send("Emulation.setCPUThrottlingRate", {"rate": cpu})
    await pg.mouse.move(w * 0.4, h * 0.35)
    await pg.wait_for_timeout(1500)
    s0 = await pg.evaluate("(()=>{var s=document.body.__inkFish.stats;return [s.n,s.ms]})()")
    await pg.evaluate(PROBE)
    if mode == "scroll":
        for i in range(40):
            await pg.mouse.wheel(0, 110); await pg.wait_for_timeout(45)
    elif mode == "idle":
        await pg.wait_for_timeout(3000)
    elif mode == "drag":
        await pg.mouse.down()
        for i in range(40):
            await pg.mouse.move(w*(0.2+0.2*i/40), h*0.4); await pg.wait_for_timeout(45)
        await pg.mouse.up(); await pg.wait_for_timeout(300); await pg.mouse.move(w*0.15,h*0.6); await pg.mouse.down()
        for i in range(12):
            await pg.mouse.move(w*(0.15+0.7*i/12), h*(0.6-0.15*i/12)); await pg.wait_for_timeout(16)
        await pg.mouse.up(); await pg.wait_for_timeout(1500)
    else:  # cursor: slow drift with rings, then a quick pass, no scroll
        for i in range(60):
            x = w * (0.25 + 0.5 * i / 60); y = h * (0.3 + 0.1 * ((i // 30) % 2))
            await pg.mouse.move(x, y); await pg.wait_for_timeout(45)
    await pg.wait_for_timeout(300)
    iv = await pg.evaluate("__iv"); lt = await pg.evaluate("__lt")
    s1 = await pg.evaluate("(()=>{var a=document.body.__inkFish;return [a.stats.n,a.stats.ms,a.water||'-',a.stats.gw||null,a.stats.wq,a.stats.max,Array.from(a.stats.ring)]})()")
    await ctx.close()
    late = sum(1 for x in iv if x > 25) / max(1, len(iv)) * 100
    lib = (s1[1] - s0[1]) / max(1, s1[0] - s0[0])
    return {"build": build, "size": w, "cpu": cpu, "mode": mode, "late": round(late, 1), "frames": len(iv), "mean": round(statistics.mean(iv), 2) if iv else 0,
            "lib": round(lib, 3), "lt": lt, "water": s1[2], "wq": s1[4], "gw": ({k: round(v / max(1, s1[3]["n"])) for k, v in s1[3].items() if k != "n"} if s1[3] else None), "errs": errs, "max": round(s1[5],1), "p95": round(sorted([x for x in s1[6] if x>0])[int(0.95*max(1,len([x for x in s1[6] if x>0])))-1] if any(x>0 for x in s1[6]) else 0,2)}
async def main():
    out = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--hide-scrollbars"])
        plan = []
        for c in os.environ["CASES"].split(";"):
            w, cpu, mode, var = c.split(","); w = int(w); h = 900 if w == 1440 else 844
            for rep in range(int(os.environ.get("REPS", "3"))):  # interleaved A/B: A B A B ...
                for build in BUILDS:
                    if var in build: plan.append((build, w, h, int(cpu), mode))
        for rep in range(0):  # extra interleaved repeats at 1440 4x scroll
            for build in BUILDS: plan.append((build, 1440, 900, 4, "scroll"))
        plan = plan[int(os.environ.get('SKIP', '0')):]
        for args in plan:
            try:
                r = await asyncio.wait_for(run(b, *args), 120)
            except Exception as e:
                r = {"build": args[0], "size": args[1], "cpu": args[3], "mode": args[4], "error": repr(e)[:80]}
                await b.close(); b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--hide-scrollbars"])
            out.append(r); print(json.dumps(r), flush=True)
        await b.close()
    json.dump(out, open(os.environ.get("OUT","/tmp/perfx.json"), "w"), indent=1)
asyncio.run(main())
