# GPU work proxy on a virtual 60 Hz clock (deterministic, independent of SwiftShader speed): per-frame surface-evaluation px
# (sim + blur passes, = "sim steps × grid"), composite px, caustic vertices and profile px, per phase, for each build
import asyncio, json, math
from playwright.async_api import async_playwright
INIT = open("/workspace/ink-fish/qa/demo-r9/drag.py").read().split('INIT = """')[1].split('"""')[0]
B = {"v1.3.1": "qa/demo-r9/base/index.html", "v1.3.2": "qa/demo-r9/v132/index.html", "v1.4": "index.html"}
GW = "(()=>{const g=document.body.__inkFish.stats.gw;return [g.n,g.sim,g.comp,g.cau,g.prof]})()"
async def run(b, ver, w, h):
    pg = await b.new_page(viewport={"width": w, "height": h}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.add_init_script(INIT)
    async def route(r):
        resp = await r.fetch(); body = await resp.text()
        await r.fulfill(response=resp, body=body.replace('water: "real",', 'water: "real", adaptive: false,'))
    await pg.route("**/index.html", route)
    await pg.goto("http://127.0.0.1:8733/" + B[ver]); await pg.wait_for_timeout(600)
    for i in range(240): await pg.evaluate("__step(1000/60)")   # warm-up (profile table, shaders)
    await pg.wait_for_timeout(500)
    out = {}
    async def phase(name, n, fn=None):
        a = await pg.evaluate(GW)
        for i in range(n):
            if fn: await fn(i)
            await pg.evaluate("__step(1000/60)")
        z = await pg.evaluate(GW); k = max(1, z[0] - a[0])
        out[name] = {"frames": z[0] - a[0], "sim_px": round((z[1] - a[1]) / k), "comp_px": round((z[2] - a[2]) / k), "cau_v": round((z[3] - a[3]) / k), "prof_px": round((z[4] - a[4]) / k)}
    sx, sy = w * 0.25, h * 0.35
    await phase("idle (no pointer)", 180)
    await pg.mouse.move(sx, sy)
    await phase("hover drift", 120, lambda i: pg.mouse.move(sx + 3 * i, sy))
    await pg.mouse.move(sx, sy + 60); await pg.mouse.down()
    await phase("press+hold", 60)
    await phase("slow drag 200 px/s", 120, lambda i: pg.mouse.move(sx + 200 * i / 60, sy + 60))
    await phase("fast flick 1200 px/s", 24, lambda i: pg.mouse.move(sx + 400 + 20 * i, sy + 60 - 4 * i))
    await pg.mouse.up()
    await phase("0–2 s after lift", 120)
    await phase("2–5 s after lift (calm)", 180)
    await pg.close()
    return out, errs
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--hide-scrollbars"])
        for (w, h) in [(1440, 900), (390, 844)]:
            for ver in B:
                o, e = await run(b, ver, w, h)
                print(json.dumps({"ver": ver, "size": w, "phases": o, "errs": e}), flush=True)
        await b.close()
asyncio.run(main())
