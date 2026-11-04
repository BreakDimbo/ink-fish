# per-frame pixel diff between two drag renders (same deterministic path/clock): mean abs diff and % pixels > 8/255
import sys, numpy as np; from PIL import Image
a, b, n = sys.argv[1], sys.argv[2], int(sys.argv[3]); rows = []
for i in range(n):
    x = np.asarray(Image.open(f'frames/{a}/f{i:04d}.png').convert('RGB'), dtype=np.int16)
    y = np.asarray(Image.open(f'frames/{b}/f{i:04d}.png').convert('RGB'), dtype=np.int16)
    d = np.abs(x - y).max(axis=2); rows.append((i, d.mean(), (d > 8).mean() * 100, d.max()))
for r in rows:
    if r[0] % 15 == 0 or r[0] in (14, 15, 16, 17): print("f%03d mean %.3f  >8: %.3f %%  max %d" % r)
m = np.array([r[1] for r in rows]); p = np.array([r[2] for r in rows])
print("ALL mean %.3f, worst frame mean %.3f (f%d), median >8: %.3f %%" % (m.mean(), m.max(), m.argmax(), np.median(p)))
