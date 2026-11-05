# r15 · ring radius vs real time: film, live v1.5.2, v1.5.3, and the physics of a real pond
import json, sys, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
D = 'data/'
def L(n):
    r = json.load(open(D + n))['rows']; t = np.array([x['t'] for x in r]); return t, r
def ser(n, key, amin=0.0, tmax=9):
    t, r = L(n); a = np.array([x['amp'] for x in r]); v = np.array([x[key] for x in r], float)
    m = (a > amin) & (v > 0) & (t > 0.05) & (t < tmax); return t[m], v[m], a
ph = json.load(open(D + 'physics.json')); tb = ph['textbook']
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
fig, (ax, bx) = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw={'width_ratios': [1.6, 1]})
T = np.linspace(0, 4, 50)
# physics band: koi 30-45 cm -> 4.0-2.7 CSS px/cm (1440 px desktop)
for ppc, a in ((4.0, .16), (2.7, .08)):
    ax.fill_between(T, tb['cgmin_cm_s'] * ppc * T, tb['cmin_cm_s'] * ppc * T, color='#3a7ca5', alpha=a, lw=0)
ax.plot(T, tb['cgmin_cm_s'] * 4 * T, color='#3a7ca5', lw=1, ls=':', label='real pond, koi = 30 cm: calm centre at $c_{g,min}$ 17.8 cm/s = 71 px/s')
ax.plot(T, tb['cmin_cm_s'] * 4 * T, color='#3a7ca5', lw=1, ls='-.', label='real pond: leading ripples at $c_{min}$ 23.2 cm/s = 93 px/s (koi 45 cm: paler band)')
S = [('promo-s02-light.json', 'film s02 (light)', '#111', 'o'), ('promo-s08-dark.json', 'film s08 (dark)', '#777', 's'),
     ('s152-jclick-light.json', 'live v1.5.2', '#c0392b', '^'), ('s153-jclick-light.json', 'v1.5.3', '#27ae60', 'D')]
for n, lab, c, mk in S:
    try:
        t, v, a = ser(n, 'crest', 0.25, 3.6); ax.plot(t, v, mk, ms=3.2, color=c, label=lab + ' - brightest crest', alpha=.9)
        t2, v2, _ = ser(n, 'lead', 0.25, 3.6); ax.plot(t2, v2, '-', lw=1, color=c, alpha=.55)
        tt, rr = L(n); aa = np.array([x['amp'] for x in rr]); m = tt > 0
        bx.plot(tt[m], aa[m] / max(1e-9, aa[m & (tt > .25) & (tt < .8)].max()) if 'promo' in n else aa[m] / max(1e-9, aa[m & (tt > .25) & (tt < .8)].max()), color=c, lw=1.2, label=lab)
    except FileNotFoundError: print('missing', n)
ax.set_xlim(0, 3.6); ax.set_ylim(0, 720); ax.set_xlabel('seconds after the tap (real time)'); ax.set_ylabel('ring radius, CSS px at 1440 x 900')
ax.set_title('How fast a tap spreads   (dots = crest, thin line = outermost visible ripple)', fontsize=10.5, loc='left')
ax.legend(fontsize=7.6, loc='upper left', frameon=False)
bx.set_xlim(0, 4); bx.set_ylim(0, 1.6); bx.set_xlabel('seconds after the tap'); bx.set_ylabel('ring contrast vs its own 0.25-0.8 s peak')
bx.set_title('How long it stays', fontsize=10.5, loc='left'); bx.legend(fontsize=8, frameon=False)
for a in (ax, bx):
    for s in ('top', 'right'): a.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig('ring-radius-vs-time.png', dpi=150); print('ok')
