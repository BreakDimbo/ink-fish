import asyncio
from playwright.async_api import async_playwright
U = "http://127.0.0.1:8732/index.html"
W = "document.body.__inkFish"
async def page(b, **kw):
    ctx = await b.new_context(viewport={"width":1440,"height":900}, **kw); pg = await ctx.new_page(); errs=[]
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.type+":"+m.text) if m.type in ("error","warning") else None)
    return ctx, pg, errs
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        # 1 default (adaptive on, SwiftShader): starts real, should fall back within a few seconds
        ctx, pg, errs = await page(b); await pg.goto(U); await pg.wait_for_timeout(1500)
        w0 = await pg.evaluate(W+".water")
        for i in range(60): await pg.mouse.move(300+i*10, 300); await pg.wait_for_timeout(50)
        await pg.wait_for_timeout(3000)
        print("adaptive on SwiftShader:", w0, "->", await pg.evaluate(W+".water"), "pond:", await pg.evaluate("document.getElementById('pond').__inkFish.water"), errs); await ctx.close()
        # 2 reduced motion
        ctx, pg, errs = await page(b, reduced_motion="reduce"); await pg.goto(U); await pg.wait_for_timeout(2500)
        print("reduced motion:", await pg.evaluate(W+".water"), await pg.evaluate("[...document.querySelectorAll('canvas.ink-fish--water')].length"), errs); await ctx.close()
        # 3 set() round trip + theme switch, adaptive off
        ctx, pg, errs = await page(b); await pg.goto(U); await pg.wait_for_timeout(2500)
        r = []
        await pg.evaluate(W+".set({adaptive:false})")
        r.append(await pg.evaluate(W+".water"))
        await pg.evaluate(W+".set({water:false})"); await pg.wait_for_timeout(300); r.append(await pg.evaluate(W+".water"))
        await pg.evaluate(W+".set({water:'real'})"); await pg.wait_for_timeout(300); r.append(await pg.evaluate(W+".water"))
        await pg.evaluate(W+".set({ripples:false})"); await pg.wait_for_timeout(300); r.append(await pg.evaluate(W+".water"))
        await pg.evaluate(W+".set({ripples:true})")
        await pg.evaluate("document.documentElement.setAttribute('data-theme','dark')"); await pg.wait_for_timeout(1500)
        await pg.evaluate(W+".set({reducedMotion:true})"); await pg.wait_for_timeout(400); r.append(await pg.evaluate(W+".water"))
        await pg.evaluate(W+".set({reducedMotion:'auto'})"); await pg.wait_for_timeout(400); r.append(await pg.evaluate(W+".water"))
        await pg.evaluate(W+".destroy()"); r.append(await pg.evaluate("document.querySelectorAll('body > canvas').length"))
        print("set/theme/destroy:", r, errs); await ctx.close()
        await b.close()
        # 4 no WebGL at all
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--disable-webgl","--disable-webgl2"])
        ctx, pg, errs = await page(b); await pg.goto(U); await pg.wait_for_timeout(2500)
        print("no webgl:", await pg.evaluate(W+".water"), await pg.evaluate("[...document.querySelectorAll('body > canvas')].map(c=>c.className+':'+getComputedStyle(c).display).join(' | ')"), errs)
        await b.close()
asyncio.run(main())
