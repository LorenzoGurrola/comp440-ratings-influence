"""
The simulated market: worlds of users arriving one at a time.

A world starts with no downloads. Each user who arrives is shown a few artists by a recommender
(recommender.py), which sees only the downloads so far and returns both the artists to show and
the download counts to show with them. The user downloads exactly one of them, picked by a choice
rule (independent_choice in choose.py, or your own rule in my_choice.py from Part 3 on). The
choice rule is given the counts the recommender showed, not the world's real counts, so a user's
choice depends only on what that user saw. The download is added to the world's counts and the
next user arrives. Worlds never see each other, so any difference between two worlds comes from
chance and from what earlier users in the same world did.

    simulate(recommender, choice, worlds, social_influence)     final market shares, one per world
    simulate_with_picks(recommender, choice, worlds, ...)       the same, and every world's picks
    simulate_world(recommender, choice, social_influence)       one world's final download counts

Each part passes the recommender and the choice rule it needs, so no part changes what another
part ran.

A market share is an artist's downloads divided by the world's downloads. NUM_SHOWN and USERS
below are two of the model's assumptions, and the optional follow-up asks you to change one
assumption. For users per world, pass users= to simulate() in followup_assumption.py, which
changes that follow-up alone; editing a value here would change every part the next time it
runs, including the Part 3 figures you have already written about. The assumptions inside the
choice, the 1.2 position discount and the +1 among them, live in your own rule in my_choice.py,
and the follow-up changes one of those by copying my_choice() into followup_assumption.py and
making the change in the copy.
"""

import numpy as np

# The eleven artists, most popular first, and their hidden true popularity. They are defined
# in artists.py so that choose.py can read them without importing this file.
# Assumption (the follow-up): which artists there are, and how much users like each.
from artists import ARTISTS, TRUE_POPULARITY

# How many artists each user is shown. The recommenders in recommender.py show this many.
# Assumption (the follow-up): the paper's participants saw all 48 songs; here a user sees five.
NUM_SHOWN = 5

# Users per world. Each user downloads exactly one artist.
# Assumption (the follow-up): a classroom-sized market, 12 people choosing 3 times, is 36 users.
USERS = 1000


def check_shown(shown):
    """Stop with a clear message if a recommender returned something other than different
    artists."""
    if not shown or len(set(shown)) != len(shown) or any(a not in ARTISTS for a in shown):
        raise ValueError(f"a recommender must return a list of different artist names; "
                         f"got {shown}")


def check_counts(counts):
    """Stop with a clear message if a recommender returned something other than a dict of counts
    to show, none of them negative."""
    if not isinstance(counts, dict) or any(
            isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0
            for value in counts.values()):
        raise ValueError(f"a recommender must return the counts to show as a dict of "
                         f"artist -> a number that is not negative; got {counts}")


def check_chances(shown, chances):
    """Stop with a clear message if a choice rule returned something other than one chance per
    shown artist, none of them negative, adding up to 1."""
    if len(chances) != len(shown):
        raise ValueError(f"a choice rule must return one chance per shown artist, in the same "
                         f"order; {len(shown)} artists were shown and it returned "
                         f"{len(chances)} chances: {chances}")
    if any(chance < 0 for chance in chances):
        raise ValueError(f"a choice rule must not return a negative chance; got {chances}")
    if abs(sum(chances) - 1) > 1e-6:
        raise ValueError(f"a choice rule must return chances that sum to 1; got {chances}, "
                         f"which sum to {sum(chances)}")


def simulate_world(recommender, choice, social_influence, users=USERS, rng=None, record=False):
    """Run one world. Returns its final download counts, artist -> int, every artist listed.

    recommender        a function (counts, rng) -> (the artists shown, top of the list first;
                       the download counts shown with them, artist -> number)
    choice             a function (shown, counts, social_influence) -> each shown artist's
                       chance of being picked, one per artist in `shown` order, summing to 1.
                       `counts` is what the recommender showed, not the world's real counts
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
        shown, shown_counts = recommender(dict(counts), rng)   # a copy, so it cannot change them
        check_shown(shown)
        check_counts(shown_counts)
        chances = choice(shown, shown_counts, social_influence)
        check_chances(shown, chances)
        pick = shown[rng.choice(len(shown), p=chances)]
        counts[pick] = counts.get(pick, 0) + 1
        if record:
            picks.append(pick)
    final = {artist: counts.get(artist, 0) for artist in ARTISTS}
    if record:
        return final, picks
    return final


def simulate_with_picks(recommender, choice, worlds=300, social_influence=0.0, users=USERS,
                        seed=440):
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
        counts, picks = simulate_world(recommender, choice, social_influence, users, rng,
                                       record=True)
        shares[w] = [counts[artist] / users for artist in ARTISTS]
        picks_by_world.append(picks)
    return shares, picks_by_world


def simulate(recommender, choice, worlds=300, social_influence=0.0, users=USERS, seed=440):
    """Run `worlds` worlds from the same start and return their final market shares: a numpy
    array with one row per world and one column per artist, in ARTISTS order. Prints nothing."""
    shares, _ = simulate_with_picks(recommender, choice, worlds, social_influence, users, seed)
    return shares
