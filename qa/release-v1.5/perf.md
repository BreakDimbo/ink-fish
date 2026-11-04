# Release perf gate, v1.5.0 vs v1.3.1

Gate: median library ms/frame (interleaved, 3 reps, headless Chrome/SwiftShader); pass if Δmedian ≤ max(v1.3.1 spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.3.1 lib ms (runs) | v1.5 lib ms (runs) | Δ | allowance | gate | frame interval v1.3.1 → v1.5 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 6.557 (6.56, 5.49, 6.98) | 6.637 (5.74, 7.15, 6.64) | +0.080 (+1.2 %) | 0.744 | PASS | 82.9 → 83.8 (+1.0 %) | 0 |
| 1440 1× idle | adaptive (fallback) | 0.916 (0.81, 2.00, 0.92) | 0.773 (0.79, 0.77, 0.73) | -0.143 (-15.6 %) | 0.593 | PASS | 16.7 → 16.7 (+0.0 %) | 0 |
| 1440 1× drag | forced (real) | 6.583 (6.18, 6.58, 6.66) | 6.175 (6.59, 5.85, 6.17) | -0.408 (-6.2 %) | 0.329 | PASS | 85.0 → 84.7 (-0.4 %) | 143,195 |
| 1440 1× drag | adaptive (fallback) | 0.896 (0.88, 1.28, 0.90) | 0.853 (0.89, 0.80, 0.85) | -0.043 (-4.8 %) | 0.200 | PASS | 16.7 → 16.7 (+0.0 %) | 0 |
| 390 4× idle | forced (real) | 8.919 (8.30, 8.92, 9.08) | 8.664 (8.59, 8.66, 9.24) | -0.255 (-2.9 %) | 0.446 | PASS | 34.2 → 32.8 (-4.0 %) | 0 |
| 390 4× idle | adaptive (real) | 8.628 (9.58, 8.63, 8.03) | 8.870 (9.27, 7.99, 8.87) | +0.242 (+2.8 %) | 0.776 | PASS | 32.4 → 31.3 (-3.3 %) | 0 |
| 390 4× drag | forced (real) | 9.762 (9.76, 8.63, 9.87) | 9.234 (8.22, 9.45, 9.23) | -0.528 (-5.4 %) | 0.620 | PASS | 38.6 → 37.6 (-2.7 %) | 25,923 |
| 390 4× drag | adaptive (real) | 9.817 (9.10, 9.93, 9.82) | 8.215 (8.21, 10.06, 8.09) | -1.602 (-16.3 %) | 0.491 | PASS | 38.6 → 35.8 (-7.3 %) | 19,411 |

**Overall: PASS**; page/console errors: 0.
