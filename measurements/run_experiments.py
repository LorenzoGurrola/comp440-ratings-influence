"""Experiments 4a-4e.  Everything at 1000 worlds, 1000 users, seed 20260922."""
import json, time
import numpy as np
import sim

SEED = 20260922
W, U = 1000, 1000
OUT = {}
t_start = time.perf_counter()

def run(tag, **kw):
    kw.setdefault('num_worlds', W); kw.setdefault('num_users', U); kw.setdefault('seed', SEED)
    t = time.perf_counter()
    res = sim.simulate(**kw)
    m = sim.measure(res)
    m['params'] = {k: v for k, v in res['params'].items()}
    m['seconds'] = time.perf_counter() - t
    print('%-34s gini %.3f  unpred %.4f  rho %.3f  beatles#1 %.3f  acc %.3f  (%.1fs)'
          % (tag, m['gini_mean'], m['unpred'], m['spearman_mean'],
             m['beatles_first'], m['accidental_hit'], m['seconds']))
    return res, m

# 4a: social influence sweep, simple_rec_alg
OUT['4a'] = {}
sweep_res = {}
for si in (0.0, 0.25, 0.5, 0.75, 0.9, 1.0):
    r, m = run(f'4a si={si}', social_influence=si, policy='simple')
    OUT['4a'][str(si)] = m
    sweep_res[si] = r

# 4b: independent-world control
_, m = run('4b si=0 random-5', social_influence=0.0, policy='random')
OUT['4b'] = {'random5_si0': m, 'simple_si0': OUT['4a']['0.0']}

# 4c: presentation order at si=0.5
OUT['4c'] = {}
for b in (1.0, 1.2, 1.5):
    _, m = run(f'4c base={b}', social_influence=0.5, policy='simple', base=b)
    OUT['4c'][str(b)] = m

# 4d: policies at si=0.5, base 1.2
OUT['4d'] = {}
for p in ('random', 'simple', 'damped', 'explore', 'shuffled'):
    _, m = run(f'4d policy={p}', social_influence=0.5, policy=p)
    OUT['4d'][p] = m

# 4e: scale
OUT['4e'] = {}
for nu in (50, 200, 1000):
    _, m = run(f'4e users={nu}', social_influence=0.5, policy='simple', num_users=nu)
    OUT['4e'][str(nu)] = m

OUT['meta'] = {'seed': SEED, 'num_worlds': W, 'num_users': U,
               'total_seconds': time.perf_counter() - t_start}

# data the figures need
np.savez_compressed('figdata.npz',
    shares_si05=sweep_res[0.5]['shares'],
    shares_si075=sweep_res[0.75]['shares'],
    shares_indep=sim.simulate(0.0, 'random', U, W, seed=SEED + 1)['shares'],
    traj_si075=sim.simulate(0.75, 'simple', U, 12, seed=SEED + 2, track_worlds=12)['traj'])

json.dump(OUT, open('results.json', 'w'), indent=1)
print('total %.1fs' % OUT['meta']['total_seconds'])
