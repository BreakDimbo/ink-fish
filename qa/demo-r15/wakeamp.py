# peak wake contrast (high-pass |luma|, 95th pct) in a band 15-120 px off the stroke path, excluding the dimple/rings near the pointer
import numpy as np, sys
from PIL import Image
from scipy.ndimage import gaussian_filter
d, kind = sys.argv[1], sys.argv[2]
def hp(i):
    a = np.asarray(Image.open(f'{d}/f{i:04d}.png').convert('L'), float); return np.abs(a - gaussian_filter(a, 6))
B = np.mean([hp(i) for i in range(2, 13)], 0)
for t in (0.4, 0.6, 0.8, 1.2, 1.6, 2.0):
    i = int(round((t + 0.5) * 30)) - 1
    try: h = hp(i) - B
    except FileNotFoundError: continue
    if kind == 'drag': x0, x1, yc = 420, 560, 330   # behind the finger (passes x 500 at 0.65 s)
    else: x0, x1, yc = 400, 560, None
    if kind == 'drag': band = np.r_[h[yc - 120:yc - 15, x0:x1].ravel(), h[yc + 15:yc + 120, x0:x1].ravel()]
    else:
        yy, xx = np.mgrid[0:h.shape[0], 0:h.shape[1]]; ys = 430 - 140 * (xx - 300) / 840; dd = np.abs(yy - ys)
        m = (dd > 15) & (dd < 120) & (xx > x0) & (xx < x1); band = h[m]
    print(d.split('/')[-1], 't', t, 'wake p95 %.2f p99 %.2f' % (np.percentile(band, 95), np.percentile(band, 99)))
