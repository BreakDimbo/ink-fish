import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome"); pg = await b.new_page(viewport={"width":1440,"height":900}); errs=[]
        pg.on("pageerror", lambda e: errs.append(str(e)))
        async def route(r):
            resp = await r.fetch(); body = await resp.text()
            await r.fulfill(response=resp, body=body.replace('water: "real",', 'water: "real", ripples: false,'))
        await pg.route("**/index.html", route)
        await pg.goto("http://127.0.0.1:8732/index.html"); await pg.wait_for_timeout(2500)
        await pg.mouse.move(300,450); await pg.mouse.down()
        for i in range(30): await pg.mouse.move(300+20*i,450); await pg.wait_for_timeout(30)
        n = await pg.evaluate("document.body.__inkFish.stats.trail"); await pg.mouse.up()
        r = await pg.evaluate("document.body.__inkFish.stats.ring.reduce((a,b)=>a+(b>0),0)")
        print("ripples:false -> trail pts", n, "ring samples", r, "errors", errs); await b.close()
asyncio.run(main())
