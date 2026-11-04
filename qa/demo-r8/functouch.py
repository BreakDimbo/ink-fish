import asyncio, sys
from playwright.async_api import async_playwright
U = "http://127.0.0.1:8732/index.html"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--disable-features=OverscrollHistoryNavigation"])
        for css in ("", "html,body{touch-action:pan-y}"):
            ctx = await b.new_context(viewport={"width":1440,"height":900}, has_touch=True, is_mobile=True); pg = await ctx.new_page()
            await pg.goto(U); await pg.wait_for_timeout(2500)
            if css: await pg.add_style_tag(content=css)
            await pg.evaluate("""window.__ev=[];['pointerdown','pointermove','pointerup','pointercancel'].forEach(t=>addEventListener(t,e=>__ev.push(t[7]+' '+document.body.__inkFish.stats.trail),{passive:true}))""")
            cdp = await ctx.new_cdp_session(pg)
            async def touch(name, pts, hold=0):
                await pg.evaluate("scrollTo(0,0)"); await pg.wait_for_timeout(300)
                await cdp.send("Input.dispatchTouchEvent", {"type":"touchStart","touchPoints":[{"x":pts[0][0],"y":pts[0][1]}]})
                if hold: await pg.wait_for_timeout(hold)
                x0,y0=pts[0]
                for (x,y) in pts[1:]:
                    for k in range(1,9):
                        await cdp.send("Input.dispatchTouchEvent", {"type":"touchMove","touchPoints":[{"x":x0+(x-x0)*k/8,"y":y0+(y-y0)*k/8}]}); await pg.wait_for_timeout(16)
                    x0,y0=x,y
                n = await pg.evaluate("document.body.__inkFish.stats.trail")
                await cdp.send("Input.dispatchTouchEvent", {"type":"touchEnd","touchPoints":[]}); await pg.wait_for_timeout(100)
                ev = await pg.evaluate("__ev.splice(0)")
                print(f"  [{css or 'default touch-action'}] {name}: trail pts {n}, scrollY {await pg.evaluate('scrollY')}, events {len(ev)} last {ev[-1:]}")
            await touch("vertical swipe", [(200,600),(210,300)])
            await touch("horizontal drag", [(200,500),(700,520)])
            await touch("hold 400 ms + S drag", [(200,500),(500,420),(800,520)], hold=400)
            await ctx.close()
        await b.close()
asyncio.run(main())
