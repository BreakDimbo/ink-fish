# Re-learning "real dynamic water" — Ultra Water, its sources, and where ink-fish v1.4 went off course

Research round, 2026-11-04 (SGT). No ink-fish code changed. Compared against v1.4-realwater HEAD 1f29c12
(last code commit 2f15a3f), v1.3.1 (qa/demo-r9/base) and v1.3.0 (qa/demo-r7/v130).

## 1. Repos read (all cloned read-only, nothing modified)
| repo | local clone | what it is | relevance |
|---|---|---|---|
| Humpalumps/Ultra-Water (MIT), HEAD 30ea65e | /workspace/ref-ultra-water | the article's project: three.js FFT ocean, island shore, floaters | optics + caustics + the one interactive piece (`impactWaves`) |
| evanw/webgl-water (MIT, 2011) | /workspace/ref-ultra-water-evanw | the classic interactive pool: GPU height-field wave equation + area-ratio caustics | **the actual "dynamic water" method** (drops, drag wakes, sphere displacement); Ultra Water credits it for caustics |
| iamtechartist/coastal-simulation (MIT) | /workspace/ref-ultra-water-coastal | WebGPU staggered-grid shallow-water solver for a coast | grid PDE solver, but no pointer input; background only |
| iamtechartist/ocean-simulation (MIT) | not cloned (listed only) | FFT/JONSWAP ocean | same family as Ultra Water's cascades |

## 2. How the effect is really built, in plain terms

### Ultra Water (the article)
- **It is not a pointer-driven simulation.** The ocean is 4 Tessendorf FFT cascades (600/85/12/2.1 m tiles, 256² each,
  Stockham IFFT, JONSWAP spectrum, ω quantised so the whole sea loops every 300 s). It never stops and never "calms";
  the README lists *"no wakes behind moving objects"* as not implemented.
- **The only dynamic disturbance is `impactWaves`** (src/water/OceanSurface.js 179–199): up to 8 impact slots
  (x, z, age, amp) fed from floaters hitting the water. Each ring is a single stationary-phase term, deep water,
  gravity only: k = g·t²/(4r²), amplitude ∝ (kL)²·exp(−(kL)² − k²/kMax² − 0.12·t)·L/(L+r), height = amp·cos(k·r),
  slope from the same term. kMax = what the pixel/mesh can resolve (band-limit = no aliasing). One cos per ring per
  pixel, no table, no state.
- **Normals / roughness**: slopes come from the cascades; sub-pixel slope *variance* (LEAN-style: E[s²] − E[s]² from
  mipmapped slope + slope² textures) is added to GGX α, plus Kaplanyan geometric specular AA. That is what keeps the far
  field from sparkling/moiré: detail that cannot be drawn becomes roughness instead of aliasing.
- **Reflection / refraction**: Fresnel with roughness-aware F90 (Lagarde), planar reflection at 0.5 res (0.35 mobile),
  sky; refraction of the opaque scene by the slope; Beer–Lambert absorption by depth; GGX transmission lobe for the sun.
- **Caustics**: Evan Wallace's area-ratio splat — a grid refracted through the (cubic B-spline filtered) 12 m cascade
  slopes onto 3 depth planes, each landed triangle adds old/new area (mean exactly 1), MSAA so thin fold slivers
  don't break into dots, blur sized by the sun disc per depth.
- **Perf**: fixed per-frame cost (IFFT is ~constant); mobile profile = 0.6 resolution, 2× MSAA, no bloom,
  auto-resolution stepping down over 2 s windows to hold 60 fps; when the tab is hidden rAF stops. No calm-sleep
  (the sea is always moving).

### Evan Wallace webgl-water (what "interactive water" actually is)
- **State**: one 256² float (or half-float) texture, RGBA = (height, vertical velocity, normal.x, normal.z),
  ping-ponged between two textures.
- **Update (wave equation)**, 2 steps per frame, 5 taps: v += (avg of 4 neighbours − h)·2.0; v *= 0.995; h += v.
  That is a discrete wave equation at the grid's maximum stable speed with exponential damping; 0.995/step ≈ 1.15 s amplitude
  half-life at 2 steps × 60 fps.
- **Disturbance**: `addDrop(x, y, radius 0.03, strength ±0.01)` = add a raised-cosine bump (0.5 − 0.5·cos(π·(1 − d/r)))
  to height. **Dragging just calls addDrop at every mousemove** — the wake is the *sum* of all those stamps, each
  propagating from where and when it was made. A moving sphere adds the volume it vacated and subtracts the volume it
  now occupies (displacement source). Walls reflect for free (clamped texture edge).
- **Normals**: finite differences of height in a separate tiny pass.
- **Render**: ray-traced pool; refraction (IOR 1.333), reflection, Fresnel mix(0.5,1,(1−cosθ)³), caustics by area
  ratio of a refracted mesh (the same method Ultra Water and ink-fish use).
- **Calm**: it does not sleep either; space bar pauses.

### Coastal-simulation (techartist)
- Conservative staggered-grid shallow-water solver (pressure gradients drive face fluxes, wetting/drying), stepped in
  a worker / WebGPU. Physically right for a shoreline at metre scale, overkill for a page pond; no pointer coupling.

## 3. What our versions do (from source)
- v1.3.0: analytic Cauchy–Poisson rings: a Bessel J0 table (NK 192 × NR 512) integrated over wavenumber with
  capillary-gravity dispersion ω² = gk + (σ/ρ)k³, ×6 viscosity, everything slowed to 0.22×. Up to 8 ring slots, ambient
  = a dozen plane waves, area-ratio caustics, refraction of fish + shadow, Beer–Lambert, Fresnel sky.
- v1.3.1: + press-and-drag **trail** as a 1-D line impulse: per pixel, loop over up to 64 polyline segments, keep the
  **nearest** one, look up its age in a second table, draw that profile at that distance.
- v1.4 (1f29c12): real-time (no slow-mo), clean-water viscosity, NR 1024, speed-gated wake (none below c_min),
  dimple + meniscus under the finger, lift-off packet, crest slivers from the Laplacian, hand-built "V wavelets" inside
  the wedge (log-phase cos terms), per-theme wavelet gain, dark-only leading-crest masks (ri+45..ri+95), ring sink τ.
- All three: the sim is an *evaluation of closed-form profiles*, never a stepped field. There is no memory of
  water state between frames other than the list of sources.

## 4. Where v1.4 diverged — gap table
| # | aspect | article / references | v1.4 | verdict |
|---|---|---|---|---|
| 1 | what "dynamic" means | Evan: a stepped field; every input is a source; everything superposes, interferes, reflects | closed-form profiles for a list of sources | **different method** — ours can only show what we wrote a formula for |
| 2 | point disturbance (press / release) | UW: 1 stationary-phase cos per ring, band-limited by kMax; Evan: raised-cosine drop | full wavenumber-summed J0 table with capillary dispersion | **kept, correct, more physical than UW**; heavier than needed but cost is fine (8 slots) |
| 3 | moving disturbance (drag) | Evan: wake = *sum* of all stamps along the path, each with its own age (Green's function convolution) — the V, the diverging wavelets and the transverse waves all emerge | *nearest* polyline segment only, 1-D line profile at that distance → crests are offset copies of the stroke ("drawn" V), then hand-made V wavelets layered in | **implemented wrongly** — root cause of the "two clean lines" look (compare-evanw-vs-v14.png, row 2–3 col 3) and of most r10–r13 tuning |
| 4 | interference / overlap | free in a field (sum) | rings sum, trail does not (min distance), wavelets are separate terms | wrong for trails |
| 5 | boundaries | Evan: walls reflect; UW: shore breakers (eikonal) | none (open page) | fine for a page — not a gap |
| 6 | band-limit / anti-aliasing | UW: kMax per pixel + LEAN variance → unresolved detail becomes roughness | WAVELET/SRC constants, B-spline caustics; dark slivers fought with masks/gains | **never implemented** — the dark "busyness/moiré" problem is the aliasing UW solves with kMax + variance |
| 7 | dark theme | UW has no dark UI theme; night is just low sun: same shader, the *reflection* carries the image (sky/sun glints), not added lines | dark-only sliver accumulator, leading-crest mask Q, per-theme gains | **our own invention**; diverged from the method (should be reflection of a dark sky with sparse glints) |
| 8 | normals | finite differences of a height field (Evan) / analytic slopes + variance (UW) | analytic slope from the table (good) | kept |
| 9 | refraction / Fresnel / Beer–Lambert | UW, Evan | implemented | kept |
| 10 | caustics | Evan area-ratio, B-spline slope, MSAA splat | implemented (no MSAA; penumbra blur) | kept; MSAA optional |
| 11 | perf: calm | neither ref sleeps (ocean / pool always on) | sim pass skipped when nothing moves, rAF pause on hidden | **ours is better** — keep |
| 12 | perf: low-end | UW: 0.6 res, 2× MSAA, no bloom, auto-resolution | adaptive judge + 2-D fallback | kept; UW's auto-resolution ladder is worth copying |
| 13 | scale | UW metres; Evan unitless | cm-scale pond, capillary band (σ/ρ = 7.4e-5 from UW's capillary cascade) | kept |

## 5. Recommended next version (v1.5) — keep / replace
**Keep**: optics (refraction of fish + shadow by slope, Beer–Lambert, Fresnel sky), area-ratio caustics, analytic
press/release rings (8 slots, J0 table), calm-skip and hidden-pause, adaptive judge + 2-D fallback, ambient swell.

**Replace the trail + V wavelets + dark masks with a small stepped height field (Evan's method), driven by the pointer:**
1. Field: RG16F ping-pong (h, v) at 1/4 CSS px (1440×900 → 360×225 = 81k cells; 390×844 → ~98×211), only allocated
   when real water is on. Update 2 sub-steps/frame, 5 taps: v += c²·(avg4 − h); v *= damping; h += v.
2. Dispersion that reads as water at cm scale (Evan's field is non-dispersive): add a cheap capillary term
   v −= β·∇⁴h (13-tap biharmonic, or a second 5-tap pass on the Laplacian) so short waves run ahead and the wedge
   angle becomes speed-dependent. Tune c and β so the field's minimum phase speed sits near the current c_min
   (23 cm/s ≈ 390 px/s) — this replaces the hand speed gate. Alternative if β is unstable: Tessendorf iWave
   (precomputed 7×7 dispersion kernel; 49 taps, ~5× the cost).
3. Sources: stamp a raised-cosine dimple at sub-steps along the pointer segment each frame (spacing ≤ radius/2 so
   fast flicks don't bead) — the V, its diverging wavelets and the transverse crests then *emerge*; the dimple under
   the finger is the stamp itself. Fish can stamp tiny displacements too (optional, later).
4. Composite: slope = analytic ring slope (existing) + finite-difference field slope (bilinear/B-spline upsampled);
   everything downstream (refraction, caustics, Fresnel) unchanged.
5. Dark: drop the sliver accumulator/masks; dark = reflection of a dark sky with a soft key light, glint width from
   slope variance (UW's LEAN idea: store h and h² mip, fold the variance into the highlight width) — fixes moiré at
   the source instead of masking crests.
6. Band-limit: clamp stamp radius ≥ 2 cells and fade the field's slope by a kMax term at the composite resolution.

**Perf under the hard gate** (no regression vs v1.3.1; median-of-3 interleaved as perf.md):
- Removed: per-pixel 64-segment nearest-distance loop + trail table fetch + wavelet terms at SIM 0.5
  (1440×900 → 324k px × up to 64 segments ≈ 20M ALU iterations/frame while dragging).
- Added: 81k cells × 2 steps × 5–13 taps ≈ 0.8–2.1M texel fetches + one normal/upsample fetch per composite pixel.
  Expected: net **cheaper while dragging**, ≈ neutral idle (field not stepped when calm). *Not measured yet* — the
  first v1.5 step must be a standalone prototype timed with perfx.
- Sleep: CPU tracks the last stamp time; after T where A₀·damping^(steps) < 1/255 of display (≈1.5–2 s) stop stepping
  and clear the field (no GPU readback). Hidden: existing rAF pause. Calm idle = exactly today's cost.
- Low-end: field at 1/8 res (~20k cells), 1 sub-step, no biharmonic; if the adaptive judge still fails → v1.3.1-style
  analytic trail, then 2-D fallback. Add UW's auto-resolution ladder (0.6 → 0.5 → 0.4 of SIM) before falling back.

## 6. Captures in this folder
- evanw-top-press-drag.mp4, evanw-oblique-press-drag.mp4 (3 s, 30 fps deterministic, SwiftShader): press 0.3 s, then
  drag ~560 px/s, lift. evw-top-sheet.png, evw-oblique-sheet.png. Script: evw.py (served on 127.0.0.1:18761, stopped).
- compare-evanw-vs-v14.png: evanw field (press / drag / after) vs v1.4 light and dark (press 1.0 s, slow 3.0 s,
  fast V 6.6 s, frames from qa/demo-r10/after-*.mp4).
- uw-light-ish-lagoon.png, uw-dark-ish-golden-hour.png (Ultra Water stills, perf HUD visible in these two),
  uw-flotsam-impacts.mp4 + uw-flotsam-sheet.png (floaters already afloat: little impact visible; the FPS counter
  reads the faked clock, not real perf), uw-crate-drop-impact.mp4 + uw-crate-drop-sheet.png (a crate dropped from 4 m: the splash and impact ring read only faintly over the FFT sea at this size; even in UW the impact ring is a subtle accent, not the main look).
  Scripts: uw.py, uw_drop.py (vite on 127.0.0.1:15199, stopped).
- Limitations: SwiftShader only, no GPU; Ultra Water is a 3-D ocean so there is no "press/drag" to capture there —
  its interactive analogue is the floater impact ring. Evan's demo has no dark theme; "dark-ish" for UW = golden hour.
