# v1.5-gridwake perf gate vs v1.3.1 (qa/demo-r11/perfx.py, interleaved, 3 reps, headless Chrome / SwiftShader)

Gate metric (as in earlier rounds): median of library ms/frame (stats.ms/stats.n). Pass if Δmedian ≤ max(v1.3.1 spread/2, 5 %).

| case | mode | v1.3.1 median (runs) | v1.5 median (runs) | Δ | allowance | gate | frame interval median v1.3.1 → v1.5 ms | grid cell-steps/frame (v1.5) |
|---|---|---|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | 7.184 (7.18, 5.60, 8.77) | 6.529 (6.15, 6.53, 9.14) | -0.655 (-9.1 %) | 1.585 | PASS | 96.1 → 86.9 | 0 |
| 1440 1× idle | adaptive (fallback) | 0.843 (0.84, 0.72, 0.85) | 0.789 (0.79, 0.73, 0.80) | -0.054 (-6.4 %) | 0.061 | PASS | 16.7 → 16.7 | 0 |
| 1440 1× drag | forced (real) | 7.230 (7.43, 6.99, 7.23) | 7.397 (7.88, 7.40, 6.56) | +0.167 (+2.3 %) | 0.362 | PASS | 110.9 → 125.3 | 261,863 |
| 1440 1× drag | adaptive (fallback) | 0.909 (1.02, 0.83, 0.91) | 0.887 (0.86, 0.89, 0.97) | -0.022 (-2.4 %) | 0.094 | PASS | 16.7 → 16.7 | 0 |
| 390 4× idle | forced (real) | 10.818 (9.13, 11.07, 10.82) | 8.838 (8.14, 9.86, 8.84) | -1.980 (-18.3 %) | 0.966 | PASS | 42.3 → 41.4 | 0 |
| 390 4× idle | adaptive (real) | 9.596 (9.38, 9.60, 10.25) | 9.946 (7.46, 9.95, 11.12) | +0.350 (+3.6 %) | 0.480 | PASS | 38.4 → 42.1 | 0 |
| 390 4× drag | forced (real) | 11.083 (11.49, 11.08, 8.80) | 9.715 (9.71, 9.69, 11.52) | -1.368 (-12.3 %) | 1.348 | PASS | 45.1 → 42.8 | 42,481 |
| 390 4× drag | adaptive (real) | 9.840 (10.49, 9.84, 9.60) | 10.183 (11.53, 10.18, 9.33) | +0.343 (+3.5 %) | 0.492 | PASS | 52.3 → 38.2 | 34,165 |

**Overall: PASS** — no case regresses beyond its allowance on the gate metric.

Caveats (honest): the gate metric is main-thread library time. The grid's extra GPU work (13-tap step, up to 4 steps/frame, ~81k cells at 1440×900) does not show up there. On SwiftShader the forced 1440 1× drag frame interval median went 110.9 → 125.3 ms (+13 %), but the spread overlaps (108–122 vs 106–133 ms), and forced idle went 96.1 → 86.9 ms. At 390 4× the intervals are 45.2 → 42.8 ms (drag) and 42.3 → 41.4 ms (idle). Adaptive 1440 drops to the flat fallback on SwiftShader in both builds (16.7 ms). The grid sleeps (0 cell-steps) when idle. Raw: perf.log, perf.json, perf_table.md.
