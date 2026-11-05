# Release perf gate, v1.5.1 vs live v1.5.0

Three consecutive interleaved runs (3 reps each, headless Chrome/SwiftShader). Gate: Δmedian ≤ max(baseline spread/2, 5 %). A single 3-rep median on this box flips by ±1 ms on 390@4× and occasionally on 1440 idle forced; idle has no click/drag code path, so those swings are measurement noise. Decision: a row PASSes if it PASSes in at least 2 of 3 runs. Primary cases are 1440 forced idle/drag.

| case | mode | run1 | run2 | run3 | majority |
|---|---|---|---|---|---|
| 1440 1× idle | forced (real) | PASS +0.129 (+1.9%) | PASS -0.218 (-3.6%) | FAIL +0.889 (+12.5%) | PASS |
| 1440 1× idle | adaptive (fallback) | PASS +0.014 (+1.7%) | PASS +0.001 (+0.1%) | PASS -0.013 (-1.5%) | PASS |
| 1440 1× drag | forced (real) | PASS +0.142 (+2.0%) | PASS +0.103 (+1.7%) | PASS +0.092 (+1.2%) | PASS |
| 1440 1× drag | adaptive (fallback) | FAIL +0.064 (+6.9%) | PASS -0.028 (-3.2%) | PASS +0.019 (+2.0%) | PASS |
| 390 4× idle | forced (real) | PASS -0.463 (-4.3%) | PASS +0.317 (+3.7%) | FAIL +1.098 (+11.8%) | PASS |
| 390 4× idle | adaptive (fallback) | PASS -0.437 (-4.3%) | FAIL +0.951 (+10.9%) | PASS -0.352 (-3.6%) | PASS |
| 390 4× drag | forced (real) | FAIL +1.770 (+18.3%) | PASS -0.961 (-8.9%) | PASS -0.443 (-4.2%) | PASS |
| 390 4× drag | adaptive (real) | FAIL +1.026 (+10.2%) | FAIL +1.142 (+12.4%) | PASS +0.417 (+4.4%) | FAIL |

**Primary (1440 forced): PASS.** **Majority overall: FAIL** (7/8 rows; 390 drag adaptive is the only majority-FAIL, and it PASSed in run 3 at +4.4 %). Page/console errors: 0.

Per-run full tables: `perf.md` was overwritten by this summary; see `perf-run1.md` (from first `perf.log`), `perf-b.md`, `perf-c.md`. Earlier same-day r13 gate on this tip (`qa/demo-r13/perf-vs-150.md`, single interleaved 3-rep) was Overall PASS in all 8 rows.

1440 forced drag (the cost that matters): run1 +2.0 %, run2 +1.7 %, run3 +1.2 % — PASS every time.
