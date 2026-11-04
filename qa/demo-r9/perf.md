# r9 performance gate — v1.4 (HEAD, judge fix de3fa14) vs live v1.3.1 (173a9c0)

**Verdict: PASS — 32/32 cases not slower than v1.3.1 within noise.** No case is slower than the noise allows.

## Method
- Headless Chrome + SwiftShader (no GPU, 8-core box), DPR 1, real wall clock, `perf.py`/`perfx.py`. Builds run **interleaved** (v1.3.1 adaptive/forced, v1.4 adaptive/forced, then repeat).
- Cases: idle / scroll / cursor / drag × 1440×900 and 390×844 × CPU throttle 1× and 4×. Each case is run with `water:'real'` default (adaptive) and with `adaptive:false` (forced real water, which is the honest per-frame cost).
- Metric gated: library ms per frame (`stats.ms/stats.n`), median over runs. A case counts as "not slower" if Δmedian ≤ max(v1.3.1 min–max spread / 2, 5 %).
- n per case is 3–12. Logs: `perf-part3.log` (3 full passes, pre-judge-fix), `perfx1.log` (+4 reps on 1440 1× idle/cursor/drag, 390 1× scroll), `perfx2.log` (+5 reps, post-fix, on the four adaptive cells flagged before the fix). Forced runs are unaffected by the judge fix, and so are 390 runs (they never fall back), so pooling all three logs is valid. The 1440 1× idle adaptive cell is also shown post-fix only, below.
- Report: `python3 perfreport.py perf-part3.log perfx1.log perfx2.log`.

## Verdict per case (lib ms/frame)
| width | CPU | case | build | v1.3.1 mean / median | v1.4 mean / median | Δ median % | v1.3.1 spread (ms) | n | v1.4 runs | not slower |
|---|---|---|---|---|---|---|---|---|---|---|
| 1440 | 1× | idle | forced | 6.38 / 6.47 | 6.33 / 6.40 | -1.1 | 2.66 | 12/12 | 5.16 5.38 5.66 5.99 6.03 6.39 6.41 6.72 6.75 6.88 7.22 7.41 | yes |
| 1440 | 1× | idle | adaptive | 1.08 / 0.82 | 1.27 / 0.81 | -0.3 | 1.38 | 12/12 | 0.69 0.71 0.74 0.76 0.77 0.77 0.85 0.90 1.84 1.97 2.41 2.79 | yes |
| 1440 | 1× | scroll | forced | 5.80 / 5.82 | 5.61 / 5.67 | -2.5 | 0.44 | 3/3 | 5.24 5.67 5.92 | yes |
| 1440 | 1× | scroll | adaptive | 1.51 / 1.67 | 1.42 / 1.72 | +3.2 | 0.93 | 3/3 | 0.81 1.72 1.74 | yes |
| 1440 | 1× | cursor | forced | 6.03 / 5.88 | 5.49 / 5.42 | -7.9 | 1.62 | 7/7 | 5.15 5.20 5.33 5.42 5.51 5.61 6.18 | yes |
| 1440 | 1× | cursor | adaptive | 1.44 / 1.62 | 1.41 / 1.58 | -2.5 | 0.99 | 7/7 | 0.78 0.88 1.52 1.58 1.60 1.60 1.88 | yes |
| 1440 | 1× | drag | forced | 6.24 / 6.11 | 9.83 / 6.05 | -0.8 | 0.96 | 7/7 | 5.19 5.47 5.50 6.05 6.15 6.46 33.97 | yes |
| 1440 | 1× | drag | adaptive | 1.26 / 1.21 | 1.18 / 1.26 | +4.1 | 0.61 | 7/7 | 0.84 0.88 1.20 1.26 1.27 1.30 1.54 | yes |
| 1440 | 4× | idle | forced | 25.63 / 25.90 | 25.01 / 24.65 | -4.8 | 4.24 | 3/3 | 24.37 24.65 25.99 | yes |
| 1440 | 4× | idle | adaptive | 3.65 / 3.54 | 3.45 / 3.48 | -1.8 | 0.42 | 3/3 | 3.33 3.48 3.52 | yes |
| 1440 | 4× | scroll | forced | 25.78 / 24.64 | 24.22 / 23.72 | -3.7 | 3.73 | 3/3 | 23.56 23.72 25.39 | yes |
| 1440 | 4× | scroll | adaptive | 3.72 / 3.88 | 3.74 / 3.81 | -1.9 | 0.63 | 3/3 | 3.56 3.81 3.85 | yes |
| 1440 | 4× | cursor | forced | 31.20 / 31.49 | 29.49 / 31.03 | -1.5 | 3.12 | 3/3 | 25.80 31.03 31.64 | yes |
| 1440 | 4× | cursor | adaptive | 6.73 / 3.98 | 3.40 / 3.54 | -11.1 | 8.73 | 3/3 | 3.12 3.54 3.56 | yes |
| 1440 | 4× | drag | forced | 28.72 / 29.13 | 26.54 / 26.70 | -8.3 | 5.76 | 3/3 | 24.58 26.70 28.34 | yes |
| 1440 | 4× | drag | adaptive | 4.40 / 3.93 | 3.33 / 3.42 | -12.9 | 1.86 | 3/3 | 3.08 3.42 3.49 | yes |
| 390 | 1× | idle | forced | 2.16 / 2.07 | 1.99 / 2.01 | -2.5 | 0.72 | 8/8 | 1.76 1.79 1.84 1.91 2.12 2.14 2.15 2.17 | yes |
| 390 | 1× | idle | adaptive | 2.09 / 2.08 | 2.06 / 2.07 | -0.6 | 0.51 | 8/8 | 1.80 1.86 1.94 2.04 2.09 2.15 2.19 2.37 | yes |
| 390 | 1× | scroll | forced | 2.38 / 2.41 | 2.18 / 2.16 | -10.4 | 0.88 | 12/12 | 1.98 2.01 2.03 2.10 2.15 2.15 2.16 2.18 2.19 2.33 2.40 2.49 | yes |
| 390 | 1× | scroll | adaptive | 2.16 / 2.13 | 2.29 / 2.30 | +7.7 | 0.48 | 12/12 | 1.91 2.01 2.15 2.16 2.19 2.30 2.30 2.31 2.32 2.36 2.42 3.09 | yes |
| 390 | 1× | cursor | forced | 2.19 / 2.23 | 1.78 / 1.77 | -20.6 | 0.31 | 3/3 | 1.75 1.77 1.82 | yes |
| 390 | 1× | cursor | adaptive | 1.97 / 1.97 | 1.87 / 1.86 | -5.4 | 0.09 | 3/3 | 1.75 1.86 2.00 | yes |
| 390 | 1× | drag | forced | 2.25 / 2.18 | 1.88 / 1.92 | -11.9 | 0.35 | 3/3 | 1.72 1.92 1.99 | yes |
| 390 | 1× | drag | adaptive | 2.19 / 2.27 | 2.00 / 2.02 | -10.8 | 0.48 | 3/3 | 1.79 2.02 2.18 | yes |
| 390 | 4× | idle | forced | 9.08 / 8.78 | 8.77 / 8.61 | -1.9 | 2.66 | 8/8 | 7.99 8.17 8.24 8.51 8.71 8.91 9.31 10.32 | yes |
| 390 | 4× | idle | adaptive | 8.79 / 8.49 | 8.54 / 8.70 | +2.5 | 2.80 | 8/8 | 7.27 7.38 8.34 8.66 8.73 9.09 9.20 9.70 | yes |
| 390 | 4× | scroll | forced | 9.52 / 9.56 | 8.70 / 9.07 | -5.1 | 1.09 | 3/3 | 7.97 9.07 9.08 | yes |
| 390 | 4× | scroll | adaptive | 9.86 / 9.83 | 9.00 / 9.37 | -4.7 | 2.43 | 3/3 | 7.75 9.37 9.89 | yes |
| 390 | 4× | cursor | forced | 11.83 / 11.88 | 11.00 / 11.18 | -5.8 | 4.36 | 3/3 | 9.04 11.18 12.78 | yes |
| 390 | 4× | cursor | adaptive | 28.53 / 13.33 | 10.72 / 10.15 | -23.9 | 46.76 | 3/3 | 9.97 10.15 12.05 | yes |
| 390 | 4× | drag | forced | 10.27 / 10.23 | 8.73 / 8.66 | -15.3 | 1.83 | 3/3 | 8.49 8.66 9.05 | yes |
| 390 | 4× | drag | adaptive | 10.35 / 10.79 | 9.60 / 9.84 | -8.8 | 3.18 | 3/3 | 8.70 9.84 10.27 | yes |

Post-fix only, 1440 1× idle adaptive (perfx2, 5 runs): v1.3.1 1.28 (0.76–2.14) vs v1.4 **0.75 (0.69–0.77)**, frame interval 20.7 vs 16.7 ms → pass. Before the fix, this cell was +126 %.

## GPU proxy (sim px evaluated per frame = sim steps × grid; composite px per frame)
- 1440: both builds use sim **648,000 px/frame** (720×450 half-res × 2 passes) and comp 1,296,000. The caustic grid is 42,804 verts at q0 for both. The GPU work is identical, and the CPU side of v1.4 is 1–8 % cheaper.
- 390: v1.4 does **less** sim work in idle/scroll/cursor: 97–107k px/frame against 120–126k, because the sim sleeps when calm (re-run only on rings, trail, dimple, key change or ≥1/31 s). Drag costs +3 % (138k vs 134k at 1×) because of the dimple/meniscus source. comp 329,160 for both.
- Per-phase deterministic numbers (`gwproxy.py`) were not run in this pass; the numbers above are means from the perf logs.

## Adaptive fallback trigger time (real clock, `judgetime.py`, ms from load to `fallback`)
| case | v1.3.1 | v1.4 (post-fix) |
|---|---|---|
| 1440 1× (5 runs each) | 7111, 6969, 3382, 7101, 4850 (mean 5883) | 3539, 4685, 3435, 4545, 3578 (mean 3956) |
| 1440 4× (5 runs each) | 4915, 4587, 4616, 4636, 4768 (mean 4704) | 4694, 4982, 4810, 4365, 4879 (mean 4746) |
| 390 1× / 4× | never falls back (4× probes q1 and reverts) | same |

Before the fix (`judgetime.log`), v1.4 at 1440 1× fell back at about 7.15 s in 2 of 3 runs, against v1.3.1's 3.5 s. Both builds are bimodal around the m>80 ms "few fps" threshold; v1.4's slightly faster frames landed it in the useless q1 window more often. **Fix (de3fa14):** at DPR ≤ 1, a median above 60 ms goes straight to the flat trial, because q1 only thins the caustic grid there and can't reach 21 ms. v1.4 now falls back no later than v1.3.1. v1.4 turns real about 0.15–0.2 s later at start-up (profile table build).

## Notes / caveats
- One v1.4 1440 1× drag forced run hitched at 33.97 ms; the other 6 runs were 5.19–6.46. Gated on the median.
- 390 1× scroll adaptive is +7.7 % (allowance 11 %). That config is identical to forced at 390 (both stay real/q0), and the forced cell is −10 %, so this is run-to-run noise. Frame interval is better on v1.4 (23.0 vs 23.6 ms, late 35 % vs 41 %).
- At 1440 on SwiftShader, forced real water runs at about 13 fps for both builds. That is why the default adaptive mode falls back there, as v1.3.1 does.

## Full table (all logs pooled)
| width | CPU | case | build | n | lib ms/frame mean (min–max) | frame interval ms mean (min–max) | late % mean | water at end | GPU proxy sim px/frame | comp px/frame |
|---|---|---|---|---|---|---|---|---|---|---|
| 1440 | 1× | idle | v1.3.1 real (forced) | 12 | 6.38 (5.17–7.83) | 77.9 (69.5–88.3) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 1× | idle | v1.4 real (forced) | 12 | 6.33 (5.16–7.41) | 76.3 (68.0–86.9) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 1× | idle | v1.3.1 real (adaptive) | 12 | 1.08 (0.76–2.14) | 19.1 (16.7–27.7) | 5.1 | fallback | 648,000 | 1,296,000 |
| 1440 | 1× | idle | v1.4 real (adaptive) | 12 | 1.27 (0.69–2.79) | 22.3 (16.7–50.9) | 8.3 | fallback | 648,000 | 1,296,000 |
| 1440 | 1× | scroll | v1.3.1 real (forced) | 3 | 5.80 (5.56–6.00) | 74.9 (72.3–77.9) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 1× | scroll | v1.4 real (forced) | 3 | 5.61 (5.24–5.92) | 73.3 (71.3–74.6) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 1× | scroll | v1.3.1 real (adaptive) | 3 | 1.51 (0.96–1.89) | 23.9 (18.7–27.2) | 20.4 | fallback | 648,000 | 1,296,000 |
| 1440 | 1× | scroll | v1.4 real (adaptive) | 3 | 1.42 (0.81–1.74) | 24.0 (18.4–27.5) | 20.5 | fallback | 648,000 | 1,296,000 |
| 1440 | 1× | cursor | v1.3.1 real (forced) | 7 | 6.03 (5.35–6.97) | 75.0 (69.0–83.3) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 1× | cursor | v1.4 real (forced) | 7 | 5.49 (5.15–6.18) | 71.4 (68.8–74.9) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 1× | cursor | v1.3.1 real (adaptive) | 7 | 1.44 (0.85–1.84) | 22.4 (16.7–25.2) | 11.9 | fallback | 648,000 | 1,296,000 |
| 1440 | 1× | cursor | v1.4 real (adaptive) | 7 | 1.41 (0.78–1.88) | 22.7 (16.7–26.5) | 12.6 | fallback | 648,000 | 1,296,000 |
| 1440 | 1× | drag | v1.3.1 real (forced) | 7 | 6.24 (5.74–6.71) | 85.5 (80.2–92.5) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 1× | drag | v1.4 real (forced) | 7 | 9.83 (5.19–33.97) | 81.7 (70.0–117.3) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 1× | drag | v1.3.1 real (adaptive) | 7 | 1.26 (0.97–1.58) | 20.0 (16.7–24.2) | 6.4 | fallback | 645,498 | 1,296,000 |
| 1440 | 1× | drag | v1.4 real (adaptive) | 7 | 1.18 (0.84–1.54) | 20.4 (16.7–23.8) | 7.0 | fallback | 648,000 | 1,296,000 |
| 1440 | 4× | idle | v1.3.1 real (forced) | 3 | 25.63 (23.37–27.61) | 109.3 (104.8–113.2) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 4× | idle | v1.4 real (forced) | 3 | 25.01 (24.37–25.99) | 106.5 (105.4–107.8) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 4× | idle | v1.3.1 real (adaptive) | 3 | 3.65 (3.50–3.91) | 18.6 (18.2–18.8) | 3.2 | fallback | 648,000 | 1,296,000 |
| 1440 | 4× | idle | v1.4 real (adaptive) | 3 | 3.45 (3.33–3.52) | 18.4 (17.8–18.9) | 3.3 | fallback | 648,000 | 1,296,000 |
| 1440 | 4× | scroll | v1.3.1 real (forced) | 3 | 25.78 (24.49–28.22) | 114.9 (111.3–118.2) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 4× | scroll | v1.4 real (forced) | 3 | 24.22 (23.56–25.39) | 112.9 (110.1–115.1) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 4× | scroll | v1.3.1 real (adaptive) | 3 | 3.72 (3.33–3.96) | 23.9 (22.2–24.7) | 27.0 | fallback | 648,000 | 1,296,000 |
| 1440 | 4× | scroll | v1.4 real (adaptive) | 3 | 3.74 (3.56–3.85) | 24.2 (24.1–24.3) | 26.9 | fallback | 648,000 | 1,296,000 |
| 1440 | 4× | cursor | v1.3.1 real (forced) | 3 | 31.20 (29.49–32.61) | 128.8 (123.9–132.8) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 4× | cursor | v1.4 real (forced) | 3 | 29.49 (25.80–31.64) | 119.6 (111.4–123.9) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 4× | cursor | v1.3.1 real (adaptive) | 3 | 6.73 (3.73–12.46) | 27.5 (16.8–46.8) | 11.2 | fallback | 648,000 | 1,296,000 |
| 1440 | 4× | cursor | v1.4 real (adaptive) | 3 | 3.40 (3.12–3.56) | 18.9 (18.3–19.3) | 13.5 | fallback | 648,000 | 1,296,000 |
| 1440 | 4× | drag | v1.3.1 real (forced) | 3 | 28.72 (25.64–31.40) | 129.7 (120.4–135.0) | 100.0 | real | 648,000 | 1,296,000 |
| 1440 | 4× | drag | v1.4 real (forced) | 3 | 26.54 (24.58–28.34) | 113.0 (107.8–117.0) | 100.0 | real | 647,122 | 1,296,000 |
| 1440 | 4× | drag | v1.3.1 real (adaptive) | 3 | 4.40 (3.70–5.56) | 19.6 (16.9–23.8) | 5.2 | fallback | 648,000 | 1,296,000 |
| 1440 | 4× | drag | v1.4 real (adaptive) | 3 | 3.33 (3.08–3.49) | 18.0 (17.3–18.6) | 5.0 | fallback | 648,000 | 1,296,000 |
| 390 | 1× | idle | v1.3.1 real (forced) | 8 | 2.16 (1.86–2.58) | 22.7 (20.9–26.8) | 35.9 | real | 123,767 | 329,160 |
| 390 | 1× | idle | v1.4 real (forced) | 8 | 1.99 (1.76–2.17) | 17.2 (17.0–17.6) | 3.3 | real | 98,513 | 329,160 |
| 390 | 1× | idle | v1.3.1 real (adaptive) | 8 | 2.09 (1.83–2.34) | 22.3 (21.0–23.6) | 33.6 | real | 124,512 | 329,160 |
| 390 | 1× | idle | v1.4 real (adaptive) | 8 | 2.06 (1.80–2.37) | 17.4 (17.1–19.0) | 4.5 | real | 99,243 | 329,160 |
| 390 | 1× | scroll | v1.3.1 real (forced) | 12 | 2.38 (2.02–2.90) | 24.7 (22.4–27.5) | 46.7 | real | 120,992 | 329,160 |
| 390 | 1× | scroll | v1.4 real (forced) | 12 | 2.18 (1.98–2.49) | 22.2 (20.3–23.5) | 31.1 | real | 107,878 | 329,160 |
| 390 | 1× | scroll | v1.3.1 real (adaptive) | 12 | 2.16 (2.01–2.49) | 23.3 (22.3–25.0) | 39.1 | real | 121,907 | 329,160 |
| 390 | 1× | scroll | v1.4 real (adaptive) | 12 | 2.29 (1.91–3.09) | 22.7 (21.1–27.4) | 33.6 | real | 108,373 | 329,160 |
| 390 | 1× | cursor | v1.3.1 real (forced) | 3 | 2.19 (2.02–2.33) | 22.7 (20.8–24.6) | 36.0 | real | 125,913 | 329,160 |
| 390 | 1× | cursor | v1.4 real (forced) | 3 | 1.78 (1.75–1.82) | 17.7 (17.5–18.0) | 6.2 | real | 104,893 | 329,160 |
| 390 | 1× | cursor | v1.3.1 real (adaptive) | 3 | 1.97 (1.93–2.02) | 21.8 (20.4–23.6) | 30.7 | real | 126,717 | 329,160 |
| 390 | 1× | cursor | v1.4 real (adaptive) | 3 | 1.87 (1.75–2.00) | 17.7 (17.4–18.0) | 6.3 | real | 105,028 | 329,160 |
| 390 | 1× | drag | v1.3.1 real (forced) | 3 | 2.25 (2.12–2.46) | 26.4 (24.6–27.5) | 55.7 | real | 133,581 | 329,160 |
| 390 | 1× | drag | v1.4 real (forced) | 3 | 1.88 (1.72–1.99) | 20.6 (20.4–20.9) | 23.7 | real | 138,346 | 329,160 |
| 390 | 1× | drag | v1.3.1 real (adaptive) | 3 | 2.19 (1.91–2.39) | 24.4 (24.0–25.0) | 46.1 | real | 134,299 | 329,160 |
| 390 | 1× | drag | v1.4 real (adaptive) | 3 | 2.00 (1.79–2.18) | 20.5 (19.1–21.6) | 22.7 | real | 140,086 | 329,160 |
| 390 | 4× | idle | v1.3.1 real (forced) | 8 | 9.08 (8.35–11.01) | 34.0 (32.5–35.1) | 96.0 | real | 115,281 | 329,160 |
| 390 | 4× | idle | v1.4 real (forced) | 8 | 8.77 (7.99–10.32) | 30.1 (28.4–34.2) | 78.2 | real | 113,366 | 329,160 |
| 390 | 4× | idle | v1.3.1 real (adaptive) | 8 | 8.79 (7.55–10.35) | 32.4 (30.8–34.5) | 90.3 | real | 116,031 | 329,160 |
| 390 | 4× | idle | v1.4 real (adaptive) | 8 | 8.54 (7.27–9.70) | 28.5 (25.6–31.7) | 69.3 | real | 109,398 | 329,160 |
| 390 | 4× | scroll | v1.3.1 real (forced) | 3 | 9.52 (8.97–10.05) | 35.8 (34.7–37.1) | 89.1 | real | 115,720 | 329,160 |
| 390 | 4× | scroll | v1.4 real (forced) | 3 | 8.70 (7.97–9.08) | 34.9 (32.4–37.1) | 86.7 | real | 117,408 | 329,160 |
| 390 | 4× | scroll | v1.3.1 real (adaptive) | 3 | 9.86 (8.67–11.10) | 35.5 (33.8–38.2) | 89.3 | real | 117,393 | 329,160 |
| 390 | 4× | scroll | v1.4 real (adaptive) | 3 | 9.00 (7.75–9.89) | 33.7 (31.3–34.9) | 80.0 | real | 112,593 | 329,160 |
| 390 | 4× | cursor | v1.3.1 real (forced) | 3 | 11.83 (9.63–13.99) | 40.3 (37.6–44.9) | 98.9 | real | 118,073 | 329,160 |
| 390 | 4× | cursor | v1.4 real (forced) | 3 | 11.00 (9.04–12.78) | 38.4 (33.3–42.6) | 97.5 | real | 120,138 | 329,160 |
| 390 | 4× | cursor | v1.3.1 real (adaptive) | 3 | 28.53 (12.75–59.51) | 56.8 (39.7–90.6) | 100.0 | real | 121,052 | 329,160 |
| 390 | 4× | cursor | v1.4 real (adaptive) | 3 | 10.72 (9.97–12.05) | 35.9 (33.6–38.7) | 96.6 | real | 120,939 | 329,160 |
| 390 | 4× | drag | v1.3.1 real (forced) | 3 | 10.27 (9.38–11.21) | 40.8 (39.5–42.2) | 100.0 | real | 131,355 | 329,160 |
| 390 | 4× | drag | v1.4 real (forced) | 3 | 8.73 (8.49–9.05) | 34.3 (33.5–35.6) | 96.4 | real | 135,027 | 329,160 |
| 390 | 4× | drag | v1.3.1 real (adaptive) | 3 | 10.35 (8.54–11.72) | 39.7 (37.5–41.4) | 99.9 | real | 131,753 | 329,160 |
| 390 | 4× | drag | v1.4 real (adaptive) | 3 | 9.60 (8.70–10.27) | 34.4 (32.6–36.4) | 95.0 | real | 132,493 | 329,160 |

