# A/A noise floor on the same run: live v1.5.1 vs itself

Gate: median library ms/frame (interleaved A B A B…, 5 reps each, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.1 lib ms (runs) | v1.5.1a lib ms (runs) | Δ | allowance | gate | frame interval v1.5.1 → v1.5.1a ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 5.992 (6.38, 6.46, 5.99, 5.84, 5.46) | 5.928 (5.72, 5.98, 5.34, 6.03, 5.93) | -0.064 (-1.1 %) | 0.503 | PASS | 75.0 → 75.6 (+0.8 %) | 0 |
| 1440 1× drag | forced (real) | 5.901 (5.83, 6.03, 5.90, 6.99, 5.84) | 6.513 (6.94, 5.81, 6.51, 7.65, 6.04) | +0.612 (+10.4 %) | 0.582 | FAIL | 80.8 → 86.3 (+6.8 %) | 133,785 |

**Overall: FAIL**; page/console errors: 0.
