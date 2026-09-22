"""Figures 1-6.  Plain matplotlib (fig1 keeps the instructor's seaborn strip plot)."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import rankdata
import sim

R = json.load(open('results.json'))
D = np.load('figdata.npz')
A = sim.ALL_ARTISTS
TP = sim.TRUE_POP
order = np.argsort(-TP)                      # artists by true popularity, descending
true_share = TP / TP.sum()

# ---- fig1: the instructor's strip plot at si=0.5 -------------------------
sh = D['shares_si05']
labels = ['%s (%d)' % (A[i], TP[i]) for i in order]
sns.set_theme(style='whitegrid', rc={'figure.figsize': (12, 5)})
fig, ax = plt.subplots()
sns.stripplot(data={labels[j]: pd.Series(sh[:, i]) for j, i in enumerate(order)},
              edgecolor='black', linewidth=1.0, size=2, alpha=0.1, color='gray', ax=ax)
ax.plot(range(len(order)), true_share[order], marker='D', linestyle='none',
        color='red', markersize=7, label='true popularity share')
ax.set_xlabel('artist (true popularity)')
ax.set_ylabel('share of the 1000 downloads in a world')
ax.set_title('Market share per artist across 1000 worlds, social influence 0.5, top-5 recommender')
ax.legend(loc='upper right')
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
fig.tight_layout(); fig.savefig('fig1_strip.png', dpi=130); plt.close(fig)
sns.reset_defaults()
matplotlib.rcParams.update(matplotlib.rcParamsDefault)

si = [0.0, 0.25, 0.5, 0.75, 0.9, 1.0]
gini = [R['4a'][str(s)]['gini_mean'] for s in si]
gsd = [R['4a'][str(s)]['gini_sd'] for s in si]
unp = [R['4a'][str(s)]['unpred'] for s in si]
ctl = R['4b']['random5_si0']

# ---- fig2: Gini vs social influence --------------------------------------
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.errorbar(si, gini, yerr=gsd, marker='o', color='black', capsize=3,
            label='top-5 recommender (bars = s.d. across worlds)')
ax.plot([0], [ctl['gini_mean']], marker='s', color='red', linestyle='none',
        markersize=9, label='independent control: random-5, influence 0')
ax.axhline(sim.gini(true_share[None, :])[0], color='gray', linestyle='--', linewidth=1,
           label='Gini of the true popularity distribution')
ax.set_xlabel('social influence'); ax.set_ylabel('mean Gini of market shares')
ax.set_ylim(0, 1)
ax.set_title('Inequality rises with social influence; the recommender sets the floor')
ax.legend(fontsize=8); fig.tight_layout(); fig.savefig('fig2_gini_vs_si.png', dpi=130); plt.close(fig)

# ---- fig3: unpredictability vs social influence --------------------------
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(si, unp, marker='o', color='black', label='top-5 recommender')
ax.plot([0], [ctl['unpred']], marker='s', color='red', linestyle='none',
        markersize=9, label='independent control: random-5, influence 0')
ax.set_xlabel('social influence')
ax.set_ylabel('unpredictability U (mean pairwise |share difference|)')
ax.set_ylim(0, max(unp) * 1.15)
ax.set_title('Unpredictability rises with social influence')
ax.legend(fontsize=8); fig.tight_layout(); fig.savefig('fig3_unpred_vs_si.png', dpi=130); plt.close(fig)

# ---- fig4: quality vs success -------------------------------------------
ind = D['shares_indep'].mean(axis=0)            # independent condition, per artist
inf = D['shares_si075']                          # (W, A) influence worlds
x_sh = np.repeat(ind[None, :], inf.shape[0], axis=0)
ind_rank = rankdata(-ind)                        # 1 = best in the independent world
inf_rank = rankdata(-inf, axis=1)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
axes[0].plot(x_sh.ravel(), inf.ravel(), 'o', color='black', markersize=2, alpha=0.06)
axes[0].plot(ind, inf.mean(axis=0), 'D', color='red', markersize=6, label='mean over worlds')
axes[0].set_xlabel('market share in the independent condition (mean over worlds)')
axes[0].set_ylabel('market share in an influence world (influence 0.75)')
axes[0].set_title('Share'); axes[0].legend(fontsize=8)
axes[1].plot(np.repeat(ind_rank[None, :], inf.shape[0], axis=0).ravel() + np.random.default_rng(0).normal(0, .06, inf.size),
             inf_rank.ravel() + np.random.default_rng(1).normal(0, .06, inf.size),
             'o', color='black', markersize=2, alpha=0.05)
axes[1].plot(ind_rank, inf_rank.mean(axis=0), 'D', color='red', markersize=6, label='mean rank over worlds')
axes[1].set_xlabel('rank in the independent condition (1 = best)')
axes[1].set_ylabel('rank in an influence world (1 = best)')
axes[1].invert_xaxis(); axes[1].invert_yaxis()
axes[1].set_title('Rank (jittered)'); axes[1].legend(fontsize=8)
fig.suptitle('Independent-condition appeal vs outcome in each influence world, 11 artists x 1000 worlds')
fig.tight_layout(); fig.savefig('fig4_quality_vs_success.png', dpi=130); plt.close(fig)

# ---- fig5: trajectories ---------------------------------------------------
traj = D['traj_si075']                           # (12, U+1, A) cumulative counts
nW, steps, _ = traj.shape
t = np.arange(1, steps)
leaders = traj[:, -1, :].argmax(axis=1)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
for w in range(nW):
    axes[0].plot(t, traj[w, 1:, leaders[w]] / t, color='black', linewidth=0.8, alpha=0.6)
    axes[1].plot(t, traj[w, 1:, sim.BEATLES] / t, color='black', linewidth=0.8, alpha=0.6)
axes[0].set_title("Eventual leader's cumulative share")
nb = int((traj[:, -1, sim.BEATLES] > 0).sum())
axes[1].set_title("Beatles' cumulative share (true popularity 100)")
axes[1].text(0.97, 0.05, 'Beatles got no downloads at all in %d of the %d worlds\n(locked out of the top-5 before any download)' % (nW - nb, nW),
             transform=axes[1].transAxes, ha='right', va='bottom', fontsize=8)
for ax in axes:
    ax.set_xlabel('users who have arrived'); ax.set_xscale('log'); ax.set_ylim(0, 1)
axes[0].set_ylabel('cumulative share of downloads')
fig.suptitle('12 worlds, social influence 0.75, top-5 recommender')
fig.tight_layout(); fig.savefig('fig5_trajectories.png', dpi=130); plt.close(fig)

# ---- fig6: policies -------------------------------------------------------
pols = ['random', 'shuffled', 'explore', 'simple', 'damped']
names = {'random': 'random-5', 'simple': 'top-5 by count', 'damped': 'damped (K=20)',
         'explore': 'top-4 + 1 random', 'shuffled': 'top-5, order shuffled'}
fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
for ax, key, lab in zip(axes,
                        ['gini_mean', 'unpred', 'spearman_mean'],
                        ['mean Gini', 'unpredictability U', 'mean Spearman rho (share vs true)']):
    v = [R['4d'][p][key] for p in pols]
    ax.barh(range(len(pols)), v, color='0.4')
    ax.set_yticks(range(len(pols))); ax.set_yticklabels([names[p] for p in pols], fontsize=8)
    ax.set_xlabel(lab); ax.invert_yaxis()
    for i, val in enumerate(v):
        ax.text(val, i, ' %.3f' % val, va='center', fontsize=8)
    ax.set_xlim(0, max(v) * 1.28)
fig.suptitle('Recommender policies at social influence 0.5, 1000 worlds x 1000 users')
fig.tight_layout(); fig.savefig('fig6_policies.png', dpi=130); plt.close(fig)

print('gini of true popularity distribution: %.4f' % sim.gini(true_share[None, :])[0])
print('independent-condition mean shares:',
      {A[i]: round(float(ind[i]), 4) for i in order})
print('leaders in the 12 tracked worlds:', [A[i] for i in leaders])
print('figures written')
