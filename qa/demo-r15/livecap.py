# r15 · REAL wall-clock capture (no virtual clock): CDP screencast frames carry their own timestamps; the page also
# logs every rAF time. Pointer actions are scheduled against wall time from the press instant.
# usage: livecap.py URL light|dark NAME KIND DUR   KIND: jclick | moveclick | drag | hold
#   env MEASURE=1: no fish (water only); PATCHJS: JSON [[from,to],...] for src/ink-fish.js
import asyncio, sys, os, json, time, base64, subprocess
from playwright.async_api import async_playwright
url, theme, name, kind = sys.argv[1:5]; DUR = float(sys.argv[5]) if len(sys.argv) > 5 else 6
OUT = f"/workspace/r15tmp/live/{name}"; os.makedirs(OUT, exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist","--hide-scrollbars"])
        pg = await b.new_page(viewport={"width": int(os.environ.get("VW", 1440)), "height": int(os.environ.get("VH", 900))}, color_scheme=theme)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.add_init_script("window.__rt=[];(function f(t){__rt.push(t);requestAnimationFrame(f)})(0);")
        async def route(r):
            resp = await r.fetch(); body = await resp.text()
            body = body.replace('water: "real",', 'water: "real", adaptive: false,')
            if os.environ.get("MEASURE"): body = body.replace("koi: true,", "koi: false, opacity: 0, shadow: 0,")
            await r.fulfill(response=resp, body=body)
        await pg.route("**/index.html", route)
        if os.environ.get("PATCHJS"):
            PJ = json.loads(os.environ["PATCHJS"])
            async def rjs(r):
                resp = await r.fetch(); body = await resp.text()
                for x, y in PJ: assert x in body, x; body = body.replace(x, y)
                await r.fulfill(response=resp, body=body)
            await pg.route("**/src/ink-fish.js*", rjs)
        await pg.goto(url); await pg.wait_for_timeout(5000)
        cdp = await pg.context.new_cdp_session(pg); frames = []
        def onf(ev):
            frames.append((ev["metadata"]["timestamp"], ev["data"]))
            asyncio.ensure_future(cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]}))
        cdp.on("Page.screencastFrame", onf)
        await cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 92, "everyNthFrame": 1})
        await pg.wait_for_timeout(800)
        X, Y = 700, 330; t0 = time.time() + 0.5; marks = {}
        async def at(s):
            d = t0 + s - time.time()
            if d > 0: await asyncio.sleep(d)
        if kind == "moveclick":  # a hand travelling ~500 px/s onto the spot, then a click
            await pg.mouse.move(X - 300, Y + 150)
            for i in range(1, 25): await at(-0.6 + 0.6 * i / 24); await pg.mouse.move(X - 300 + 300 * i / 24, Y + 150 - 150 * i / 24)
        await at(0); marks["press"] = time.time(); await pg.mouse.move(X, Y); await pg.mouse.down()
        if kind in ("jclick", "moveclick"): await at(0.12); await pg.mouse.up()
        elif kind == "hold": await at(1.0); await pg.mouse.up()
        elif kind == "drag":  # press, then a slow stroke ~200 px/s for 2 s, lift
            for i in range(1, 61): await at(0.15 + 2.0 * i / 60); await pg.mouse.move(X + 400 * i / 60, Y)
            await pg.mouse.up()
        await at(DUR); await cdp.send("Page.stopScreencast"); await pg.wait_for_timeout(300)
        rt = await pg.evaluate("__rt.filter(t => t > performance.now() - (%f + 0.3) * 1000)" % DUR); wst = await pg.evaluate("document.body.__inkFish.water")
        print(name, "frames", len(frames), "errors", errs, "water", wst)
        meta = []
        for i, (ts, data) in enumerate(frames):
            open(f"{OUT}/f{i:04d}.jpg", "wb").write(base64.b64decode(data)); meta.append(dict(i=i, t=ts - marks["press"]))
        iv = [b_ - a for a, b_ in zip(rt, rt[1:])]
        simrate = sum(min(x, 100) for x in iv) / max(1e-9, sum(iv))  # the library caps a frame's dt at 0.1 s: its clock vs the wall's
        iv.sort()
        json.dump(dict(frames=meta, raf_median_ms=iv[len(iv) // 2] if iv else None, raf_p90_ms=iv[int(len(iv) * .9)] if iv else None, simrate=simrate, water=wst), open(f"{OUT}/meta.json", "w"))
        print("rAF median %.1f ms p90 %.1f ms sim/wall %.3f" % (iv[len(iv) // 2], iv[int(len(iv) * .9)], simrate))
        await b.close()
asyncio.run(main())
