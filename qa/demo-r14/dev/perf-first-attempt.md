# Perf gate, v1.5.2 vs live v1.5.1

Gate: median library ms/frame (interleaved, 3 reps, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.1 lib ms (runs) | v1.5.2 lib ms (runs) | Δ | allowance | gate | frame interval v1.5.1 → v1.5.2 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 7.388 (7.80, 8.37, 6.94, 7.39, 7.20) | 7.737 (7.60, 7.74, 7.63, 10.88, 8.27) | +0.349 (+4.7 %) | 0.719 | PASS | 86.4 → 99.0 (+14.6 %) | 0 |
| 1440 1× drag | forced (real) | 7.134 (7.46, 7.13, 6.97, 7.07, 7.54) | 7.686 (7.91, 7.49, 7.28, 7.69, 7.83) | +0.552 (+7.7 %) | 0.357 | FAIL | 91.1 → 130.3 (+43.0 %) | 132,849 |
| 390 4× drag | adaptive (real) | 10.861 (13.14, 4.41, 10.86, 11.54, 5.37) | 9.643 (5.04, 12.35, 9.64, 5.05, 11.79) | -1.218 (-11.2 %) | 4.367 | PASS | 42.4 → 48.7 (+15.0 %) | 16,793 |

**Overall: FAIL**; page/console errors: 0.
