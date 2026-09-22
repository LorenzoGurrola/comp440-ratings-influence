"""The instructor's Spring-2024 Colab notebook, kept for reference.

Source: "Simulation of Feedback Effects in Recommenders"
(Google Drive id 1B_DZK-Tlv6Duv5Al_r0Z7mdS8nwlFvx6).

The code below is the notebook's code cells verbatim, with three changes,
each marked with a  # PORT:  comment:

  1. `simple_rec_alg` truncates its result to NUM_RECS.  As saved, the notebook
     sorts every downloaded artist and pads to NUM_RECS but never truncates, so
     once six distinct artists have been downloaded `simulate_one_user` raises
     ValueError("Recommendation function must return exactly 5 recs").  The
     notebook's saved output is a completed 1000-world run, so the version that
     was executed must have truncated.  The docstring's step 2 says to truncate.
  2. The seaborn/pandas plotting import and `plot_results` are left in place but
     `plot_results` is not used by the driver (fig1 is drawn in figures.py).
  3. `simulate_all_worlds` takes a `verbose` flag so timing runs are quiet.

NUM_WORLDS / NUM_USERS / NUM_RECS are module-level globals, exactly as in the
notebook; the driver overrides them by assignment before calling.
"""

# Necessary modules
import copy
import numpy as np
import random
import string

# number of simulated worlds
NUM_WORLDS = 1000

# number of users per world
# for simplicity each user downloads one artist
NUM_USERS = 1000

# number of recommendations shown to each user
NUM_RECS = 5

# Mostly taken from https://www.billboard.com/charts/greatest-hot-100-artists/
# Relative "true" artist interest levels for different artists if
# social influence were not a factor in recommender systems.
#
# These should be secret. Your recommendation algorithm can't possible know
# this, so don't use it!
TRUE_ARTIST_POPULARITY = {
    'Beatles'       : 100,
    'Taylor Swift'  : 90,
    'Mariah Carey'  : 90,
    'Drake'         : 70,
    'Katy Perry'    : 70,
    'Bruno Mars'    : 50,
    'Justin Bieber' : 50,
    'Cher'          : 30,
    'Bon Jovi'      : 30,
    'Miles Davis'   : 20,
    'John Coltrane' : 10
}

# Simple list of artists. Your recommendation algorithm *can* know this!
ALL_ARTISTS = list(TRUE_ARTIST_POPULARITY)


def pick_from_weights(weight_dict):
  """
  Given a dictionary mapping keys to weights, returns one random key from
  the dictionary, but the randomness is weight by the values.
  """
  keys = list(weight_dict.keys())
  vals = [weight_dict[k] for k in keys]
  total = sum(vals)
  return random.choices(keys, weights=vals, k=1)[0]

def normalize_weights(weight_dict):
  """
  Normalies the weights in a weight dictionary so all the values sum to 1.0.
  """
  total = sum(weight_dict.values())
  return {k : v / total for (k, v) in weight_dict.items() }

def multiply_weights(weight_dict, factor):
  """
  Multiplies the weights in a dictionary by a constant value.
  """
  return { k : factor * v for (k, v) in weight_dict.items() }

def add_weights(weight_dict1, weight_dict2):
  return {
      k : (weight_dict1.get(k, 0.0) + weight_dict2.get(k, 0.0))
      for k in set(weight_dict1).union(weight_dict2)
  }


def simulate_one_user(downloads, rec_fn, social_influence: float):
  """
  One user selecting from recs represented as an artist -> downloads dict.
  """
  assert(social_influence >= 0.0)
  assert(social_influence <= 1.0)

  recs = rec_fn(downloads)
  if type(recs) is not list:
    raise ValueError(f"Recommendation function must return a list")
  if len(recs) != NUM_RECS:
    raise ValueError(f"Recommendation function must return exactly {NUM_RECS} recs")

  # Calculate rec weights
  rec_weights = {}
  for rank, artist in enumerate(recs):
    rank_penalty = 1.2 ** -rank   # rank 0 = 1.0, 1 = 0.8, etc.
    count = downloads.get(artist, 0) + 1 # add one to give undownloaded things a chance
    rec_weights[artist] = count * rank_penalty

  # Normalize social weights and true weights, then combine using influence factor
  social_weights = normalize_weights(rec_weights)
  true_weights = normalize_weights({ k : TRUE_ARTIST_POPULARITY[k] for k in recs })
  combined_weights = add_weights(
      multiply_weights(social_weights, social_influence),
      multiply_weights(true_weights, 1.0 - social_influence)
  )

  return pick_from_weights(combined_weights)


def simulate_one_world(rec_fn, social_influence: float):
  downloads = {}
  for _ in range(NUM_USERS):
    artist = simulate_one_user(downloads, rec_fn, social_influence)
    downloads[artist] = downloads.get(artist, 0) + 1
  return downloads


def simulate_all_worlds(rec_fn, social_influence: float, verbose=True):  # PORT: verbose
  results = { k : [] for k in ALL_ARTISTS }
  for u in range(NUM_WORLDS):
    if verbose and u % 100 == 0:
      print('simulating world', u)
    downloads = simulate_one_world(rec_fn, social_influence)
    downloads = normalize_weights(downloads)
    for k in results:
      results[k].append(downloads.get(k, 0.0))
  return results


def plot_results(results):
  import seaborn as sns
  import pandas as pd
  import matplotlib.pyplot as plt
  sns.set(rc={'figure.figsize':(12, 5)})
  plt.xticks(rotation=45)
  series = { k : pd.Series(results[k]) for k in ALL_ARTISTS}
  labels = { k : ('%s (%d)' % (k, TRUE_ARTIST_POPULARITY[k])) for k in ALL_ARTISTS }
  sns.stripplot({labels[k]: series[k] for k in ALL_ARTISTS},
                edgecolor='black', linewidth=1.0, size=2, alpha=0.1, color='gray')


def simple_rec_alg(download_counts):
  """
  Given download counts, return an ordered list of recommendations.
  """

  # Sort items by downloads, descending
  recs = sorted(list(download_counts), key=lambda k: download_counts[k], reverse=True)

  # If there are not enough recs, randomly add artists with 1 download
  while len(recs) < NUM_RECS:
    artist = random.choice(ALL_ARTISTS)  # randomly pick artist
    if artist not in recs:
      recs.append(artist)

  return recs[:NUM_RECS]   # PORT: truncation (docstring step 2); see module docstring


def simple_rec_alg_as_saved(download_counts):
  """simple_rec_alg exactly as saved in the notebook, with no truncation."""
  recs = sorted(list(download_counts), key=lambda k: download_counts[k], reverse=True)
  while len(recs) < NUM_RECS:
    artist = random.choice(ALL_ARTISTS)
    if artist not in recs:
      recs.append(artist)
  return recs


def random_rec_alg(download_counts):
  """Five uniformly random distinct artists, in random order."""
  return random.sample(ALL_ARTISTS, NUM_RECS)
