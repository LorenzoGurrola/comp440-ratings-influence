"""
The two-artist hand check for Part 3.

    uv run python hand_check.py             the case, and whether my_choice is written yet
    uv run python hand_check.py --compare   the same, and the chances my_choice() gives for the
                                            case: run it after you have worked them out by hand

There is no single right answer: the check is whether your code gives what you worked out
for your own rule. passes() is the gate for Parts 3 and 4: my_choice is written, runs on the
case, and returns two chances that are zero or more and sum to 1. problem() says in plain words
why it does not pass. Nothing in this file changes.
"""

import math
import sys

from artists import TRUE_POPULARITY
from my_choice import my_choice

# The case: two artists, Bruno Mars at the top of the list (position 0) with 3 downloads and
# Justin Bieber below it (position 1) with none, so Justin Bieber is missing from the counts.
CHECK_SHOWN = ["Bruno Mars", "Justin Bieber"]
CHECK_COUNTS = {"Bruno Mars": 3}
CHECK_SOCIAL_INFLUENCE = 0.5

NOT_WRITTEN = "my_choice is not written yet."
NORMALIZE_HINT = "normalize() in choose.py scales a list of weights so they sum to 1."


def chances():
    """The chances my_choice() gives for the case. Raises whatever my_choice() raises."""
    return my_choice(CHECK_SHOWN, dict(CHECK_COUNTS), CHECK_SOCIAL_INFLUENCE)


def problem():
    """None when my_choice passes the check; otherwise one plain sentence saying why not."""
    try:
        got = chances()
    except NotImplementedError:
        return NOT_WRITTEN
    except Exception as error:   # any other error in the rule, reported plainly
        return (f"my_choice stops with an error on the hand-check case: "
                f"{type(error).__name__}: {error}")
    try:
        got = [float(chance) for chance in got]
    except (TypeError, ValueError):
        return (f"my_choice must return a list of numbers, one chance per artist shown; "
                f"it returned {got!r}.")
    if len(got) != len(CHECK_SHOWN):
        return (f"my_choice must return one chance per artist shown: {len(CHECK_SHOWN)} artists "
                f"were shown and it returned {len(got)} chances.")
    if not all(math.isfinite(chance) for chance in got):
        return f"my_choice returned something that is not a number: {got}."
    if any(chance < 0 for chance in got):
        return f"my_choice returned a negative chance: {got}. A chance must be 0 or more."
    if abs(sum(got) - 1) > 1e-6:
        return (f"my_choice returned chances that sum to {sum(got):.4f}, not 1. "
                f"{NORMALIZE_HINT}")
    return None


def passes():
    """True once my_choice is written, runs on the case, and returns two chances that are zero
    or more and sum to 1. Prints nothing."""
    return problem() is None


def hand_check(compare=False):
    """Print the case and whether my_choice is written. With compare=True, also print the
    chances my_choice() gives for the case, and a plain sentence if they do not pass."""
    top, below = CHECK_SHOWN
    print(f"Hand check, at social influence {CHECK_SOCIAL_INFLUENCE}:")
    print(f"  {top:<14} at the top of the list (position 0), {CHECK_COUNTS.get(top, 0)} downloads, "
          f"true popularity {TRUE_POPULARITY[top]}")
    print(f"  {below:<14} below it (position 1), no downloads, "
          f"true popularity {TRUE_POPULARITY[below]}")
    why = problem()
    if not compare:
        print(NOT_WRITTEN if why == NOT_WRITTEN else "my_choice is written.")
        print("Work out by hand the chance your rule gives each artist. Then "
              "`uv run python hand_check.py --compare` prints what your code gives.")
        return
    try:
        got = [float(chance) for chance in chances()]
    except Exception:   # nothing printable came back; problem() says why
        got = None
    if got is not None and len(got) == len(CHECK_SHOWN):
        print(f"  my_choice() gives:   {top} {got[0]:.4f}   {below} {got[1]:.4f}")
    if why is not None:
        print(why)


if __name__ == "__main__":
    hand_check(compare="--compare" in sys.argv)
