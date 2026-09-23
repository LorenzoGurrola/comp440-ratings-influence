"""
Part 2: the recommender on its own.

    uv run python part2_policy.py

The same users as Part 1, still ignoring the counts (social influence 0), but now every user is
shown the five most downloaded artists so far (top_five in recommender.py) instead of five random
ones.

Prints the five measures over WORLDS worlds and how many of the eleven artists have any
download in world 0. Saves figures/part2_strip.png, the same kind of figure as Part 1's.
"""

from pathlib import Path

import measures
import plots
from recommender import top_five
from sim import ARTISTS, simulate

WORLDS = 300   # enough to see the pattern in a few seconds; use 1000 for your final figures
FIGURES = Path(__file__).resolve().parent / "figures"


def main():
    shares = simulate(top_five, WORLDS, social_influence=0.0)
    measures.print_summary(f"top_five, social influence 0, {WORLDS} worlds:", shares)

    downloaded = sum(1 for share in shares[0] if share > 0)
    print(f"\nArtists with any download in world 0: {downloaded} of {len(ARTISTS)}")

    path = plots.strip_plot(shares, FIGURES / "part2_strip.png",
                            "Do identical worlds end the same way? "
                            "The top five shown, users ignore the counts")
    print(f"\nSaved figures/{path.name}")


if __name__ == "__main__":
    main()
