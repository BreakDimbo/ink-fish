# contact sheet: rows = builds, cols = frames (crop around the click spot)
import sys; from PIL import Image, ImageDraw
kind, theme, out = sys.argv[1:4]; builds = sys.argv[4].split(','); fr = [int(x) for x in sys.argv[5].split(',')]
box = tuple(int(x) for x in sys.argv[6].split(',')) if len(sys.argv) > 6 else (450, 130, 950, 530)
W, H = (box[2]-box[0])//2*1, (box[3]-box[1])//2*1
W, H = box[2]-box[0], box[3]-box[1]; s = 0.6
o = Image.new('RGB', (int(W*s)*len(fr), int(H*s)*len(builds)), 'gray'); d = ImageDraw.Draw(o)
for r, b in enumerate(builds):
    for c, n in enumerate(fr):
        im = Image.open(f'frames/{kind}-{b}-{theme}/f{n:04d}.png').convert('RGB').crop(box).resize((int(W*s), int(H*s)))
        o.paste(im, (c*int(W*s), r*int(H*s))); d.text((c*int(W*s)+6, r*int(H*s)+6), f'{b} f{n} t={n/30:.2f}s', fill='red')
o.save(out)
