#!/bin/sh
# r13 renders: clicks for v1.5.0 / v1.2.1 / v1.3.0 / new, drags for v1.5.0 / new; light + dark
cd /workspace/ink-fish/qa/demo-r13
U=http://127.0.0.1:8733
for t in light dark; do
  for b in v150:qa/demo-r13/v150/index.html v121:qa/demo-r13/v121/index.html v130:qa/demo-r13/v130/index.html new:index.html; do
    n=${b%%:*}; p=${b#*:}
    python3 -u drag.py $U/$p $t click-$n-$t click 180 > log-click-$n-$t.txt 2>&1; echo click $n $t $?
  done
  for b in v150:qa/demo-r13/v150/index.html new:index.html; do
    n=${b%%:*}; p=${b#*:}
    python3 -u drag.py $U/$p $t drag-$n-$t combo 300 > log-drag-$n-$t.txt 2>&1; echo drag $n $t $?
  done
done
echo RENDERDONE
