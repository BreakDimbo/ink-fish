# r15 perf, idle re-run (interrupted after 17/21 runs)

Gate: median library ms/frame (interleaved A B A B…, REPS reps each, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.2 lib ms (runs) | v1.5.3 lib ms (runs) | Δ | allowance | gate | frame interval v1.5.2 → v1.5.3 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 5.744 (6.00, 5.38, 6.35, 5.61, 5.47, 5.88) | 6.242 (6.68, 5.68, 6.65, 6.55, 5.93, 5.70) | +0.498 (+8.7 %) | 0.481 | FAIL | 76.4 → 78.7 (+3.1 %) | 0 |

**Overall: FAIL**; page/console errors: 0.
