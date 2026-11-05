# r15 · real-time side-by-sides (30 fps = 1:1 wall clock). Every panel is the same 960x402 CSS-px window, centred
# where the film's tap sits (600, 292), so a ring's speed on screen compares directly.
# sbs.py OUT.mp4 THEME "label|src" ... ; src = film mp4 (starts tap-0.5 s) or a stepcap frame dir (t0 -0.5 s, 30 Hz)
import sys, os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
out, theme = sys.argv[1], sys.argv[2]; P = [a.split('|') for a in sys.argv[3:]]
GUIDE = os.environ.get('GUIDE'); N = int(os.environ.get('N', 147)); W, H, LB = 960, 402, 34
F = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 17)
FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 15)
bg, fg = ((242, 237, 228), (40, 36, 32)) if theme == 'light' else ((14, 13, 11), (205, 200, 190))
src = []
for lab, s in P:
    if s.endswith('.mp4'):
        d = f'/workspace/r15tmp/sbs-tmp-{abs(hash(s))}'; os.makedirs(d, exist_ok=True)
        if not os.path.exists(d + '/f0001.png'): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', s, d + '/f%04d.png'], check=True)
        src.append((lab, lambda k, d=d: Image.open(f'{d}/f{k + 2:04d}.png')))   # film frame j=k+1 (1-based file k+2): t = (k+1)/30 - 0.5
    else:
        src.append((lab, lambda k, s=s: Image.open(f'{s}/f{k:04d}.png').crop((100, 38, 1060, 440))))  # step frame k: t = (k+1)/30 - 0.5
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{(H + LB) * len(src)}', '-r', '30', '-i', '-',
                      '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
for k in range(N):
    t = (k + 1) / 30 - 0.5; o = Image.new('RGB', (W, (H + LB) * len(src)), bg); d = ImageDraw.Draw(o)
    for r, (lab, g) in enumerate(src):
        try: im = g(k).convert('RGB').resize((W, H))
        except FileNotFoundError: im = Image.new('RGB', (W, H), bg)
        y0 = r * (H + LB); o.paste(im, (0, y0 + LB)); d.text((12, y0 + 6), lab, font=F, fill=fg)
        if r == 0: d.text((W - 190, y0 + 8), f't = {t:+.2f} s', font=FS, fill=fg)
        if GUIDE and t > 0:
            for v, dash in ((71, 6), (93, 3)):   # real pond at koi scale: c_g,min and c_min fronts
                R = v * t; cx, cy = 600, y0 + LB + 292
                for a in np.arange(0, 2 * np.pi, dash / max(R, 1) * 2):
                    x, y = cx + R * np.cos(a), cy + R * np.sin(a)
                    if y0 + LB <= y < y0 + LB + H: d.point((x, y), fill=(58, 124, 165))
    p.stdin.write(o.tobytes())
p.stdin.close(); p.wait(); print(out)
