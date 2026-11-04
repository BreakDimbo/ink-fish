# Perf gate, v1.5.1 vs v1.3.1

Gate: median library ms/frame (interleaved, 3 reps, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.3.1 lib ms (runs) | v1.5.1 lib ms (runs) | Δ | allowance | gate | frame interval v1.3.1 → v1.5.1 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 7.539 (7.84, 7.54, 7.35) | 7.744 (7.88, 7.30, 7.74) | +0.205 (+2.7 %) | 0.377 | PASS | 94.6 → 90.7 (-4.1 %) | 0 |
| 1440 1× idle | adaptive (fallback) | 0.865 (0.86, 0.90, 0.83) | 0.835 (0.83, 0.81, 0.96) | -0.030 (-3.5 %) | 0.043 | PASS | 16.7 → 16.7 (+0.0 %) | 0 |
| 1440 1× drag | forced (real) | 7.623 (7.79, 7.06, 7.62) | 7.033 (7.12, 6.75, 7.03) | -0.590 (-7.7 %) | 0.381 | PASS | 97.1 → 91.1 (-6.2 %) | 139,079 |
| 1440 1× drag | adaptive (fallback) | 0.971 (0.97, 0.93, 1.33) | 0.874 (0.87, 0.91, 0.86) | -0.097 (-10.0 %) | 0.202 | PASS | 16.7 → 16.7 (+0.0 %) | 0 |
| 390 4× idle | forced (real) | 9.727 (9.73, 11.03, 9.39) | 9.890 (11.12, 9.03, 9.89) | +0.163 (+1.7 %) | 0.817 | PASS | 38.6 → 36.5 (-5.4 %) | 0 |
| 390 4× idle | adaptive (real) | 10.530 (9.10, 10.53, 12.28) | 9.439 (9.14, 9.44, 10.14) | -1.091 (-10.4 %) | 1.591 | PASS | 39.6 → 34.7 (-12.2 %) | 0 |
| 390 4× drag | forced (real) | 11.025 (11.67, 11.03, 10.14) | 10.539 (10.32, 12.54, 10.54) | -0.486 (-4.4 %) | 0.768 | PASS | 43.2 → 42.3 (-1.9 %) | 26,274 |
| 390 4× drag | adaptive (real) | 10.775 (11.19, 4.27, 10.78) | 10.487 (10.49, 10.32, 11.21) | -0.288 (-2.7 %) | 3.463 | PASS | 42.6 → 43.1 (+1.1 %) | 20,315 |

**Overall: PASS**; page/console errors: 0.
