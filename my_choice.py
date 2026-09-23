"""
Your choice rule, for Part 3.

Describe the rule in README Part 3 to Claude in your own words. Claude writes it here, and then
run `uv run python hand_check.py`.
"""

from artists import TRUE_POPULARITY
from choose import normalize


def my_choice(shown, counts, social_influence):
    """Return the chance that a user picks each shown artist: a list of numbers, one per artist
    in `shown` and in the same order, summing to 1.

    shown              the artists on the list, top first (positions 0, 1, 2, ...)
    counts             downloads so far in this world, artist -> int; an artist with no
                       downloads yet is missing, so read it as counts.get(artist, 0)
    social_influence   from 0 (users ignore the counts) to 1 (users go by the counts alone)

    The rule may use `normalize`, which scales a list of weights so they sum to 1, and
    TRUE_POPULARITY, which gives each artist its hidden true popularity.
    """
    raise NotImplementedError("Part 3: describe the rule to Claude first")
