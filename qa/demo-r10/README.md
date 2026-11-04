# demo-r10 — round 13 (2026-11-04 SGT), code at 2f15a3f

## Videos (10 s, deterministic combo: press, slow drag 200 px/s, lift, fast flick 1250 px/s, lift)
- side-by-side-light.mp4, side-by-side-dark.mp4: v1.3.1 live (left) vs v1.4 r13 (right)
- before-*.mp4 (v1.3.1), after-*.mp4 (v1.4 r13). after-light was rendered at cc21ed3; every later commit is dark-only, so the light look is the same.
- side-by-side-*-ref.mp4 (local only, not committed): the same pair plus a 10 s real-water clip from research-real-water/clips (YouTube downloads: E2unnSK7WTE 0:53, 4CU8gYYkwSw 0:20). The pipeline's committed reference is the still row in gap-v14-r13.png.
- gap-v14-r13.png: reference / v1.3.1 / v1.3.2 rows (gap.png) + v1.4 r13 light + dark at the same moments
- closeup-{light,dark}-200.png: dimple (3.5 s), release packet 0.5 s after lift, fast V (6.6 s), all at 200 %

## Measurements
- Light calm-centre edge 311 px/s (16-frame fit, threshold 2 levels, tapM vs stillM). Full-screen visibility after release 1.5 s; azimuthal peak > 2 levels inside the 228 px disc for 0.80 s. Identical to r11 (the light tap path did not change). Log: ../demo-r9/tgt-tap-r13.log
- Dark release packet (crestcount.py tapDb vs tapD12 at 6c6214f, RMAX=400): slivers > 12 levels per ray at 0.1/0.33/0.5/0.67/0.83 s after lift = 11/13/12/3/0 (was 27/21/18/10/5). Visible about 0.75 s (was > 1 s). Press packet 17/16/14/13 at 0.1–0.5 s (was 36/32/26/18).
- Dark busyness, whole combo (busy-r13.log): pixels ≥ 12 levels above the median 11.1 % → 3.5 % mean (−69 %), peak 26.2 % → 7.0 % (−73 %). Fish and UI are in both counts, so the cut in slivers alone is larger.
- Light fast-V interior (1250 px/s, frame 33, box 160×40 inside the wedge): p2–p98 span 13 → 18 grey levels (std 3.0 → 4.8) at wavelet gain 0.009 → 0.045.
