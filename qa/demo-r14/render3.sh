#!/bin/sh
# r14 wake-isolation renders (combo drag): is the trailing wake code unchanged, and what does the 0.6 s ease-on change?
#   v151nopk  = live v1.5.1 with its press packet suppressed (no 0.25 s swap ring)
#   newbare   = v1.5.2 with the promo ring off (strength 0, fish nudge 0) and the ease-on off (GRID_ON → 1e-9)
#   newease   = v1.5.2 with the promo ring off, ease-on as shipped (0.6 s)
cd /workspace/ink-fish-r14/qa/demo-r14
PK='[["if (P.clk && addRipple(P.x0, P.y0, 1, true, P.clk.q))", "if (false)"]]'
NR='["pring: 0.11", "pring: 0"], ["pring: 0.14", "pring: 0"], ["CLK_S = 1.46, CLK_S_DRAG = 0.55", "CLK_S = 0, CLK_S_DRAG = 0"]'
for t in light dark; do
  PATCHJS="$PK" python3 -u drag.py http://127.0.0.1:8842/ink-fish/index.html $t drag-v151nopk-$t combo 300 > log-drag-v151nopk-$t.txt 2>&1 &
  PATCHJS="[$NR, [\"GRID_ON = 0.6\", \"GRID_ON = 1e-9\"]]" python3 -u drag.py http://127.0.0.1:8861/ink-fish/index.html $t drag-newbare-$t combo 300 > log-drag-newbare-$t.txt 2>&1 &
done
PATCHJS="[$NR]" python3 -u drag.py http://127.0.0.1:8861/ink-fish/index.html light drag-newease-light combo 300 > log-drag-newease-light.txt 2>&1 &
wait; echo RENDERDONE
