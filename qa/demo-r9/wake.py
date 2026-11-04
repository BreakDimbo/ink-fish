# strength / half-angle / crest spacing of the pressed wake vs speed (virtual 60 Hz clock, water only, light, 1440×900)
# straight stroke along y=450 from x=200 at U px/s; frame taken when the finger reaches x=1150 (still pressed)
import asyncio, json, math, os, sys, numpy as np
from PIL import Image
from playwright.async_api import async_playwright
INIT = open("/workspace/ink-fish/qa/demo-r9/drag.py").read().split('INIT = """')[1].split('"""')[0]
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8733/index.html"
THEME = os.environ.get("THEME", "light"); HOVER = os.environ.get("HOVER")
US = [int(u) for u in os.environ.get("US", "200,400,600,900,1200,1800,2400").split(",")]
X0, X1, Y, T0 = 200, 1150, 450, 0.3
async def shot(b, U):
    pg = await b.new_page(viewport={"width": 1440, "height": 900}, color_scheme=THEME); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.add_init_script(INIT)
    async def route(r):
        resp = await r.fetch(); body = await resp.text()
        body = body.replace('water: "real",', 'water: "real", adaptive: false,').replace("koi: true,", "koi: false, opacity: 0, shadow: 0,")
        await r.fulfill(response=resp, body=body)
    await pg.route("**/index.html", route)
    await pg.goto(URL); await pg.wait_for_timeout(600)
    for i in range(300): await pg.evaluate("__step(1000/60)")
    await pg.wait_for_timeout(1500)
    n_end = int(round((T0 + (X1 - X0) / U) * 60)) if U else int(round((T0 + 0.6) * 60))
    down = False
    for i in range(n_end + 1):
        t = i / 60
        if U:
            x = X0 + U * max(0, t - T0)
            await pg.mouse.move(x, Y)
            if not HOVER and not down and t >= T0 - 1e-9: await pg.mouse.down(); down = True
        await pg.evaluate("__step(1000/60)")
    p = f"/tmp/wake_{THEME}_{'h' if HOVER else 'p'}_{U}.png"
    await pg.screenshot(path=p, timeout=180000); await pg.close()
    return p, n_end, errs
async def main():
    res = {}; stills = {}
    if os.environ.get("ANALYZE"):
        for U in US: res[U] = (f"/tmp/wake_{THEME}_{'h' if HOVER else 'p'}_{U}.png", 0, "-"); stills[U] = f"/tmp/wake_{THEME}_still_{U}.png"
    else:
      async with async_playwright() as pw:
          b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--hide-scrollbars"])
          for U in US: res[U] = await shot(b, U)
          # stills at the same frame counts (pointer never enters)
          for U in US:
              if os.environ.get("REUSE_STILLS") and os.path.exists(f"/tmp/wake_{THEME}_still_{U}.png"): stills[U] = f"/tmp/wake_{THEME}_still_{U}.png"; continue
              pg = await b.new_page(viewport={"width": 1440, "height": 900}, color_scheme=THEME)
              await pg.add_init_script(INIT)
              async def route(r):
                  resp = await r.fetch(); body = await resp.text()
                  body = body.replace('water: "real",', 'water: "real", adaptive: false,').replace("koi: true,", "koi: false, opacity: 0, shadow: 0,")
                  await r.fulfill(response=resp, body=body)
              await pg.route("**/index.html", route)
              await pg.goto(URL); await pg.wait_for_timeout(600)
              for i in range(300): await pg.evaluate("__step(1000/60)")
              await pg.wait_for_timeout(1500)
              for i in range(res[U][1] + 1): await pg.evaluate("__step(1000/60)")
              sp = f"/tmp/wake_{THEME}_still_{U}.png"; await pg.screenshot(path=sp, timeout=180000); await pg.close(); stills[U] = sp
          await b.close()
    print(f"| U px/s | U cm/s | wake strength Σ|dL| behind (×1e3) | mean |dL| in wedge | half-angle: arm slope fit 100–500 px behind (°) [offset px] | max-contrast median (°) | outer edge (50 %) (°) | asin(cg,min/U) (°) | crests across the wedge 200 px behind: median spacing (px) | errors |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    yy, xx = np.mgrid[0:900, 0:1440]
    for U in US:
        a = np.asarray(Image.open(res[U][0]).convert("L"), float); s = np.asarray(Image.open(stills[U]).convert("L"), float)
        d = np.abs(a - s); d[d <= 1] = 0
        fx = X1; along = fx - xx; lat = yy - Y
        behind = (along > 30) & (along < 700) & (np.abs(lat) < 300) & (np.hypot(along, lat) > 30) & (yy > 80)
        E = d[behind].sum()
        angs = []; angm = []; fit = []
        for s0 in range(60, 500, 20):
            col = (along >= s0) & (along < s0 + 20)
            for sg in (1, -1):
                m = col & (np.sign(lat) == sg) & (np.abs(lat) > 3) & (np.abs(lat) < 300) & (yy > 80)
                if not m.any(): continue
                prof = np.bincount(np.abs(lat[m]).astype(int), d[m], 300) / np.maximum(np.bincount(np.abs(lat[m]).astype(int), minlength=300), 1)
                if prof.max() < 2: continue
                # the arm: the outermost lateral position where |dL| is above half its max (the leading crest of the wedge)
                idx = np.where(prof > 0.5 * prof.max())[0]
                angs.append(math.degrees(math.atan2(idx.max(), s0 + 10))); angm.append(math.degrees(math.atan2(int(np.argmax(prof)), s0 + 10))); fit.append((s0 + 10, int(np.argmax(prof))))
        A = float(np.median(angs)) if angs else float("nan"); Am = float(np.median(angm)) if angm else float("nan")
        fz = np.array([f for f in fit if f[0] >= 100]); Af = math.degrees(math.atan(np.polyfit(fz[:, 0], fz[:, 1], 1)[0])) if len(fz) > 4 else float("nan"); r0 = np.polyfit(fz[:, 0], fz[:, 1], 1)[1] if len(fz) > 4 else float("nan")
        wedge = behind & (np.abs(np.degrees(np.arctan2(np.abs(lat), np.maximum(along, 1)))) < (A if A == A else 20) + 3)
        mw = float(d[wedge].mean()) if wedge.any() else 0
        # crest spacing across one arm at 200 px behind: peaks of the signed difference along the lateral line
        # crests across the wedge 200 px behind: peaks (prominence ≥ 2 grey levels) of the signed difference, averaged
        # over a 9-px strip, from the track out to the arm (+30 px), both sides
        from scipy.signal import find_peaks
        sgn = (a - s)[:, fx - 204:fx - 195].mean(1); armw = int(fz[fz[:, 0] == 210][:, 1].mean() + 30) if len(fz) and (fz[:, 0] == 210).any() else 120
        pk = []; gaps = []
        for side in (1, -1):
            line = sgn[Y + 4:Y + armw] if side > 0 else sgn[Y - armw:Y - 4][::-1]
            q = find_peaks(line, prominence=2)[0]; pk += list(q); gaps += list(np.diff(q))
        sp = float(np.median(gaps)) if len(gaps) > 1 else float("nan")
        cg = 17.7 * 16.7  # cg,min ≈ 17.7 cm/s
        th = math.degrees(math.asin(min(1, cg / U))) if U else float("nan")
        print(f"| {U} | {U/16.7:.0f} | {E/1e3:.1f} | {mw:.2f} | {Af:.1f} [{r0:.0f}] | {Am:.1f} | {A:.1f} (n={len(angs)}) | {th:.1f} | {sp:.1f} ({len(pk)} crests) | {res[U][2]} |", flush=True)
asyncio.run(main())
