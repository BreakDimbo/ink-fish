#!/bin/sh
# r14 step-3 renders. Servers: 8841 = v1.3.1 (promo build), 8842 = live v1.5.1, 8861 = new (this worktree)
cd /workspace/ink-fish-r14/qa/demo-r14
B="v131:8841 v151:8842 new:8861"
# batch 1: promo-stage drag starts (first 40 frames = 1.3 s; the press is at f9) for live and new
for s in s10_peak_light s09_peak_dark; do for b in v151:8842 new:8861; do n=${b%%:*}; p=${b#*:}
  SHOTSPY=$PWD/r14shots.py OUTDIR=$PWD/stage/$n HOSTPORT=127.0.0.1:$p NMAX=40 python3 -u promocap.py $s > log-stage-$n-$s.txt 2>&1 &
done; done
# clicks (jump onto the spot and click, as in the film; then a 1 s hold) on the three builds, light
for b in $B; do n=${b%%:*}; p=${b#*:}
  python3 -u drag.py http://127.0.0.1:$p/ink-fish/index.html light click-$n-light jclick 240 > log-click-$n-light.txt 2>&1 &
done; wait; echo batch1
for b in $B; do n=${b%%:*}; p=${b#*:}
  python3 -u drag.py http://127.0.0.1:$p/ink-fish/index.html dark click-$n-dark jclick 240 > log-click-$n-dark.txt 2>&1 &
done
for t in light dark; do for b in v151:8842 new:8861; do n=${b%%:*}; p=${b#*:}
  python3 -u drag.py http://127.0.0.1:$p/ink-fish/index.html $t drag-$n-$t combo 300 > log-drag-$n-$t.txt 2>&1 &
done; done; wait; echo RENDERDONE
