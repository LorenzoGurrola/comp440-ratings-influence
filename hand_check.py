"""
The two-artist hand check for Part 3.

    uv run python hand_check.py --case    the case alone, before you say what your rule should do
    uv run python hand_check.py           the case, then each step of your rule on it

Prints the case, then each step of your rule computed on it, one row per step, with the label
the rule gave that step (step() in choose.py), and last the chances my_choice() returns. With
--case it prints the case and nothing else, so that you can say first which artist your rule
should favor, and by how much. Then you read the rows and say whether they match what you said.
There is no single right answer and nothing to work out by hand: the check is whether the code
does what you meant.

passes() is the gate for Parts 3 and 4: my_choice is written, runs on the case, and returns two
chances that are zero or more and sum to 1. problem() says in plain words why it does not pass.
Nothing in this file changes.
"""

import math
import sys

import choose
from artists import TRUE_POPULARITY
from my_choice import my_choice

# The case: two artists, Bruno Mars at the top of the list (position 0) with 3 downloads and
# Justin Bieber below it (position 1) with none, so Justin Bieber is missing from the counts.
CHECK_SHOWN = ["Bruno Mars", "Justin Bieber"]
CHECK_COUNTS = {"Bruno Mars": 3}
CHECK_SOCIAL_INFLUENCE = 0.5

NOT_WRITTEN = "my_choice is not written yet."
NORMALIZE_HINT = "normalize() in choose.py scales a list of weights so they sum to 1."
LAST_ROW = "chances my_choice returns"
LABEL_WIDTH = 56   # a longer label goes on a line of its own, above its numbers
COLUMN_WIDTH = 15


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


def recorded_steps():
    """Run my_choice on the case with its steps recorded. Returns (steps, chances, error): the
    labeled steps in order, as (label, values); the chances, or None; and the error my_choice
    stopped with, or None."""
    choose._STEPS = []
    try:
        got, error = chances(), None
    except Exception as stopped:   # the steps before the error are still worth showing
        got, error = None, stopped
    finally:
        steps, choose._STEPS = choose._STEPS, None
    return steps, got, error


def row(label, values):
    """One row of the table: the label, then one number per artist, 4 decimals."""
    try:
        cells = [f"{float(value):.4f}" for value in values]
    except TypeError:             # a single number, not a list
        try:
            cells = [f"{float(values):.4f}"]
        except (TypeError, ValueError):
            cells = [repr(values)]
    except ValueError:
        cells = [repr(values)]
    numbers = "".join(f"{cell:>{COLUMN_WIDTH}}" for cell in cells)
    if len(label) > LABEL_WIDTH:
        return f"  {label}\n  {'':<{LABEL_WIDTH}}{numbers}"
    return f"  {label:<{LABEL_WIDTH}}{numbers}"


def print_case():
    """Print the two-artist case: who is shown where, with how many downloads, and the level."""
    top, below = CHECK_SHOWN
    print(f"Hand check, at social influence {CHECK_SOCIAL_INFLUENCE}:")
    print(f"  {top:<14} at the top of the list (position 0), {CHECK_COUNTS.get(top, 0)} downloads, "
          f"true popularity {TRUE_POPULARITY[top]}")
    print(f"  {below:<14} below it (position 1), no downloads, "
          f"true popularity {TRUE_POPULARITY[below]}")


def hand_check():
    """Print the case, each labeled step of my_choice on it, and the chances it returns."""
    print_case()
    steps, got, error = recorded_steps()
    if isinstance(error, NotImplementedError):
        print(NOT_WRITTEN)
        return
    print("\nYour rule, step by step, on this case:")
    print(f"  {'':<{LABEL_WIDTH}}" + "".join(f"{name:>{COLUMN_WIDTH}}" for name in CHECK_SHOWN))
    for label, values in steps:
        print(row(label, values))
    if got is not None:
        print(row(LAST_ROW, got))
    if not steps:
        print("my_choice has no labeled steps, so only the chances it returns are shown.")
    why = problem()
    if why is not None:
        print(why)


if __name__ == "__main__":
    if "--case" in sys.argv:
        print_case()
    else:
        hand_check()
