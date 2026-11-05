# Test-only: qa/qahooks.py with its spec's first two anchors updated for v1.5.3 (the GRID_P / GRID lines were retuned:
# GRID_P 0.015, GRID c2/b/k/mu/damp/rate). Same hooks injected; the shipped library and qa-hooks.json are unchanged.
import json, os, sys
SPEC = json.load(open("/workspace/ink-fish-r15/qa/release-v1.5/qa-hooks.json", encoding="utf-8"))
_SRC = open("/workspace/ink-fish-r15/src/ink-fish.js", encoding="utf-8").read()
a0, b0 = SPEC[0]; a0 = a0.replace("GRID_GAIN = 150;", "GRID_GAIN = 150, GRID_ON = 0.6, GRID_OND = 120;"); b0 = b0.replace("|| 150;", "|| 150, GRID_ON = 0.6, GRID_OND = 120;")
SPEC[0] = [a0.replace("GRID_P = 0.02", "GRID_P = 0.015"), b0.replace("GRID_P = 0.02", "GRID_P = 0.015")]
a1, b1 = SPEC[1]; assert b1.startswith(a1)
new1 = [l for l in _SRC.split("\n") if l.startswith("    var GRID = { c2:")][0]
SPEC[1] = [new1, new1 + b1[len(a1):]]
def patch(src):
    for a, b in SPEC:
        if src.count(a) != 1:
            print("qahooks153: anchor missing, hooks not injected", file=sys.stderr); return src
    for a, b in SPEC: src = src.replace(a, b)
    return src
async def install(page):
    async def route(r):
        resp = await r.fetch(); body = await resp.text()
        await r.fulfill(response=resp, body=patch(body), headers={k: v for k, v in resp.headers.items() if k.lower() not in ("content-length", "content-encoding")})
    await page.route("**/ink-fish.js*", route)
