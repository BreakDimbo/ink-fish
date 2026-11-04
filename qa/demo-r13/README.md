# r13: v1.5.1, clicks go back to the original restrained ring

Branch `v1.5.1-click` (off main f4a3191 = v1.5.0). Not pushed or tagged.

## What "original" means here
These are click clips of each build at the same spot and clock: a 0.12 s click at t = 0.5 s and a still 1 s hold at t = 2.6 s (`drag.py … click`). The contact sheets are `sheet/click-light.png` and `sheet/click-dark.png`.
- **v1.2.1 (88409f0)**: a single hairline ring, a train of 3 thin shade+light fronts that grow to about 300 px and fade over 3.6 s. Fish that a ring crosses bend slightly. This is the "restrained" look, so we took it as the original.
- v1.3.0 (0828e80): the first real-water click, a soft GL ring that is wider and more watery. It is still calm, but it is not the hairline.
- v1.5.0: a press packet plus a dimple, a lift packet, and a grid stamp. Its rings are large and dense and fill the whole frame.

## v1.5.1 behaviour
- pointerdown always draws v1.2.1's ring. The ring is ported exactly: same radius curve, envelope, 3-front train, palette, and fish refraction and nudge. It draws in both water modes.
- If the press never moves past the drag threshold, it stays a click: no press packet, no dimple, no grid pressure, and no lift packet. Mouse uses 6 px; touch uses 8 px plus a hold or a sideways start. This covers taps and still press-and-holds.
- If the press becomes a stroke within 0.25 s, the click ring is removed. v1.5.0's press packet takes its place, born at the down point and time with the same phase (so the random stream also matches). The dimple ramp and the grid's fresh-press ramp are both back-dated to the down time.
- If the stroke starts after a still hold, the hold was a click. Its ring stays, and the stroke starts fresh at the point where the drag began.

## Evidence
- `click-sbs-light.mp4` / `click-sbs-dark.mp4`: v1.5.0 | v1.2.1 | v1.5.1.
- `drag-sbs-light.mp4` / `drag-sbs-dark.mp4`: v1.5.0 | v1.5.1 on the combo path (a slow stroke, then a flick).
- `dragdiff-light.txt` / `dragdiff-dark.txt`: per-frame pixel diff against v1.5.0. Mean abs diff over all 300 frames is 0.068 in light and 0.030 in dark. The only visible differences are the two down frames (f15, f180), where v1.5.0 already shows a half-strength dimple and v1.5.1 shows nothing yet. From the next frame the drawing matches (`sheet/drag-onset-light.png`). After that the only trace is a max channel difference of 8/255 or less in the wave field, which fades out; frames from f270 on are identical.
- `perf-vs-131.md` and `perf-vs-150.md`: both PASS in all 8 rows. `func.log`: 10/10 pass. `touch.log`: pass. `behave.json`: sleep, hidden and scroll all match v1.5.0. The new click section shows a tap and a 1 s still hold leave grid = false and hmax = 0, and a flick still wakes the grid. There were 0 errors in every run.
- `drag-new-light.mp4` was rendered before the shared-phase fix (2370e13) and is superseded by `drag-new2-light.mp4`.
