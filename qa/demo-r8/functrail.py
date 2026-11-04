import asyncio
from playwright.async_api import async_playwright
U = "http://127.0.0.1:8732/index.html"
W = "document.body.__inkFish"
async def page(b, **kw):
    ctx = await b.new_context(viewport={"width":1440,"height":900}, **kw); pg = await ctx.new_page(); errs=[]
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.type+":"+m.text) if m.type in ("error","warning") else None)
    async def route(r):
        resp = await r.fetch(); body = await resp.text()
        await r.fulfill(response=resp, body=body.replace('water: "real",', 'water: "real", adaptive: false,'))
    await pg.route("**/index.html", route)
    return ctx, pg, errs
async def drag(pg, pts, steps=12):
    await pg.mouse.move(*pts[0]); await pg.mouse.down()
    for (x,y) in pts[1:]:
        await pg.mouse.move(x, y, steps=steps)
    n = await pg.evaluate(W+".stats.trail"); await pg.mouse.up(); return n
async def touch(pg, cdp, pts, hold=0):
    await cdp.send("Input.dispatchTouchEvent", {"type":"touchStart","touchPoints":[{"x":pts[0][0],"y":pts[0][1]}]})
    if hold: await pg.wait_for_timeout(hold)
    x0,y0 = pts[0]
    for (x,y) in pts[1:]:
        for k in range(1,9):
            await cdp.send("Input.dispatchTouchEvent", {"type":"touchMove","touchPoints":[{"x":x0+(x-x0)*k/8,"y":y0+(y-y0)*k/8}]}); await pg.wait_for_timeout(16)
        x0,y0=x,y
    n = await pg.evaluate(W+".stats.trail")
    await cdp.send("Input.dispatchTouchEvent", {"type":"touchEnd","touchPoints":[]}); return n
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
        ctx, pg, errs = await page(b); await pg.goto(U); await pg.wait_for_timeout(2500)
        S = [(300,400),(600,340),(900,420),(1100,380)]
        print("real:", await pg.evaluate(W+".water"), "drag pts:", await drag(pg, S))
        await pg.wait_for_timeout(4500); print(" after 4.5 s:", await pg.evaluate(W+".stats.trail"))
        await pg.mouse.move(300,400); await pg.mouse.move(900,400, steps=20); print(" hover (no press):", await pg.evaluate(W+".stats.trail"))
        # press on the headline text: a selection, never a trail
        h = await pg.evaluate("(()=>{var e=document.querySelector('h1');var r=e.getBoundingClientRect();return [r.left+r.width*0.3,r.top+r.height/2]})()")
        print(" drag from h1 text:", await drag(pg, [tuple(h),(h[0]+300,h[1]+10)]), "selection:", repr(await pg.evaluate("String(getSelection()).slice(0,30)")))
        await pg.evaluate(W+".set({trail:false})"); print(" trail:false drag:", await drag(pg, S)); await pg.evaluate(W+".set({trail:true})")
        await pg.evaluate(W+".set({water:false})"); await pg.wait_for_timeout(300); print("flat:", await pg.evaluate(W+".water"), "drag pts:", await drag(pg, S))
        print(" errors:", errs); await ctx.close()
        ctx, pg, errs = await page(b, reduced_motion="reduce"); await pg.goto(U); await pg.wait_for_timeout(2000)
        print("reduced motion:", await pg.evaluate(W+".water"), "drag pts:", await drag(pg, S), errs); await ctx.close()
        await b.close()
asyncio.run(main())
