#!/bin/sh
# r14 clicks with the pointer parked on the spot first (the r13 'click' path: no hover packet from a jump, which v1.5.x
# draws on its own and which is not the click). jclick renders are kept for reference
cd /workspace/ink-fish-r14/qa/demo-r14
for t in light dark; do for b in v131:8841 v151:8842 new:8861; do n=${b%%:*}; p=${b#*:}
  python3 -u drag.py http://127.0.0.1:$p/ink-fish/index.html $t pclick-$n-$t click 240 > log-pclick-$n-$t.txt 2>&1 &
done; done; wait; echo RENDERDONE
