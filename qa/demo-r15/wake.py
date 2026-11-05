# lateral spread of the drag wake at column x=500 (pointer passes at t=0.65 s), CSS px from the stroke line y=330
import numpy as np, sys, json
from PIL import Image
from scipy.ndimage import gaussian_filter
d = sys.argv[1]; out = sys.argv[2]; HZ = 30; t0 = -0.5
def hp(i):
    a = np.asarray(Image.open(f'{d}/f{i:04d}.png').convert('L'), float); h = np.abs(a - gaussian_filter(a, 6))
    col = h[:, 470:531].mean(1); return np.maximum(col[330:330 + 400], col[330 - 300:330][::-1].tolist() + [0] * 100)
B = np.mean([hp(i) for i in range(2, 13)], 0); nz = np.median(B)
rows = []
for i in range(13, 135, 3):
    t = t0 + (i + 1) / HZ; p = gaussian_filter(hp(i) - B, 2); m = np.where(p > max(0.35, 4 * nz))[0]
    lead = int(m.max()) if len(m) else 0; rows.append(dict(t=round(t, 3), since=round(t - 0.65, 3), lead=lead, amp=round(float(p[5:].max()), 3)))
    print(rows[-1])
json.dump(dict(noise=nz, rows=rows), open(out, 'w'))
