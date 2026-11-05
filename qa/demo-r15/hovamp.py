import numpy as np, sys
from PIL import Image
from scipy.ndimage import gaussian_filter
def prof(im, cx, cy, rmax=400):
    a = np.asarray(Image.open(im).convert('L'), float); h = a - gaussian_filter(a, 6)
    yy, xx = np.indices(h.shape); r = np.hypot(xx - cx, yy - cy).astype(int); out = np.zeros(rmax)
    for k in range(4, rmax):
        m = r == k
        if m.sum() > 20: out[k] = np.median(np.abs(h[m]))
    return out
def amp(d, i, cx, cy, bx, by):
    p = prof(f'{d}/f{i:04d}.png', cx, cy); b = prof(f'{d}/f{i:04d}.png', bx, by)
    return p.max() - np.median(b[4:]), int(p.argmax())
for v in ('s152', 's153'):
    d = f'step/{v}-moveclick-light'
    for age in (0.3, 0.5, 0.8):
        ih = int(round(age * 30)) - 1          # hover ring at (400,480) born t=-1.0
        ic = int(round((1.0 + age) * 30)) - 1  # click ring at (700,330) born t=0
        print(v, f'age {age}', 'hover amp/r', amp(d, ih, 400, 480, 1200, 150), 'click amp/r', amp(d, ic, 700, 330, 1200, 150))
