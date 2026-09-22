"""
Part 3: social influence.

    uv run python part3_influence.py

First checks that choose.py holds Part 3's rule. If choice_weights() does not give the hand
check's answer yet, it prints the hand check, says so in one line, and stops.

Then prints the five measures for the independent control (Part 1's run: random_five at social
influence 0, the same worlds) and for the top_five recommender at each social-influence level in
LEVELS, WORLDS worlds each. Saves figures/part3_gini.png and figures/part3_unpredictability.png:
each measure against social influence, with the independent control marked.
"""

import sys
from pathlib import Path

import choose
import measures
import plots
from policy import random_five, top_five
from sim import simulate

WORLDS = 300   # enough to see the pattern; use 1000 for your final figures
LEVELS = [0.0, 0.25, 0.5, 0.75, 1.0]   # social-influence levels, each from 0 to 1; yours to choose
FIGURES = Path(__file__).resolve().parent / "figures"


def main():
    if not choose.is_implemented():
        choose.hand_check()
        print("\nPart 3's rule is not in choose.py yet: choice_weights() does not give the hand "
              "check's A 0.6638, B 0.3362.")
        return 1

    control = measures.print_summary(
        f"Independent control: random_five, social influence 0, {WORLDS} worlds:",
        simulate(random_five, WORLDS, social_influence=0.0))

    ginis, unpredictabilities = [], []
    for level in LEVELS:
        print()
        result = measures.print_summary(f"top_five, social influence {level}, {WORLDS} worlds:",
                                        simulate(top_five, WORLDS, social_influence=level))
        ginis.append(result["mean_gini"])
        unpredictabilities.append(result["unpredictability"])

    gini_path = plots.line_plot(
        LEVELS, [ginis], FIGURES / "part3_gini.png", "social influence",
        "mean Gini of market shares", "Does inequality rise with social influence?",
        labels=["top_five recommender"], control=(0.0, control["mean_gini"]))
    unpredictability_path = plots.line_plot(
        LEVELS, [unpredictabilities], FIGURES / "part3_unpredictability.png", "social influence",
        "unpredictability (mean share difference between worlds)",
        "Does unpredictability rise with social influence?",
        labels=["top_five recommender"], control=(0.0, control["unpredictability"]))
    print(f"\nSaved figures/{gini_path.name} and figures/{unpredictability_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
