# 3-way still: v1.3.1 | v1.5 grid wake | webgl-water reference (Evan Wallace demo, drag frame), light and dark rows
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
R9 = "/workspace/ink-fish/qa/demo-r9/frames"; R11 = "/workspace/ink-fish/qa/demo-r11/frames"
REF = "/workspace/ink-fish/qa/relearn-ultra-water/frames-evw-top"
def lab(im, t, dark):
    d = ImageDraw.Draw(im); w = d.textlength(t, font=F)
    d.rectangle((8, 8, 20 + w, 30), fill=(0, 0, 0) if dark else (255, 255, 255)); d.text((14, 10), t, font=F, fill=(220, 215, 205) if dark else (40, 36, 32)); return im
fr = 198  # t = 6.6 s: end of the 1250 px/s flick
box = (640, 210, 1120, 660)
rows = []
for th in ("light", "dark"):
    dk = th == "dark"
    a = lab(Image.open(f"{R9}/before-{th}/f{fr:04d}.png").convert("RGB").crop(box), f"v1.3.1 · {th} · t 6.6 s flick", dk)
    b = lab(Image.open(f"{R11}/after-{th}/f{fr:04d}.png").convert("RGB").crop(box), f"v1.5 grid wake · {th}", dk)
    r = lab(Image.open(f"{REF}/f0050.png").convert("RGB").crop((230, 75, 710, 525)), "webgl-water (reference) · drag", True)
    row = Image.new("RGB", (1440, 450)); [row.paste(x, (i * 480, 0)) for i, x in enumerate((a, b, r))]; rows.append(row)
out = Image.new("RGB", (1440, 900)); out.paste(rows[0], (0, 0)); out.paste(rows[1], (0, 450)); out.save("/workspace/ink-fish/qa/demo-r11/still-3way.png")
