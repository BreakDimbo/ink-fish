# r14 shots: the promo's own shot definitions plus variants (imported from inkfish-promo/scripts/shots.py, unchanged)
import importlib.util, math
spec = importlib.util.spec_from_file_location("pshots", "/workspace/inkfish-promo/scripts/shots.py")
P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
SHOTS = dict(P.SHOTS)
# s02 with the pointer parked on the click spot from the start: the click alone, no hover ring from the jump
SHOTS["s02_parked"] = dict(P.SHOTS["s02_ring_light"], path=P.ring(2.0, 600, 292, (600, 292)))
# s08 (dark wide, the promo's last ring), parked variant
SHOTS["s08_parked"] = dict(P.SHOTS["s08_wide_dark"], path=P.ring(4.5, 860, 330, (860, 330)))
# diagnostics: the new build with its promo ring turned off (what the stroke itself adds at the start)
SHOTS["s10_noring"] = dict(P.SHOTS["s10_peak_light"], patch=[("**/ink-fish/src/ink-fish.js*", [("pring: 0.11", "pring: 0")])])
for on in ("0.12", "0.35", "1.0"):
    SHOTS["s10_noring_on" + on] = dict(P.SHOTS["s10_peak_light"], patch=[("**/ink-fish/src/ink-fish.js*", [("pring: 0.11", "pring: 0"), ("GRID_ON = 0.6", "GRID_ON = " + on)])])
