# v1.5.2 self-score against the promo (v1.3.1, 173a9c0): code at d512d3f

Scale 0–10, where 10 = indistinguishable from the promo film's first ripple. Target ≥ 8.

| aspect | score | evidence | note |
|---|---|---|---|
| click / tap ring | 9 | click-sbs-{light,dark}.mp4, sheet-click-{light,dark}.jpg, sheet-promo-stage-{light-s02,dark-s08}.jpg | The v1.3.1 ring with its own weights and slow front, light and dark. At s1.46 it is a touch stronger than a parked v1.3.1 click, because it reproduces the hover packet the film's pointer jump added. d512d3f is pixel-identical to a9b68f0 (clickC-check.txt, max diff 0). |
| hold | 9 | same renders (still hold at 2.6–3.6 s) | Same ring, no swap to v1.5.0's press packet. |
| drag start (first ~1 s) | 7 | dragstart-sbs2-{s10_peak_light,s09_peak_dark}-halfspeed.mp4, sheet-dragstart2-*.jpg | Restrained: v1.5.1's big opening packet is gone, and the wake eases on (0.6 s / 120 px). For the perf gate, a press that turns into a stroke within 0.4 s drops its ring over 0.3 s, so the faint ring the film shows growing behind the drag is absent. |
| wake after the start | 9 | drag-sbs2-{light,dark}.mp4, dragdiff-*.txt, dragdiff-new2.txt | v1.5.1's wake code, untouched (isolation diff identical). Only the slow-start onset is eased. Versus live: mean 0.49/255 light, 0.22 dark. |
| taste (restraint, no glow/particles) | 9 | — | Nothing added. Idle is bitwise equal to live. |
| perf | pass | perf3-vs-151.md, perf3-aa.md, perf4-vs-151.md, perf4-aa.md | Idle −0.7 % lib / +1.8 % frame interval. 1440 drag (rotated order, 6 reps): −2.6 % / +0.6 %, inside the A/A floor of +0.8 % / +0.7 %. 390 adaptive drag: +4.2 %, allowance 12 %. |

**Overall: 8.5 / 10.** Click and hold match the promo. The drag start is restrained, but it now lacks the promo's faint opening ring. That is the price of no perf regression in a pure drag. A press held ≥ 0.4 s before dragging keeps its ring.
