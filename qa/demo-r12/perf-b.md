# Perf gate at ad04871 (scissored 5 px grid)

Gate: median library ms/frame (interleaved, 3 reps, headless Chrome/SwiftShader); pass if Δmedian ≤ max(v1.3.1 spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.3.1 lib ms (runs) | v1.5 lib ms (runs) | Δ | allowance | gate | frame interval v1.3.1 → v1.5 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 5.563 (5.56, 5.83, 5.51) | 5.374 (5.37, 5.88, 5.24) | -0.189 (-3.4 %) | 0.278 | PASS | 72.6 → 80.5 (+10.9 %) | 0 |
| 1440 1× idle | adaptive (fallback) | 1.718 (1.72, 0.72, 1.90) | 0.765 (0.80, 0.77, 0.72) | -0.953 (-55.5 %) | 0.592 | PASS | 26.0 → 16.7 (-35.8 %) | 0 |
| 1440 1× drag | forced (real) | 6.492 (6.49, 7.04, 6.23) | 5.883 (7.16, 5.86, 5.88) | -0.609 (-9.4 %) | 0.406 | PASS | 85.8 → 83.1 (-3.2 %) | 141,160 |
| 1440 1× drag | adaptive (fallback) | 1.399 (1.55, 1.40, 1.39) | 0.842 (0.92, 0.84, 0.84) | -0.557 (-39.8 %) | 0.083 | PASS | 20.9 → 16.7 (-20.0 %) | 0 |
| 390 4× idle | forced (real) | 9.414 (9.14, 10.09, 9.41) | 9.737 (9.74, 9.13, 9.84) | +0.323 (+3.4 %) | 0.476 | PASS | 35.5 → 35.7 (+0.5 %) | 0 |
| 390 4× idle | adaptive (real) | 8.796 (8.80, 8.51, 9.62) | 8.045 (9.74, 8.04, 7.84) | -0.751 (-8.5 %) | 0.557 | PASS | 33.2 → 30.0 (-9.5 %) | 0 |
| 390 4× drag | forced (real) | 9.183 (9.55, 8.55, 9.18) | 8.661 (8.66, 9.33, 8.37) | -0.522 (-5.7 %) | 0.500 | PASS | 38.3 → 37.3 (-2.7 %) | 26,008 |
| 390 4× drag | adaptive (real) | 9.937 (10.41, 9.94, 9.66) | 8.390 (8.39, 8.54, 8.04) | -1.547 (-15.6 %) | 0.497 | PASS | 39.1 → 36.2 (-7.4 %) | 20,779 |

**Overall: PASS**; page/console errors: 0.
