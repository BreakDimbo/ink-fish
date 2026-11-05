# r15 · ring kinematics from the library's own closed-form spectra (numpy copies of WATER.spec / specP):
# slope profile dη/dr(r, t) = Σ_k F_k(t)·(−k J1(k r)); crest = r of max |slope|; lead = outermost r with
# |slope| ≥ 15 % of that frame's max (≈ where the film stops showing the ring). Also the textbook numbers.
import numpy as np, json, sys
from scipy.special import j1
G, SR = 9.81, 7.4e-5
def ring(S, NU, SRC, SRCL, two=True, slow=1.0, NK=192, DK=None, RMAX=900, ts=np.arange(0.05, 3.01, 0.05)):
    DK = DK or 4.2 / 4.5 / NK; kp = (np.arange(NK) + 0.5) * DK; km = kp / S
    W = np.sqrt(G * km + SR * km ** 3); VD = 2 * NU * km ** 2; CG = (G + 3 * SR * km ** 2) / (2 * W) / S; RA = 0.48 * 2 * np.pi / DK
    r = np.arange(0, RMAX, 1.0); J = -kp[:, None] * j1(kp[:, None] * r[None, :]); out = []
    for t in ts:
        tp = t * slow
        src = (0.42 * np.exp(-kp ** 2 * SRC ** 2 / 4) + 0.58 * np.exp(-kp ** 2 * SRCL ** 2 / 4)) if two else np.exp(-kp ** 2 * SRC ** 2 / 4)
        e = (CG * tp - RA) / 60; alw = np.where(e > 0, np.exp(-np.maximum(e, 0) ** 2), 1)
        F = DK * kp * src * np.exp(-VD * tp) * np.cos(W * tp) * (alw if two else 1)
        s = np.abs(F @ J); s[:3] = 0; m = s.max(); c = int(s.argmax()); L = int(np.where(s >= 0.15 * m)[0].max())
        out.append(dict(t=round(float(t), 3), crest=c, lead=L, amp=float(m)))
    return out
def textbook():
    k = np.logspace(0, 4.5, 20000); w = np.sqrt(G * k + SR * k ** 3); c = w / k; cg = (G + 3 * SR * k ** 2) / (2 * w)
    i, j = c.argmin(), cg.argmin()
    return dict(cmin_cm_s=100 * c[i], lam_cmin_cm=100 * 2 * np.pi / k[i], cgmin_cm_s=100 * cg[j], lam_cgmin_cm=100 * 2 * np.pi / k[j])
if __name__ == "__main__":
    tb = textbook(); print("textbook (σ/ρ = 7.4e-5):", {k: round(v, 2) for k, v in tb.items()})
    res = dict(textbook=tb)
    for name, S in (("v151_16.7pxcm", 6e-4), ("new_4.0pxcm", 2.5e-3), ("new_2.7pxcm", 1 / 270.)):
        res[name] = ring(S, 1.2e-6, 3.2, 8)
        print(name, [(o["t"], o["crest"], o["lead"]) for o in res[name][1::4]])
    # the promo ring (v1.3.1 · PR_SLOW 0.22, ν 6e-6, one source width 7 px, its own k grid)
    res["promo_code"] = ring(6e-4, 6e-6, 7, 0, two=False, slow=0.22, DK=4.2 / 7 / 192, RMAX=640)
    print("promo_code", [(o["t"], o["crest"], o["lead"]) for o in res["promo_code"][1::4]])
    json.dump(res, open("physics.json", "w"))
