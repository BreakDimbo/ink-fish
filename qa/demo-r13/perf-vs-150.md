# Perf gate, v1.5.1 vs v1.5.0

Gate: median library ms/frame (interleaved, 3 reps, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.0 lib ms (runs) | v1.5.1 lib ms (runs) | Δ | allowance | gate | frame interval v1.5.0 → v1.5.1 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 7.185 (8.01, 6.72, 7.18) | 7.744 (7.88, 7.30, 7.74) | +0.559 (+7.8 %) | 0.647 | PASS | 86.9 → 90.7 (+4.4 %) | 0 |
| 1440 1× idle | adaptive (fallback) | 0.873 (0.97, 0.77, 0.87) | 0.835 (0.83, 0.81, 0.96) | -0.038 (-4.4 %) | 0.096 | PASS | 16.7 → 16.7 (+0.0 %) | 0 |
| 1440 1× drag | forced (real) | 7.168 (7.37, 6.92, 7.17) | 7.033 (7.12, 6.75, 7.03) | -0.135 (-1.9 %) | 0.358 | PASS | 93.8 → 91.1 (-2.9 %) | 139,079 |
| 1440 1× drag | adaptive (fallback) | 0.958 (0.96, 0.95, 0.97) | 0.874 (0.87, 0.91, 0.86) | -0.084 (-8.8 %) | 0.048 | PASS | 16.7 → 16.7 (+0.0 %) | 0 |
| 390 4× idle | forced (real) | 10.244 (9.45, 10.24, 10.35) | 9.890 (11.12, 9.03, 9.89) | -0.354 (-3.5 %) | 0.512 | PASS | 37.1 → 36.5 (-1.6 %) | 0 |
| 390 4× idle | adaptive (real) | 10.920 (11.06, 10.92, 10.00) | 9.439 (9.14, 9.44, 10.14) | -1.481 (-13.6 %) | 0.546 | PASS | 35.9 → 34.7 (-3.2 %) | 0 |
| 390 4× drag | forced (real) | 10.038 (10.04, 11.02, 9.18) | 10.539 (10.32, 12.54, 10.54) | +0.501 (+5.0 %) | 0.924 | PASS | 41.6 → 42.3 (+1.9 %) | 26,274 |
| 390 4× drag | adaptive (real) | 10.416 (9.60, 10.86, 10.42) | 10.487 (10.49, 10.32, 11.21) | +0.071 (+0.7 %) | 0.630 | PASS | 39.7 → 43.1 (+8.7 %) | 20,315 |

**Overall: PASS**; page/console errors: 0.
