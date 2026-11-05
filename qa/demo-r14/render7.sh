#!/bin/sh
# r14 perf step B check: composite scissored to the ring box, re-render the parked clicks and the drag (light+dark) as *A, to diff
cd /workspace/ink-fish-r14/qa/demo-r14
for t in light dark; do
  NOVIDEO=1 python3 -u drag.py http://127.0.0.1:8861/ink-fish/index.html $t pclickB-new-$t click 240 > log-pclickB-new-$t.txt 2>&1 &
  NOVIDEO=1 python3 -u drag.py http://127.0.0.1:8861/ink-fish/index.html $t dragB-new-$t combo 300 > log-dragB-new-$t.txt 2>&1 &
done; wait; echo RENDERDONE
