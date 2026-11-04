# the adaptive judge on a virtual clock (r7 judge.py), both builds: frame gaps scripted per (water state, quality)
import asyncio, sys, json
from playwright.async_api import async_playwright
INIT = open("/workspace/ink-fish/qa/demo-r7/cap.py").read().split('INIT = """')[1].split('"""')[0]
B = {"v1.3.1": "qa/demo-r9/base/index.html", "v1.4": "index.html"}
CASES = {
  "30Hz cap, fast GPU": {"real0": 33.3, "real1": 33.3, "flat": 33.3},
  "fill-bound, ok at q1": {"real0": 30, "real1": 17, "flat": 16.7},
  "weak phone": {"real0": 45, "real1": 34, "flat": 17},
  "slow, q1 no gain": {"real0": 50, "real1": 49, "flat": 18},
  "page-bound 22 fps": {"real0": 45, "real1": 45, "flat": 45},
  "6 fps (SwiftShader 1440)": {"real0": 150, "real1": 120, "flat": 17},
  "24 fps (SwiftShader 390)": {"real0": 41, "real1": 30, "flat": 17},
  "healthy": {"real0": 16.7, "real1": 16.7, "flat": 16.7},
}
async def run(b, url, G, secs=45):
    pg = await b.new_page(viewport={"width": 1440, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.add_init_script(INIT)
    await pg.goto(url); await pg.wait_for_timeout(500)
    await pg.evaluate("sessionStorage.clear()")
    for i in range(40): await pg.evaluate("__step(16.7)")
    await pg.wait_for_timeout(400)
    trace, lastk = [], None
    T0 = await pg.evaluate("performance.now()")
    js = """(G)=>{const a=document.body.__inkFish;let n=0;const t0=performance.now();
      while(performance.now()-t0<%d){const k=a.water==='real'?'real'+(a.stats.wq||0):'flat';__step(G[k]);n++;}
      return [a.water,a.stats.wq||0,performance.now()];}"""
    for k in range(secs * 2):
        w, q, now = await pg.evaluate(js % 500, G)
        key = f"{w}/q{q}"
        if key != lastk: trace.append(f"{(now - T0) / 1000:.1f}s:{key}"); lastk = key
    ss = await pg.evaluate("sessionStorage.getItem('ink-fish:water-fallback')")
    await pg.close()
    return trace, bool(ss), errs
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for name, G in CASES.items():
            for ver, path in B.items():
                tr, ss, errs = await run(b, "http://127.0.0.1:8733/" + path, G)
                print(f"{ver:7} {name:24} {' -> '.join(tr)}  remembered={ss} {errs}", flush=True)
        await b.close()
asyncio.run(main())
