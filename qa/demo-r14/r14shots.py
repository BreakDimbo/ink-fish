# r14 shots: the promo's own shot definitions plus variants (imported from inkfish-promo/scripts/shots.py, unchanged)
import importlib.util, math
spec = importlib.util.spec_from_file_location("pshots", "/workspace/inkfish-promo/scripts/shots.py")
P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
SHOTS = dict(P.SHOTS)
# s02 with the pointer parked on the click spot from the start: the click alone, no hover ring from the jump
SHOTS["s02_parked"] = dict(P.SHOTS["s02_ring_light"], path=P.ring(2.0, 600, 292, (600, 292)))
# s08 (dark wide, the promo's last ring), parked variant
SHOTS["s08_parked"] = dict(P.SHOTS["s08_wide_dark"], path=P.ring(4.5, 860, 330, (860, 330)))
