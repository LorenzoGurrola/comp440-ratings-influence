"""
Follow-up: what is shown. Optional, not graded.

    uv run python followup_shown.py

Two markets at social influence 0.5. Both show the five most downloaded artists (top_five in
recommender.py) and both use your Part 3 rule, as in the paper's two experiments:

    "random order"      the five are shown in a random order, so where an artist sits on the
                        list says nothing about its downloads (the paper's experiment 1)
    "sorted by count"   the five are shown most downloaded first (the paper's experiment 2)

Needs Part 3's rule in my_choice.py; without it, it says so and stops. Prints one table of the five
measures, WORLDS worlds per row: the independent condition (Part 1's run: random_five with the
shipped choice rule at social influence 0, the same worlds), then each market. Saves
figures/followup_quality_vs_success.png, the paper's Figure 3 for each market: an artist's share,
and its rank, in the independent condition against the same in each world of the market.
"""

import sys
from pathlib import Path

import hand_check
import measures
import plots
from choose import independent_choice
from my_choice import my_choice
from recommender import random_five, top_five
from sim import simulate

WORLDS = 300   # enough to see the pattern; use 1000 if you want steadier numbers
SOCIAL_INFLUENCE = 0.5
FIGURES = Path(__file__).resolve().parent / "figures"


def shuffled_top_five(counts, rng):
    """The same five artists top_five shows, in a random order, with the same counts."""
    shown, shown_counts = top_five(counts, rng)
    rng.shuffle(shown)
    return shown, shown_counts


CONDITIONS = {"random order": shuffled_top_five, "sorted by count": top_five}


def main():
    if not hand_check.passes():
        print("This follow-up needs Part 3's rule in my_choice.py, and the hand check does not "
              "pass yet; uv run python hand_check.py shows the case.")
        return 1

    independent = simulate(random_five, independent_choice, WORLDS, social_influence=0.0)
    shares_by_condition = {}
    for label, recommender in CONDITIONS.items():
        shares_by_condition[label] = simulate(recommender, my_choice, WORLDS, SOCIAL_INFLUENCE)
    print(f"The independent condition, then the two markets (the top five shown, social influence "
          f"{SOCIAL_INFLUENCE}); {WORLDS} worlds per row:")
    rows = [("independent condition", independent)] + list(shares_by_condition.items())
    measures.print_table(rows)

    path = plots.quality_vs_success(independent, shares_by_condition,
                                    FIGURES / "followup_quality_vs_success.png")
    print(f"\nSaved figures/{path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
