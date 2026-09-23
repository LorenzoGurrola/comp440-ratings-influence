"""
The two-artist hand check for Part 3.

    uv run python hand_check.py            the case, and the chances my_choice() gives for it
    uv run python hand_check.py --target   the same, and the chances the README's Part 3 rule
                                           gives: run it after you have worked them out by hand

Parts 3, 4 and 5 stop until passes() is true, so this is the one number to check by hand.
Nothing in this file changes.
"""

import sys

from artists import TRUE_POPULARITY
from my_choice import my_choice

# The case: two artists, Bruno Mars at the top of the list (position 0) with 3 downloads and
# Justin Bieber below it (position 1) with none, so Justin Bieber is missing from the counts.
CHECK_SHOWN = ["Bruno Mars", "Justin Bieber"]
CHECK_COUNTS = {"Bruno Mars": 3}
CHECK_SOCIAL_INFLUENCE = 0.5

# The chances the README's Part 3 rule gives for this case, one per artist in CHECK_SHOWN order.
# hand_check() prints them only when asked, so that the student works them out first.
CHECK_TARGET = [0.6638, 0.3362]


def chances():
    """The chances my_choice() gives for the case, or None with one line printed saying why not:
    the rule is not written yet, or it failed on the case."""
    try:
        return my_choice(CHECK_SHOWN, dict(CHECK_COUNTS), CHECK_SOCIAL_INFLUENCE)
    except NotImplementedError as error:
        print(f"my_choice is not written yet: {error}")
    except Exception as error:   # any other error in the rule, reported plainly
        print(f"my_choice failed on the hand check: {type(error).__name__}: {error}")
    return None


def hand_check(target=False):
    """Print the case and the chances my_choice() gives for it. With target=True, also print the
    chances the README's Part 3 rule gives."""
    top, below = CHECK_SHOWN
    print(f"Hand check: {top} is shown at the top of the list (position 0) and {below} below it "
          f"(position 1),")
    print(f"at social influence {CHECK_SOCIAL_INFLUENCE}. {top} has "
          f"{CHECK_COUNTS.get(top, 0)} downloads, {below} has none, and both have true "
          f"popularity {TRUE_POPULARITY[top]}.")
    got = chances()
    if got is not None:
        print(f"  my_choice() gives:                {top} {got[0]:.4f}   {below} {got[1]:.4f}")
    if target:
        print(f"  the README's Part 3 rule gives:   {top} {CHECK_TARGET[0]:.4f}   "
              f"{below} {CHECK_TARGET[1]:.4f}   (at social influence "
              f"{CHECK_SOCIAL_INFLUENCE})")


def passes():
    """True once my_choice() gives the README Part 3 rule's answer for the case. False while the
    rule is not written, fails on the case, or gives a different answer. Prints nothing."""
    try:
        got = my_choice(CHECK_SHOWN, dict(CHECK_COUNTS), CHECK_SOCIAL_INFLUENCE)
    except Exception:   # a rule that cannot run has not passed
        return False
    return (len(got) == len(CHECK_TARGET)
            and all(abs(g - t) < 0.001 for g, t in zip(got, CHECK_TARGET)))


if __name__ == "__main__":
    hand_check(target="--target" in sys.argv)
