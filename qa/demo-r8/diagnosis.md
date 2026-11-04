# Why v1.3.1's trail read as viscous (measured, dark, column x=900, 1600 px/s stroke)
| | v1.3.1 | v1.3.2 | real water @16.7 px/cm |
|---|---|---|---|
| outer front speed | ~70 px/s (4.2 cm/s) | ~295 px/s (17.7 cm/s) | min group 17.7 cm/s ≈ 295 px/s; capillary ≥ 490 px/s |
| distance travelled before fade | ~113 px | ~445 px | — |
| peak contrast decay | ×0.17/s, dying in place, pulsing every 0.3–0.4 s | holds ~flat travelling 0.9 s, then ends by 1.5 s (geometric 1/√r + end fade) | low damping |
Causes in code: SLOW=0.22 time scale; NU 6× water; 0.5 s ring fade-in; 12 age rows linearly crossfaded (pulsing/ghosting instead of travelling); SRC 7 px broad gel hump; no geometric spreading. Cursor lag: none (head point updates per pointermove).
Fix: real-time clock, NU 1.2e-6, SRC 5, static 384-row (≈10 ms/row) profile LUT built once (no per-frame profile pass), trough sign, 1/√r, 50 ms fade-in; flat fallback lines move at 300 px/s with 1/√r.
Strip: strip-detach-dark.png (fast flick, every 4th frame, fronts leaving the stroke).
