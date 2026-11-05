# per-frame pixel difference between two frame folders (mean abs over RGB, max channel diff)
import sys, numpy as np
from PIL import Image
a, b = sys.argv[1], sys.argv[2]; frames = [int(x) for x in sys.argv[3].split(",")]
for i in frames:
    A = np.asarray(Image.open(f"{a}/f{i:04d}.png").convert("RGB"), dtype=np.int16)
    B = np.asarray(Image.open(f"{b}/f{i:04d}.png").convert("RGB"), dtype=np.int16)
    d = np.abs(A - B); print(f"f{i:04d} mean {d.mean():.4f} max {d.max()} px>8 {(d.max(axis=2)>8).mean()*100:.3f}%")
