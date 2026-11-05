# r14 dev: a grid of crops, one row per frame index, one column per source folder: cmp.py out.jpg cx,cy,w,h,scale idxs dir1[:label] dir2[:label] ...
import sys
from PIL import Image, ImageDraw
out, box, idx = sys.argv[1], [float(v) for v in sys.argv[2].split(",")], [int(v) for v in sys.argv[3].split(",")]
cols = [a.split(":") for a in sys.argv[4:]]
cx, cy, w, h, sc = box[:5]; T0 = box[5] if len(box) > 5 else 60
tw, th = int(w * sc), int(h * sc)
G = Image.new("RGB", (tw * len(cols), (th + 18) * len(idx) + 18), (255, 255, 255)); d = ImageDraw.Draw(G)
for j, c in enumerate(cols): d.text((j * tw + 6, 3), c[1] if len(c) > 1 else c[0][-30:], fill=(0, 0, 0))
for i, k in enumerate(idx):
    for j, c in enumerate(cols):
        try: im = Image.open(f"{c[0]}/f{k:04d}.png").convert("RGB")
        except Exception: continue
        im = im.crop((int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2))).resize((tw, th), Image.LANCZOS)
        G.paste(im, (j * tw, 18 + i * (th + 18) + 18))
    d.text((4, 18 + i * (th + 18) + 3), f"f{k} (t={(k - T0) / 30:+.2f}s from press)" , fill=(0, 0, 0))
G.save(out, quality=90)
