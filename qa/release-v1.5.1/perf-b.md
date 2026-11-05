# Release perf gate (rerun), v1.5.1 vs live v1.5.0

Gate: median library ms/frame (interleaved, 3 reps, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.0 lib ms (runs) | v1.5.1 lib ms (runs) | Δ | allowance | gate | frame interval v1.5.0 → v1.5.1 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 6.113 (6.35, 5.68, 6.11) | 5.895 (5.89, 5.99, 5.48) | -0.218 (-3.6 %) | 0.333 | PASS | 79.7 → 76.7 (-3.7 %) | 0 |
| 1440 1× idle | adaptive (fallback) | 0.780 (0.77, 0.79, 0.78) | 0.781 (0.78, 0.83, 0.76) | +0.001 (+0.1 %) | 0.039 | PASS | 16.7 → 16.7 (+0.0 %) | 0 |
| 1440 1× drag | forced (real) | 6.235 (6.04, 6.24, 6.31) | 6.338 (6.34, 5.90, 7.32) | +0.103 (+1.7 %) | 0.312 | PASS | 88.6 → 93.2 (+5.3 %) | 136,960 |
| 1440 1× drag | adaptive (fallback) | 0.881 (0.90, 0.88, 0.88) | 0.853 (0.89, 0.85, 0.84) | -0.028 (-3.2 %) | 0.044 | PASS | 16.7 → 16.7 (+0.0 %) | 0 |
| 390 4× idle | forced (real) | 8.555 (8.55, 7.99, 9.93) | 8.872 (8.87, 8.70, 9.95) | +0.317 (+3.7 %) | 0.969 | PASS | 33.5 → 35.9 (+7.1 %) | 0 |
| 390 4× idle | adaptive (real) | 8.754 (8.75, 8.46, 9.66) | 9.705 (9.71, 8.70, 10.38) | +0.951 (+10.9 %) | 0.602 | FAIL | 33.0 → 35.5 (+7.5 %) | 0 |
| 390 4× drag | forced (real) | 10.801 (10.80, 9.14, 11.09) | 9.840 (9.45, 10.85, 9.84) | -0.961 (-8.9 %) | 0.975 | PASS | 43.6 → 41.5 (-4.9 %) | 26,176 |
| 390 4× drag | adaptive (real) | 9.180 (8.72, 9.18, 10.29) | 10.322 (10.32, 11.44, 9.78) | +1.142 (+12.4 %) | 0.784 | FAIL | 38.8 → 41.2 (+6.2 %) | 19,849 |

**Overall: FAIL**; page/console errors: 0.
