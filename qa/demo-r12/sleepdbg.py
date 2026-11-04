# eyeball + numeric check of the grid wake's calm-sleep, hidden-pause and scroll behaviour (deterministic clock)
import sys as _s; _s.path.insert(0, "/workspace/ink-fish/qa"); import qahooks  # release build ships no QA hooks; splice them back for tests
import asyncio, os, json
from playwright.async_api import async_playwright
src = open("/workspace/ink-fish/qa/demo-r12/drag.py").read()
INIT = src.split('INIT = """')[1].split('"""')[0]
U = "http://127.0.0.1:8733/index.html"; OUT = "/workspace/ink-fish/qa/demo-r12/behave"; os.makedirs(OUT, exist_ok=True)
A = "document.body.__inkFish"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist","--hide-scrollbars"])
        for theme in ("light",):
            pg = await b.new_page(viewport={"width": 1440, "height": 900}, color_scheme=theme); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.add_init_script(INIT)
            await qahooks.install(pg)
            async def route(r):
                resp = await r.fetch(); body = await resp.text()
                await r.fulfill(response=resp, body=body.replace('water: "real",', 'water: "real", adaptive: false,'))
            await pg.route("**/index.html", route)
            await pg.goto(U); await pg.wait_for_timeout(600)
            st = lambda ms=1000/30: pg.evaluate(f"__step({ms})")
            for i in range(90): await st()
            async def peek(): return await pg.evaluate(f"(()=>{{var k={A}._peek();return k?{{grid:k.grid,hmax:k.hmax}}:null}})()")
            async def flick(y):
                await pg.mouse.move(250, y); await st(); await pg.mouse.down()
                for i in range(21): await pg.mouse.move(250 + 40 * i, y - 4 * i); await st()
                await pg.mouse.up(); await pg.mouse.move(1300, 120)
            log = {"theme": theme}
            # 1) calm-sleep: grid awake until ~2 s after the lift, then cleared and stopped
            await flick(520); tl = []
            for k in range(1, 31):
                await st(100)
                tl.append([round(k * 0.1, 1), await pg.evaluate(f"(()=>{{var k={A}._peek();return k?{{grid:k.grid,hmax:k.hmax,gpr:k.gpr,T:k.T,last:k.last}}:null}})()"), await pg.evaluate("performance.now()")])
                if k in (5, 15, 19, 25): pass #-{k/10:.1f}s.png")
            log["sleep"] = tl; print(json.dumps(log), flush=True); return
            # 2) hidden-pause: hide mid-wake, the loop stops (no frames counted), show again, the wake resumes and still sleeps
            await flick(520); await st(100); await st(100)
            n0 = await pg.evaluate(f"{A}.stats.n")
            await pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'hidden'});document.dispatchEvent(new Event('visibilitychange'))")
            for i in range(30): await st(100)
            n1 = await pg.evaluate(f"{A}.stats.n"); run_h = await pg.evaluate(f"{A}.running")
            await pg.evaluate("delete document.hidden;delete document.visibilityState;Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'visible'});document.dispatchEvent(new Event('visibilitychange'))")
            await st(); await st(); after = await peek(); await pg.screenshot(path=f"{OUT}/{theme}-after-hidden.png")
            for i in range(25): await st(100)
            log["hidden"] = {"frames while hidden (3 s)": n1 - n0, "running while hidden": run_h, "right after show": after, "2.5 s after show": await peek()}
            # 3) scroll: wake made, page scrolled 200 px mid-life: the wake should move up 200 px with the page
            for i in range(10): await st(100)
            await flick(620); await st(); await pg.screenshot(path=f"{OUT}/{theme}-scroll-before.png")
            await pg.evaluate("window.scrollBy(0,200)"); await st(); await st(); await pg.screenshot(path=f"{OUT}/{theme}-scroll-after.png")
            log["scroll"] = {"scrollY": await pg.evaluate("scrollY"), "peek": await peek()}
            log["errors"] = errs + await pg.evaluate("__errs")
            print(json.dumps(log), flush=True); await pg.close()
        await b.close()
asyncio.run(main())
