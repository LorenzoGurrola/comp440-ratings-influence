"""Vectorised port of the instructor's feedback-effects simulation.

All worlds in a run are advanced together, one arriving user at a time, with
numpy doing the per-world work.  The mechanics are the notebook's:

  rec_weight(rank r, artist a) = (shown_count(a) + PSEUDO) * BASE ** (-r)
  social  = rec_weight normalised over the NUM_RECS recs
  true    = TRUE_ARTIST_POPULARITY normalised over the NUM_RECS recs
  combined= social_influence * social + (1 - social_influence) * true
  the user downloads one of the 5 recs, drawn with probability `combined`

`shown_count` is the raw download count for every policy except `damped`,
which shows a shrunken count (see POLICIES below).

Parameters: social_influence, policy, num_users, num_worlds, num_recs,
rank-penalty base (default 1.2), pseudo-count (default 1.0), seed.
"""

import numpy as np
from scipy.stats import rankdata

TRUE_ARTIST_POPULARITY = {
    'Beatles': 100, 'Taylor Swift': 90, 'Mariah Carey': 90, 'Drake': 70,
    'Katy Perry': 70, 'Bruno Mars': 50, 'Justin Bieber': 50, 'Cher': 30,
    'Bon Jovi': 30, 'Miles Davis': 20, 'John Coltrane': 10,
}
ALL_ARTISTS = list(TRUE_ARTIST_POPULARITY)
TRUE_POP = np.array([TRUE_ARTIST_POPULARITY[a] for a in ALL_ARTISTS], dtype=float)
NUM_ARTISTS = len(ALL_ARTISTS)
BEATLES = ALL_ARTISTS.index('Beatles')
LOW_TRUE = np.array([TRUE_ARTIST_POPULARITY[a] <= 30 for a in ALL_ARTISTS])

_BIG = np.float64(1e18)


def _popularity_order(counts, first_seen, rng):
    """Artists ranked as the notebook's simple_rec_alg ranks them.

    Downloaded artists first, by count descending, ties broken by which was
    downloaded first (Python's sort is stable and dict order is first-download
    order).  Never-downloaded artists come last in a fresh uniform random
    order, which is exactly what the notebook's rejection-sampling padding loop
    ("draw a random artist, keep it if it is not already in recs") produces.
    """
    downloaded = counts > 0
    primary = np.where(downloaded, -counts.astype(np.float64), _BIG)
    secondary = np.where(downloaded, first_seen, rng.random(counts.shape))
    return np.lexsort((secondary, primary), axis=1)


# --- recommender policies -------------------------------------------------
# Each returns (recs, shown): recs is (W, R) artist indices in presentation
# order, shown is (W, R) the download count displayed next to each rec.

def pol_simple(counts, first_seen, rng, R, n):
    """Top-R by download count (the notebook's simple_rec_alg)."""
    recs = _popularity_order(counts, first_seen, rng)[:, :R]
    return recs, np.take_along_axis(counts, recs, 1).astype(float)


def pol_random(counts, first_seen, rng, R, n):
    """R uniformly random distinct artists in random order; counts not used."""
    recs = np.argsort(rng.random(counts.shape), axis=1)[:, :R]
    return recs, np.take_along_axis(counts, recs, 1).astype(float)


def pol_damped(counts, first_seen, rng, R, n, K=20.0):
    """Damped popularity: score = (count + K/A) / (n + K), a uniform prior of
    strength K spread over the A artists, n = downloads so far in the world.

    The score is strictly increasing in the raw count, so the ORDER is the same
    as pol_simple.  What changes is the number shown: the rec displays
    shown = n * score = n * (count + K/A) / (n + K), a count shrunk toward the
    equal-share value n/A.
    """
    recs = _popularity_order(counts, first_seen, rng)[:, :R]
    c = np.take_along_axis(counts, recs, 1).astype(float)
    shown = n * (c + K / NUM_ARTISTS) / (n + K)
    return recs, shown


def pol_explore(counts, first_seen, rng, R, n):
    """Top-(R-1) by count, plus one uniformly random artist from the rest,
    placed last."""
    order = _popularity_order(counts, first_seen, rng)
    top = order[:, :R - 1]
    j = rng.integers(0, NUM_ARTISTS - (R - 1), size=counts.shape[0])
    extra = order[np.arange(counts.shape[0]), (R - 1) + j][:, None]
    recs = np.concatenate([top, extra], axis=1)
    return recs, np.take_along_axis(counts, recs, 1).astype(float)


def pol_shuffled(counts, first_seen, rng, R, n):
    """Same top-R set as pol_simple, shown with its counts but in a fresh
    random order, so the position effect no longer favours the leader
    ("show counts but hide the ranking")."""
    recs = _popularity_order(counts, first_seen, rng)[:, :R]
    perm = np.argsort(rng.random(recs.shape), axis=1)
    recs = np.take_along_axis(recs, perm, 1)
    return recs, np.take_along_axis(counts, recs, 1).astype(float)


POLICIES = {
    'simple': pol_simple,
    'random': pol_random,
    'damped': pol_damped,
    'explore': pol_explore,
    'shuffled': pol_shuffled,
}


def simulate(social_influence=0.5, policy='simple', num_users=1000,
             num_worlds=1000, num_recs=5, base=1.2, pseudo=1.0, seed=0,
             track_worlds=0):
    """Run `num_worlds` independent worlds.

    Returns dict with 'shares' (W, A) final market shares, 'counts' (W, A),
    and, if track_worlds > 0, 'traj' (track_worlds, num_users+1, A) cumulative
    counts after each arrival for the first `track_worlds` worlds.
    """
    assert 0.0 <= social_influence <= 1.0
    rng = np.random.default_rng(seed)
    W, A, R = num_worlds, NUM_ARTISTS, num_recs
    pol = POLICIES[policy] if isinstance(policy, str) else policy

    counts = np.zeros((W, A), dtype=np.int64)
    first_seen = np.full((W, A), np.inf)
    rank_penalty = base ** (-np.arange(R, dtype=float))
    rows = np.arange(W)
    traj = np.zeros((track_worlds, num_users + 1, A), dtype=np.int32) if track_worlds else None

    for step in range(num_users):
        recs, shown = pol(counts, first_seen, rng, R, step)
        w = (shown + pseudo) * rank_penalty
        social = w / w.sum(axis=1, keepdims=True)
        tw = TRUE_POP[recs]
        true = tw / tw.sum(axis=1, keepdims=True)
        comb = social_influence * social + (1.0 - social_influence) * true
        cum = np.cumsum(comb, axis=1)
        u = rng.random((W, 1)) * cum[:, -1:]
        pick = (cum < u).sum(axis=1)
        chosen = recs[rows, pick]
        new = counts[rows, chosen] == 0
        counts[rows, chosen] += 1
        fs = first_seen[rows, chosen]
        first_seen[rows, chosen] = np.where(new, float(step), fs)
        if track_worlds:
            traj[:, step + 1, :] = counts[:track_worlds]

    shares = counts / counts.sum(axis=1, keepdims=True)
    out = {'shares': shares, 'counts': counts,
           'params': dict(social_influence=social_influence, policy=policy,
                          num_users=num_users, num_worlds=num_worlds,
                          num_recs=num_recs, base=base, pseudo=pseudo, seed=seed)}
    if track_worlds:
        out['traj'] = traj
    return out


# --- measures -------------------------------------------------------------

def gini(shares):
    """Gini coefficient of each world's A market shares. (W,) -> per world."""
    x = np.sort(shares, axis=1)
    A = x.shape[1]
    i = np.arange(1, A + 1)
    tot = x.sum(axis=1)
    return (2.0 * (x * i).sum(axis=1)) / (A * tot) - (A + 1.0) / A


def unpredictability(shares):
    """Salganik's U: for each artist, the mean absolute difference in market
    share between all pairs of worlds; then averaged over artists.
    Returns (U, per-artist array)."""
    W = shares.shape[0]
    x = np.sort(shares, axis=0)
    i = np.arange(W)[:, None]
    s = ((2 * i - W + 1) * x).sum(axis=0)
    per_artist = s / (W * (W - 1) / 2.0)
    return per_artist.mean(), per_artist


def spearman_per_world(shares):
    """Spearman rank correlation between an artist's share and its true
    popularity, one value per world (ties get average ranks)."""
    r = rankdata(shares, axis=1)
    t = rankdata(TRUE_POP)
    rc = r - r.mean(axis=1, keepdims=True)
    tc = t - t.mean()
    num = (rc * tc).sum(axis=1)
    den = np.sqrt((rc ** 2).sum(axis=1) * (tc ** 2).sum())
    with np.errstate(invalid='ignore', divide='ignore'):
        return np.where(den > 0, num / den, np.nan)


def measure(res):
    shares = res['shares']
    W = shares.shape[0]
    g = gini(shares)
    U, U_artist = unpredictability(shares)
    rho = spearman_per_world(shares)
    mx = shares.max(axis=1, keepdims=True)
    is_top = shares == mx
    n_top = is_top.sum(axis=1)
    beatles_top = (is_top[:, BEATLES] & (n_top == 1))
    low_top = (is_top[:, LOW_TRUE].any(axis=1) & (n_top == 1))
    nonzero = (shares > 0).sum(axis=1)
    return {
        'num_worlds': int(W),
        'gini_mean': float(g.mean()), 'gini_sd': float(g.std(ddof=1)),
        'unpred': float(U),
        'unpred_by_artist': {a: float(v) for a, v in zip(ALL_ARTISTS, U_artist)},
        'spearman_mean': float(np.nanmean(rho)), 'spearman_sd': float(np.nanstd(rho, ddof=1)),
        'beatles_first': float(beatles_top.mean()),
        'accidental_hit': float(low_top.mean()),
        'top_tie_frac': float((n_top > 1).mean()),
        'leader_share_mean': float(shares.max(axis=1).mean()),
        'leader_share_sd': float(shares.max(axis=1).std(ddof=1)),
        'beatles_share_mean': float(shares[:, BEATLES].mean()),
        'beatles_share_sd': float(shares[:, BEATLES].std(ddof=1)),
        'nonzero_artists_mean': float(nonzero.mean()),
        'mean_shares': {a: float(v) for a, v in zip(ALL_ARTISTS, shares.mean(axis=0))},
    }


def shares_from_original(results):
    """Turn sim_original.simulate_all_worlds output into a (W, A) array."""
    return np.array([results[a] for a in ALL_ARTISTS]).T
