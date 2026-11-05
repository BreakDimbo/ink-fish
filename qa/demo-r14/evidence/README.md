# r14 step 1: which build and which click settings the promo was recorded with

**Answer: ink-fish v1.3.1, commit 173a9c0 (tag v1.3.1), real-water mode.**

## Evidence
1. `/workspace/inkfish-promo/storyboard.md` says all footage is "ink-fish v1.3.1 真实渲染" (real v1.3.1 renders).
2. The git reflog of /workspace/ink-fish shows HEAD at 173a9c0 (= v1.3.1) from 2026-11-03 21:22 to 2026-11-04 11:12 SGT.
   The promo frames were captured on 2026-11-03 between 22:36 and 23:35 SGT (footage/frames mtimes), which is inside that window.
   The capture script served /workspace/ink-fish/src from that working tree.
3. **Pixel-exact re-render.** I re-rendered promo shot `s02_ring_light` (the click ring in segment R, 9.07–15.07 s of the final cut) with the promo's own capture script (`promocap.py` is the promo's cap.py; only the output dir and port are parameterised).
   - From a clean `git archive v1.3.1`, all 72 frames are **identical** to the promo footage frames (mean 0, max 0): `repro-v131-vs-promo-footage.txt`.
   - The same shot on live v1.5.1 (6e725b9) differs strongly. At f71 the mean diff is 4.10, the max is 144, and 16.7 % of pixels differ by more than 8: `repro-v151-vs-promo-footage.txt` and `s02-f71-promo-v131-v151.jpg`.

## Settings (stage/pond.html in the promo project)
- The page calls `InkFish.mount` with `{fixed:true, ripples:true, water:'real', adaptive:false, maxDpr:<shot dpr>, koi:<shot>, theme:'auto'}`.
- The theme is set by `data-theme`, and the look is the v1.3.1 default `?q` set for that theme (no overrides).
- The click is a 0.12 s mouse press (`ring()` in shots.py), so it is a **firm v1.3.1 Cauchy–Poisson ring** with life 5 s and slow-mo 0.22.

## What the promo click actually contains
`hovercheck.py` logs every `addRipple` call while replaying the promo gestures on v1.3.1. Logged calls are `[t, x, y, s, firm]`:

| shot | what is logged |
|---|---|
| s02_ring_light (light, segment R) | `[8000, 600,292, 0.46, hover]` and `[8000, 600,292, 1, firm]` |
| s08_wide_dark (dark, segment W) | `[10500, 860,330, 0.46, hover]` and `[10500, 860,330, 1, firm]` |
| s10_peak_light (drag, segment PK) | `[6300, 90,230, 1, firm]`, with no hover ring because the pointer was already parked there |

- In s02 and s08 the pointer jumps from its park spot onto the click spot in the same frame. That jump adds a co-located hover packet (s 0.46) on top of the firm ring.
- In real mode both packets share the same spectrum and start time, so the ring seen in the promo is **one v1.3.1 ring at s = 1.46**.
- In the drag shot, the press ring (s = 1) is cut to ×0.55 when the press turns into a stroke inside 0.4 s (v1.3.1 rule), so the opening ripple of the promo drag is **s = 0.55**.

Those two numbers (click 1.46, drag opening 0.55, both in v1.3.1 units) are the targets for the port.
