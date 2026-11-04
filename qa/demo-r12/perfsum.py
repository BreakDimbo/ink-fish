# perf gate table from a perfx log: perfsum.py LOG TITLE OUT.md
import json, statistics as st, collections, sys
log, title, out = sys.argv[1:4]
C = collections.defaultdict(list)
for l in open(log):
    if l.startswith('{'):
        r = json.loads(l); C[(r['size'], r['cpu'], r['mode'], r['build'])].append(r)
o = [f"# {title}", "", "Gate: median library ms/frame (interleaved, 3 reps, headless Chrome/SwiftShader); pass if Δmedian ≤ max(v1.3.1 spread/2, 5 %). Frame interval (median of per-run means) shown too: the gate metric misses GPU cost.", "",
     "| case | mode | v1.3.1 lib ms (runs) | v1.5 lib ms (runs) | Δ | allowance | gate | frame interval v1.3.1 → v1.5 ms (Δ) | grid cell-steps/frame |", "|---|---|---|---|---|---|---|---|---|"]
ok_all = True; errs = 0
for size, cpu in ((1440, 1), (390, 4)):
    for mode in ('idle', 'drag'):
        for m in ('forced', 'adaptive'):
            a = C[(size, cpu, mode, f'v1.3.1 real ({m})')]; b = C[(size, cpu, mode, f'v1.5 real ({m})')]
            if not a or not b: continue
            errs += sum(len(r['errs']) for r in a + b)
            va = [r['lib'] for r in a]; vb = [r['lib'] for r in b]; ma, mb = st.median(va), st.median(vb)
            al = max((max(va) - min(va)) / 2, 0.05 * ma); d = mb - ma; ok = d <= al; ok_all &= ok
            ia = st.median([r['mean'] for r in a]); ib = st.median([r['mean'] for r in b])
            o.append(f"| {size} {cpu}× {mode} | {m} ({a[0]['water']}) | {ma:.3f} ({', '.join('%.2f' % x for x in va)}) | {mb:.3f} ({', '.join('%.2f' % x for x in vb)}) | {d:+.3f} ({d / ma * 100:+.1f} %) | {al:.3f} | {'PASS' if ok else 'FAIL'} | {ia:.1f} → {ib:.1f} ({(ib - ia) / ia * 100:+.1f} %) | {st.median([(r['gw'] or {}).get('grid', 0) for r in b]):,.0f} |")
o += ["", f"**Overall: {'PASS' if ok_all else 'FAIL'}**; page/console errors: {errs}."]
open(out, 'w').write("\n".join(o) + "\n"); print("\n".join(o))
