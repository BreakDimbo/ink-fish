# front propagation + decay from renders: |frame − still baseline| (water only, no fish), column x, below a straight stroke at y=450
import sys, numpy as np
from PIL import Image
run, base = sys.argv[1], sys.argv[2]
X = int(sys.argv[3]) if len(sys.argv) > 3 else 900
T_PASS = 0.3 + (X - 200) / 1600            # when the pointer crossed the column
def L(p): return np.asarray(Image.open(p).convert("L"), dtype=np.float32)
rows = []
for i in range(0, 75):
    a = L(f"frames/{run}/f{i:04d}.png"); b = L(f"frames/{base}/f{i:04d}.png")
    col = np.abs(a - b)[450:900, X - 3:X + 4].mean(axis=1)            # dy = 0..449
    col = np.convolve(col, np.ones(3) / 3, "same")
    rows.append(col)
R = np.array(rows); noise = np.percentile(R[:5], 99) + 0.6
print(f"noise floor {noise:.2f} grey levels; column x={X}; pointer crossed at t={T_PASS:.3f} s")
print(" t-tpass(s)  outer front dy(px)  peak |dL|  peak at dy  energy(sum dL)")
fr = []
for i, col in enumerate(R):
    t = i / 30 - T_PASS
    if t < -0.04: continue
    idx = np.where(col > noise)[0]
    outer = int(idx.max()) if len(idx) else -1
    pk = float(col.max()); 
    print(f"  {t:6.3f}   {outer:6d}   {pk:7.2f}   {int(col.argmax()):5d}   {col.sum():8.0f}")
    fr.append((t, outer, pk, col.sum()))
fr = np.array(fr)
ok = (fr[:, 1] > 15) & (fr[:, 1] < 440) & (fr[:, 0] > 0)
if ok.sum() >= 3:
    v = np.polyfit(fr[ok, 0], fr[ok, 1], 1)[0]; print(f"outer front speed ≈ {v:.0f} px/s (fit over {ok.sum()} frames)")
E = fr[fr[:, 0] > 0.1]
if len(E) > 4:
    k = np.polyfit(E[:, 0], np.log(np.maximum(E[:, 2], 1e-3)), 1)[0]; print(f"peak contrast decay: ×{np.exp(k):.2f} per second (rate {-k:.2f}/s)")
    k2 = np.polyfit(E[:, 0], np.log(np.maximum(E[:, 3], 1e-3)), 1)[0]; print(f"total disturbance decay: ×{np.exp(k2):.2f} per second")
