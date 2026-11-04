# perf at b3bb1df (dispersion tune, dark sheen)

Gate: median library ms/frame (interleaved, 3 reps, headless Chrome/SwiftShader); pass if Δmedian ≤ max(v1.3.1 spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.3.1 lib ms (runs) | v1.5 lib ms (runs) | Δ | allowance | gate | frame interval v1.3.1 → v1.5 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 5.820 (5.82, 5.44, 5.98) | 5.194 (6.58, 5.19, 5.11) | -0.626 (-10.8 %) | 0.291 | PASS | 80.8 → 75.6 (-6.5 %) | 0 |
| 1440 1× idle | adaptive (fallback) | 0.859 (0.74, 0.86, 1.65) | 0.728 (0.76, 0.73, 0.71) | -0.131 (-15.3 %) | 0.458 | PASS | 16.7 → 16.7 (+0.0 %) | 0 |
| 1440 1× drag | forced (real) | 6.811 (5.80, 7.62, 6.81) | 7.067 (6.86, 7.13, 7.07) | +0.256 (+3.8 %) | 0.909 | PASS | 81.8 → 88.8 (+8.6 %) | 242,352 |
| 1440 1× drag | adaptive (fallback) | 1.788 (1.96, 0.96, 1.79) | 0.831 (0.81, 0.83, 0.88) | -0.957 (-53.5 %) | 0.502 | PASS | 24.2 → 16.7 (-31.2 %) | 0 |
| 390 4× idle | forced (real) | 9.494 (9.98, 7.49, 9.49) | 8.404 (7.91, 8.40, 8.41) | -1.090 (-11.5 %) | 1.247 | PASS | 34.4 → 31.4 (-8.6 %) | 0 |
| 390 4× idle | adaptive (real) | 9.587 (10.06, 8.95, 9.59) | 8.624 (10.01, 8.62, 7.87) | -0.963 (-10.0 %) | 0.559 | PASS | 34.2 → 29.2 (-14.6 %) | 0 |
| 390 4× drag | forced (real) | 9.487 (10.30, 9.49, 8.85) | 9.052 (9.22, 9.05, 7.98) | -0.435 (-4.6 %) | 0.727 | PASS | 37.9 → 37.2 (-1.9 %) | 42,047 |
| 390 4× drag | adaptive (real) | 9.422 (9.42, 9.54, 9.05) | 9.365 (9.70, 9.37, 8.61) | -0.057 (-0.6 %) | 0.471 | PASS | 37.6 → 38.0 (+1.0 %) | 32,729 |

**Overall: PASS**; page/console errors: 0.
