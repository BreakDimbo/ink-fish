# functional checks for v1.4 (demo page, SwiftShader). Prints one line per check; any page error / console error is listed
import asyncio, json
from playwright.async_api import async_playwright
U = "http://127.0.0.1:8733/index.html"
W = "document.body.__inkFish"
ALL = []
async def page(b, rep=None, **kw):
    ctx = await b.new_context(viewport={"width": 1440, "height": 900}, **kw); pg = await ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append("pageerror:" + str(e)))
    pg.on("console", lambda m: errs.append(m.type + ":" + m.text) if m.type == "error" else None)
    if rep:
        async def route(r):
            resp = await r.fetch(); body = await resp.text()
            await r.fulfill(response=resp, body=body.replace('water: "real",', rep))
        await pg.route("**/index.html", route)
    await pg.goto(U.replace("index.html", "qa/demo-r9/blank.html")); await pg.evaluate("sessionStorage.clear()")
    return ctx, pg, errs
async def drag(pg, pts, steps=12):
    await pg.mouse.move(*pts[0]); await pg.mouse.down()
    for (x, y) in pts[1:]: await pg.mouse.move(x, y, steps=steps)
    n = await pg.evaluate(W + ".stats.trail"); await pg.mouse.up(); return n
def rep(name, ok, detail, errs):
    ALL.append((name, ok, len(errs))); print(f"{'PASS' if ok and not errs else 'FAIL'} {name}: {detail} errors={errs}", flush=True)
S = [(300, 400), (600, 340), (900, 420), (1100, 380)]
async def main():
    async with async_playwright() as p:
        SW = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=SW)
        # 1 adaptive fallback (default options on SwiftShader): starts real, falls back, remembered for the session
        ctx, pg, errs = await page(b); await pg.goto(U); await pg.wait_for_timeout(1200)
        w0 = await pg.evaluate(W + ".water")
        for i in range(60): await pg.mouse.move(300 + i * 10, 300); await pg.wait_for_timeout(50)
        await pg.wait_for_timeout(3000)
        w1 = await pg.evaluate(W + ".water"); ss = await pg.evaluate("sessionStorage.getItem('ink-fish:water-fallback')")
        n = await drag(pg, S)
        rep("adaptive fallback", w0 == "real" and w1 == "fallback" and bool(ss), f"{w0} -> {w1}, remembered={bool(ss)}, flat trail pts after fallback={n}", errs); await ctx.close()
        # 2 reduced motion: flat water, no trail, no WebGL canvas
        ctx, pg, errs = await page(b, reduced_motion="reduce"); await pg.goto(U); await pg.wait_for_timeout(2500)
        wc = await pg.evaluate("[...document.querySelectorAll('canvas.ink-fish--water')].filter(c=>getComputedStyle(c).display!=='none').length")
        n = await drag(pg, S)
        rep("reduced motion", (await pg.evaluate(W + ".water")) != "real" and n == 0, f"water={await pg.evaluate(W + '.water')}, visible GL canvases={wc}, drag trail pts={n}", errs); await ctx.close()
        # 3 forced real: trail, ripples:false, trail:false, dimple only while pressed, theme switch, set() round trip, destroy
        ctx, pg, errs = await page(b, 'water: "real", adaptive: false,'); await pg.goto(U); await pg.wait_for_timeout(2500)
        wr = await pg.evaluate(W + ".water")
        await pg.mouse.move(300, 420); await pg.mouse.down()
        for i in range(30): await pg.mouse.move(300 + 4 * i, 420); await pg.wait_for_timeout(33)   # slow ≈ 120 px/s
        slow_pts = await pg.evaluate(W + ".stats.trail")
        for i in range(12): await pg.mouse.move(420 + 60 * i, 420 - 8 * i); await pg.wait_for_timeout(16)  # fast
        fast_pts = await pg.evaluate(W + ".stats.trail"); await pg.mouse.up()
        await pg.wait_for_timeout(4500); left = await pg.evaluate(W + ".stats.trail")
        rep("real-water trail gating", wr == "real" and fast_pts > slow_pts, f"water={wr}, trail pts slow={slow_pts}, after fast={fast_pts}, 4.5 s after lift={left}", errs)
        await pg.evaluate(W + ".set({trail:false})"); n = await drag(pg, S); await pg.evaluate(W + ".set({trail:true})")
        rep("trail:false", n == 0, f"drag trail pts={n}", errs)
        await pg.evaluate(W + ".set({ripples:false})"); await pg.wait_for_timeout(200); n = await drag(pg, S)
        rp = await pg.evaluate(W + ".water"); await pg.evaluate(W + ".set({ripples:true})"); await pg.wait_for_timeout(300)
        rep("ripples:false", n == 0, f"drag trail pts={n}, water={rp}", errs)
        await pg.evaluate("document.documentElement.setAttribute('data-theme','dark')"); await pg.wait_for_timeout(1500)
        d1 = await pg.evaluate(W + ".water"); n = await drag(pg, [(300, 300), (1000, 250)], steps=6)
        await pg.evaluate("document.documentElement.setAttribute('data-theme','light')"); await pg.wait_for_timeout(1500)
        rep("theme switch light→dark→light", d1 == "real", f"water in dark={d1}, dark fast-drag trail pts={n}, back to light water={await pg.evaluate(W + '.water')}", errs)
        r = []
        await pg.evaluate(W + ".set({water:false})"); await pg.wait_for_timeout(300); r.append(await pg.evaluate(W + ".water"))
        fl = await drag(pg, [(300, 300), (1000, 250)], steps=6)
        await pg.evaluate(W + ".set({water:'real'})"); await pg.wait_for_timeout(300); r.append(await pg.evaluate(W + ".water"))
        await pg.evaluate(W + ".set({reducedMotion:true})"); await pg.wait_for_timeout(400); r.append(await pg.evaluate(W + ".water"))
        await pg.evaluate(W + ".set({reducedMotion:'auto'})"); await pg.wait_for_timeout(400); r.append(await pg.evaluate(W + ".water"))
        rep("set() round trip", r == ["flat", "real", "flat", "real"], f"water false/real/RM/auto = {r}, flat fast-drag trail pts={fl}", errs)
        await pg.mouse.move(500, 300); await pg.mouse.down(); await pg.mouse.move(510, 300)
        await pg.evaluate(W + ".destroy()"); await pg.mouse.up(); await pg.wait_for_timeout(500)
        left = await pg.evaluate("[...document.querySelectorAll('body > canvas')].length")
        rep("destroy (mid-press)", left == 0, f"body canvases left={left}", errs); await ctx.close()
        # 4 touch: pan-y — vertical swipe scrolls, horizontal drag draws, hold + drag draws
        ctx = await b.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True, device_scale_factor=2); pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append("pageerror:" + str(e))); pg.on("console", lambda m: errs.append(m.type + ":" + m.text) if m.type == "error" else None)
        async def route(r):
            resp = await r.fetch(); body = await resp.text()
            await r.fulfill(response=resp, body=body.replace('water: "real",', 'water: "real", adaptive: false,'))
        await pg.route("**/index.html", route)
        await pg.goto(U); await pg.wait_for_timeout(2500)
        ta = await pg.evaluate("getComputedStyle(document.documentElement).touchAction+'/'+getComputedStyle(document.body).touchAction")
        cdp = await ctx.new_cdp_session(pg)
        async def touch(pts, hold=0):
            await pg.evaluate("scrollTo(0,0)"); await pg.wait_for_timeout(300)
            await cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": pts[0][0], "y": pts[0][1]}]})
            if hold: await pg.wait_for_timeout(hold)
            x0, y0 = pts[0]
            for (x, y) in pts[1:]:
                for k in range(1, 9):
                    await cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x0 + (x - x0) * k / 8, "y": y0 + (y - y0) * k / 8}]}); await pg.wait_for_timeout(16)
                x0, y0 = x, y
            n = await pg.evaluate(W + ".stats.trail")
            await cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []}); await pg.wait_for_timeout(200)
            return n, await pg.evaluate("scrollY")
        v = await touch([(200, 600), (205, 250)]); h = await touch([(40, 200), (360, 215)]); hd = await touch([(60, 220), (200, 180), (340, 230)], hold=400)
        rep("touch (pan-y)", v[0] == 0 and v[1] > 0 and h[0] > 0 and hd[0] > 0, f"touch-action={ta}; vertical swipe: trail {v[0]}, scrollY {v[1]}; horizontal: trail {h[0]}, scrollY {h[1]}; hold+drag: trail {hd[0]}", errs)
        await ctx.close(); await b.close()
        # 5 no WebGL at all: 2D fallback
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--disable-webgl", "--disable-webgl2", "--disable-3d-apis"])
        ctx, pg, errs = await page(b); await pg.goto(U); await pg.wait_for_timeout(2500)
        w = await pg.evaluate(W + ".water"); n = await drag(pg, [(300, 300), (1000, 250)], steps=6)
        cv = await pg.evaluate("[...document.querySelectorAll('body > canvas')].map(c=>c.className+':'+getComputedStyle(c).display).join(' | ')")
        rep("no WebGL → 2D fallback", w in ("fallback", "flat"), f"water={w}, fast-drag flat trail pts={n}, canvases: {cv}", errs); await ctx.close(); await b.close()
    print("SUMMARY", json.dumps(ALL))
asyncio.run(main())
