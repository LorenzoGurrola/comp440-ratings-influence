# Feedback-effects simulation: port, timings and measurements

Exploratory measurement for a planning document. Everything here is a number out of the simulation; nothing is student-facing and nothing is a claim about the class activity.

Scratchpad path removed; the files listed below sit next to this report.

## 0. Files

- `sim_original.py` — the instructor's Colab code cells, kept verbatim for reference.
- `sim.py` — the numpy port, the policies, and the measures.
- `check_agreement.py` → `check_agreement.json` — agreement check, timings, world-count stability.
- `run_experiments.py` → `results.json`, `figdata.npz` — experiments 4a–4e.
- `figures.py` → `fig1`–`fig6` PNGs.
- `make_report.py` → this file. Every number below is read from the JSON, not retyped.

## 1. What the source notebook actually does

Extracted from the Drive copy of "Simulation of Feedback Effects in Recommenders" (id `1B_DZK-Tlv6Duv5Al_r0Z7mdS8nwlFvx6`), 14 cells, 6 of them code. The mechanics are as given in the task and are preserved exactly.

Two things about the source worth recording, because both drive the results:

1. **`simple_rec_alg` never truncates, and does not need to.** As saved it sorts every downloaded artist by count and pads to 5, with no truncation step, so on its face it would return more than 5 recs and trip `simulate_one_user`'s `ValueError`. It never does, because the padding only runs while fewer than 5 artists have been downloaded, and only a recommended artist can be downloaded. Once 5 distinct artists have downloads, the rec list is exactly those 5 forever and no sixth artist can ever enter. Verified: 20 worlds at 1000 users, all 20 ended with exactly 5 artists having any downloads. Adding `recs[:NUM_RECS]` is therefore a no-op — verified bit-for-bit on a seeded world — and the port keeps it only as documentation.
2. **So 6 of the 11 artists get a share of exactly 0 in every world**, under every top-5-by-count setting, at every level of social influence including 0. This is the single largest driver of every inequality number below.

## 2. Agreement between the pure-Python original and the numpy port

Both at social influence 0.5, `simple_rec_alg`, 1000 users, 200 worlds. The original is one run (seed 2024); the port is 8 independent seeds, so the spread column is the port's own Monte-Carlo noise at 200 worlds. `z` is how many of those standard deviations the original sits from the port's mean.

| measure | original (200 worlds) | port: mean of 8 seeds | port sd over seeds | port min–max | z |
| --- | --- | --- | --- | --- | --- |
| mean Gini | 0.6805 | 0.6792 | 0.0035 | 0.6742 – 0.6850 | 0.38 |
| mean share of the top artist | 0.3693 | 0.3670 | 0.0052 | 0.3595 – 0.3750 | 0.44 |
| mean Beatles share | 0.1998 | 0.1923 | 0.0126 | 0.1781 – 0.2136 | 0.60 |
| unpredictability U | 0.1014 | 0.1012 | 0.0022 | 0.0964 – 0.1039 | 0.08 |
| mean Spearman rho | 0.3888 | 0.3824 | 0.0277 | 0.3430 – 0.4384 | 0.23 |
| fraction of worlds Beatles #1 | 0.3200 | 0.3187 | 0.0381 | 0.2750 – 0.3900 | 0.03 |
| artists with any download | 5.0000 | 5.0000 | 0.0000 | 5.0000 – 5.0000 | 0.00 |

Largest |z| is 0.60. The two implementations agree distributionally; nothing is outside the noise the port shows against itself.

## 3. Timings

Single core, Python 3.11, numpy 2.x, in this container.

| run | seconds |
| --- | --- |
| original, 100 worlds x 1000 users | 1.02 |
| original, 200 worlds x 1000 users | 2.12 |
| **original, 1000 x 1000 (extrapolated x10 from the 100-world run)** | **10.2** |
| port, 100 worlds x 1000 users | 0.13 |
| port, 300 worlds x 1000 users | 0.23 |
| **port, 1000 x 1000** | **0.74** |

Speedup at 1000 x 1000: **14x** (10.2 s to 0.74 s). The original is faster than it looks because of the lock-in above: its dictionaries only ever hold 5 artists. The port advances all worlds together, one arriving user at a time, so its cost is dominated by the 1000 sequential steps rather than by the number of worlds — 10x the worlds costs only 5.5x the time. No multiprocessing was needed; the whole experiment suite below runs in 13 seconds.

## 4. How many worlds are needed

Five independent seeds at each world count, social influence 0.5, `simple_rec_alg`, 1000 users. The number that matters is the spread across seeds: that is how far one run of N worlds can land from another.

| measure | 100 worlds: mean (sd over 5 seeds) | 300 worlds: mean (sd over 5 seeds) | 1000 worlds: mean (sd over 5 seeds) |
| --- | --- | --- | --- |
| mean Gini | 0.6791 (0.0033) | 0.6792 (0.0014) | 0.6791 (0.0010) |
| unpredictability U | 0.1020 (0.0021) | 0.1013 (0.0012) | 0.1011 (0.0007) |
| mean Spearman rho | 0.3724 (0.0255) | 0.3852 (0.0134) | 0.3861 (0.0085) |
| mean top-artist share | 0.3658 (0.0036) | 0.3663 (0.0033) | 0.3665 (0.0015) |
| mean Beatles share | 0.1840 (0.0162) | 0.1988 (0.0090) | 0.1983 (0.0054) |
| fraction Beatles #1 | 0.3060 (0.0385) | 0.3193 (0.0281) | 0.3340 (0.0175) |

Gini, U, and top-artist share are already stable at 100 worlds (seed-to-seed sd 0.003 or less). The two fidelity measures are not: at 300 worlds the fraction of worlds Beatles finishes #1 still moves +/- 0.028 between seeds, and mean Spearman +/- 0.013. Since the port costs under a second per run, **everything in section 6 was run at 1000 worlds rather than the 300 the task allowed**, which halves that: +/- 0.018 on Beatles-#1 and +/- 0.009 on Spearman. Even at 1000 worlds, treat the "Beatles #1" and "accidental hit" columns as +/- 0.015 (one standard error). A separate check of 10 seeds at 1000 worlds, social influence 0.5, gave Beatles-#1 values of 0.289–0.332 (mean 0.318, sd 0.014, matching the binomial 0.015); the headline seed below happens to sit at the low end, 0.289.

## 5. Measures

- **Gini** — Gini coefficient of the 11 artists' final market shares inside one world, averaged over worlds. The 6 zero-share artists are included, as they must be. For reference the Gini of the true popularity vector itself is 0.301.
- **U (unpredictability)** — Salganik, Dodds & Watts: for each artist, the mean absolute difference in market share between all pairs of worlds; then averaged over the 11 artists.
- **Spearman rho** — rank correlation between final share and true popularity within a world (average ranks for ties, and there are many: the 6 zero-share artists all tie), averaged over worlds.
- **Beatles #1** — fraction of worlds in which Beatles (true popularity 100) finishes with strictly the largest share. Exact ties for first are counted for nobody; they are rare (under 0.01 except at 50 users, where they are 0.051).
- **accidental hit** — fraction of worlds in which an artist with true popularity <= 30 (Cher, Bon Jovi, Miles Davis, John Coltrane) finishes strictly first.
- **leader share** — the largest share in a world, averaged over worlds. Reported because it is the quantity the strip plot is about.
- **artists with any download** — mean number of the 11 artists with a nonzero final share.

## 6a. Social influence sweep, top-5 recommender

1000 worlds, 1000 users, rank-penalty base 1.2, seed 20260922.

| social influence | Gini (sd) | U | Spearman rho (sd) | Beatles #1 | accidental hit | leader share (sd) | artists with any download |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | 0.640 (0.030) | 0.0876 | 0.482 (0.255) | 0.551 | 0.000 | 0.297 (0.039) | 5.00 |
| 0.25 | 0.657 (0.030) | 0.0914 | 0.448 (0.254) | 0.477 | 0.000 | 0.324 (0.041) | 5.00 |
| 0.5 | 0.679 (0.030) | 0.1009 | 0.388 (0.265) | 0.289 | 0.003 | 0.365 (0.051) | 5.00 |
| 0.75 | 0.723 (0.030) | 0.1229 | 0.263 (0.284) | 0.166 | 0.161 | 0.469 (0.070) | 5.00 |
| 0.9 | 0.783 (0.027) | 0.1418 | 0.156 (0.291) | 0.124 | 0.275 | 0.607 (0.087) | 5.00 |
| 1.0 | 0.842 (0.027) | 0.1555 | 0.013 (0.309) | 0.101 | 0.342 | 0.738 (0.104) | 4.85 |

Gini rises from 0.640 to 0.842 and U from 0.0876 to 0.1555 across the sweep. Fidelity falls monotonically on all three fidelity measures: Spearman 0.482 to 0.013, Beatles-#1 0.551 to 0.101, accidental hits 0.000 to 0.342.

## 6b. The independent-world control

Social influence 0, random-5 recommender (no counts shown, no popularity ordering), against social influence 0 with the top-5 recommender.

| condition | Gini (sd) | U | Spearman rho (sd) | Beatles #1 | accidental hit | leader share (sd) | artists with any download |
| --- | --- | --- | --- | --- | --- | --- | --- |
| random-5, influence 0 | 0.278 (0.015) | 0.0099 | 0.977 (0.016) | 0.599 | 0.000 | 0.157 (0.009) | 11.00 |
| top-5 by count, influence 0 | 0.640 (0.030) | 0.0876 | 0.482 (0.255) | 0.551 | 0.000 | 0.297 (0.039) | 5.00 |

This is the largest gap anywhere in the measurements, and social influence is 0 on both rows. Gini 0.278 vs 0.640, U 0.0099 vs 0.0876, Spearman 0.977 vs 0.482. The recommender alone — with users choosing purely on true preference — produces most of the inequality and most of the unpredictability that the sweep in 6a then adds to. Under random-5 all 11 artists get downloads and the mean shares track the true popularity vector to within 0.012 per artist (largest gap Beatles, true share 0.164 vs realised 0.153; the small bias toward the unpopular artists is the 5-of-11 subsetting: an artist is only ever compared against 4 others, not 10).

## 6c. Presentation order, social influence 0.5, top-5 recommender

Rank penalty `base ** -rank` applied to the rec weight. Base 1.0 removes the position effect entirely (counts visible, order irrelevant); 1.2 is the notebook default; 1.5 is a strong ordering effect.

| rank-penalty base | Gini (sd) | U | Spearman rho (sd) | Beatles #1 | accidental hit | leader share (sd) | artists with any download |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 (no position effect) | 0.647 (0.030) | 0.0981 | 0.378 (0.266) | 0.393 | 0.000 | 0.311 (0.042) | 5.00 |
| 1.2 (notebook default) | 0.679 (0.030) | 0.1009 | 0.388 (0.265) | 0.289 | 0.003 | 0.365 (0.051) | 5.00 |
| 1.5 (strong) | 0.706 (0.029) | 0.1058 | 0.408 (0.254) | 0.240 | 0.034 | 0.429 (0.058) | 5.00 |

The position effect is worth 0.059 of Gini and 0.0077 of U between base 1.0 and 1.5, against the 0.363 of Gini that the recommender's top-5 structure contributes on its own (6b). Accidental hits go 0.000 / 0.003 / 0.034: at base 1.0 a low-popularity artist never finishes first in 1000 worlds; at base 1.5 it happens in 3.4% of them. Mean Spearman moves very little (0.378 to 0.408) while Beatles-#1 falls (0.393 to 0.240) — a stronger top-slot advantage makes whoever is leading lead harder, which raises the leader's share (0.311 to 0.429) without making the leader more often the right artist.

## 6d. Recommender policies, social influence 0.5, base 1.2

Exactly what each one does:

- **random-5** — five uniformly random distinct artists in random order. Counts are not used for selection or ordering, but the drawn artists' real counts are still what the user sees, so social influence still operates.
- **top-5 by count** — the notebook's `simple_rec_alg`.
- **damped (K=20)** — score `(count + K/A) / (n + K)`, with `A` = 11 artists, `n` = downloads so far in that world, `K` = 20 pseudo-observations spread uniformly over the 11 artists. Ranking is by that score, and the rec **displays** `n * score` in place of the raw count, so what the user sees is shrunk toward the equal-share value `n/A`. Note that the score is strictly increasing in the raw count for fixed `n`, so **the ordering is identical to top-5 by count** (verified on 2000 random count vectors at n = 10, 100 and 1000); only the displayed numbers change. And with K = 20 against n = 1000 the shrinkage is small: the shown count works out to `0.980 * count + 1.78` at n = 1000 and `0.643 * count + 1.17` at n = 36. In practice this policy behaves like raising the +1 pseudo-count to roughly +2.8, which is why its numbers are nearly identical to top-5 by count.
- **top-4 + 1 random** — the top 4 by count, plus one uniformly random artist from the other 7, placed last (so it also carries the largest rank penalty).
- **top-5, order shuffled** — the same top-5 set, with its real counts shown, but presented in a fresh random order for every user: counts visible, ranking hidden.

| policy | Gini (sd) | U | Spearman rho (sd) | Beatles #1 | accidental hit | leader share (sd) | artists with any download |
| --- | --- | --- | --- | --- | --- | --- | --- |
| random-5 | 0.245 (0.030) | 0.0185 | 0.906 (0.054) | 0.420 | 0.000 | 0.153 (0.013) | 11.00 |
| top-5, order shuffled | 0.646 (0.030) | 0.0975 | 0.386 (0.256) | 0.423 | 0.000 | 0.311 (0.042) | 5.00 |
| top-4 + 1 random | 0.655 (0.023) | 0.0993 | 0.633 (0.207) | 0.294 | 0.005 | 0.384 (0.051) | 10.95 |
| top-5 by count | 0.679 (0.030) | 0.1009 | 0.388 (0.265) | 0.289 | 0.003 | 0.365 (0.051) | 5.00 |
| damped (K=20) | 0.680 (0.029) | 0.1024 | 0.354 (0.265) | 0.337 | 0.001 | 0.365 (0.050) | 5.00 |

The only policy that changes the picture is random-5. The one structural difference is the last column: random-5 and top-4+1-random give all 11 artists a chance of a download, the other three lock in 5. But top-4+1-random keeps Gini at 0.655 and U at 0.0993, close to plain top-5 (0.679, 0.1009), because the explore slot is last and carries the full rank penalty — what it buys is fidelity: Spearman 0.633 vs 0.388, the largest fidelity gain of any policy here. Shuffling the order is worth about as much as removing the position effect altogether (Gini 0.646 here vs 0.647 at base 1.0 in 6c), which is the consistency check one would want between those two conditions.

## 6e. Scale: users per world

Social influence 0.5, top-5 recommender, base 1.2, 1000 worlds.

| users per world | Gini (sd) | U | Spearman rho (sd) | Beatles #1 | accidental hit | leader share (sd) | artists with any download | ties for first |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 0.692 (0.040) | 0.1167 | 0.315 (0.277) | 0.173 | 0.081 | 0.397 (0.081) | 4.96 | 0.051 |
| 200 | 0.678 (0.033) | 0.1072 | 0.361 (0.266) | 0.231 | 0.026 | 0.372 (0.061) | 5.00 | 0.005 |
| 1000 | 0.679 (0.030) | 0.1009 | 0.388 (0.265) | 0.289 | 0.003 | 0.365 (0.051) | 5.00 | 0.001 |

The averages barely move: Gini 0.692 / 0.678 / 0.679, U 0.1167 / 0.1072 / 0.1009. What moves is the spread across worlds, which is what a single classroom run is a draw from — the standard deviation of the leader's share is 0.081 at 50 users and 0.051 at 1000, and the standard deviation of Gini is 0.040 vs 0.030. Fidelity is visibly worse at 50 users (Beatles #1 in 0.173 of worlds vs 0.289; accidental hits 0.081 vs 0.003), and 5% of 50-user worlds end in a tie for first.

A separate lock-in measurement, 300 tracked worlds: the artist leading after user *t* is still leading at user 1000 in

| social influence | t=10 | t=20 | t=50 | t=100 | t=200 | t=500 |
| --- | --- | --- | --- | --- | --- | --- |
| 0.50 | 0.587 | 0.637 | 0.743 | 0.790 | 0.863 | 0.960 |
| 0.75 | 0.737 | 0.810 | 0.887 | 0.937 | 0.967 | 0.990 |

So a 12-person, 3-round market is 36 downloads: inside the range where the leader is already mostly determined (t=20–50) but where the world-to-world spread is at its widest and ties for first are common. A classroom run of that size can show a leader emerging and can show that two rooms differ; it cannot separate a Gini of 0.65 from 0.69, and it cannot measure U at all, since U is defined across worlds and one room is one world.

## 7. Figures

- `fig1_strip.png` — the instructor's strip plot at social influence 0.5, artists ordered by true popularity, red diamond at each artist's true-popularity share. The band of points at exactly 0 is the lock-in from section 1.
- `fig2_gini_vs_si.png` — mean Gini vs social influence (6a), with the random-5 control at influence 0 marked and the Gini of the true popularity distribution as a dashed line.
- `fig3_unpred_vs_si.png` — unpredictability U vs social influence, same control marked.
- `fig4_quality_vs_success.png` — x = each artist's mean share in the independent condition (influence 0, random-5); y = that artist's share in each of the 1000 influence worlds at influence 0.75. Left panel share, right panel rank. 11 artists x 1000 worlds. The horizontal band at rank 8.5 is the six locked-out artists, all tied at share 0.
- `fig5_trajectories.png` — 12 worlds at influence 0.75: left, the eventual leader's cumulative share as users arrive (log x); right, Beatles' cumulative share in the same 12 worlds. Beatles got no downloads at all in 8 of the 12.
- `fig6_policies.png` — Gini, U and mean Spearman per policy (6d).

## 8. Modeling assumptions that visibly drive the results

Ordered by how much of the measured effect they account for.

1. **The recommender can only show artists that already have downloads.** `simple_rec_alg` pads with random artists only while fewer than 5 have been downloaded, so each world freezes to 5 artists within the first handful of users and the other 6 score exactly 0 forever. This produces Gini 0.640 at social influence 0 against 0.278 for random-5 at the same influence — i.e. most of the headline inequality is the recommender's catalogue coverage, not social influence. It is also what makes accidental hits possible at all: a true-30 artist that lands in the frozen 5 has only 4 competitors.
2. **The rank penalty `1.2 ** -rank`.** Arbitrary, and the results move with it: base 1.0 to 1.5 moves Gini 0.647 to 0.706 and accidental hits 0.000 to 0.034 at fixed social influence 0.5.
3. **Counts enter the choice linearly.** The social weight is proportional to the download count, not to its log or its share. A log or square-root transform would damp the feedback loop; nothing in the notebook justifies the linear choice.
4. **The +1 pseudo-count.** At user 1 it is the whole weight; by user 1000 it is noise. It sets how hard the first few users lock the world in, which is the entire mechanism behind the t=10 and t=20 rows of the lock-in table. The damped policy in 6d is, in effect, the pseudo-count moved from 1 to about 2.8, and it changes almost nothing at 1000 users.
5. **One download per user, and the world is one choice deep.** A user picks exactly one of the 5 recs and never returns, so there is no repeat listening, no dwell time, and no way for an artist to be liked without being downloaded. Market share and download count are the same object.
6. **True popularity is fixed, known to the simulator, and normalised over only the 5 recs shown.** The "true" weights are renormalised within the rec set, so an artist's true appeal is only ever measured against the 4 others it happens to be shown with. That is why the independent condition in 6b does not reproduce the true popularity vector exactly.
7. **Social and true weights are mixed linearly with a single scalar.** Every user in a world has the same social influence; there are no early adopters, no contrarians, no heterogeneity at all.
8. **Worlds are fully independent and users arrive in sequence.** No word of mouth between worlds, no simultaneous arrivals, no cold-start catalogue differences.

## 9. What did not get done / caveats

- Nothing failed. No multiprocessing was written: the vectorised port made it unnecessary (0.74 s for 1000 x 1000), and adding processes would only have parallelised across worlds, which is already the cheap axis.
- The `damped` policy required a judgement call the task flagged: the given score formula is order-preserving in the raw count, so it cannot change the ranking. Implemented as a change to the **displayed** count, described in full in 6d. A version that ranks differently would need a different score, not a different K.
- "Beatles #1" and "accidental hit" carry a Monte-Carlo standard error of about 0.015 even at 1000 worlds. Differences smaller than about 0.04 between two rows of those columns are not resolved here.
- Ties for first are counted for nobody. At 50 users that discards 5.1 per cent of worlds from both the Beatles-#1 and accidental-hit columns; at 1000 users it is 0.1 per cent or less.
- The Gini is computed over all 11 artists including the zeros, which is the right choice but means the numbers are not comparable to a Gini computed over only the artists with downloads.
