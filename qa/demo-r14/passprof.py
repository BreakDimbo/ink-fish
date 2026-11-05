# r14 dev: which promo pass costs GPU time? hold a press at the centre (promo ring live, no wake), mean rAF interval
# over 3 s on SwiftShader, for route-patched variants of the new build; interleaved, REPS each
import asyncio, os, json, statistics
from playwright.async_api import async_playwright
U = "http://127.0.0.1:8861/ink-fish/index.html"
SIM = "gl.uniform4fv(Psp.u.I, pI);\n        gl.drawArrays(gl.TRIANGLES, 0, 3);"
V = {
  "base": [],
  "tinybox": [("var PR_REACH = function (t) { return", "var PR_REACH = function (t) { return 20; return")],
  "noclear": [("gl.bindFramebuffer(gl.FRAMEBUFFER, pT.fW); gl.viewport(0, 0, sw, shh); gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);", "gl.bindFramebuffer(gl.FRAMEBUFFER, pT.fW); gl.viewport(0, 0, sw, shh);")],
  "nopromo": [("var nP = promo(prings, look);", "var nP = 0;")],
  "nocomp": [("look.psg, nP ? 1 : 0, 0)", "look.psg, 0, 0)")],
  "nopass": [("gl.bindVertexArray(vaoT); gl.drawArrays(gl.TRIANGLES, 0, 3);\n        // the box", "// the box"), (SIM, "gl.uniform4fv(Psp.u.I, pI);"),
             ("if (r1 >= r0) gl.drawElements", "if (false) gl.drawElements"),
             ("gl.uniform2f(Pb.u.cb, cr / W_, cr / H_);\n        gl.bindVertexArray(vaoT); gl.drawArrays(gl.TRIANGLES, 0, 3);", "gl.uniform2f(Pb.u.cb, cr / W_, cr / H_);")],
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
    await pg.goto(U); await pg.wait_for_timeout(3500)
    await pg.mouse.move(w * .5, h * .45); await pg.wait_for_timeout(800)
    await pg.mouse.down(); await pg.wait_for_timeout(400)
    await pg.evaluate(PROBE); await pg.wait_for_timeout(3000)
    iv = await pg.evaluate("__iv"); await pg.mouse.up(); await ctx.close()
    return statistics.mean(iv)
async def main():
    R = {k: [] for k in V}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--hide-scrollbars"])
        for rep in range(int(os.environ.get("REPS", "3"))):
            for k in V:
                m = await run(b, k, 1440, 900); R[k].append(round(m, 1)); print(k, round(m, 1), flush=True)
        await b.close()
    for k in V: print("%-8s median %.1f ms  %s" % (k, statistics.median(R[k]), R[k]))
asyncio.run(main())
