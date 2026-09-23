"""
The choice rule the model ships with: what a user picks from the artists shown.

A choice rule is a function (shown, counts, social_influence) that returns a list of chances,
one per shown artist in the same order, summing to 1. sim.py calls the rule once for each user
and draws that user's download with those chances.

independent_choice is the rule Parts 1 and 2 use: users ignore the download counts. Your Part 3
rule goes in my_choice.py, and each part passes sim.py the recommender and the choice rule it
needs. Nothing in this file changes.
"""

from artists import TRUE_POPULARITY


def normalize(weights):
    """Scale a list of weights so they sum to 1."""
    total = sum(weights)
    return [w / total for w in weights]


def independent_choice(shown, counts, social_influence):
    """Users ignore the counts: each shown artist's chance is its true popularity as a share of
    the true popularity of the artists shown. `counts` and `social_influence` are not used."""
    return normalize([TRUE_POPULARITY[artist] for artist in shown])
