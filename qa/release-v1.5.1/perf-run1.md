# Release perf gate run 1, v1.5.1 vs live v1.5.0

Gate: median library ms/frame (interleaved, 3 reps, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.0 lib ms (runs) | v1.5.1 lib ms (runs) | Δ | allowance | gate | frame interval v1.5.0 → v1.5.1 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 6.627 (6.26, 7.42, 6.63) | 6.756 (6.76, 9.02, 6.53) | +0.129 (+1.9 %) | 0.580 | PASS | 87.4 → 84.6 (-3.2 %) | 0 |
| 1440 1× idle | adaptive (fallback) | 0.823 (0.79, 0.82, 1.04) | 0.837 (0.80, 0.84, 0.85) | +0.014 (+1.7 %) | 0.126 | PASS | 16.7 → 16.7 (+0.0 %) | 0 |
| 1440 1× drag | forced (real) | 7.264 (7.26, 7.48, 6.58) | 7.406 (7.41, 7.27, 7.41) | +0.142 (+2.0 %) | 0.449 | PASS | 99.2 → 93.9 (-5.3 %) | 137,242 |
| 1440 1× drag | adaptive (fallback) | 0.923 (0.92, 0.94, 0.87) | 0.987 (0.99, 0.92, 1.29) | +0.064 (+6.9 %) | 0.046 | FAIL | 16.7 → 16.7 (+0.0 %) | 0 |
| 390 4× idle | forced (real) | 10.809 (10.81, 9.73, 11.19) | 10.346 (10.93, 9.91, 10.35) | -0.463 (-4.3 %) | 0.729 | PASS | 37.5 → 37.7 (+0.6 %) | 0 |
| 390 4× idle | adaptive (fallback) | 10.206 (10.28, 10.21, 10.00) | 9.769 (10.54, 9.47, 9.77) | -0.437 (-4.3 %) | 0.510 | PASS | 36.1 → 34.7 (-3.7 %) | 0 |
| 390 4× drag | forced (real) | 9.692 (10.48, 9.69, 9.31) | 11.462 (11.46, 11.02, 11.88) | +1.770 (+18.3 %) | 0.585 | FAIL | 41.9 → 45.2 (+7.9 %) | 26,978 |
| 390 4× drag | adaptive (real) | 10.084 (9.88, 10.08, 10.13) | 11.110 (11.11, 10.16, 12.12) | +1.026 (+10.2 %) | 0.504 | FAIL | 42.1 → 43.6 (+3.5 %) | 20,416 |

**Overall: FAIL**; page/console errors: 0.
