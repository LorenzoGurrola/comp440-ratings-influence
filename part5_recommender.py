"""
Part 5: your recommender.

    uv run python part5_recommender.py

Runs three recommenders at social influence 0.5, WORLDS worlds each, all with your Part 3 choice
rule: yours (my_recommender in my_recommender.py), the shipped top_five, and random_five, the
control. Prints one table of the five measures, one row per recommender, and saves
figures/part5_recommenders.png: mean Gini, unpredictability and fidelity, one bar per recommender.
Stops with a message if my_recommender is not written yet, or if Part 3's rule is not in
my_choice.py.
"""

import sys
from pathlib import Path

import numpy as np

import hand_check
import measures
import plots
from my_choice import my_choice
from my_recommender import my_recommender
from recommender import random_five, top_five
from sim import simulate

WORLDS = 300   # enough to see the pattern; use 1000 for your final figures
SOCIAL_INFLUENCE = 0.5
FIGURES = Path(__file__).resolve().parent / "figures"


def main():
    try:
        my_recommender({}, np.random.default_rng(0))   # one call, as for a world's first user
    except NotImplementedError as error:
        print(f"my_recommender is not written yet: {error}")
        return 1
    if not hand_check.passes():
        print("Part 5 needs Part 3's rule in my_choice.py, and the hand check does not pass yet; "
              "uv run python hand_check.py shows the case.")
        return 1

    rows = []
    for name, recommender in [("my_recommender", my_recommender), ("top_five", top_five),
                              ("random_five", random_five)]:
        rows.append((name, simulate(recommender, my_choice, WORLDS, SOCIAL_INFLUENCE)))
    print(f"Each recommender at social influence {SOCIAL_INFLUENCE}; {WORLDS} worlds per row:")
    results = measures.print_table(rows)

    names = [name for name, _ in rows]
    path = plots.recommender_bars(dict(zip(names, results)), FIGURES / "part5_recommenders.png")
    print(f"\nSaved figures/{path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
