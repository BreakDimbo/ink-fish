# post-a9b68f0

Gate: median library ms/frame (interleaved, 3 reps, headless Chrome/SwiftShader); pass if Δmedian ≤ max(baseline spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.

| case | mode | v1.5.1 lib ms (runs) | v1.5.2 lib ms (runs) | Δ | allowance | gate | frame interval v1.5.1 → v1.5.2 ms (Δ) | grid cell-steps/frame |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 5.533 (6.03, 6.10, 5.53, 5.36, 5.18) | 6.155 (6.66, 6.02, 6.16, 5.46, 6.69) | +0.622 (+11.2 %) | 0.463 | FAIL | 73.9 → 86.0 (+16.4 %) | 0 |
| 1440 1× drag | forced (real) | 5.982 (6.21, 6.04, 5.68, 5.87, 5.98) | 6.478 (6.95, 6.60, 6.46, 5.91, 6.48) | +0.496 (+8.3 %) | 0.299 | FAIL | 83.0 → 115.2 (+38.8 %) | 131,582 |
| 390 4× drag | adaptive (real) | 9.502 (8.39, 9.50, 10.31, 10.00, 9.31) | 9.430 (9.43, 10.03, 9.03, 9.30, 10.61) | -0.072 (-0.8 %) | 0.960 | PASS | 37.7 → 48.7 (+28.9 %) | 19,351 |

**Overall: FAIL**; page/console errors: 0.
