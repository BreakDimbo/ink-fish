# Release perf gate (run 3), v1.5.1 vs live v1.5.0

Gate: median library ms/frame (interleaved, 3 reps, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.0 lib ms (runs) | v1.5.1 lib ms (runs) | Δ | allowance | gate | frame interval v1.5.0 → v1.5.1 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 7.093 (6.54, 7.09, 7.83) | 7.982 (7.08, 8.28, 7.98) | +0.889 (+12.5 %) | 0.643 | FAIL | 91.7 → 94.3 (+2.8 %) | 0 |
| 1440 1× idle | adaptive (fallback) | 0.862 (0.86, 0.84, 0.86) | 0.849 (0.85, 0.85, 0.96) | -0.013 (-1.5 %) | 0.043 | PASS | 16.7 → 16.7 (+0.0 %) | 0 |
| 1440 1× drag | forced (real) | 7.655 (7.60, 8.01, 7.66) | 7.747 (7.67, 7.88, 7.75) | +0.092 (+1.2 %) | 0.383 | PASS | 101.5 → 99.3 (-2.2 %) | 136,387 |
| 1440 1× drag | adaptive (fallback) | 0.962 (0.95, 1.03, 0.96) | 0.981 (0.96, 1.00, 0.98) | +0.019 (+2.0 %) | 0.048 | PASS | 16.7 → 16.7 (+0.0 %) | 0 |
| 390 4× idle | forced (real) | 9.278 (9.28, 8.79, 9.60) | 10.376 (10.38, 12.03, 9.56) | +1.098 (+11.8 %) | 0.464 | FAIL | 36.3 → 37.9 (+4.6 %) | 0 |
| 390 4× idle | adaptive (real) | 9.747 (8.53, 10.29, 9.75) | 9.395 (9.39, 10.11, 8.96) | -0.352 (-3.6 %) | 0.879 | PASS | 35.7 → 34.9 (-2.1 %) | 0 |
| 390 4× drag | forced (real) | 10.513 (10.51, 9.03, 11.07) | 10.070 (10.63, 9.06, 10.07) | -0.443 (-4.2 %) | 1.024 | PASS | 40.9 → 40.2 (-1.7 %) | 26,462 |
| 390 4× drag | adaptive (real) | 9.533 (8.87, 10.27, 9.53) | 9.950 (10.38, 9.95, 8.91) | +0.417 (+4.4 %) | 0.701 | PASS | 39.1 → 39.2 (+0.1 %) | 20,320 |

**Overall: FAIL**; page/console errors: 0.
