"""
The simulated market: worlds of users arriving one at a time.

A world starts with no downloads. Each user who arrives is shown a few artists by a policy
(recommender.py), which sees only the downloads so far, and downloads exactly one of them, picked by
choose.py. The download is added to the world's counts and the next user arrives. Worlds never
see each other, so any difference between two worlds comes from chance and from what earlier
users in the same world did.

    simulate(policy, worlds, social_influence)    final market shares, one row per world
    simulate_with_picks(policy, worlds, ...)      the same, and every world's downloads in order
    simulate_world(policy, social_influence)      one world's final download counts

A market share is an artist's downloads divided by the world's downloads. Each constant below
is one of the model's assumptions, and Part 6 asks you to change one. Passing the new value to
simulate() in part6_assumption.py changes Part 6 alone. Editing the value here changes every
part the next time it runs, including the Part 3 figures you have already written about.
"""

import numpy as np

import choose

# The eleven artists, most popular first, and their hidden true popularity. They are defined
# in artists.py so that choose.py can read them without importing this file.
# Assumption (Part 6): which artists there are, and how much users like each.
from artists import ARTISTS, TRUE_POPULARITY

# How many artists each user is shown. The policies in recommender.py show this many.
# Assumption (Part 6): the paper's participants saw all 48 songs; here a user sees five.
NUM_SHOWN = 5

# Each step down the list divides an artist's social weight by this: position 0 counts fully,
# position 1 counts 1/1.2, position 2 counts 1/1.2^2, and so on.
# Assumption (Part 6): 1.0 would mean the order of the list does not matter.
POSITION_DISCOUNT = 1.2

# Added to every artist's count before the counts are compared, so that an artist nobody has
# downloaded yet can still be picked. Assumption (Part 6).
PSEUDO_COUNT = 1

# Users per world. Each user downloads exactly one artist.
# Assumption (Part 6): a classroom-sized market, 12 people choosing 3 times, is 36 users.
USERS = 1000


def check_shown(shown):
    """Stop with a clear message if a policy returned something other than different artists."""
    if not shown or len(set(shown)) != len(shown) or any(a not in ARTISTS for a in shown):
        raise ValueError(f"a policy must return a list of different artist names; got {shown}")


def simulate_world(policy, social_influence, users=USERS, rng=None,
                   position_discount=POSITION_DISCOUNT, pseudo_count=PSEUDO_COUNT, record=False):
    """Run one world. Returns its final download counts, artist -> int, every artist listed.

    policy             a function (counts, rng) -> the artists shown, top of the list first
    social_influence   from 0 (users ignore the counts) to 1 (users go by the counts alone)
    users              how many users arrive; each downloads exactly one artist
    rng                a numpy random generator; a fresh one if not given
    record             if True, return (counts, picks), where picks lists every user's
                       download in the order the users arrived
    """
    if rng is None:
        rng = np.random.default_rng()
    counts = {}   # artist -> downloads so far; an artist enters at its first download
    picks = []
    for _ in range(users):
        shown = policy(dict(counts), rng)   # a copy, so a policy cannot change the counts
        check_shown(shown)
        pick = choose.choose(shown, counts, social_influence, rng, position_discount, pseudo_count)
        counts[pick] = counts.get(pick, 0) + 1
        if record:
            picks.append(pick)
    final = {artist: counts.get(artist, 0) for artist in ARTISTS}
    if record:
        return final, picks
    return final


def simulate_with_picks(policy, worlds=300, social_influence=0.0, users=USERS, seed=440,
                        position_discount=POSITION_DISCOUNT, pseudo_count=PSEUDO_COUNT):
    """Run `worlds` worlds from the same start. Returns (shares, picks_by_world): shares is a
    numpy array with one row per world and one column per artist in ARTISTS order, each row
    that world's final market shares; picks_by_world[w] lists world w's downloads in order.
    The same seed gives the same worlds every time."""
    if not 0 <= social_influence <= 1:
        raise ValueError(f"social_influence must be between 0 and 1; got {social_influence}")
    rng = np.random.default_rng(seed)
    shares = np.zeros((worlds, len(ARTISTS)))
    picks_by_world = []
    for w in range(worlds):
        counts, picks = simulate_world(policy, social_influence, users, rng,
                                       position_discount, pseudo_count, record=True)
        shares[w] = [counts[artist] / users for artist in ARTISTS]
        picks_by_world.append(picks)
    return shares, picks_by_world


def simulate(policy, worlds=300, social_influence=0.0, users=USERS, seed=440,
             position_discount=POSITION_DISCOUNT, pseudo_count=PSEUDO_COUNT):
    """Run `worlds` worlds from the same start and return their final market shares: a numpy
    array with one row per world and one column per artist, in ARTISTS order. Prints nothing."""
    shares, _ = simulate_with_picks(policy, worlds, social_influence, users, seed,
                                    position_discount, pseudo_count)
    return shares
