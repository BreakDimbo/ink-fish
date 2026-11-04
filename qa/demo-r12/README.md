# qa/demo-r12 — v1.5 grid wake, round 12

- `sbs-light.mp4`, `sbs-dark.mp4`: v1.3.1 (left, ../demo-r9/before-*.mp4) vs v1.5 at 985d08c (right), 10 s, 30 fps
- `after-light.mp4`, `after-dark.mp4`: the v1.5 halves; `still-3way.png`: v1.3.1 / v1.5 / webgl-water reference at t = 6.6 s
- `perf-a.md` (b3bb1df, 4 px grid) and `perf-b.md` (ad04871, 5 px grid, scissored): the interleaved gate including frame interval
- `behave/` + `behave.json`: calm-sleep, hidden-pause and scroll checks; `func.log`, `touch.log`: functional suite
- `probe/`: tuning crops and height dumps; `sheet/`: contact sheets used for scoring; `scores.md`: rubric scores
- `frames/` (raw PNG frames, about 350 MB) is not committed
