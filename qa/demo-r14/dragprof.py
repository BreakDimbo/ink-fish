# r14 perf dev: the perf gate's 1440 forced drag (perfx motion) for route-patched variants of the new build;
# interleaved, REPS each: library ms/frame and mean rAF interval
import asyncio, os, json, statistics
from playwright.async_api import async_playwright
U = os.environ.get("U", "http://127.0.0.1:8861/ink-fish/index.html")
SIM = "gl.uniform4fv(Psp.u.I, pI);\n        gl.drawArrays(gl.TRIANGLES, 0, 3);"
DL = lambda L: [("{ P.clk.s = CLK_S_DRAG; P.clk.f = 0.55; }", "{ P.clk.s = CLK_S_DRAG; P.clk.f = 0.55; P.clk.dl = 1; }"),
                ("o3.life = WATER.plife;", "o3.life = cc.dl ? %s : WATER.plife;" % L), ("cq0.t > clkLife()", "cq0.t > (cq0.dl ? %s : clkLife())" % L)]
V = {
  "base": [],
  "nopromo": [("var nP = promo(prings, look);", "var nP = 0;")],
  "dl2": DL("2.0"),
  "nosim": [(SIM, "gl.uniform4fv(Psp.u.I, pI);")],
  "nocau": [("if (r1 >= r0) gl.drawElements", "if (false) gl.drawElements")],
  "noblur": [("gl.uniform2f(Pb.u.cb, cr / W_, cr / H_);\n        gl.bindVertexArray(vaoT); gl.drawArrays(gl.TRIANGLES, 0, 3);", "gl.uniform2f(Pb.u.cb, cr / W_, cr / H_);")],
  "nocomp": [("var Po = nP ? PoP : Po0;", "var Po = Po0;")],
}
if os.environ.get("ONLY"): V = {k: v for k, v in V.items() if k in os.environ["ONLY"].split(",")}
PROBE = "(()=>{window.__iv=[];let l=0;function f(t){if(l)__iv.push(t-l);l=t;requestAnimationFrame(f)};requestAnimationFrame(f)})()"
async def run(b, name, w, h):
    ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, color_scheme=os.environ.get("THEME", "light"))
    pg = await ctx.new_page()
    async def route(r):
        resp = await r.fetch(); body = await resp.text()
        for a, c in V[name]:
            assert a in body, (name, a); body = body.replace(a, c)
        await r.fulfill(response=resp, body=body)
    async def rindex(r):
        resp = await r.fetch(); body = await resp.text()
        await r.fulfill(response=resp, body=body.replace('water: "real",', 'water: "real", adaptive: false,'))
    await pg.route("**/src/ink-fish.js*", route); await pg.route("**/index.html", rindex)
    await pg.goto(U); await pg.evaluate("sessionStorage.clear()"); await pg.wait_for_timeout(3500)
    await pg.mouse.move(w * 0.4, h * 0.35); await pg.wait_for_timeout(1500)
    s0 = await pg.evaluate("(()=>{var s=document.body.__inkFish.stats;return [s.n,s.ms]})()")
    await pg.evaluate(PROBE)
    await pg.mouse.down()
    for i in range(40):
        await pg.mouse.move(w*(0.2+0.2*i/40), h*0.4); await pg.wait_for_timeout(45)
    await pg.mouse.up(); await pg.wait_for_timeout(300); await pg.mouse.move(w*0.15,h*0.6); await pg.mouse.down()
    for i in range(12):
        await pg.mouse.move(w*(0.15+0.7*i/12), h*(0.6-0.15*i/12)); await pg.wait_for_timeout(16)
    await pg.mouse.up(); await pg.wait_for_timeout(1800)
    iv = await pg.evaluate("__iv"); s1 = await pg.evaluate("(()=>{var s=document.body.__inkFish.stats;return [s.n,s.ms]})()")
    await ctx.close()
    return (s1[1]-s0[1])/max(1,s1[0]-s0[0]), statistics.mean(iv)
async def main():
    R = {k: [] for k in V}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--hide-scrollbars"])
        for rep in range(int(os.environ.get("REPS", "3"))):
            for k in V:
                m = await run(b, k, 1440, 900); R[k].append(m); print(k, "lib %.3f iv %.1f" % m, flush=True)
        await b.close()
    for k in V: print("%-8s lib median %.3f  iv median %.1f" % (k, statistics.median(x[0] for x in R[k]), statistics.median(x[1] for x in R[k])))
asyncio.run(main())
