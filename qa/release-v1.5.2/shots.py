# release screenshots of the live-style demo (no QA hooks), light and dark, 1440 and 390; reports page/console errors
import asyncio, json
from playwright.async_api import async_playwright
U = "http://127.0.0.1:8861/ink-fish/index.html"; OUT = "/workspace/ink-fish-r14/qa/release-v1.5.2"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist","--hide-scrollbars"])
        res = []
        for theme in ("light", "dark"):
            for w, h in ((1440, 900), (390, 844)):
                pg = await b.new_page(viewport={"width": w, "height": h}, color_scheme=theme); errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                await pg.goto(U); await pg.wait_for_timeout(2500)
                # one fast flick through the pond so the grid wake is in the shot
                y = h * 0.55; await pg.mouse.move(w * 0.15, y); await pg.mouse.down()
                for i in range(12): await pg.mouse.move(w * (0.15 + 0.05 * i), y - 3 * i); await pg.wait_for_timeout(16)
                await pg.wait_for_timeout(150)
                await pg.screenshot(path=f"{OUT}/demo-{theme}-{w}.png")
                await pg.mouse.up(); await pg.wait_for_timeout(500)
                info = await pg.evaluate("(()=>{var a=document.body.__inkFish;return {version:InkFish.version,water:a&&a.water,hooks:{peek:!!(a&&a._peek),gain:'__inkFishGridGain' in window}}})()")
                res.append({"theme": theme, "w": w, **info, "errors": errs}); await pg.close()
        await b.close()
        print(json.dumps(res, indent=1))
asyncio.run(main())
