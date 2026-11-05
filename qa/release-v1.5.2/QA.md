# Release QA, v1.5.2 (served from the worktree, tip incl. ?v=1.5.2)

- func: 10/10 PASS, 0 errors (func.log)
- touch: PASS (touch-action pan-y; vertical swipe scrolls with no trail; horizontal and hold+drag draw a trail; 0 errors) (touch.log)
- behave (deterministic clock, test-only hooks via qahooks152.py): calm-sleep clears the grid by 2.5 s, hidden tab stops (0 frames), scroll carries the wake, tap and still hold leave no grid, a flick wakes it. Matches the v1.5.1 release numbers to 4 decimals; 0 errors (behave.json). Run 1 failed only because the old hook spec's anchor predates GRID_ON (behave.err.run1)
- shots: light/dark × 1440/390, InkFish.version 1.5.2, no hooks (peek/gain false), 0 page/console errors (shots.json, demo-*.png). 1440 reports water "fallback" on SwiftShader (adaptive), as in the v1.5.1 release
- hooks: none in the shipped src (hooks-check.txt)
- perf: gate already passed, not rerun (qa/demo-r14/perf3-vs-151.md, perf3-aa.md, perf4-vs-151.md, perf4-aa.md)
