# Test-only: qa/qahooks.py with its spec's first anchor updated for v1.5.2 (the GRID_P line gained GRID_ON, GRID_OND).
# The shipped library and qa/release-v1.5/qa-hooks.json are unchanged.
import json, os, sys
SPEC = json.load(open("/workspace/ink-fish-r14/qa/release-v1.5/qa-hooks.json", encoding="utf-8"))
SPEC[0] = [SPEC[0][0].replace("GRID_GAIN = 150;", "GRID_GAIN = 150, GRID_ON = 0.6, GRID_OND = 120;"),
           SPEC[0][1].replace("|| 150;", "|| 150, GRID_ON = 0.6, GRID_OND = 120;")]
def patch(src):
    for a, b in SPEC:
        if src.count(a) != 1:
            print("qahooks152: anchor missing, hooks not injected", file=sys.stderr); return src
    for a, b in SPEC: src = src.replace(a, b)
    return src
async def install(page):
    async def route(r):
        resp = await r.fetch(); body = await resp.text()
        await r.fulfill(response=resp, body=patch(body), headers={k: v for k, v in resp.headers.items() if k.lower() not in ("content-length", "content-encoding")})
    await page.route("**/ink-fish.js*", route)
