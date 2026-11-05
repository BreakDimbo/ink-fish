# Release QA, v1.5.3 (served from the worktree at tip c7e3daf, incl. ?v=1.5.3; run-qa.sh, 2026-11-05 ~16:53 SGT)

- func: 10/10 PASS, 0 errors (func.log)
- touch: PASS (touch-action pan-y; vertical swipe scrolls with no trail; horizontal and hold+drag draw a trail; 0 errors) (touch.log)
- behave (deterministic clock, test-only hooks via qahooks153.py = v1.5.2's hook spec with the two retuned GRID-line anchors updated): same lifecycle as v1.5.2. The calm sleep clears the grid by 2.5 s, a hidden tab stops (0 frames), scroll carries the wake, a tap and a still hold leave no grid, and a flick wakes it. The heights differ from v1.5.2 by design: the slower grid keeps more amplitude (sleep 0.5 s hmax 0.0243 vs 0.0138, scroll 0.0958 vs 0.0342, flick 0.0575 vs 0.0526). Light and dark agree; 0 errors (behave.json)
- shots: light/dark × 1440/390, InkFish.version 1.5.3, no hooks (peek/gain false), 0 page/console errors (shots.json, demo-*.png). 1440 reports water "fallback" on SwiftShader (adaptive), as in the v1.5.1 and v1.5.2 releases
- hooks: none in the shipped src (hooks-check.txt)
- perf: the gate passed in r15 and was not rerun. Drag +4.0% / idle +7.2% vs live v1.5.2, both inside the A/A allowance (qa/demo-r15/perf-vs-152.md, perf-aa.md, perf2-idle-*.md)
- earlier r15 checks: 30/60/120 Hz ring radius within 2 px; side-by-sides vs the promo (qa/demo-r15/README.md)
