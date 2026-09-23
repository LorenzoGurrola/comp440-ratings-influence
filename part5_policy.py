"""
Part 5: your policy.

    uv run python part5_policy.py

Runs three policies at social influence 0.5, WORLDS worlds each: yours (my_policy in
my_policy.py), the shipped top_five, and random_five, the control. Prints one table of the five
measures, one row per policy, and saves figures/part5_policies.png: mean Gini, unpredictability
and fidelity, one bar per policy. Stops with a message if my_policy is not written yet, or if
Part 3's rule is not in choose.py.
"""

import sys
from pathlib import Path

import numpy as np

import choose
import measures
import plots
from my_policy import my_policy
from recommender import random_five, top_five
from sim import simulate

WORLDS = 300   # enough to see the pattern; use 1000 for your final figures
SOCIAL_INFLUENCE = 0.5
FIGURES = Path(__file__).resolve().parent / "figures"


def main():
    try:
        my_policy({}, np.random.default_rng(0))   # one call, as for a world's first user
    except NotImplementedError as error:
        print(f"my_policy is not written yet: {error}")
        return 1
    if not choose.is_implemented():
        print("Part 5 needs Part 3's rule in choose.py, and it is not in yet; "
              "uv run python choose.py shows the hand check.")
        return 1

    rows = []
    for name, policy in [("my_policy", my_policy), ("top_five", top_five),
                         ("random_five", random_five)]:
        rows.append((name, simulate(policy, WORLDS, SOCIAL_INFLUENCE)))
    print(f"Each policy at social influence {SOCIAL_INFLUENCE}; {WORLDS} worlds per row:")
    results = measures.print_table(rows)

    names = [name for name, _ in rows]
    path = plots.policy_bars(dict(zip(names, results)), FIGURES / "part5_policies.png")
    print(f"\nSaved figures/{path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
