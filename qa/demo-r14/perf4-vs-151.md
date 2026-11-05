# 1440 forced drag, rotated order, 6 reps: live v1.5.1 vs v1.5.2

Gate: median library ms/frame (interleaved A B A B…, REPS reps each, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.1 lib ms (runs) | v1.5.2 lib ms (runs) | Δ | allowance | gate | frame interval v1.5.1 → v1.5.2 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× drag | forced (real) | 7.093 (7.07, 7.12, 6.32, 7.42, 6.92, 7.20) | 6.905 (6.62, 7.37, 6.75, 7.32, 7.06, 6.64) | -0.188 (-2.6 %) | 0.550 | PASS | 88.6 → 89.1 (+0.6 %) | 133,078 |

**Overall: PASS**; page/console errors: 0.
