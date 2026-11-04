# quick look + slope stats for the v1.5 prototype: probe.py THEME KIND TIMES(comma) TAG
import sys as _s; _s.path.insert(0, "/workspace/ink-fish/qa"); import qahooks  # release build ships no QA hooks; splice them back for tests
import asyncio, sys, os, json
sys.argv_saved = list(sys.argv)
from playwright.async_api import async_playwright
sys.path.insert(0, "/workspace/ink-fish/qa/demo-r9")
theme, kind, times, tag = sys.argv[1:5]
times = [float(x) for x in times.split(",")]
src = open("/workspace/ink-fish/qa/demo-r9/drag.py").read()
INIT = src.split('INIT = """')[1].split('"""')[0]
ns = {}; exec("import math\n" + "def ss(u): return u * u * (3 - 2 * u)\n" + src.split("# returns (x, y, pressed) at t seconds\n")[1].split("async def main")[0].replace("kind ==", "K =="), {"K": kind, "math": __import__("math"), "ss": lambda u: u*u*(3-2*u)}, ns)
path = ns["path"]
URL = os.environ.get("URL", "http://127.0.0.1:8733/index.html")
OUT = f"/workspace/ink-fish/qa/demo-r12/probe/{tag}"; os.makedirs(OUT, exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist","--hide-scrollbars"])
        pg = await b.new_page(viewport={"width": 1440, "height": 900}, color_scheme=theme)
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
        await pg.add_init_script(INIT + ";window.__inkFishGridGain=" + os.environ.get("GG","0") + ";window.__inkFishGrid=" + os.environ.get("GRID","null"))
        await qahooks.install(pg)
        async def route(r):
            resp = await r.fetch(); body = await resp.text()
            await r.fulfill(response=resp, body=body.replace('water: "real",', 'water: "real", adaptive: false,'))
        await pg.route("**/index.html", route)
        await pg.goto(URL); await pg.wait_for_timeout(600)
        for i in range(150): await pg.evaluate("__step(1000/30)")
        down = False; res = []
        N = int(max(times) * 30) + 1
        for i in range(N):
            q = path(i / 30)
            if q:
                x, y, pr = q
                await pg.mouse.move(x, y)
                if pr and not down: await pg.mouse.down(); down = True
                if not pr and down: await pg.mouse.up(); down = False
            await pg.evaluate("__step(1000/30)")
            if any(abs(i / 30 - t) < 1e-6 or (i == round(t * 30)) for t in times):
                pk = await pg.evaluate("document.body.__inkFish._peek ? document.body.__inkFish._peek() : null")
                await pg.screenshot(path=f"{OUT}/t{i/30:.2f}.png")
                if os.environ.get("HDUMP"):
                    hd = await pg.evaluate("document.body.__inkFish._peek(true)")
                    if hd:
                        import numpy as np
                        from PIL import Image
                        a = np.array(hd["h"], dtype=np.float32).reshape(hd["gy"], hd["gx"]); sc = float(os.environ.get("HDUMP"))
                        Image.fromarray(np.clip(128 + a * sc, 0, 255).astype(np.uint8)).resize((hd["gx"] * 2, hd["gy"] * 2), Image.NEAREST).save(f"{OUT}/h{i/30:.2f}.png")
                res.append({"t": round(i / 30, 2), **(pk or {})}); print(json.dumps(res[-1]), flush=True)
        print("errors:", errs, "water:", await pg.evaluate("document.body.__inkFish.water"), flush=True)
        await b.close()
asyncio.run(main())
