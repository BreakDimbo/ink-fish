import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--hide-scrollbars"])
        for path in sys.argv[1:]:
            ctx = await b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1); pg = await ctx.new_page()
            async def route(r):
                resp = await r.fetch(); body = await resp.text()
                await r.fulfill(response=resp, body=body.replace('water: "real",', 'water: "real", adaptive: false,'))
            await pg.route("**/index.html", route)
            await pg.goto("http://127.0.0.1:8733/" + path); await pg.evaluate("sessionStorage.clear()")
            out = []
            for i in range(28):
                await pg.wait_for_timeout(250)
                out.append(await pg.evaluate("(()=>{var s=document.body.__inkFish.stats;return [s.n, Math.round(s.ms), s.gw?Math.round(s.gw.prof||0):-1]})()"))
            print(path, out, flush=True); await ctx.close()
        await b.close()
asyncio.run(main())
