# ink-fish v1.4 — measured targets

Measured on water-only renders (`MEASURE=1`: koi off, 1440×900, light, SwiftShader, deterministic virtual clock),
|frame − still| in grey levels. Scripts: `tgt.py` (tap / slow / fast), `wake.py` (speed sweep). Logs alongside.
Scale: 1 cm = 16.7 px; cg,min ≈ 17.7 cm/s ≈ 296 px/s; c,min ≈ 23 cm/s ≈ 385 px/s.

| target | goal | measured | verdict |
|---|---|---|---|
| calm-centre (inner) edge speed, release ring | 280–320 px/s | **322 px/s** (16-frame fit, threshold 2 grey levels) | borderline (+2 px/s over) |
| crests in a packet (t 0.17–0.30 s, r 28–226 px) | ≥ 8 | press 20 → 9, release 17 → 7–9 (front spacing 7 px, back 22–35 px) | pass (fine front, coarse back) |
| slow drag (200 px/s) wake energy vs v1.3.2 | ≤ 15 % | **7.2 %** behind the finger, steady stroke t 2.5–4.5 s (50.6 % incl. the dimple; 223 % over the whole window because the v1.4 press packet at 0.5 s is ~2× stronger) | pass (wake) |
| fast drag V half-angle (~1245 px/s) | 12–16° | arm-slope fit **12.1°** at 1200 px/s (sweep); tgt.py max-contrast median 21.5° (26.5° at 60–100 px behind → 17° at 300 px: the arm starts ~30 px off the track, a finger-width offset) | pass on the asymptotic angle; near-field arm wider |
| visible duration | 1–1.5 s | ≥ 0.5 % of the water ≥ 3 grey levels off: press 1.87 s, release 1.77 s; azimuthal peak > 2 levels inside the 228-px disc: release 0.80 s (packet leaves the disc) | slightly long (+0.3 s) |
| stray hover ring after lift (combo, 5.0 s) | none | none (frame 150 compared with the old render) | fixed |

## Pressed wake vs speed (`wake.py`, straight stroke y = 450, frame when the finger reaches x = 1150)

Strength: `0.6·√(U/600)` through a `1.25·tanh` soft limit, gated by a smoothstep over 280–420 px/s (no hard cap).
Line source: 8 px wide (finger width), so the arm sits near cg,min/U.

| U px/s | U cm/s | wake strength Σ|dL| behind (×1e3) | mean |dL| in wedge | half-angle: arm slope fit 100–500 px behind (°) [offset px] | max-contrast median (°) | outer edge (50 %) (°) | asin(cg,min/U) (°) | crests across the wedge 200 px behind: median spacing (px) | errors |
|---|---|---|---|---|---|---|---|---|---|
| 200 | 12 | 0.0 | 0.00 | nan [nan] | nan | nan (n=0) | 90.0 | nan (0 crests) | [] |
| 400 | 24 | 417.5 | 1.09 | 34.7 [26] | 39.0 | 48.6 (n=36) | 47.6 | 40.0 (4 crests) | [] |
| 600 | 36 | 905.5 | 2.51 | 29.9 [-3] | 29.4 | 36.3 (n=44) | 29.5 | 49.0 (4 crests) | [] |
| 900 | 54 | 1697.4 | 5.30 | 17.7 [20] | 21.6 | 27.0 (n=44) | 19.2 | 14.5 (8 crests) | [] |
| 1200 | 72 | 1942.2 | 6.71 | 12.1 [30] | 19.9 | 23.5 (n=44) | 14.3 | 18.0 (7 crests) | [] |
| 1800 | 108 | 1699.4 | 8.22 | 11.7 [12] | 14.1 | 16.7 (n=44) | 9.5 | 12.0 (7 crests) | [] |
| 2400 | 144 | 1574.0 | 9.90 | 9.3 [8] | 11.0 | 12.8 (n=44) | 7.1 | 10.5 (8 crests) | [] |

Reading it: strength (mean |dL| in the wedge) rises continuously 0 → 1.1 → 2.5 → 5.3 → 6.7 → 8.2 → 9.9 with no
plateau. Σ|dL| over the area peaks at 1200 px/s and then falls as the wedge narrows. The half-angle (arm-slope fit)
narrows monotonically: 35° → 30° → 18° → 12° → 12° → 9°, within about 2–3° of asin(cg,min/U) from 600 px/s up
(it reads 2° narrow at 1200 px/s and 2° wide at 1800–2400). At 400 px/s, just above c,min, it is the onset regime:
weak and wide, as expected. Crest spacing across the wedge 200 px behind is noisy (4–8 crests) but falls overall from
40–50 px at 400–600 px/s to 10–18 px at 900–2400 px/s.

## Hover (unpressed) wake vs speed (`HOVER=1 wake.py`)

The hover wake is a train of dropped rings (spacing 130 + 190·fw px, fw = clamp((U − 450)/900)). Its strength s0 is now
a continuous blend from the slow-ring value to the decaying fast train (no step at fw = 0). The angle columns are
not a wedge measurement here: they fit ring arcs.

| U px/s | U cm/s | wake strength Σ|dL| behind (×1e3) | mean |dL| in wedge | half-angle: arm slope fit 100–500 px behind (°) [offset px] | max-contrast median (°) | outer edge (50 %) (°) | asin(cg,min/U) (°) | crests across the wedge 200 px behind: median spacing (px) | errors |
|---|---|---|---|---|---|---|---|---|---|
| 200 | 12 | 702.8 | 1.76 | -10.2 [259] | 34.8 | 42.2 (n=44) | 90.0 | 46.0 (5 crests) | [] |
| 400 | 24 | 1087.4 | 2.51 | -10.9 [208] | 29.0 | 44.7 (n=44) | 47.6 | 25.0 (12 crests) | [] |
| 600 | 36 | 1189.4 | 2.94 | 28.6 [6] | 30.5 | 44.2 (n=44) | 29.5 | 35.5 (4 crests) | [] |
| 900 | 54 | 1305.4 | 3.68 | 28.2 [-24] | 25.0 | 40.5 (n=44) | 19.2 | 21.0 (5 crests) | [] |
| 1200 | 72 | 1502.2 | 4.52 | 18.5 [-3] | 17.1 | 35.6 (n=44) | 14.3 | nan (0 crests) | [] |
| 1800 | 108 | 1676.2 | 6.06 | 9.4 [12] | 12.7 | 26.3 (n=42) | 9.5 | 18.5 (8 crests) | [] |
| 2400 | 144 | 993.8 | 4.50 | 2.9 [13] | 3.3 | 18.8 (n=28) | 7.1 | nan (0 crests) | [] |

Reading it: strength rises continuously from 200 to 1800 px/s (1.8 → 6.1 mean |dL|) but **drops at 2400 px/s**
(4.5). Over the 950-px stroke only about 3 rings fall, at ≥ 320 px spacing, and each later ring decays by 0.62.
This is a remaining flaw: the hover train's spacing should shrink, or its decay ease off, above ~1800 px/s.

## Round 11 checks (HEAD 5b8d0b8)
- Calm-centre (inner) edge speed is 311 px/s (target ≤ 320): pass. See tgt-tap2.log.
- Visible after release, full-screen (≥ 0.5 % of water ≥ 3 grey levels): 1.5 s (target ≈ 1.5 s): pass. Peak azimuthal visibility lasts 0.80 s.
- Hover wake, mean |dL| in wedge: 5.76 at 1800 px/s and 7.00 at 2400 px/s. It no longer weakens (previously 6.06 → 4.50). See wake-hover2.log.
- Fast-V interior fill: not done.
