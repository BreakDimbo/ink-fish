# v1.4 look scores (HEAD renders, judged by eye against qa/research-real-water)

Judged from side-by-side.mp4, side-by-side-dark.mp4, gap-v14.png, closeup-*-200.png and the wake-sweep frames.

| criterion | score | notes |
|---|---|---|
| water-likeness (light) | 8 | packets read as real capillary–gravity rings: fine fast front, coarser back, calm centre growing at ≈ cg,min |
| crest packets (press / lift / hover) | 8 | 9–20 crests (front 7 px, back 22–35 px); no fill-in rings now that the k-grid mirror is fixed |
| fast V | 7.5 | thin arms that narrow with speed (12° at 1200 px/s by slope fit) with a few parallel fine crests; the near-field arm starts ~30 px wide, and the inside of the V is calm rather than holding divergent wavelets |
| dimple (light) | 7.5 | thin bright meniscus rim, soft grey core; the floor-shadow offset is hard to see |
| dimple (dark) | 6 | reads as a thin grey circle outline (a drawn ring) rather than sky slivers on a meniscus |
| dark theme, reflection-led | 6.5 | thin cool slivers on the fine front (3–4 px, no glow), but the back crests are broad (~8 px) and dull, and late packets almost vanish |
| motion / timing | 7.5 | continuous speed response; the stray 5 s ring is gone; packets stay visible 1.8 s (target 1–1.5); the hover train weakens at 2400 px/s |
| restraint / page fit | 8.5 | quiet idle, no clipping in light |
| **average** | **7.4** | **gate not met**: dark dimple 6 and dark reflections 6.5 are below 7; water-likeness is 8 (light) |

## Round 11 re-score (2026-11-04 ~16:35 SGT, renders at 90b022c/8535a3c)
| criterion | prev | now | why |
|---|---|---|---|
| water-likeness (light) | 8 | 8 | unchanged look; packets now fade out by ~1.5 s |
| crest packets | 8 | 8 | calm-centre edge 311 px/s (≤ 320) |
| fast V | 7.5 | 7.5 | arms crisp at ~12°, but the inside of the V is still smooth in light (no fine divergent crests yet) |
| dimple (light) | 7.5 | 7.5 | unchanged |
| dimple (dark) | 6 | 7.5 | thin sky crescent on the far side of the light plus a darker soft core; a faint full outline is still visible |
| dark reflections | 6.5 | 7.5 | crest slivers come from phase (curvature vs slope), so back crests stay thin and late packets glint faintly; slivers bead a little where the ambient swell tilts them |
| motion | 7.5 | 8 | hover wake at 2400 px/s is now stronger than at 1800 (7.00 vs 5.76 mean dL); visible 1.5 s |
| restraint | 8.5 | 8.5 | |
| **average** | 7.4 | **7.81** | gate (≥ 8, none < 7): the "none < 7" part passes; the average misses by 0.19 |

## Round 12 re-score (2026-11-04 ~16:55 SGT, renders at 6c6214f)
| criterion | r11 | r12 | why |
|---|---|---|---|
| water-likeness (light) | 8 | 8 | |
| crest packets | 8 | 8 | |
| fast V | 7.5 | 7.5 | Inside the wedge there are now fine diagonal wavelets, fine at the tip and coarser downstream. In dark they show, but they cross the stroke-start ring arcs into a hatch rather than clean divergent crests. In light they are barely visible. |
| dimple (light) | 7.5 | 7.5 | |
| dimple (dark) | 7.5 | 8 | The full outline is gone: just the sky crescent and the soft dark core. |
| dark reflections | 7.5 | 7.5 | No more beading on the swell tilt (the sliver phase is now computed in the sim against the disturbance slope only). Crests are a little uniform and wider, and a faint moiré shows in the calm centre. |
| motion | 8 | 8 | |
| restraint | 8.5 | 8 | Dark is busier: more of the packet reads. |
| **average** | 7.81 | **7.81** | Nothing scores below 7, but the average misses the ≥ 8 gate. |

## Round 13 re-score (2026-11-04 ~18:15 SGT, renders at 2f15a3f, qa/demo-r10)
| criterion | r12 | r13 | why |
|---|---|---|---|
| water-likeness (light) | 8 | 8 | unchanged |
| crest packets | 8 | 8 | Light unchanged (calm edge 311 px/s, 1.5 s). Dark now shows only the leading crests of each packet. |
| fast V | 7.5 | 8 | Light: the inside of the wedge now holds visible fine chevron crests (span 13 → 18 levels), fine at the tip and coarser downstream, still restrained. Dark: a faint chevron fill and no more hatching (start-arc rings sink in ~0.6 s and only their leading crests show). Flaws: in light the chevrons still meet the start arcs at the far left; in dark a few beaded dots inside the wedge. |
| dimple (light) | 7.5 | 7.5 | unchanged |
| dimple (dark) | 8 | 8 | unchanged, clean crescent |
| dark reflections | 7.5 | 8 | Busyness −69 % mean / −73 % peak. Thin leading slivers only, with width and brightness varied along the crest; no moiré in the calm centre (it is masked out now). Flaws: the release packet goes very faint by 0.5 s (maybe slightly under-stated against the strider reference), and the finest front crests break into short dashes. |
| motion | 8 | 8 | |
| restraint | 8 | 8.5 | dark is calm again |
| **average** | 7.81 | **8.0** | Gate met (≥ 8, nothing < 7), but only just: the light dimple at 7.5 is the weakest item |
