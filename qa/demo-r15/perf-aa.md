# r15 perf A/A: v1.5.2 vs v1.5.2 again

Gate: median library ms/frame (interleaved A B A B…, REPS reps each, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.2 lib ms (runs) | v1.5.2a lib ms (runs) | Δ | allowance | gate | frame interval v1.5.2 → v1.5.2a ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 6.209 (5.76, 6.38, 6.21, 6.04, 6.85) | 6.267 (6.27, 5.96, 6.40, 6.21, 6.47) | +0.058 (+0.9 %) | 0.543 | PASS | 79.3 → 82.9 (+4.6 %) | 0 |
| 1440 1× drag | forced (real) | 6.443 (8.79, 7.18, 5.51, 5.94, 6.44) | 6.828 (6.83, 7.51, 7.64, 5.52, 6.09) | +0.385 (+6.0 %) | 1.640 | PASS | 92.0 → 94.1 (+2.2 %) | 132,576 |

**Overall: PASS**; page/console errors: 0.
