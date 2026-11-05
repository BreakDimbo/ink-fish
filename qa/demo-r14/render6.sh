#!/bin/sh
# r14 perf step A check: after the composite split, re-render the parked clicks and the drag (light+dark) as *A, to diff
cd /workspace/ink-fish-r14/qa/demo-r14
for t in light dark; do
  NOVIDEO=1 python3 -u drag.py http://127.0.0.1:8861/ink-fish/index.html $t pclickA-new-$t click 240 > log-pclickA-new-$t.txt 2>&1 &
  NOVIDEO=1 python3 -u drag.py http://127.0.0.1:8861/ink-fish/index.html $t dragA-new-$t combo 300 > log-dragA-new-$t.txt 2>&1 &
done; wait; echo RENDERDONE
