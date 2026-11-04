# v1.5-gridwake look scores (renders at 0416d43, same rubric as qa/demo-r9/scores.md)

Judged from sbs-light.mp4, sbs-dark.mp4 (v1.3.1 | v1.5, same deterministic combo: press, slow 200 px/s drag, lift, 1250 px/s flick, lift), still-3way.png (v1.3.1 | v1.5 | webgl-water at t = 6.6 s) and probe/ crops.

| criterion | r12 (v1.4) | v1.5 | why |
|---|---|---|---|
| water-likeness (light) | 8 | 7.5 | The wake is now a simulated field: it refracts and casts caustics like the rings. But it reads as two smooth soft lines. Next to webgl-water it lacks the dense crossing ripple texture behind the pointer. |
| crest packets (press / lift / hover) | 8 | 8 | Unchanged (closed-form rings kept). |
| fast V | 7.5 | 7.5 | Clean, unbeaded and narrow (about 12° at 1250 px/s), with a sharp tip at the pointer. The inside of the wedge is smooth: no fine divergent crests. Short ripples leading is barely visible at this gain. |
| dimple (light) | 7.5 | 7.5 | Unchanged. |
| dimple (dark) | 8 | 8 | Unchanged crescent and soft core. |
| dark theme, reflection-led | 7.5 | 6.5 | The masks are gone and calm water stays clean (no ambient glint blotches at rest). But the result is too dim: the press and lift rings are barely visible, the V shows as one brighter glint arm plus a faint second arm, and v1.4's crest slivers are not replaced by anything of similar presence. |
| motion / timing | 8 | 8 | A slow drag carries only its dent (no wake, as designed). The flick's V detaches immediately. The field fades from 1.5 to 2 s after the lift, then stops stepping. No onset pop, thanks to the 0.12 s pressure ramp. |
| restraint / page fit | 8 | 8.5 | Dark is calmer than v1.4. Idle is untouched. |
| **average** | **7.81** | **7.69** | **Gate not met** (needs avg ≥ 8 and none < 7): dark reflections is 6.5 and the average is 7.69. |
