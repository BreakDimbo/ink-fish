# which rings does the promo's s02 click gesture create in v1.3.1? (addRipple calls logged via a test-only route patch)
import asyncio, importlib.util, os
from playwright.async_api import async_playwright
spec = importlib.util.spec_from_file_location("shots", "/workspace/inkfish-promo/scripts/shots.py")
S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
INIT = open(os.path.join(os.path.dirname(__file__), "promocap.py")).read().split('INIT = """')[1].split('"""')[0] % 12345
async def main():
    shot = S.SHOTS[os.environ.get("SHOT","s02_ring_light")]; url = shot["url"].replace("127.0.0.1:8765", "127.0.0.1:8841")
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
        pg = await b.new_page(viewport={"width": shot["vp"][0], "height": shot["vp"][1]}, device_scale_factor=1)
        await pg.add_init_script(INIT + "window.__rips=[];")
        async def route(r):
            resp = await r.fetch(); body = await resp.text()
            a = "var addRipple = function (x, y, s, firm) {"
            assert a in body
            body = body.replace(a, a + "window.__rips.push([performance.now(),x,y,s,!!firm]);")
            await r.fulfill(response=resp, body=body)
        await pg.route("**/src/ink-fish.js", route)
        await pg.goto(url); await pg.wait_for_timeout(800)
        x, y = shot["path"](-1); await pg.mouse.move(x, y)
        for i in range(150): await pg.evaluate("__step(1000/30)")
        down = False
        for i in range(int(os.environ.get("NF","75"))):
            st = shot["path"](i / 30); await pg.mouse.move(st[0], st[1]); want = len(st) > 2 and st[2]
            if want and not down: await pg.mouse.down(); down = True
            if not want and down: await pg.mouse.up(); down = False
            await pg.evaluate("__step(1000/30)")
        print("addRipple calls [t_ms, x, y, s_requested, firm]:", await pg.evaluate("__rips"))
        await b.close()
asyncio.run(main())
