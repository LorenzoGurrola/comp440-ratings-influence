"""
Follow-up: one assumption. Optional, not graded.

    uv run python followup_assumption.py

Until you delete the line that ends "delete this line when you start", this script prints
"Follow-up not started" and does nothing else. Once you start, it must:

  1. Rerun Part 3's sweep, top_five with your choice rule at each level in LEVELS with WORLDS
     worlds, twice: once with the model as it shipped ("before") and once with the one assumption
     you chose changed ("after").
  2. Print one table of the five measures (measures.print_table), with a "before" row and an
     "after" row for each level.
  3. Save figures/followup_trajectories.png: plots.trajectories() on the picks that
     simulate_with_picks() returns for top_five at social influence 0.75 with 12 worlds,
     your assumption changed.

Make the change in this file, so that sim.py, choose.py, my_choice.py and recommender.py stay as
Parts 1 to 4 ran them. Where the change goes depends on the assumption:

  * users per world: pass users= to simulate(), as the example below does.
  * something about what the recommender shows, including which counts it shows: write a changed
    recommender in this file, and pass it to simulate() for the "after" runs.
  * something inside your choice rule, such as the 1.2 position discount, the +1, counts
    entering the choice linearly, or the true popularities: copy my_choice() into this file
    under a new name, make the one change in the copy, and pass the copy to simulate() for the
    "after" runs. my_choice.py itself keeps the rule Part 3 checked.
"""

import sys
from pathlib import Path

import measures
import plots
from my_choice import my_choice
from recommender import top_five
from sim import simulate, simulate_with_picks

WORLDS = 300   # enough to see the pattern; use 1000 if you want steadier numbers
LEVELS = [0.0, 0.25, 0.5, 0.75, 1.0]   # the levels Part 3 ran
FIGURES = Path(__file__).resolve().parent / "figures"


def main():
    print("Follow-up not started"); return 0  # delete this line when you start

    # The shape to follow, for users per world (1,000 as shipped, 36 for a classroom-sized
    # market: 12 people choosing 3 times):
    # rows = []
    # for level in LEVELS:
    #     before = simulate(top_five, my_choice, WORLDS, level, users=1000)
    #     after = simulate(top_five, my_choice, WORLDS, level, users=36)
    #     rows += [(f"before, {level}", before), (f"after, {level}", after)]
    # measures.print_table(rows)
    # shares, picks = simulate_with_picks(top_five, my_choice, 12, 0.75, users=36)
    # plots.trajectories(picks, FIGURES / "followup_trajectories.png")

    return 0


if __name__ == "__main__":
    sys.exit(main())
