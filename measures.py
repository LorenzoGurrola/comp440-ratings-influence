"""
The measures. gini() takes one world's market shares, eleven numbers in the order of
sim.ARTISTS; the others take an array of shares with one row per world and one column per
artist. A share is an artist's downloads divided by the world's downloads, so a world's shares
sum to 1.

Gini: inequality within one world, the paper's Figure 1. With s_1 ... s_11 the eleven
artists' shares, zeros included,

    Gini = (the mean of |s_i - s_j| over all 11 x 11 pairs i, j) / (2 x the mean share)

The same number, with less arithmetic, for working it by hand: sort the eleven shares from
smallest to largest, s_(1) <= s_(2) <= ... <= s_(11); then, because the shares sum to 1,

    Gini = (2/11) x (1 x s_(1) + 2 x s_(2) + ... + 11 x s_(11)) - 12/11

0 means every artist has the same share; 10/11 = 0.909 means one artist has every download.

Unpredictability: how much the worlds differ, the paper's Figure 2. For each artist, the mean of
|its share in world w - its share in world v| over all pairs of different worlds w and v; then
the mean of that over the eleven artists. 0 means every world ends the same way.

Fidelity: in each world, the Spearman rank correlation between the artists' shares and their
true popularity; then the mean over worlds. 1 means a world ranks the artists exactly as their
true popularity does; 0 means no relation.

True best wins: the fraction of worlds in which the Beatles, true popularity 100, end with
strictly the largest share. Accidental hits: the fraction of worlds won outright by an artist
with true popularity 30 or less. A tie for first place counts for nobody.

    uv run python measures.py      checks these functions against cases worked out by hand
"""

import sys

import numpy as np
from scipy.stats import spearmanr

from artists import ARTISTS, TRUE_POPULARITY

# True popularity as an array, one entry per artist in ARTISTS order.
TRUE = np.array([TRUE_POPULARITY[artist] for artist in ARTISTS], dtype=float)


def gini(shares_1d):
    """The Gini coefficient of one world's shares: the mean of |s_i - s_j| over all pairs
    i, j, divided by 2 x the mean share."""
    s = np.asarray(shares_1d, dtype=float)
    differences = np.abs(s[:, None] - s[None, :])   # |s_i - s_j| for every pair i, j
    return float(differences.mean() / (2 * s.mean()))


def mean_gini(shares):
    """Each world's Gini, averaged over the worlds."""
    return float(np.mean([gini(world) for world in np.asarray(shares)]))


def unpredictability(shares):
    """For each artist, the mean |difference in its share| over all pairs of different worlds;
    then the mean over artists. Needs at least two worlds."""
    shares = np.asarray(shares, dtype=float)
    worlds = len(shares)
    if worlds < 2:
        return float("nan")
    per_artist = []
    for column in shares.T:   # one artist's share in every world
        differences = np.abs(column[:, None] - column[None, :])   # every world against every world
        # That grid holds each pair of different worlds twice (w, v and v, w) and a world
        # against itself as 0, so its sum over worlds x (worlds - 1) is the mean over pairs.
        per_artist.append(differences.sum() / (worlds * (worlds - 1)))
    return float(np.mean(per_artist))


def fidelity(shares):
    """In each world, the Spearman rank correlation between the shares and true popularity;
    then the mean over worlds. A world where every artist has the same share has no
    correlation and is left out."""
    correlations = [spearmanr(world, TRUE).statistic for world in np.asarray(shares)]
    return float(np.nanmean(correlations))


def winner(world):
    """The column of the artist with strictly the largest share, or None if first is tied."""
    leaders = np.flatnonzero(world == world.max())
    return leaders[0] if len(leaders) == 1 else None


def true_best_wins(shares):
    """The fraction of worlds in which the true best artist, the Beatles, finishes strictly
    first."""
    best = int(np.argmax(TRUE))
    return float(np.mean([winner(world) == best for world in np.asarray(shares)]))


def accidental_hits(shares, cutoff=30):
    """The fraction of worlds won outright by an artist with true popularity `cutoff` or less."""
    winners = [winner(world) for world in np.asarray(shares)]
    return float(np.mean([w is not None and TRUE[w] <= cutoff for w in winners]))


def summary(shares):
    """All five measures for one set of worlds, as a dict."""
    return {
        "mean_gini": mean_gini(shares),
        "unpredictability": unpredictability(shares),
        "fidelity": fidelity(shares),
        "true_best_wins": true_best_wins(shares),
        "accidental_hits": accidental_hits(shares),
    }


def print_summary(label, shares):
    """Print `label`, then one line per measure with 3 decimals. Returns summary(shares)."""
    result = summary(shares)
    print(label)
    print(f"  mean Gini          {result['mean_gini']:.3f}   inequality within a world")
    print(f"  unpredictability   {result['unpredictability']:.3f}"
          f"   how much an artist's share differs between worlds")
    print(f"  fidelity           {result['fidelity']:.3f}"
          f"   rank correlation of shares with true popularity")
    print(f"  true best wins     {result['true_best_wins']:.3f}"
          f"   fraction of worlds the Beatles finish strictly first")
    print(f"  accidental hits    {result['accidental_hits']:.3f}"
          f"   fraction of worlds won by true popularity 30 or less")
    return result


# The table's columns: the header each is printed under, and its key in summary().
COLUMNS = [("Gini", "mean_gini"), ("unpredictability", "unpredictability"),
           ("fidelity", "fidelity"), ("true best wins", "true_best_wins"),
           ("accidental hits", "accidental_hits")]


def print_table(rows):
    """Print the five measures for several sets of worlds as one table. `rows` is a list of
    (label, shares). Prints a header line, then one line per row: its label and the five
    measures, 3 decimals each, in aligned columns. Gini and fidelity are means over the worlds.
    Returns the summary() of each row, in order."""
    width = max(len(label) for label, _ in rows)
    print(" " * width + "".join(f"  {header}" for header, _ in COLUMNS))
    results = []
    for label, shares in rows:
        result = summary(shares)
        results.append(result)
        print(f"{label:<{width}}"
              + "".join(f"  {result[key]:>{len(header)}.3f}" for header, key in COLUMNS))
    return results


def self_check():
    """Check the measures against cases worked out by hand. Returns True if all match."""
    two_worlds = np.zeros((2, 11))
    two_worlds[0, 0] = 1.0   # world 0: the Beatles get every download
    two_worlds[1, 1] = 1.0   # world 1: Taylor Swift gets every download
    three_worlds = np.array([[0.2, 0.8], [0.4, 0.6], [0.6, 0.4]])
    cases = [
        ("Gini of [1, 0, 0, 0], one artist has everything: 3/4",
         0.75, gini([1, 0, 0, 0])),
        ("Gini of eleven equal shares: 0",
         0.0, gini([1 / 11] * 11)),
        ("Gini of true popularity itself, as shares",
         0.3010, gini(TRUE / TRUE.sum())),
        ("Unpredictability, two worlds each won entirely by a different artist: 2/11",
         2 / 11, unpredictability(two_worlds)),
        ("Unpredictability, three worlds of two artists, pair differences 0.2, 0.4, 0.2",
         0.8 / 3, unpredictability(three_worlds)),
    ]
    all_match = True
    for name, expected, computed in cases:
        match = abs(expected - computed) < 0.0005
        all_match = all_match and match
        print(f"{'ok  ' if match else 'FAIL'}  {name}: "
              f"expected {expected:.4f}, computed {computed:.4f}")
    return all_match


if __name__ == "__main__":
    sys.exit(0 if self_check() else 1)
