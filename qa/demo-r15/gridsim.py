# r15 · numpy copy of the drag-wake step (FS_GSTEP) to calibrate a retune offline: speeds (impulse ring radius vs t)
# and the response to a moving pressure (peak |∇h| over the run), old (v1.5.2) vs new parameters.
import numpy as np, sys, json
def run(P, rate, gp, U, dur=1.0, impulse=False, gc=5.0, W=1440, H=900):
    gx, gy = int(W / gc), int(H / gc); h = np.zeros((gy, gx)); v = np.zeros_like(h)
    yy, xx = np.mgrid[0:gy, 0:gx] + 0.5
    e = np.minimum(np.minimum(xx, yy), np.minimum(gx - xx, gy - yy)); sp = 0.82 + 0.18 * np.clip(e / 7, 0, 1) ** 2 * (3 - 2 * np.clip(e / 7, 0, 1))
    def sh(a, dx, dy): return np.roll(np.roll(a, dy, 0), dx, 1)
    n = int(round(dur * rate)); x0, y0 = 300 / gc, 450 / gc; R = P["R"]; peak = 0; rad = []
    for i in range(n):
        t = (i + 1) / rate
        if impulse: ax = bx = x0 + 100 / gc; ay = by = y0; on = t <= 0.12
        else: ax = x0 + U * (t - 1 / rate) / gc; bx = x0 + U * t / gc; ay = by = y0; on = True
        L = sh(h, 1, 0) + sh(h, -1, 0) + sh(h, 0, 1) + sh(h, 0, -1) - 4 * h
        s4 = L + 4 * h; dg = sh(h, 1, 1) + sh(h, -1, 1) + sh(h, 1, -1) + sh(h, -1, -1); f4 = sh(h, 2, 0) + sh(h, -2, 0) + sh(h, 0, 2) + sh(h, 0, -2)
        B = 20 * h - 8 * s4 + 2 * dg + f4; Lv = sh(v, 1, 0) + sh(v, -1, 0) + sh(v, 0, 1) + sh(v, 0, -1) - 4 * v
        abx, aby = bx - ax, by - ay; tt = np.clip(((xx - ax) * abx + (yy - ay) * aby) / max(abx * abx + aby * aby, 1e-4), 0, 1)
        dd = np.hypot(xx - ax - abx * tt, yy - ay - aby * tt); w = np.where(dd < R, 0.5 + 0.5 * np.cos(np.pi * dd / R), 0)
        ln = np.hypot(abx, aby); amp = (gp * (2 * R) / (2 * R + ln)) if on else 0
        v = (v + P["c2"] * L - P["b"] * B - P["k"] * h + P["mu"] * Lv - amp * w) * P["damp"] * sp; h = h + v
        gyx = np.hypot(np.gradient(h, axis=1), np.gradient(h, axis=0)) / gc; peak = max(peak, gyx.max())
        if impulse and i % max(1, rate // 20) == 0:
            cx, cy = x0 + 100 / gc, y0; r = np.hypot(xx - cx, yy - cy) * gc; m = gyx.max()
            lead = r[gyx > 0.15 * m].max() if m > 0 else 0; crest = r.flat[gyx.argmax()]
            rad.append((round(t, 3), round(float(crest), 1), round(float(lead), 1)))
    return peak, rad
OLD = dict(c2=0.19, b=0.03, k=0.03, mu=0.006, damp=0.991, R=2.0)
f = float(sys.argv[1]) if len(sys.argv) > 1 else 0.307; RATE = 60; q = (f * 120 / RATE) ** 2
NEW = dict(c2=0.19 * q, b=0.03 * q, k=0.03 * q, mu=0.012, damp=0.991 ** (120 / RATE), R=2.0)
print("NEW", {k: round(v, 5) for k, v in NEW.items()}, "nyq", 8 * NEW["c2"] + 64 * NEW["b"] + NEW["k"])
po, ro = run(OLD, 120, 0.02, 0, 1.2, impulse=True); pn, rn = run(NEW, RATE, 0.02, 0, 1.2, impulse=True)
print("impulse old", ro[::2]); print("impulse new", rn[::2]); print("impulse peak old %.3g new %.3g" % (po, pn))
out = {}
for U in (200, 600, 1200):
    a, _ = run(OLD, 120, 0.02, U, 0.8); b, _ = run(NEW, RATE, 0.02, U, 0.8); out[U] = (a, b); print("U=%d peak old %.3g new %.3g ratio %.2f" % (U, a, b, b / a))
