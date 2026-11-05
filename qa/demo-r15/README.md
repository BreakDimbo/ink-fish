# r15 · 点水的扩散速度 — water at a real pond's speed (v1.5.3-slowclick)

Feedback (15:54 SGT): "还是不对，点水的扩散速度也太快了" + "去调研学习真实的水的扩散速度，全部优化".

## 1 · The film (final master `inkfish-promo-master-1440p.mp4`)
* Capture: `cap.py` steps a virtual clock 1000/30 ms per frame, encoded 30 fps; `compose.py` uses `setpts=N/30/TB`.
  **Playback is 1:1 real time (time-scale factor 1.0, no retime).** The ring's slowness is in the code (v1.3.1 `PR_SLOW 0.22`).
* s02 (light, tap at 9.567 s, dsf 8/3): crest 33 px @0.3 s, 50 @0.5, 93 @1.0, 138 @1.5, 150 @1.7 → **≈ 86 CSS px/s**,
  outermost ripple ~20 px ahead; clear to ~1.6 s, faint to ~3 s, gone ~3.5 s. (`data/promo-s02-light.json`)
* s08 (dark, tap at 37.367 s): 60 px @0.77 s → 147 @1.77 s → **≈ 87 px/s**, visible to ~3.0 s. (`data/promo-s08-dark.json`)

## 2 · Live v1.5.2 (1440×900, frame-exact 30 Hz clock = what a real device shows)
* A tap's **first visible ring is the pointer's arrival (hover) ring**, not the click ring: crest 94 px @0.13 s,
  211 @0.40 (≈ **500 px/s**), outermost ripple ~700 px by 1.07 s (≈ **650 px/s**). The film's 86 px/s ring sits under it.
  → **v1.5.2 / film ≈ 5.8× (crest) to 7.5× (outer ripple).**
* Drag (200 px/s stroke): the press ring and the lift ring sweep the screen at ~550–600 px/s; grid wake impulse
  crest ~200 px/s, front ~330 px/s (gridsim). Below its own c_min (~300 px/s) a slow drag left no wake at all.
* Box wall-clock capture (CDP screencast) reads lower (hover crest ~230 px/s): SwiftShader runs 10–15 fps at
  sim/wall ≈ 0.8, so all comparisons use the device-equivalent virtual clock (`stepcap.py`); wall clock in `livecap.py`.

## 3 · A real pond (cited)
ω² = gk + (σ/ρ)k³ (water, σ = 0.072 N/m): **c_min = 23.2 cm/s at λ = 1.73 cm; c_g,min = 17.8 cm/s at λ = 4.39 cm**
(`physics.json`). A stone/fingertip ring packet: short capillary ripples lead (c_g = 3c/2), longer gravity waves follow
(c_g = c/2); the calm centre grows at c_g,min. Viscous decay 2νk² — much faster with a surface film (Marangoni).
Kelvin wake half-angle 19.47°; no steady wake below c_min for straight motion.
Sources: Lamb, *Hydrodynamics* (viscous damping of waves, 2νk²); Le Méhauté, JFM (ring packets); photoplaza "ringwaves.pdf" (pond ring-packet
experiment, 30 fps, packet ≈ c_g,min); Kobe Univ. EOS wave notes; WHOI GFD lecture 2; Wikipedia "Capillary wave",
"Kelvin wake pattern"; Science (AAAS) news on the Kelvin angle (Rabaud & Moisy, PRL 2013); arXiv 0704.3990 (sub-c_min circular sources);
arXiv 1805.06777; Proc. R. Soc. A 1965 & JGR 1989 (film damping).

**Scale.** A koi is ~120 CSS px nose-to-tail at 1440; a young koi ≈ 30 cm → **4 px/cm** (v1.5.2 implied 16.7 px/cm,
i.e. a 7 cm koi). At 4 px/cm: c_g,min = **71 px/s**, c_min = **93 px/s** (45 cm koi → 48/63 px/s). The film's 86 px/s
crest falls inside this band. At 390 px the koi is ~94 px (3.1 px/cm → 55/72 px/s); v1.5.3 keeps one CSS-px scale.

## 4 · v1.5.3 (branch `v1.5.3-slowclick` off aa6c705)
* `S = 2.5e-3 m/px` (koi scale) for the hover/lift rings, trail and flat fallback (fronts 300 → 88 px/s); the grid wake
  at 60 Hz with c2/β/κ scaled (c_min ≈ 0.31 cell/step ≈ 92 px/s); stroke gate at 23 cm/s ≈ 93 px/s.
* The promo click ring (`PR_S = 6e-4`, `PR_SLOW 0.22`) and the idle swell keep their own scale: already the film.
* The arrival hover ring at a click spot is folded into the click (as CLK_S assumed) — the double ring is gone.
* Restraint: `RING_G = 0.25` (hover/lift rings as faint as v1.5.2's, under the click ring); drag-wake pressure weighted
  by stroke speed 0.35 → 1.6 (flick = v1.5.2 contrast; slow drag a faint V).
* Every speed is per real second: rings use their age in s, the grid steps `60 × dt` (≤4/frame, dt ≤ 0.1 s).

### Measured (frame-exact clock, 1440×900)
| | crest px/s | outer ripple | visible | ring contrast @0.3/0.5/0.8 s |
|---|---|---|---|---|
| film s02 / s08 | 86 / 87 | +20 px | ~3 s | — |
| live v1.5.2 first ring | ~500 | ~650 px/s, 700 px by 1 s | — | hover 6.8 / 4.6 / 1.9 |
| **v1.5.3 click** | **86** (27@0.27, 50@0.53, 96@1.07, 142@1.6) | +25 px | ~3.5 s | click 7.3 / 7.1 / 7.2 |
| v1.5.3 hover | ~80 | | ~2 s | 6.1 / 4.3 / 3.4 |
| real pond, 30 cm koi | 71 (calm centre) | 93 (lead) | film-dependent | |
* Drag wake: lateral front ~70–80 px/s (24 px @0.57 s → 131 @2.17 s), c_min 93. Flick wake peak contrast 9.0 vs 9.3 (v1.5.2).
* 30 / 60 / 120 Hz: crest radii within 2 px at 0.25–1.25 s, amplitudes ±1 %; flick wake frames corr ≥ 0.993.
* func.py 10/10 PASS, touchonly PASS (v1.5.2 baseline: same values; its FAILs are only a harness 404 for qa/demo-r9/blank.html, absent from the archive).

## Files
* `click-sbs-light.mp4`, `click-sbs-dark.mp4`: film | live v1.5.2 | v1.5.3, same 960×402 CSS window, 30 fps = real time.
* `click-sbs-guides-light.mp4`: same + blue dotted circles = real pond fronts (71 / 93 px/s). No usable licensed real-water
  clip is on the box, so the physics reference is these guides + the plot.
* `drag-sbs-light.mp4`, `drag-sbs-dark.mp4`: v1.5.2 | v1.5.3, press, 200 px/s stroke for 2 s, lift.
* `ring-radius-vs-time.png`: radius vs t (film, live, new, physics band), contrast vs t, drag-wake front.
* Tools: `stepcap.py` (frame-exact), `livecap.py` (wall clock), `ringhp2.py` (ring meter), `hovamp.py`, `wake.py`,
  `wakeamp.py`, `physics.py`, `gridsim.py`, `sbs.py`, `plot.py`, `perfx.py`/`perfsum.py`; data in `data/`.

## Perf (headless Chrome/SwiftShader, 1440×900, 1× CPU, forced real water, interleaved + rotated)
Gate: Δ median library ms/frame ≤ max(baseline spread/2, 5 %).
| case | v1.5.2 | v1.5.3 | Δ | allowance | gate | A/A (v1.5.2 vs itself) |
|---|---|---|---|---|---|---|
| drag (5 reps) | 6.443 | 6.698 | +0.255 (+4.0 %) | 1.640 | **PASS** | +0.385 (+6.0 %) |
| idle (5 reps) | 6.209 | 6.654 | +0.445 (+7.2 %) | 0.543 | **PASS** | +0.058 (+0.9 %) |
* Frame interval: drag 92.0 → 90.4 ms (−1.8 %), idle 79.3 → 85.5 ms (A/A 79.3 → 82.9). Grid cell-steps per frame
  during drag 126 k vs 133 k (the 60 Hz grid does a little less work). 0 page/console errors. (`perf-vs-152.md`, `perf-aa.md`)
* Idle re-run (7 reps, interrupted after 17/21 runs, `perf2-idle-*.md`): v1.5.3 +8.7 % but the A/A copy +14.0 % in the
  same batch, both over the gate: the box's idle noise floor exceeds 5 %. Pooled over both batches: idle +5.5 %
  (21 baseline runs vs 11), drag +0.9 %. Nothing on the idle path changed (no grid, same swell, same ring count;
  RING_G is one multiply), so no regression is shown, though a quiet-box re-run would make idle certain.

## Self-score (out of 10)
* Speed matches the film: **9.5**. Crest 86 px/s against the film's 86/87, lead +25 vs +20 px.
* Physically plausible: **8**. The crest sits inside the c_g,min–c_min band at the koi scale and the drag wake front is about 75 px/s. Fast flicks are narrower than Kelvin's 19.5°, the grid can't resolve the 1.7 cm capillary length, and mobile uses the same CSS-px scale.
* Restraint: **8**. Hover and lift rings are as faint as in v1.5.2 and below the click ring, and the screen-filling fast rings are gone. One new look: a slow drag now leaves a faint V.
* Frame-rate independence: **9.5**. At 30/60/120 Hz the crest is within 2 px and the flick wake correlates at ≥ 0.993.
* Perf: **8**. Gate PASS. Idle is noisy on this box: pooled +5.5 % with no code cause.
* Overall: **8.6**.

## Trade-offs / open
1. One CSS-px scale everywhere. On a 390 px phone the koi is about 94 px, so the water runs about 28 % fast relative to the fish.
2. A slow drag (≥ ~95 px/s) now leaves a faint V wake. That is physically right, because it is faster than c_min, but it is new compared with v1.5.2. Knob: the slow end of `gSp` is 0.35.
3. Flick wakes stay about 1.6 s (v1.5.2: about 0.8 s) because slower waves stay nearby. Their V is narrower than Kelvin's angle.
4. The click ring's tail measures longer than in the film: 0.25 vs about 0.1 of peak at 2 s. The ring code is the same as in v1.5.2, so the cause is probably the film being rendered at dpr 3 / 2.67 and then downscaled. Left unchanged.
5. The arrival hover ring no longer fires at the click spot; it is folded into the click.
6. Not yet done (release step): the `index.html` `?v=1.5.2` cache-bust is not bumped.
