# 1440 forced drag, rotated order, 6 reps: A/A

Gate: median library ms/frame (interleaved A B A B…, REPS reps each, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.1 lib ms (runs) | v1.5.1a lib ms (runs) | Δ | allowance | gate | frame interval v1.5.1 → v1.5.1a ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× drag | forced (real) | 7.093 (7.07, 7.12, 6.32, 7.42, 6.92, 7.20) | 7.153 (7.08, 7.22, 7.54, 7.05, 7.12, 7.19) | +0.060 (+0.8 %) | 0.550 | PASS | 88.6 → 89.2 (+0.7 %) | 136,740 |

**Overall: PASS**; page/console errors: 0.
