# qa/demo-r11 — v1.5-gridwake prototype (height-field drag wake)

- sbs-light.mp4, sbs-dark.mp4: v1.3.1 (left) | v1.5 at 0416d43 (right), 1920×600, 30 fps, combo script
- after-light.mp4, after-dark.mp4: v1.5 alone at 1440×900
- still-3way.png: v1.3.1 | v1.5 | webgl-water reference (Evan Wallace demo, drag frame), light and dark rows, t = 6.6 s
- perf.md (at 50f0b8c) and perf2.md (rerun at 0416d43): interleaved median-of-3 vs v1.3.1, 4 cases, forced + adaptive
- func.log/touch.log (50f0b8c+), func2.log/touch2.log (0416d43): all pass
- scores.md: look scores
- probe.py: slope stats + crops (QA hook: window.__inkFishGridGain, instance._peek()); probe/: calibration crops
- drag.py, perfx.py, perfreport.py, sbs.sh, still3.py, chain.sh: the scripts used
