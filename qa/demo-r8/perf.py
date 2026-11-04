import os
import asyncio, json, sys, statistics
from playwright.async_api import async_playwright
BASE = "http://127.0.0.1:8732/"
BUILDS = {
  "v1.3.1 flat": ("qa/demo-r8/base/index.html", ('water: "real",', '')),
  "v1.3.1 real (adaptive)": ("qa/demo-r8/base/index.html", None),
  "v1.3.1 real (forced)": ("qa/demo-r8/base/index.html", ('water: "real",', 'water: "real", adaptive: false,')),
  "v1.3.2 flat": ("index.html", ('water: "real",', '')),
  "v1.3.2 real (adaptive)": ("index.html", None),
  "v1.3.2 real (forced)":   ("index.html", ('water: "real",', 'water: "real", adaptive: false,')),
}
PROBE = """(()=>{window.__iv=[];window.__lt=0;let l=0;function f(t){if(l)__iv.push(t-l);l=t;requestAnimationFrame(f)};requestAnimationFrame(f);
try{new PerformanceObserver(e=>{__lt+=e.getEntries().length}).observe({type:'longtask',buffered:false})}catch(e){}})()"""
async def run(b, build, w, h, cpu, mode):
    path, rep = BUILDS[build]
    ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2, color_scheme="light")
    pg = await ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    if rep:
        async def route(r):
            resp = await r.fetch(); body = await resp.text()
            await r.fulfill(response=resp, body=body.replace(rep[0], rep[1]))
        await pg.route("**/index.html", route)
    await pg.goto(BASE + path); await pg.evaluate("sessionStorage.clear()"); await pg.wait_for_timeout(3500)
    cdp = await ctx.new_cdp_session(pg)
    await cdp.send("Emulation.setCPUThrottlingRate", {"rate": cpu})
    await pg.mouse.move(w * 0.4, h * 0.35)
    await pg.wait_for_timeout(1500)
    s0 = await pg.evaluate("(()=>{var s=document.body.__inkFish.stats;return [s.n,s.ms]})()")
    await pg.evaluate(PROBE)
    if mode == "scroll":
        for i in range(80):
            await pg.mouse.wheel(0, 110); await pg.wait_for_timeout(45)
    else:  # cursor: slow drift with rings, then a quick pass, no scroll
        for i in range(120):
            x = w * (0.25 + 0.5 * i / 120); y = h * (0.3 + 0.1 * ((i // 30) % 2))
            await pg.mouse.move(x, y); await pg.wait_for_timeout(45)
    await pg.wait_for_timeout(300)
    iv = await pg.evaluate("__iv"); lt = await pg.evaluate("__lt")
    s1 = await pg.evaluate("(()=>{var a=document.body.__inkFish;return [a.stats.n,a.stats.ms,a.water||'-',a.stats.gw||null,a.stats.wq]})()")
    await ctx.close()
    late = sum(1 for x in iv if x > 25) / max(1, len(iv)) * 100
    lib = (s1[1] - s0[1]) / max(1, s1[0] - s0[0])
    return {"build": build, "size": w, "cpu": cpu, "mode": mode, "late": round(late, 1), "frames": len(iv), "mean": round(statistics.mean(iv), 2) if iv else 0,
            "lib": round(lib, 3), "lt": lt, "water": s1[2], "wq": s1[4], "gw": ({k: round(v / max(1, s1[3]["n"])) for k, v in s1[3].items() if k != "n"} if s1[3] else None), "errs": errs}
async def main():
    out = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--hide-scrollbars"])
        plan = []
        for (w, h) in [(1440, 900), (390, 844)]:
            for cpu in [1, 4]:
                for mode in ["scroll", "cursor"]:
                    for build in BUILDS: plan.append((build, w, h, cpu, mode))
        for rep in range(1):  # extra interleaved repeats at 1440 4x scroll
            for build in BUILDS: plan.append((build, 1440, 900, 4, "scroll"))
        import os
        plan = plan[int(os.environ.get('SKIP', '0')):]
        for args in plan:
            r = await run(b, *args); out.append(r); print(json.dumps(r), flush=True)
        await b.close()
    json.dump(out, open("/workspace/ink-fish/qa/demo-r8/perf%s.json" % os.environ.get("SKIP", ""), "w"), indent=1)
asyncio.run(main())
