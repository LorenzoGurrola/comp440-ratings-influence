"""
Part 4: what is shown.

    uv run python part4_shown.py

Two markets at social influence 0.5, both with the top_five recommender, as in the paper's two
experiments:

    "order does not matter"   position discount 1.0: an artist's place on the list does not
                              change its social weight; only its downloads do
    "sorted by count"         position discount 1.2, the model's default: each step down the
                              list divides an artist's social weight by 1.2

Needs Part 3's rule in choose.py; without it, it says so and stops. Prints one table of the five
measures, WORLDS worlds per row: the independent condition (Part 1's run: random_five at social
influence 0, the same worlds), then each market. Saves figures/part4_quality_vs_success.png, the
paper's Figure 3 for each market: an artist's share, and its rank, in the independent condition
against the same in each world of the market.
"""

import sys
from pathlib import Path

import choose
import measures
import plots
from recommender import random_five, top_five
from sim import simulate

WORLDS = 300   # enough to see the pattern; use 1000 for your final figures
SOCIAL_INFLUENCE = 0.5
CONDITIONS = {"order does not matter": 1.0, "sorted by count": 1.2}   # label -> position discount
FIGURES = Path(__file__).resolve().parent / "figures"


def main():
    if not choose.is_implemented():
        print("Part 4 needs Part 3's rule in choose.py, and it is not in yet; "
              "uv run python choose.py shows the hand check.")
        return 1

    independent = simulate(random_five, WORLDS, social_influence=0.0)
    shares_by_condition = {}
    for label, discount in CONDITIONS.items():
        shares_by_condition[label] = simulate(top_five, WORLDS, SOCIAL_INFLUENCE,
                                              position_discount=discount)
    print(f"The independent condition, then the two markets (top_five, social influence "
          f"{SOCIAL_INFLUENCE}); {WORLDS} worlds per row:")
    rows = [("independent condition", independent)] + list(shares_by_condition.items())
    measures.print_table(rows)

    path = plots.quality_vs_success(independent, shares_by_condition,
                                    FIGURES / "part4_quality_vs_success.png")
    print(f"\nSaved figures/{path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
