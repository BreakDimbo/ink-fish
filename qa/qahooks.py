# Test-only injection of the QA hooks that the release library no longer ships
# (window.__inkFishGridGain, window.__inkFishGrid, water.peek(full), api._peek(full)).
# Usage in a Playwright script:  import qahooks; await qahooks.install(page)
# It serves src/ink-fish.js with the hooks spliced back at fixed anchors (spec in release-v1.5/qa-hooks.json);
# if an anchor is missing the library is served unchanged and the scripts' peeks read null.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = json.load(open(os.path.join(HERE, "release-v1.5", "qa-hooks.json"), encoding="utf-8"))
def patch(src):
    for a, b in SPEC:
        if src.count(a) != 1:
            print("qahooks: anchor missing, hooks not injected", file=sys.stderr); return src
    for a, b in SPEC: src = src.replace(a, b)
    return src
async def install(page):
    async def route(r):
        resp = await r.fetch(); body = await resp.text()
        await r.fulfill(response=resp, body=patch(body), headers={k: v for k, v in resp.headers.items() if k.lower() not in ("content-length", "content-encoding")})
    await page.route("**/ink-fish.js*", route)
