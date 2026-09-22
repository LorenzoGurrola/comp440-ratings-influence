"""
What a user picks from the artists shown.

    uv run python choose.py      prints the two-artist hand check for Part 3

choice_weights() gives each shown artist its chance of being picked, and choose() draws one
artist with those chances. As shipped, users ignore the download counts and pick by true
popularity alone. Part 3 adds social influence, in the marked block.
"""

from artists import TRUE_POPULARITY

# The hand check: two artists, A at the top of the list (position 0) and B below it
# (position 1). A has 3 downloads, B has none, and both have true popularity 50.
CHECK_SHOWN = ["A", "B"]
CHECK_COUNTS = {"A": 3, "B": 0}
CHECK_TRUE_POPULARITY = {"A": 50, "B": 50}
# The chances the rule in README Part 3 gives for that case at social influence 0.5.
CHECK_TARGET = {"A": 0.6638, "B": 0.3362}


def choice_weights(shown, counts, social_influence, position_discount=1.2, pseudo_count=1,
                   true_popularity=TRUE_POPULARITY):
    """The chance that a user picks each shown artist: a dict artist -> chance, summing to 1.

    shown              the artists on the list, top first (positions 0, 1, 2, ...)
    counts             downloads so far in this world, artist -> int; an artist with no
                       downloads yet is missing, so read it as counts.get(artist, 0)
    social_influence   from 0 (users ignore the counts) to 1 (users go by the counts alone)
    position_discount  each step down the list divides an artist's social weight by this
    pseudo_count       added to every count, so an artist with no downloads can still be picked
    true_popularity    artist -> hidden true popularity; the model's own unless a check
                       passes its own
    """
    # True preference: each shown artist's true popularity, as a share of the shown total.
    total = sum(true_popularity[artist] for artist in shown)
    true_weights = {artist: true_popularity[artist] / total for artist in shown}

    # ---- Part 3: social influence goes here. ----
    # As shipped, users ignore the counts. Describe the rule in README Part 3 to Claude
    # in your own words; it writes the rule here; then run `uv run python choose.py`.

    return true_weights


def choose(shown, counts, social_influence, rng, position_discount=1.2, pseudo_count=1):
    """One user's download: an artist from `shown`, drawn at random with the chances that
    choice_weights() gives. `rng` is a numpy random generator."""
    weights = choice_weights(shown, counts, social_influence, position_discount, pseudo_count)
    artists = list(weights)
    chances = [weights[artist] for artist in artists]
    return artists[rng.choice(len(artists), p=chances)]


def hand_check(social_influence=0.5):
    """Print the chances choice_weights() gives for the hand-check case, and the chances the
    rule in README Part 3 gives for it at social influence 0.5."""
    got = choice_weights(CHECK_SHOWN, CHECK_COUNTS, social_influence, position_discount=1.2,
                         pseudo_count=1, true_popularity=CHECK_TRUE_POPULARITY)
    print("Hand check: two artists are shown, A at the top (position 0) and B below it")
    print("(position 1). A has 3 downloads, B has 0, and both have true popularity 50.")
    print("Position discount 1.2, pseudo-count 1.")
    print(f"  choice_weights() at social influence {social_influence}:"
          f"   A {got['A']:.4f}   B {got['B']:.4f}")
    print(f"  the rule in README Part 3, at social influence 0.5:"
          f"   A {CHECK_TARGET['A']:.4f}   B {CHECK_TARGET['B']:.4f}")


def is_implemented():
    """True once choice_weights() gives the README Part 3 rule's answer for the hand check."""
    got = choice_weights(CHECK_SHOWN, CHECK_COUNTS, 0.5, position_discount=1.2,
                         pseudo_count=1, true_popularity=CHECK_TRUE_POPULARITY)
    return abs(got["A"] - CHECK_TARGET["A"]) < 0.001


if __name__ == "__main__":
    hand_check()
