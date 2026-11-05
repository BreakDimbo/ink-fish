# ring radius vs time, robust to moving fish: high-pass luma (minus a gaussian blur), azimuthal MEDIAN per 1-px radius
# bin (a ring is coherent around the circle; fish and the idle texture are not), absolute, lightly smoothed over r.
# Noise = the same profile on pre-press frames (max over them per r, x1.5). Reports the crest (max excess) and the
# leading edge (outermost r with excess > 3 x noise median), in CSS px (divide by scale), t from the press.
# usage: ringhp.py DIR fmt ibg0 ibg1 i0 i1 fps t_press_s cx cy rmax scale out.json   (env Y0/Y1 picture rows, SIG)
import sys, os, json, numpy as np; from PIL import Image; from scipy.ndimage import gaussian_filter, uniform_filter1d
D, fmt = sys.argv[1:3]; ibg0, ibg1, i0, i1 = map(int, sys.argv[3:7]); fps, tp, cx, cy, rmax, sc = map(float, sys.argv[7:13]); out = sys.argv[13]
SIG = float(os.environ.get("SIG", 6)); Y0 = float(os.environ.get("Y0", 0)); Y1 = float(os.environ.get("Y1", 1e9))
def L(i): return np.asarray(Image.open(f"{D}/{fmt % i}").convert("L"), dtype=np.float32)
a = L(ibg0); H, W = a.shape; yy, xx = np.mgrid[0:H, 0:W]; rr = np.hypot(xx - cx, yy - cy)
ok = (rr < rmax) & (yy >= Y0) & (yy < Y1); ri = rr[ok].astype(int); order = np.argsort(ri, kind="stable"); ris = ri[order]
cuts = np.searchsorted(ris, np.arange(int(rmax) + 1))
def prof(i):
    im = L(i); hp = (im - gaussian_filter(im, SIG))[ok][order]
    p = np.array([np.median(hp[cuts[r]:cuts[r + 1]]) if cuts[r + 1] - cuts[r] > 12 else 0. for r in range(int(rmax))])
    return uniform_filter1d(np.abs(p), 3)
noise = np.max([prof(i) for i in range(ibg0, ibg1 + 1)], axis=0) * 1.5 + 0.05; nm = float(np.median(noise))
res = []
for i in range(i0, i1 + 1):
    p = prof(i); ex = p - noise; ex[:4] = 0
    crest = int(np.argmax(ex)); amp = float(ex[crest]); lead = np.where(ex > 3 * nm)[0]; lead = int(lead.max()) if len(lead) else 0
    t = i / fps - tp
    res.append(dict(i=i, t=round(t, 4), crest=round(crest / sc, 1), lead=round(lead / sc, 1), amp=round(amp, 3)))
    print("%d t=%.3f crest %.1f lead %.1f amp %.3f (noise %.3f)" % (i, t, crest / sc, lead / sc, amp, nm), flush=True)
json.dump(dict(scale=sc, noise=nm, rows=res), open(out, "w"))
