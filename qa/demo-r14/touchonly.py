# r14 copy of demo-r9/touchonly.py
# functional checks for v1.4 (demo page, SwiftShader). Prints one line per check; any page error / console error is listed
import asyncio, json
from playwright.async_api import async_playwright
import sys
U = sys.argv[1]
W = "document.body.__inkFish"
ALL = []
async def page(b, rep=None, **kw):
    ctx = await b.new_context(viewport={"width": 1440, "height": 900}, **kw); pg = await ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append("pageerror:" + str(e)))
    pg.on("console", lambda m: errs.append(m.type + ":" + m.text) if m.type == "error" and "Failed to load resource" not in m.text else None)
    pg.on("response", lambda r: errs.append(f"http{r.status}:{r.url}") if r.status >= 400 and not r.url.endswith("/favicon.ico") else None)
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
        SW = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--disable-features=OverscrollHistoryNavigation"]
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=SW)
        # 4 touch: pan-y — vertical swipe scrolls, horizontal drag draws, hold + drag draws
        ctx = await b.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True, device_scale_factor=2); pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append("pageerror:" + str(e))); pg.on("console", lambda m: errs.append(m.type + ":" + m.text) if m.type == "error" else None)
        async def route(r):
            resp = await r.fetch(); body = await resp.text()
            await r.fulfill(response=resp, body=body.replace('water: "real",', 'water: "real", adaptive: false,'))
        await pg.route("**/index.html", route)
        await pg.route("**/base/index.html", route)
        await pg.goto(U); await pg.wait_for_timeout(2500)
        await pg.add_style_tag(content="body{touch-action:pan-y}")  # host sets pan-y, as the README requires (zh-blog-mirrors does)
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
            n = await pg.evaluate("(" + W + "||{stats:{trail:-1}}).stats.trail+0") if True else 0
            if n < 0: print("  touch: instance missing, url=", pg.url, flush=True)
            await cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []}); await pg.wait_for_timeout(200)
            return n, await pg.evaluate("scrollY")
        v = await touch([(200, 600), (205, 250)]); h = await touch([(120, 200), (360, 215)]); hd = await touch([(120, 220), (220, 180), (340, 230)], hold=400)
        rep("touch (pan-y)", v[0] == 0 and v[1] > 0 and h[0] > 0 and hd[0] > 0, f"touch-action={ta}; vertical swipe: trail {v[0]}, scrollY {v[1]}; horizontal: trail {h[0]}, scrollY {h[1]}; hold+drag: trail {hd[0]}", errs)
        await ctx.close(); await b.close()
asyncio.run(main())
