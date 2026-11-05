# r15 perf: v1.5.2 vs v1.5.3 (1440, forced real water, 5 interleaved rotated reps)

Gate: median library ms/frame (interleaved A B A B…, REPS reps each, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.2 lib ms (runs) | v1.5.3 lib ms (runs) | Δ | allowance | gate | frame interval v1.5.2 → v1.5.3 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 6.209 (5.76, 6.38, 6.21, 6.04, 6.85) | 6.654 (5.84, 7.19, 6.65, 6.04, 6.75) | +0.445 (+7.2 %) | 0.543 | PASS | 79.3 → 85.5 (+7.9 %) | 0 |
| 1440 1× drag | forced (real) | 6.443 (8.79, 7.18, 5.51, 5.94, 6.44) | 6.698 (7.26, 7.38, 6.70, 6.20, 6.00) | +0.255 (+4.0 %) | 1.640 | PASS | 92.0 → 90.4 (-1.8 %) | 126,276 |

**Overall: PASS**; page/console errors: 0.
