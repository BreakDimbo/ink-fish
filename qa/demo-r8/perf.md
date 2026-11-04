# v1.3.2 vs v1.3.1 — CPU-side (perf.py from r7, interleaved, SwiftShader, loaded box; perf.json / perf.log)
Library ms/frame (forced real): 1440 1× scroll 10.65→10.47, cursor 11.10→10.78; 1440 4× scroll 49.0/43.7→50.6/45.1 (+3 %), cursor 47.5→47.8;
390 1× scroll 2.99→2.89, cursor 2.75→3.32 (+21 %, single run, noise: 4× cursor 13.2→13.1); 390 4× scroll 13.7→13.7.
Flat lib ms: unchanged (0.38–2.84 vs 0.43–2.83). Adaptive 1440: both fall back, late % 6.4→6.7 (1×), 16.4/21.6→22.8/15.5 (4×).
Outlier: 390 4× scroll adaptive — v1.3.1 fell back inside the run window, v1.3.2 had not yet (judge timing; forced real is identical 45.6 vs 46.8 ms).
Profile pass: per-frame ring rows gone; one-time table build (8 frames × 48 rows), trail adds 0 profile px (v1.3.1: +5,000 px/frame while dragging).
Trail (perftrail, 1440 DPR1, 2 reps): v1.3.1 hover 114.6/115.6, drag 150.0/129.5 ms; v1.3.2 hover 114.7/113.8, drag 117.7/127.4 ms.
Functional: adaptive→fallback ok; reduced motion flat, no trail; setOptions/theme/destroy ok; no-WebGL fallback ok; touch trail with pan-y ok, vertical swipe scrolls; trail:false 0 pts; ripples:false 0 pts; flat trail 30 pts; 0 page errors.
