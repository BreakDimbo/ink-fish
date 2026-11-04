# perf.md from perf JSON-lines logs: mean and min–max of library ms/frame per case, v1.3.1 vs v1.4, interleaved runs
import json, sys, collections, statistics as st
files = sys.argv[1:]
C = collections.defaultdict(list)
for f in files:
    for l in open(f):
        l = l.strip()
        if not l.startswith("{"): continue
        try: r = json.loads(l)
        except Exception: continue
        if "error" in r: continue
        C[(r["size"], r["cpu"], r["mode"], r["build"])].append(r)
def agg(rs, k):
    v = [r[k] for r in rs]; return st.mean(v), min(v), max(v)
out = []
out.append("| width | CPU | case | build | n | lib ms/frame mean (min–max) | frame interval ms mean (min–max) | late % mean | water at end | GPU proxy sim px/frame | comp px/frame |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|")
verdict = []
for size in (1440, 390):
    for cpu in (1, 4):
        for mode in ("idle", "scroll", "cursor", "drag"):
            for kind in ("forced", "adaptive"):
                row = {}
                for ver in ("v1.3.1", "v1.4"):
                    b = f"{ver} real ({kind})"; rs = C.get((size, cpu, mode, b), [])
                    if not rs: out.append(f"| {size} | {cpu}× | {mode} | {b} | 0 | — | — | — | — | — | — |"); continue
                    m, lo, hi = agg(rs, "lib"); fm, flo, fhi = agg(rs, "mean"); la = st.mean(r["late"] for r in rs)
                    w = ",".join(sorted(set(r["water"] for r in rs)))
                    sim = st.mean(r["gw"]["sim"] for r in rs if r.get("gw")); comp = st.mean(r["gw"]["comp"] for r in rs if r.get("gw"))
                    out.append(f"| {size} | {cpu}× | {mode} | {b} | {len(rs)} | {m:.2f} ({lo:.2f}–{hi:.2f}) | {fm:.1f} ({flo:.1f}–{fhi:.1f}) | {la:.1f} | {w} | {sim:,.0f} | {comp:,.0f} |")
                    row[ver] = (m, lo, hi, fm, flo, fhi, len(rs), st.median(r["lib"] for r in rs), sorted(r["lib"] for r in rs))
                if len(row) == 2:
                    a, b = row["v1.3.1"], row["v1.4"]
                    # noise = the wider of the two run spreads; slower = v1.4 mean above v1.3.1 mean by more than that spread
                    # noise = the v1.3.1 run-to-run spread (its own min–max); gate on the median, so one hitched run (box load) can't
                    # pass or fail a case on its own; the mean is shown too
                    noise = a[2] - a[1]; d = b[7] - a[7]
                    ok = d <= max(noise / 2, 0.05 * a[7])
                    verdict.append((size, cpu, mode, kind, a[0], b[0], a[7], b[7], d / a[7] * 100, noise, ok, a[6], b[6], b[8]))
print("\n".join(out))
print()
print("| width | CPU | case | build | v1.3.1 mean / median | v1.4 mean / median | Δ median % | v1.3.1 spread (ms) | n | v1.4 runs | not slower |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for v in verdict:
    print(f"| {v[0]} | {v[1]}× | {v[2]} | {v[3]} | {v[4]:.2f} / {v[6]:.2f} | {v[5]:.2f} / {v[7]:.2f} | {v[8]:+.1f} | {v[9]:.2f} | {v[11]}/{v[12]} | {' '.join('%.2f' % x for x in v[13])} | {'yes' if v[10] else '**NO**'} |")
