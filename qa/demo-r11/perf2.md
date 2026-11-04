# v1.5-gridwake perf gate at 0416d43 vs v1.3.1 (rerun; perfx.py, interleaved, 3 reps, headless Chrome / SwiftShader)

Gate: median library ms/frame; pass if Δmedian ≤ max(v1.3.1 spread/2, 5 %). Raw: perf2.log / perf2.json. (The first run at 50f0b8c is in perf.md.)

| case | mode | v1.3.1 median (runs) | v1.5 median (runs) | Δ | allowance | gate | frame interval median v1.3.1 → v1.5 ms | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 5.544 (5.13, 5.63, 5.54) | 5.284 (5.25, 5.28, 5.59) | -0.260 (-4.7 %) | 0.277 | PASS | 71.4 → 72.6 | 0 |
| 1440 1× idle | adaptive (fallback) | 1.795 (1.74, 1.88, 1.79) | 0.707 (0.70, 0.71, 0.85) | -1.088 (-60.6 %) | 0.090 | PASS | 26.5 → 16.7 | 0 |
| 1440 1× drag | forced (real) | 6.039 (5.64, 6.04, 6.97) | 6.602 (5.45, 6.60, 7.06) | +0.563 (+9.3 %) | 0.663 | PASS | 85.8 → 90.6 | 242,024 |
| 1440 1× drag | adaptive (fallback) | 1.233 (1.23, 0.99, 1.29) | 0.807 (0.79, 0.81, 0.83) | -0.426 (-34.5 %) | 0.151 | PASS | 20.8 → 16.7 | 0 |
| 390 4× idle | forced (real) | 11.367 (11.37, 10.88, 12.23) | 9.938 (9.94, 9.89, 11.46) | -1.429 (-12.6 %) | 0.677 | PASS | 42.3 → 37.5 | 0 |
| 390 4× idle | adaptive (real) | 10.876 (9.34, 10.88, 10.90) | 10.805 (10.80, 10.07, 11.04) | -0.071 (-0.7 %) | 0.782 | PASS | 37.1 → 35.9 | 0 |
| 390 4× drag | forced (real) | 11.995 (12.09, 11.99, 10.94) | 10.019 (10.63, 10.02, 9.73) | -1.976 (-16.5 %) | 0.600 | PASS | 45.1 → 41.9 | 43,367 |
| 390 4× drag | adaptive (real) | 10.943 (11.92, 9.92, 10.94) | 9.493 (4.63, 10.58, 9.49) | -1.450 (-13.3 %) | 1.002 | PASS | 41.7 → 39.8 | 34,181 |

**Overall: PASS**; page/console errors across runs: 0.
