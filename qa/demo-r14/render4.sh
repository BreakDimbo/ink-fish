#!/bin/sh
# r14: re-render what the distance-aware ease-on (GRID_OND) touches: drags and drag starts (clicks and holds have no stroke)
cd /workspace/ink-fish-r14/qa/demo-r14
NR='["pring: 0.11", "pring: 0"], ["pring: 0.14", "pring: 0"], ["CLK_S = 1.46, CLK_S_DRAG = 0.55", "CLK_S = 0, CLK_S_DRAG = 0"]'
for s in s10_peak_light s09_peak_dark; do
  SHOTSPY=$PWD/r14shots.py OUTDIR=$PWD/stage/new HOSTPORT=127.0.0.1:8861 NMAX=40 python3 -u promocap.py $s > log-stage-new-$s.txt 2>&1 &
done
for t in light dark; do
  python3 -u drag.py http://127.0.0.1:8861/ink-fish/index.html $t drag-new-$t combo 300 > log-drag-new-$t.txt 2>&1 &
done
PATCHJS="[$NR]" python3 -u drag.py http://127.0.0.1:8861/ink-fish/index.html light drag-newease-light combo 300 > log-drag-newease-light.txt 2>&1 &
wait; echo RENDERDONE
