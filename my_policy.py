"""
Your recommender, for Part 5.

Describe your rule to Claude in words first. Claude writes it here, and part5_policy.py compares
it with top_five and random_five from recommender.py, which are written the same way.
"""


def my_policy(counts, rng):
    """Return five different artist names, in display order: position 0 is the top of the list.

    counts  downloads so far in this world, artist -> int; an artist with no downloads yet is
            missing, so read it as counts.get(artist, 0)
    rng     a numpy random generator; use it for anything random, so that runs repeat exactly

    A policy may use the counts and the list of artists (sim.ARTISTS). It must never use
    TRUE_POPULARITY: a real recommender cannot see how much users truly like each artist.
    """
    raise NotImplementedError("Part 5: describe your rule to Claude first")
