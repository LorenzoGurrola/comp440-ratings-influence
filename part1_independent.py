"""
Part 1: users on their own.

    uv run python part1_independent.py

Runs the market as it ships: every user is shown five artists picked at random (random_five in
policy.py) and picks by true popularity alone, because choose.py ignores the counts (social
influence 0). This is the independent condition, the control for the later parts.

Prints the five measures over WORLDS worlds; then world 0's share for each artist and world 0's
Gini, the number to recompute by hand (the formula is at the top of measures.py).
Saves figures/part1_strip.png: one column per artist, one dot per world.
"""

from pathlib import Path

import measures
import plots
from policy import random_five
from sim import ARTISTS, simulate

WORLDS = 300   # enough to see the pattern in a few seconds; use 1000 for your final figures
FIGURES = Path(__file__).resolve().parent / "figures"


def main():
    shares = simulate(random_five, WORLDS, social_influence=0.0)
    measures.print_summary(f"random_five, social influence 0, {WORLDS} worlds:", shares)

    print()
    print("World 0, each artist's share of the world's downloads:")
    for artist, share in zip(ARTISTS, shares[0]):
        print(f"  {artist:<14} {share:.3f}")
    print(f"World 0's Gini: {measures.gini(shares[0]):.3f}")

    path = plots.strip_plot(shares, FIGURES / "part1_strip.png",
                            "Do identical worlds end the same way? "
                            "Five random artists shown, users ignore the counts")
    print(f"\nSaved figures/{path.name}")


if __name__ == "__main__":
    main()
