"""
A recommender maps the world's download counts so far to two things: the five artists a user is
shown, in display order, and the download counts shown with them. Position 0 is the top of the
list. The choice rule sees only what the recommender shows.
"""

from sim import ARTISTS, NUM_SHOWN


def top_five(counts, rng):
    """The shipped recommender: the five most downloaded artists, most downloaded first.

    `counts` lists only artists with a download, in the order of their first download, and
    ties keep that order. Until five artists have a download, random artists fill the list.
    It shows the real download counts with the artists, so it returns `counts` unchanged.
    """
    shown = sorted(counts, key=lambda artist: counts[artist], reverse=True)[:NUM_SHOWN]
    while len(shown) < NUM_SHOWN:
        artist = ARTISTS[rng.integers(len(ARTISTS))]   # any artist, at random
        if artist not in shown:
            shown.append(artist)
    return shown, counts


def random_five(counts, rng):
    """The control: five different artists picked at random, in random order.

    It ignores `counts` when it picks who to show, so every artist is equally likely to be
    shown to every user. It shows the real download counts with the artists, so it returns
    `counts` unchanged.
    """
    shuffled = list(ARTISTS)
    rng.shuffle(shuffled)
    return shuffled[:NUM_SHOWN], counts
