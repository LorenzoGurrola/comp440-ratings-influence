"""
The figures, in plain matplotlib. Each function saves one PNG to `path`, making the folder if
needed, and returns the path. Every figure has labeled axes, and its title is the question it
answers.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")   # draw straight to files; no window opens
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import rankdata

from artists import ARTISTS, TRUE_POPULARITY

TRUE = np.array([TRUE_POPULARITY[artist] for artist in ARTISTS], dtype=float)
ARTIST_LABELS = [f"{artist} ({TRUE_POPULARITY[artist]})" for artist in ARTISTS]


def save(fig, path):
    """Save `fig` as a PNG at `path` and close it. Returns the path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=120, bbox_inches="tight")   # "tight" keeps a legend below the axes
    plt.close(fig)
    return path


def strip_plot(shares, path, title):
    """One column per artist, one dot per world at the artist's share in that world, and a
    diamond at the artist's true share: its true popularity over the total of all eleven."""
    shares = np.asarray(shares)
    # Spread each column's dots sideways a little so they do not sit on top of each other.
    jitter = np.random.default_rng(0).uniform(-0.25, 0.25, size=shares.shape)
    fig, ax = plt.subplots(figsize=(11, 5))
    for i in range(len(ARTISTS)):
        ax.plot(i + jitter[:, i], shares[:, i], "o", color="C0", markersize=2, alpha=0.2)
    ax.plot(range(len(ARTISTS)), TRUE / TRUE.sum(), "D", color="C3", markersize=7,
            label="true popularity / total true popularity")
    ax.set_xticks(range(len(ARTISTS)), ARTIST_LABELS, rotation=45, ha="right")
    ax.set_xlabel("artist (true popularity)")
    ax.set_ylabel("share of the world's downloads\n(one dot per world)")
    ax.set_title(title)
    ax.legend()
    return save(fig, path)


def line_plot(x, ys, path, xlabel, ylabel, title, labels=None, control=None):
    """One line per series in `ys`, each against `x`, with `labels` naming the series.
    `control`, an (x, y) point, is drawn as a separate square labeled "independent control"."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for i, y in enumerate(ys):
        ax.plot(x, y, "o-", label=labels[i] if labels else None)
    if control is not None:
        ax.plot([control[0]], [control[1]], "s", color="black", markersize=8,
                label="independent control")
    ax.set_ylim(bottom=min(0, ax.get_ylim()[0]))   # start the y axis at 0
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if labels or control is not None:
        ax.legend()
    return save(fig, path)


def quality_vs_success(indep_shares, infl_shares_by_condition, path):
    """The paper's Figure 3 layout. One row per condition in `infl_shares_by_condition` (a dict
    label -> shares), two panels per row. Left: x is each artist's mean share in the independent
    condition, y its share in each world of the condition, one dot per artist per world. Right:
    the same with ranks, 1 = most downloaded; artists tied in a world share the average rank."""
    indep_mean = np.asarray(indep_shares).mean(axis=0)
    indep_rank = rankdata(-indep_mean)
    rows = len(infl_shares_by_condition)
    # sharey="col": every row's share panel has the same y axis, and so does every rank panel.
    fig, axes = plt.subplots(rows, 2, figsize=(11, 4.3 * rows), squeeze=False, sharey="col")
    jitter = np.random.default_rng(0)   # spreads the rank dots so they do not overlap
    for row, (label, shares) in enumerate(infl_shares_by_condition.items()):
        shares = np.asarray(shares)
        worlds = len(shares)
        ranks = np.array([rankdata(-world) for world in shares])
        left, right = axes[row]
        left.plot(np.tile(indep_mean, worlds), shares.ravel(), "o", color="C0",
                  markersize=3, alpha=0.1)
        left.set_xlabel("share in the independent condition (mean over its worlds)")
        left.set_ylabel("share in one world of this condition")
        left.set_title(f"{label}: share")
        right.plot(np.tile(indep_rank, worlds) + jitter.uniform(-0.2, 0.2, ranks.size),
                   ranks.ravel() + jitter.uniform(-0.2, 0.2, ranks.size),
                   "o", color="C0", markersize=3, alpha=0.1)
        right.set_xlim(len(ARTISTS) + 0.5, 0.5)   # rank 1 at the right and at the top, as
        right.set_ylim(len(ARTISTS) + 0.5, 0.5)   # the largest shares are in the share panel
        right.set_xticks(range(1, len(ARTISTS) + 1))
        right.set_yticks(range(1, len(ARTISTS) + 1))
        right.set_xlabel("rank in the independent condition (1 = most downloaded)")
        right.set_ylabel("rank in one world of this condition")
        right.set_title(f"{label}: rank")
    fig.suptitle("Does quality still predict success? Quality is an artist's share "
                 "in the independent condition.")
    return save(fig, path)


def trajectories(picks_by_world, path, artist="Beatles"):
    """Two panels on a log x axis, one line per world. Left: the cumulative share of the
    artist who leads that world at the end, as users arrive. Right: `artist`'s cumulative
    share in the same worlds."""
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
    for w, picks in enumerate(picks_by_world):
        users = np.arange(1, len(picks) + 1)
        leader = max(ARTISTS, key=picks.count)   # the most downloaded artist at the end
        style = "-" if w < 10 else "--"          # matplotlib has ten colors; dashed after that
        left.plot(users, np.cumsum([pick == leader for pick in picks]) / users, style,
                  label=f"world {w}: {leader}")
        right.plot(users, np.cumsum([pick == artist for pick in picks]) / users, style)
    left.set_title("each world's leader at the end")
    right.set_title(f"{artist} (true popularity {TRUE_POPULARITY[artist]})")
    fig.legend(title="world: its leader at the end", loc="upper center",
               bbox_to_anchor=(0.5, 0), ncol=6, fontsize="small")   # below both panels
    for ax in (left, right):
        ax.set_xscale("log")
        ax.set_ylim(0, 1)
        ax.set_xlabel("users who have arrived (log scale)")
    left.set_ylabel("cumulative share of the world's downloads")
    fig.suptitle("When does a world lock in, and can a mediocre artist hold the lead?")
    return save(fig, path)


def recommender_bars(results_by_recommender, path):
    """Three panels: mean Gini, unpredictability and fidelity, one bar per recommender, each value
    printed at the end of its bar. `results_by_recommender` maps a recommender's name to the dict
    measures.summary() returns."""
    names = list(results_by_recommender)
    panels = [("mean_gini", "mean Gini (inequality within a world)"),
              ("unpredictability", "unpredictability (difference between worlds)"),
              ("fidelity", "fidelity (rank correlation with true popularity)")]
    fig, axes = plt.subplots(1, 3, figsize=(14, 1.5 + 0.6 * len(names)))
    for ax, (key, label) in zip(axes, panels):
        values = [results_by_recommender[name][key] for name in names]
        ax.barh(names, values, color="C0")
        for i, value in enumerate(values):
            ax.text(value, i, f" {value:.3f}", va="center")
        ax.margins(x=0.25)   # room for the numbers at the ends of the bars
        ax.invert_yaxis()    # the first recommender at the top
        ax.set_xlabel(label)
    axes[0].set_ylabel("recommender")
    fig.suptitle("What does each recommender rule cost and buy?")
    return save(fig, path)
