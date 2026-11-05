# r15 perf A/A idle re-run (partial)

Gate: median library ms/frame (interleaved A B A B…, REPS reps each, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.2 lib ms (runs) | v1.5.2a lib ms (runs) | Δ | allowance | gate | frame interval v1.5.2 → v1.5.2a ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 5.744 (6.00, 5.38, 6.35, 5.61, 5.47, 5.88) | 6.549 (6.86, 6.55, 6.18, 6.57, 5.82) | +0.805 (+14.0 %) | 0.481 | FAIL | 76.4 → 78.6 (+2.9 %) | 0 |

**Overall: FAIL**; page/console errors: 0.
