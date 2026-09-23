"""
Part 3: social influence.

    uv run python part3_influence.py

First checks that my_choice.py holds a rule that passes the hand check: it runs, and it returns
chances that are zero or more and sum to 1 (hand_check.passes()). If not, it says why in one
line and stops.

Then prints one table of the five measures, WORLDS worlds per row: first the independent control
(Part 1's run: random_five with the shipped choice rule at social influence 0, the same worlds),
then the top_five recommender with your rule at each social-influence level in LEVELS. Saves
figures/part3_gini.png and figures/part3_unpredictability.png: each measure against social
influence, with the independent control marked.

Last, it prints your four Part 0 predictions as WRITEUP.md has them, for the step that asks which
you would now change.
"""

import sys
from pathlib import Path

import hand_check
import measures
import plots
from choose import independent_choice
from my_choice import my_choice
from recommender import random_five, top_five
from run_all import slots
from sim import simulate

WORLDS = 300   # enough to see the pattern; use 1000 for steadier numbers
LEVELS = [0.0, 0.25, 0.5, 0.75, 1.0]   # social-influence levels, each from 0 to 1; yours to choose
FIGURES = Path(__file__).resolve().parent / "figures"


def print_predictions():
    """Print the four Part 0 slots of WRITEUP.md, each label and then the answer as written."""
    print("\nYour Part 0 predictions, as WRITEUP.md has them:")
    predictions = [(label, answer) for part, label, answer in slots() if part == 0]
    if not predictions:
        print("  (no Part 0 slots found in WRITEUP.md)")
    for label, answer in predictions:
        print(f"  {label}")
        print(f"      {answer}")


def main():
    why = hand_check.problem()
    if why is not None:
        print(f"Part 3 needs a rule in my_choice.py that passes the hand check: {why}")
        return 1

    rows = [("independent control",
             simulate(random_five, independent_choice, WORLDS, social_influence=0.0))]
    for level in LEVELS:
        rows.append((f"social influence {level}",
                     simulate(top_five, my_choice, WORLDS, social_influence=level)))
    print(f"The independent control (random_five, social influence 0), then top_five at each "
          f"level; {WORLDS} worlds per row:")
    results = measures.print_table(rows)
    control = results[0]
    ginis = [result["mean_gini"] for result in results[1:]]
    unpredictabilities = [result["unpredictability"] for result in results[1:]]

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
    print_predictions()
    return 0


if __name__ == "__main__":
    sys.exit(main())
