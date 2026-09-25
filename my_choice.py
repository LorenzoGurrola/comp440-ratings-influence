"""
Your choice rule, for Part 3.

You design the rule. Claude asks you questions about it, writes it here from your answers, and
shows you the code. Then `uv run python hand_check.py` shows each step of your rule on a
two-artist case, so you can say whether each step does what you meant.
"""

from artists import TRUE_POPULARITY
from choose import normalize, step


def my_choice(shown, counts, social_influence):
    """Return the chance that a user picks each shown artist: a list of numbers, one per artist
    in `shown` and in the same order, summing to 1.

    shown              the artists on the list, top first (positions 0, 1, 2, ...)
    counts             the download counts shown with the artists, artist -> number; an artist
                       shown without a count is missing, so read it as counts.get(artist, 0)
    social_influence   from 0 (users ignore the counts) to 1 (users go by the counts alone)

    The rule may use `normalize`, which scales a list of weights so they sum to 1, and
    TRUE_POPULARITY, which gives each artist its hidden true popularity. `step` labels each
    stage of the rule, so that hand_check.py can show it.
    """
    taste = step("taste weight: each shown artist's true popularity, as a share",
                 normalize([TRUE_POPULARITY[artist] for artist in shown]))

    squared_counts = [counts.get(artist, 0) ** 2 for artist in shown]
    if sum(squared_counts) == 0:
        downloads = step("download weight: nobody has a download yet, so fall back to taste",
                          taste)
    else:
        downloads = step("download weight: downloads squared, as a share",
                          normalize(squared_counts))

    return step("chances: taste and download weight blended by social_influence",
                [social_influence * d + (1 - social_influence) * t
                 for d, t in zip(downloads, taste)])
