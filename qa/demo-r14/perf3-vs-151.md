# Perf gate on d512d3f: live v1.5.1 vs v1.5.2

Gate: median library ms/frame (interleaved A B A B…, 5 reps each, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.1 lib ms (runs) | v1.5.2 lib ms (runs) | Δ | allowance | gate | frame interval v1.5.1 → v1.5.2 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 5.992 (6.38, 6.46, 5.99, 5.84, 5.46) | 5.949 (5.95, 5.87, 6.57, 5.69, 6.82) | -0.043 (-0.7 %) | 0.503 | PASS | 75.0 → 76.3 (+1.8 %) | 0 |
| 1440 1× drag | forced (real) | 5.901 (5.83, 6.03, 5.90, 6.99, 5.84) | 6.393 (6.39, 5.37, 7.01, 6.42, 5.94) | +0.492 (+8.3 %) | 0.582 | PASS | 80.8 → 88.7 (+9.8 %) | 133,408 |
| 390 4× drag | adaptive (real) | 9.482 (11.05, 8.75, 8.98, 9.48, 9.88) | 9.879 (10.73, 10.93, 9.88, 9.68, 9.25) | +0.397 (+4.2 %) | 1.151 | PASS | 37.5 → 40.3 (+7.4 %) | 19,981 |

**Overall: PASS**; page/console errors: 0.
