# forced real water, SwiftShader, 1440x900: the same S path hovered vs pressed (trail), mean frame interval + gw counters
import asyncio, json
from playwright.async_api import async_playwright
U = "http://127.0.0.1:8732/index.html"
async def run(b, press):
    pg = await b.new_page(viewport={"width":1440,"height":900})
    async def route(r):
        resp = await r.fetch(); body = await resp.text()
        await r.fulfill(response=resp, body=body.replace('water: "real",', 'water: "real", adaptive: false,'))
    await pg.route("**/*index.html", route)
    await pg.goto(U); await pg.wait_for_timeout(3000)
    await pg.evaluate("window.__f=[];(function L(t){__f.push(t);requestAnimationFrame(L)})(performance.now())")
    g0 = await pg.evaluate("JSON.stringify(document.body.__inkFish.stats.gw)")
    await pg.mouse.move(300,400)
    if press: await pg.mouse.down()
    for i in range(100):
        u=i/99; await pg.mouse.move(300+800*u, 400-70*__import__('math').sin(u*5)); await pg.wait_for_timeout(40)
    r = await pg.evaluate("(()=>{var f=__f,d=[];for(var i=1;i<f.length;i++)d.push(f[i]-f[i-1]);return {frames:d.length,mean:d.reduce((a,b)=>a+b,0)/d.length,trail:document.body.__inkFish.stats.trail,gw:document.body.__inkFish.stats.gw}})()")
    if press: await pg.mouse.up()
    g0=json.loads(g0); gw=r['gw']; n=gw['n']-g0['n']
    r['per_frame']={k:round((gw[k]-g0[k])/max(1,n)) for k in gw if k!='n'}; del r['gw']
    await pg.close(); return r
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
        for rep in range(2):
            for press in (False, True):
                r = await run(b, press); print(("press-drag" if press else "hover     "), json.dumps(r))
        await b.close()
asyncio.run(main())
