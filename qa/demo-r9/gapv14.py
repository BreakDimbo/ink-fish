# gap-v14.png: gap.png rows (reference, v1.3.1, v1.3.2) + v1.4 light + v1.4 dark at the same combo moments (frames 45,105,150,198,225),
# each tile an 800×468 crop around the action, scaled 0.5 → 400×234 under a 16 px label bar; plus 200 % close-ups (dimple, lift packet)
from PIL import Image, ImageDraw, ImageFont
G = Image.open("../research-real-water/gap.png").convert("RGB")
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
MOM = [(45, "press 1.5s slow", (500, 345)), (105, "slow 3.5s", (900, 345)), (150, "0.5s after lift", (1050, 380)),
       (198, "fast 6.6s", (850, 470)), (225, "0.8s after flick", (850, 470))]
def tile(run, f, c, label):
    im = Image.open(f"frames/{run}/f{f:04d}.png").convert("RGB")
    x0 = min(max(c[0] - 400, 0), 1440 - 800); y0 = min(max(c[1] - 234, 0), 900 - 468)
    t = Image.new("RGB", (400, 250), (0, 0, 0)); t.paste(im.crop((x0, y0, x0 + 800, y0 + 468)).resize((400, 234), Image.LANCZOS), (0, 16))
    ImageDraw.Draw(t).text((3, 2), label, fill=(255, 255, 0), font=F); return t
out = Image.new("RGB", (2000, 1250)); out.paste(G, (0, 0))
for r, (run, tag) in enumerate([("after-light", "v1.4 light"), ("after-dark", "v1.4 dark")]):
    for i, (f, lab, c) in enumerate(MOM): out.paste(tile(run, f, c, f"{tag} {lab}"), (400 * i, 750 + 250 * r))
out.save("gap-v14.png")
for th in ("light", "dark"):
    run = f"after-{th}"; cs = []
    for f, c, lab in ((105, (900, 345), "dimple + meniscus under the finger, slow drag 200 px/s (t 3.5 s)"), (150, (1100, 380), "release ring packet, 0.5 s after lift (t 5.0 s)")):
        im = Image.open(f"frames/{run}/f{f:04d}.png").convert("RGB")
        x0, y0 = min(max(c[0] - 240, 0), 1440 - 480), min(max(c[1] - 170, 0), 900 - 340)
        z = im.crop((x0, y0, x0 + 480, y0 + 340)).resize((960, 680), Image.NEAREST if False else Image.LANCZOS)
        d = ImageDraw.Draw(z); d.rectangle((0, 0, 960, 18), fill=(0, 0, 0)); d.text((5, 3), f"v1.4 {th} 200 %: {lab}", fill=(255, 255, 0), font=F); cs.append(z)
    o = Image.new("RGB", (1924, 680), (0, 0, 0)); o.paste(cs[0], (0, 0)); o.paste(cs[1], (964, 0)); o.save(f"closeup-{th}-200.png")
