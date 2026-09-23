"""
The choice rule the model ships with: what a user picks from the artists shown.

A choice rule is a function (shown, counts, social_influence) that returns a list of chances,
one per shown artist in the same order, summing to 1. `counts` is the download counts shown with
the artists, artist -> number, which is what the recommender chose to show and not the world's
real counts. sim.py calls the rule once for each user and draws that user's download with those
chances.

independent_choice is the rule Parts 1 and 2 use: users ignore the download counts. Your Part 3
rule goes in my_choice.py, and each part passes sim.py the recommender and the choice rule it
needs. step() labels one stage of a choice rule so that hand_check.py can print it. Nothing in
this file changes.
"""

from artists import TRUE_POPULARITY

# hand_check.py sets this to a list while it runs your rule on its case, so that step() records
# each stage. During a simulation it stays None, and step() only hands its values back.
_STEPS = None


def step(label, values):
    """Label one stage of a choice rule and return `values` unchanged, for example
    `social = step("social share, scaled to sum to 1", normalize(weights))`. During the hand
    check, hand_check.py prints each labeled stage as one row; during a simulation step() does
    nothing else. Use a plain string as the label, not an f-string, so it costs nothing in a run."""
    if _STEPS is not None:
        try:
            _STEPS.append((label, list(values)))
        except TypeError:   # a single number, not a list
            _STEPS.append((label, values))
    return values


def normalize(weights):
    """Scale a list of weights so they sum to 1. The weights must not all be 0."""
    total = sum(weights)
    if total == 0:
        raise ValueError(f"normalize() was given weights that sum to 0, {weights}, so it cannot "
                         f"scale them to sum to 1")
    return [w / total for w in weights]


def independent_choice(shown, counts, social_influence):
    """Users ignore the counts they are shown: each shown artist's chance is its true popularity
    as a share of the true popularity of the artists shown. `counts`, the download counts shown
    with the artists, and `social_influence` are not used."""
    return normalize([TRUE_POPULARITY[artist] for artist in shown])
