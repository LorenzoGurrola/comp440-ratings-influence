"""Agreement between sim_original (pure Python) and sim (numpy), plus timings."""
import json, random, time
import numpy as np
import sim, sim_original as so

OUT = {}

# ---- timing: original, 100 worlds x 1000 users, simple_rec_alg, si=0.5
so.NUM_WORLDS, so.NUM_USERS = 100, 1000
random.seed(11)
t0 = time.perf_counter()
res100 = so.simulate_all_worlds(so.simple_rec_alg, 0.5, verbose=False)
t_orig_100 = time.perf_counter() - t0
OUT['orig_100x1000_sec'] = t_orig_100
OUT['orig_1000x1000_sec_extrapolated'] = t_orig_100 * 10

# ---- timing: fast port, same shape, and at 1000 worlds
t0 = time.perf_counter(); sim.simulate(0.5, 'simple', 1000, 100, seed=11); OUT['fast_100x1000_sec'] = time.perf_counter() - t0
t0 = time.perf_counter(); sim.simulate(0.5, 'simple', 1000, 1000, seed=11); OUT['fast_1000x1000_sec'] = time.perf_counter() - t0
t0 = time.perf_counter(); sim.simulate(0.5, 'simple', 1000, 300, seed=11); OUT['fast_300x1000_sec'] = time.perf_counter() - t0

# ---- agreement: 200 worlds each, si=0.5, simple_rec_alg
so.NUM_WORLDS, so.NUM_USERS = 200, 1000
random.seed(2024)
t0 = time.perf_counter()
ro = so.simulate_all_worlds(so.simple_rec_alg, 0.5, verbose=False)
OUT['orig_200x1000_sec'] = time.perf_counter() - t0
so_shares = sim.shares_from_original(ro)
mo = sim.measure({'shares': so_shares})

# several independent seeds of the fast port at 200 worlds, to show the
# original's numbers sit inside the fast port's own seed-to-seed spread
fast = [sim.measure(sim.simulate(0.5, 'simple', 1000, 200, seed=s)) for s in range(8)]
keys = ['gini_mean', 'leader_share_mean', 'beatles_share_mean', 'unpred',
        'spearman_mean', 'beatles_first', 'nonzero_artists_mean']
agree = {}
for k in keys:
    fv = np.array([f[k] for f in fast])
    agree[k] = {'original': mo[k], 'fast_mean': float(fv.mean()),
                'fast_sd_over_seeds': float(fv.std(ddof=1)),
                'fast_min': float(fv.min()), 'fast_max': float(fv.max()),
                'z': float((mo[k] - fv.mean()) / fv.std(ddof=1)) if fv.std(ddof=1) > 0 else 0.0}
OUT['agreement_200_worlds'] = agree
OUT['agreement_mean_shares'] = {
    'original': mo['mean_shares'],
    'fast_seed0': fast[0]['mean_shares'],
}

# ---- world-count stability: 5 seeds each at 100 / 300 / 1000 worlds
stab = {}
for W in (100, 300, 1000):
    runs = [sim.measure(sim.simulate(0.5, 'simple', 1000, W, seed=100 + s)) for s in range(5)]
    stab[W] = {k: {'mean': float(np.mean([r[k] for r in runs])),
                   'sd_over_seeds': float(np.std([r[k] for r in runs], ddof=1)),
                   'range': float(np.ptp([r[k] for r in runs]))}
               for k in ['gini_mean', 'unpred', 'spearman_mean', 'beatles_first',
                         'leader_share_mean', 'beatles_share_mean']}
OUT['stability'] = stab

json.dump(OUT, open('check_agreement.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in OUT.items() if k.endswith('sec') or k.endswith('extrapolated')}, indent=1))
print(json.dumps(agree, indent=1))
