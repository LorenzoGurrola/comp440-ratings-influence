"""
Part 6: one assumption.

    uv run python part6_assumption.py

Until you delete the line that ends "delete this line when you start", this script prints
"Part 6 not started" and does nothing else. Once you start, it must:

  1. Rerun Part 3's sweep, top_five at each level in LEVELS with WORLDS worlds, twice: once
     with the model as it shipped ("before") and once with the one assumption you chose
     changed ("after").
  2. Print, for each level, the five measures before and after.
  3. Save figures/part6_trajectories.png: plots.trajectories() on the picks that
     simulate_with_picks() returns for top_five at social influence 0.75 with 12 worlds,
     your assumption changed.

Make the change in this file, so that sim.py, choose.py and policy.py stay as Parts 1 to 5
ran them. Pass a changed number to simulate() (position_discount, pseudo_count or users), or
write a changed policy here and pass it in. An assumption that lives in choose.py, such as
counts entering the choice linearly, is changed the same way: write the changed rule here as
a function and use it for the "after" runs only (choose.choice_weights = your_rule, then put
the original back), so that choose.py keeps the rule Part 3 checked.
"""

import sys
from pathlib import Path

import measures
import plots
from policy import top_five
from sim import simulate, simulate_with_picks

WORLDS = 300   # enough to see the pattern; use 1000 for your final numbers
LEVELS = [0.0, 0.25, 0.5, 0.75, 1.0]   # use the levels you chose in Part 3
FIGURES = Path(__file__).resolve().parent / "figures"


def main():
    print("Part 6 not started"); return 0  # delete this line when you start

    # The shape to follow, for the position discount (1.2 as shipped, 1.0 changed):
    # for level in LEVELS:
    #     measures.print_summary(f"before, social influence {level}:",
    #                            simulate(top_five, WORLDS, level, position_discount=1.2))
    #     measures.print_summary(f"after, social influence {level}:",
    #                            simulate(top_five, WORLDS, level, position_discount=1.0))
    # shares, picks = simulate_with_picks(top_five, 12, 0.75, position_discount=1.0)
    # plots.trajectories(picks, FIGURES / "part6_trajectories.png")

    return 0


if __name__ == "__main__":
    sys.exit(main())
