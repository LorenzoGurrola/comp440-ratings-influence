"""
A policy maps the world's download counts so far to the five artists a user is shown, in
display order. Position 0 is the top of the list.
"""

from sim import ARTISTS, NUM_SHOWN


def top_five(counts, rng):
    """The shipped recommender: the five most downloaded artists, most downloaded first.

    `counts` lists only artists with a download, in the order of their first download, and
    ties keep that order. Until five artists have a download, random artists fill the list.
    """
    shown = sorted(counts, key=lambda artist: counts[artist], reverse=True)[:NUM_SHOWN]
    while len(shown) < NUM_SHOWN:
        artist = ARTISTS[rng.integers(len(ARTISTS))]   # any artist, at random
        if artist not in shown:
            shown.append(artist)
    return shown


def random_five(counts, rng):
    """The control: five different artists picked at random, in random order.

    It ignores `counts`, so every artist is equally likely to be shown to every user.
    """
    shuffled = list(ARTISTS)
    rng.shuffle(shuffled)
    return shuffled[:NUM_SHOWN]
