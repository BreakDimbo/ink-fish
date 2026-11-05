#!/bin/sh
# r14 step-3 renders of the new build after the perf pass (live and promo-build renders from render.sh are unchanged)
cd /workspace/ink-fish-r14/qa/demo-r14
for s in s10_peak_light s09_peak_dark; do
  SHOTSPY=$PWD/r14shots.py OUTDIR=$PWD/stage/new HOSTPORT=127.0.0.1:8861 NMAX=40 python3 -u promocap.py $s > log-stage-new-$s.txt 2>&1 &
done
for t in light dark; do
  python3 -u drag.py http://127.0.0.1:8861/ink-fish/index.html $t click-new-$t jclick 240 > log-click-new-$t.txt 2>&1 &
  python3 -u drag.py http://127.0.0.1:8861/ink-fish/index.html $t drag-new-$t combo 300 > log-drag-new-$t.txt 2>&1 &
done; wait; echo RENDERDONE
