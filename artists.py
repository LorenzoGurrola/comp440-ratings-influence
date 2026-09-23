"""
The eleven artists and their hidden true popularity.

They live in this small file, rather than in sim.py, so that sim.py and choose.py can both
read them without importing each other. sim.py makes them available as sim.ARTISTS and
sim.TRUE_POPULARITY too.
"""

# Hidden true popularity: how much users like each artist when nobody sees any counts. These
# are the Spring 2024 notebook's numbers, loosely based on Billboard's greatest artists.
# Assumption (the follow-up): a student may change these numbers.
# A recommender must never read them: a real recommender cannot see true popularity.
TRUE_POPULARITY = {
    "Beatles": 100,
    "Taylor Swift": 90,
    "Mariah Carey": 90,
    "Drake": 70,
    "Katy Perry": 70,
    "Bruno Mars": 50,
    "Justin Bieber": 50,
    "Cher": 30,
    "Bon Jovi": 30,
    "Miles Davis": 20,
    "John Coltrane": 10,
}

# The artists, most popular first. Every array of shares in this repo has one column per
# artist, in this order. A recommender may use this list.
# Assumption (the follow-up): which artists exist, and how many.
ARTISTS = list(TRUE_POPULARITY)
