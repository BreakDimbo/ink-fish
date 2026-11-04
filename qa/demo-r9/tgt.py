# measured targets from water-only renders (MEASURE=1 drag.py captures, |frame − still| in grey levels, 1440×900, 30 fps)
# usage: tgt.py tap RUN STILL | slow RUN STILL [REF_RUN REF_STILL] | fast RUN STILL
import sys, math, numpy as np
from PIL import Image
def L(run, i): return np.asarray(Image.open(f"frames/{run}/f{i:04d}.png").convert("L"), dtype=np.float32)
def D(run, still, i): return L(run, i) - L(still, i)
mode = sys.argv[1]
if mode == "tap":
    run, still = sys.argv[2], sys.argv[3]
    CX, CY, RM = 700, 290, 228          # clear water up to r = 228 (header rule at y≈62)
    yy, xx = np.mgrid[0:900, 0:1440]; R = np.hypot(xx - CX, yy - CY)
    sel = R < RM; ri = R[sel].astype(int)
    cnt = np.bincount(ri, minlength=RM)
    def prof(i):
        d = D(run, still, i)[sel]
        sg = np.bincount(ri, d, minlength=RM) / np.maximum(cnt, 1)          # signed azimuthal mean
        ab = np.bincount(ri, np.abs(d), minlength=RM) / np.maximum(cnt, 1)  # mean |dL|
        return sg, ab
    # noise from the still-vs-still difference is 0 (deterministic), so use the far ring of the last frames
    N = int(sys.argv[4]) if len(sys.argv) > 4 else 120
    P = [prof(i) for i in range(N)]
    noise = max(0.25, float(np.percentile(np.concatenate([P[i][1][30:] for i in range(N - 6, N)]), 99)))
    thr = max(0.6, 2 * noise)
    print(f"noise (99th pct |dL| late frames) {noise:.2f}; visibility threshold {thr:.2f} grey levels (azimuthal mean)")
    for name, f0, f1 in (("press", 0, 60), ("release", 60, N)):
        rows = []
        for i in range(f0 + 1, f1):
            sg, ab = P[i]; t = (i - f0) / 30
            idx = np.where(ab[26:] > thr)[0] + 26
            inner = int(idx.min()) if len(idx) else -1; outer = int(idx.max()) if len(idx) else -1
            w = ab[26:RM - 2]; rc = float((np.arange(26, RM - 2) * w).sum() / max(w.sum(), 1e-6))
            rows.append((t, inner, outer, rc, float(ab[26:].max()), sg))
        print(f"\n[{name} packet]  t(s)  inner  outer  centroid  peak|dL|")
        for r in rows[:36]: print(f"   {r[0]:5.2f} {r[1]:5d} {r[2]:6d} {r[3]:8.1f} {r[4]:7.2f}")
        ok = [r for r in rows if 40 < r[1] < 200 and r[2] < RM - 4]
        if len(ok) >= 3:
            v_in = np.polyfit([r[0] for r in ok], [r[1] for r in ok], 1)[0]
            print(f"  calm-centre (inner) edge speed ≈ {v_in:.0f} px/s over {len(ok)} frames")
        ok2 = [r for r in rows if 40 < r[2] < RM - 4]
        if len(ok2) >= 3:
            v_out = np.polyfit([r[0] for r in ok2], [r[2] for r in ok2], 1)[0]
            print(f"  outer front speed ≈ {v_out:.0f} px/s over {len(ok2)} frames")
        # crests when the packet sits at ~150 px: local maxima of the signed profile above the threshold, within the packet
        best = min(rows, key=lambda r: abs(r[3] - 150))
        sg = np.convolve(best[5], np.ones(2) / 2, "same")
        pk = [r for r in range(28, RM - 2) if sg[r] > sg[r - 1] and sg[r] >= sg[r + 1] and sg[r] > thr / 2]
        tr = [r for r in range(28, RM - 2) if sg[r] < sg[r - 1] and sg[r] <= sg[r + 1] and sg[r] < -thr / 2]
        print(f"  at t={best[0]:.2f} s (centroid {best[3]:.0f} px): {len(pk)} bright crests, {len(tr)} dark troughs above ±{thr/2:.2f}: crests at r={pk}")
        if len(pk) > 2: dl = np.diff(pk); print(f"  crest spacing: inner {dl[:3].tolist()} … outer {dl[-3:].tolist()} px")
        vis = [r for r in rows if r[4] > thr]
        print(f"  visible (peak azimuthal |dL| > {thr:.2f}) until t={vis[-1][0] if vis else 0:.2f} s after the {name}")
        # also the per-pixel view: fraction of pixels with |dL| > 3 grey levels (what an eye picks out)
        for i in range(f0 + 1, f1):
            d = np.abs(D(run, still, i))[sel]
            if (d > 3).mean() < 0.002 and i > f0 + 6: print(f"  per-pixel: <0.2 % of the disc above 3 grey levels from t={(i - f0)/30:.2f} s"); break
elif mode == "slow":
    # energy behind the finger over the slow 200 px/s stroke (t 0.5–4.5 s, x 300→1100, y 430−50·sin): Σ|dL| excluding r<30 around the finger
    def energy(run, still, excl=30):
        E, Ed = 0.0, 0.0
        yy, xx = np.mgrid[0:900, 0:1440]
        for i in range(15, 150):
            t = i / 30; u = min(max((t - 0.5) / 4, 0), 1); fx, fy = 300 + 800 * u, 430 - 50 * math.sin(u * math.pi)
            d = np.abs(D(run, still, i))[200:700, 150:1250]
            m = np.hypot(xx[200:700, 150:1250] - fx, yy[200:700, 150:1250] - fy) >= excl
            d = np.where(d > 1.0, d, 0)   # ignore sub-grey-level dither
            E += float(d[m].sum()); Ed += float(d.sum())
        return E, Ed
    E, Ed = energy(sys.argv[2], sys.argv[3])
    print(f"slow drag: Σ|dL| behind finger (excl. r<30) {E:.3e}, incl. dimple {Ed:.3e}")
    if len(sys.argv) > 5:
        Er, Erd = energy(sys.argv[4], sys.argv[5])
        print(f"reference: behind {Er:.3e}, incl. {Erd:.3e}  →  ratio behind {E / Er * 100:.1f} %, incl. dimple {Ed / Erd * 100:.1f} %")
elif mode == "fast":
    # wake half-angle: fast path 280,470 → 1140,330 over t 0.5–1.2 s (≈1245 px/s). In each frame while moving,
    # for distances s behind the finger, find the angle of max |dL| on each side of the track
    run, still = sys.argv[2], sys.argv[3]
    ux, uy = 860, -140; n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
    yy, xx = np.mgrid[0:900, 0:1440]
    res = []
    for i in range(27, 37):
        t = i / 30; u = (t - 0.5) / 0.7; fx, fy = 280 + 860 * u, 470 - 140 * u
        d = np.abs(D(run, still, i)); d = np.maximum(d - 1.0, 0)
        rx, ry = xx - fx, yy - fy
        along = -(rx * ux + ry * uy); side = rx * (-uy) + ry * ux
        ang = np.degrees(np.arctan2(side, along))
        for s0 in range(60, 320, 20):
            band = (along > s0) & (along < s0 + 20) & (np.abs(ang) < 45)
            if band.sum() < 50: continue
            for sgn in (1, -1):
                m = band & (np.sign(ang) == sgn) & (np.abs(ang) > 2)
                a = np.abs(ang[m]); w = d[m]
                if w.max() < 2: continue
                h, e = np.histogram(a, bins=43, range=(2, 45), weights=w); c = np.histogram(a, bins=43, range=(2, 45))[0]
                h = h / np.maximum(c, 1); res.append((t, s0, sgn, float(e[np.argmax(h)] + 0.5), float(h.max())))
    A = np.array([r[3] for r in res])
    print(f"fast drag (~1245 px/s): {len(res)} (frame, distance, side) samples; arm angle of max contrast: median {np.median(A):.1f}°, IQR {np.percentile(A,25):.1f}–{np.percentile(A,75):.1f}°")
    for s0 in range(60, 320, 40):
        a = [r[3] for r in res if s0 <= r[1] < s0 + 40]
        if a: print(f"   {s0:3d}–{s0+40:3d} px behind: median {np.median(a):.1f}° (n={len(a)})")
