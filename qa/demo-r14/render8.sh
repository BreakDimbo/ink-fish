#!/bin/sh
# r14 after d512d3f (a pure stroke lets its ring go): drag-start stage shots and the drags as *new2; the parked click as
# pclickC to confirm it is unchanged
cd /workspace/ink-fish-r14/qa/demo-r14
for s in s10_peak_light s09_peak_dark; do
  SHOTSPY=$PWD/r14shots.py OUTDIR=$PWD/stage/new2 HOSTPORT=127.0.0.1:8861 NMAX=40 python3 -u promocap.py $s > log-stage-new2-$s.txt 2>&1 &
done
for t in light dark; do
  python3 -u drag.py http://127.0.0.1:8861/ink-fish/index.html $t drag-new2-$t combo 300 > log-drag-new2-$t.txt 2>&1 &
  NOVIDEO=1 python3 -u drag.py http://127.0.0.1:8861/ink-fish/index.html $t pclickC-new-$t click 240 > log-pclickC-new-$t.txt 2>&1 &
done; wait; echo RENDERDONE
