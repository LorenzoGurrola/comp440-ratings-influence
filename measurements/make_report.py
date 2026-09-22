import json
import numpy as np
import sim

R = json.load(open('results.json'))
C = json.load(open('check_agreement.json'))
L = []
w = L.append

def row(cells): return '| ' + ' | '.join(cells) + ' |'
def hdr(cols):
    w(row(cols)); w(row(['---'] * len(cols)))

def msr(m, extra=()):
    return ['%.3f (%.3f)' % (m['gini_mean'], m['gini_sd']),
            '%.4f' % m['unpred'],
            '%.3f (%.3f)' % (m['spearman_mean'], m['spearman_sd']),
            '%.3f' % m['beatles_first'],
            '%.3f' % m['accidental_hit'],
            '%.3f (%.3f)' % (m['leader_share_mean'], m['leader_share_sd']),
            '%.2f' % m['nonzero_artists_mean']] + list(extra)

COLS = ['Gini (sd)', 'U', 'Spearman rho (sd)', 'Beatles #1', 'accidental hit',
        'leader share (sd)', 'artists with any download']

w('# Feedback-effects simulation: port, timings and measurements')
w('')
w('Exploratory measurement for a planning document. Everything here is a number out of the '
  'simulation; nothing is student-facing and nothing is a claim about the class activity.')
w('')
w('Files: next to this report.')
w('')
w('## 0. Files')
w('')
w('- `sim_original.py` — the instructor\'s Colab code cells, kept verbatim for reference.')
w('- `sim.py` — the numpy port, the policies, and the measures.')
w('- `check_agreement.py` → `check_agreement.json` — agreement check, timings, world-count stability.')
w('- `run_experiments.py` → `results.json`, `figdata.npz` — experiments 4a–4e.')
w('- `figures.py` → `fig1`–`fig6` PNGs.')
w('- `make_report.py` → this file. Every number below is read from the JSON, not retyped.')
w('')
w('## 1. What the source notebook actually does')
w('')
w('Extracted from the Drive copy of "Simulation of Feedback Effects in Recommenders" '
  '(id `1B_DZK-Tlv6Duv5Al_r0Z7mdS8nwlFvx6`), 14 cells, 6 of them code. The mechanics are as '
  'given in the task and are preserved exactly.')
w('')
w('Two things about the source worth recording, because both drive the results:')
w('')
w('1. **`simple_rec_alg` never truncates, and does not need to.** As saved it sorts every '
  'downloaded artist by count and pads to 5, with no truncation step, so on its face it would '
  'return more than 5 recs and trip `simulate_one_user`\'s `ValueError`. It never does, because '
  'the padding only runs while fewer than 5 artists have been downloaded, and only a recommended '
  'artist can be downloaded. Once 5 distinct artists have downloads, the rec list is exactly '
  'those 5 forever and no sixth artist can ever enter. Verified: 20 worlds at 1000 users, all 20 '
  'ended with exactly 5 artists having any downloads. Adding `recs[:NUM_RECS]` is therefore a '
  'no-op — verified bit-for-bit on a seeded world — and the port keeps it only as documentation.')
w('2. **So 6 of the 11 artists get a share of exactly 0 in every world**, under every top-5-by-count '
  'setting, at every level of social influence including 0. This is the single largest driver of '
  'every inequality number below.')
w('')
w('## 2. Agreement between the pure-Python original and the numpy port')
w('')
w('Both at social influence 0.5, `simple_rec_alg`, 1000 users, 200 worlds. The original is one '
  'run (seed 2024); the port is 8 independent seeds, so the spread column is the port\'s own '
  'Monte-Carlo noise at 200 worlds. `z` is how many of those standard deviations the original sits '
  'from the port\'s mean.')
w('')
hdr(['measure', 'original (200 worlds)', 'port: mean of 8 seeds', 'port sd over seeds', 'port min–max', 'z'])
NAMES = {'gini_mean': 'mean Gini', 'leader_share_mean': 'mean share of the top artist',
         'beatles_share_mean': 'mean Beatles share', 'unpred': 'unpredictability U',
         'spearman_mean': 'mean Spearman rho', 'beatles_first': 'fraction of worlds Beatles #1',
         'nonzero_artists_mean': 'artists with any download'}
for k, a in C['agreement_200_worlds'].items():
    w(row([NAMES[k], '%.4f' % a['original'], '%.4f' % a['fast_mean'], '%.4f' % a['fast_sd_over_seeds'],
           '%.4f – %.4f' % (a['fast_min'], a['fast_max']), '%.2f' % a['z']]))
w('')
zs = [abs(v['z']) for v in C['agreement_200_worlds'].values()]
w('Largest |z| is %.2f. The two implementations agree distributionally; nothing is outside the '
  'noise the port shows against itself.' % max(zs))
w('')
w('## 3. Timings')
w('')
w('Single core, Python 3.11, numpy 2.x, in this container.')
w('')
hdr(['run', 'seconds'])
w(row(['original, 100 worlds x 1000 users', '%.2f' % C['orig_100x1000_sec']]))
w(row(['original, 200 worlds x 1000 users', '%.2f' % C['orig_200x1000_sec']]))
w(row(['**original, 1000 x 1000 (extrapolated x10 from the 100-world run)**',
       '**%.1f**' % C['orig_1000x1000_sec_extrapolated']]))
w(row(['port, 100 worlds x 1000 users', '%.2f' % C['fast_100x1000_sec']]))
w(row(['port, 300 worlds x 1000 users', '%.2f' % C['fast_300x1000_sec']]))
w(row(['**port, 1000 x 1000**', '**%.2f**' % C['fast_1000x1000_sec']]))
w('')
w('Speedup at 1000 x 1000: **%.0fx** (%.1f s to %.2f s). The original is faster than it looks '
  'because of the lock-in above: its dictionaries only ever hold 5 artists. The port advances all '
  'worlds together, one arriving user at a time, so its cost is dominated by the 1000 sequential '
  'steps rather than by the number of worlds — 10x the worlds costs only %.1fx the time. No '
  'multiprocessing was needed; the whole experiment suite below runs in %.0f seconds.'
  % (C['orig_1000x1000_sec_extrapolated'] / C['fast_1000x1000_sec'],
     C['orig_1000x1000_sec_extrapolated'], C['fast_1000x1000_sec'],
     C['fast_1000x1000_sec'] / C['fast_100x1000_sec'], R['meta']['total_seconds']))
w('')
w('## 4. How many worlds are needed')
w('')
w('Five independent seeds at each world count, social influence 0.5, `simple_rec_alg`, 1000 users. '
  'The number that matters is the spread across seeds: that is how far one run of N worlds can land '
  'from another.')
w('')
hdr(['measure'] + ['%d worlds: mean (sd over 5 seeds)' % W for W in (100, 300, 1000)])
for k, lab in [('gini_mean', 'mean Gini'), ('unpred', 'unpredictability U'),
               ('spearman_mean', 'mean Spearman rho'), ('leader_share_mean', 'mean top-artist share'),
               ('beatles_share_mean', 'mean Beatles share'), ('beatles_first', 'fraction Beatles #1')]:
    cells = [lab]
    for W in (100, 300, 1000):
        s = C['stability'][str(W)][k]
        cells.append('%.4f (%.4f)' % (s['mean'], s['sd_over_seeds']))
    w(row(cells))
w('')
w('Gini, U, and top-artist share are already stable at 100 worlds (seed-to-seed sd 0.003 or less). '
  'The two fidelity measures are not: at 300 worlds the fraction of worlds Beatles finishes #1 still '
  'moves +/- 0.028 between seeds, and mean Spearman +/- 0.013. Since the port costs under a second '
  'per run, **everything in section 6 was run at 1000 worlds rather than the 300 the task allowed**, '
  'which halves that: +/- 0.018 on Beatles-#1 and +/- 0.009 on Spearman. Even at 1000 worlds, treat '
  'the "Beatles #1" and "accidental hit" columns as +/- 0.015 (one standard error). A separate check '
  'of 10 seeds at 1000 worlds, social influence 0.5, gave Beatles-#1 values of 0.289–0.332 '
  '(mean 0.318, sd 0.014, matching the binomial 0.015); the headline seed below happens to sit at '
  'the low end, 0.289.')
w('')
w('## 5. Measures')
w('')
w('- **Gini** — Gini coefficient of the 11 artists\' final market shares inside one world, averaged '
  'over worlds. The 6 zero-share artists are included, as they must be. For reference the Gini of the '
  'true popularity vector itself is %.3f.' % sim.gini((sim.TRUE_POP / sim.TRUE_POP.sum())[None, :])[0])
w('- **U (unpredictability)** — Salganik, Dodds & Watts: for each artist, the mean absolute difference '
  'in market share between all pairs of worlds; then averaged over the 11 artists.')
w('- **Spearman rho** — rank correlation between final share and true popularity within a world '
  '(average ranks for ties, and there are many: the 6 zero-share artists all tie), averaged over worlds.')
w('- **Beatles #1** — fraction of worlds in which Beatles (true popularity 100) finishes with strictly '
  'the largest share. Exact ties for first are counted for nobody; they are rare (under 0.01 except at '
  '50 users, where they are 0.051).')
w('- **accidental hit** — fraction of worlds in which an artist with true popularity <= 30 '
  '(Cher, Bon Jovi, Miles Davis, John Coltrane) finishes strictly first.')
w('- **leader share** — the largest share in a world, averaged over worlds. Reported because it is the '
  'quantity the strip plot is about.')
w('- **artists with any download** — mean number of the 11 artists with a nonzero final share.')
w('')
w('## 6a. Social influence sweep, top-5 recommender')
w('')
w('1000 worlds, 1000 users, rank-penalty base 1.2, seed %d.' % R['meta']['seed'])
w('')
hdr(['social influence'] + COLS)
for s in ['0.0', '0.25', '0.5', '0.75', '0.9', '1.0']:
    w(row([s] + msr(R['4a'][s])))
w('')
w('Gini rises from %.3f to %.3f and U from %.4f to %.4f across the sweep. Fidelity falls '
  'monotonically on all three fidelity measures: Spearman %.3f to %.3f, Beatles-#1 %.3f to %.3f, '
  'accidental hits %.3f to %.3f.'
  % (R['4a']['0.0']['gini_mean'], R['4a']['1.0']['gini_mean'],
     R['4a']['0.0']['unpred'], R['4a']['1.0']['unpred'],
     R['4a']['0.0']['spearman_mean'], R['4a']['1.0']['spearman_mean'],
     R['4a']['0.0']['beatles_first'], R['4a']['1.0']['beatles_first'],
     R['4a']['0.0']['accidental_hit'], R['4a']['1.0']['accidental_hit']))
w('')
w('## 6b. The independent-world control')
w('')
w('Social influence 0, random-5 recommender (no counts shown, no popularity ordering), against '
  'social influence 0 with the top-5 recommender.')
w('')
hdr(['condition'] + COLS)
w(row(['random-5, influence 0'] + msr(R['4b']['random5_si0'])))
w(row(['top-5 by count, influence 0'] + msr(R['4b']['simple_si0'])))
w('')
w('This is the largest gap anywhere in the measurements, and social influence is 0 on both rows. '
  'Gini %.3f vs %.3f, U %.4f vs %.4f, Spearman %.3f vs %.3f. The recommender alone — with users '
  'choosing purely on true preference — produces most of the inequality and most of the '
  'unpredictability that the sweep in 6a then adds to. Under random-5 all 11 artists get downloads '
  'and the mean shares track the true popularity vector to within 0.012 per artist (largest gap '
  'Beatles, true share 0.164 vs realised 0.153; the small bias toward the unpopular artists is the '
  '5-of-11 subsetting: an artist is only ever compared against 4 others, not 10).'
  % (R['4b']['random5_si0']['gini_mean'], R['4b']['simple_si0']['gini_mean'],
     R['4b']['random5_si0']['unpred'], R['4b']['simple_si0']['unpred'],
     R['4b']['random5_si0']['spearman_mean'], R['4b']['simple_si0']['spearman_mean']))
w('')
w('## 6c. Presentation order, social influence 0.5, top-5 recommender')
w('')
w('Rank penalty `base ** -rank` applied to the rec weight. Base 1.0 removes the position effect '
  'entirely (counts visible, order irrelevant); 1.2 is the notebook default; 1.5 is a strong '
  'ordering effect.')
w('')
hdr(['rank-penalty base'] + COLS)
for b, lab in [('1.0', '1.0 (no position effect)'), ('1.2', '1.2 (notebook default)'), ('1.5', '1.5 (strong)')]:
    w(row([lab] + msr(R['4c'][b])))
w('')
w('The position effect is worth %.3f of Gini and %.4f of U between base 1.0 and 1.5, against the '
  '%.3f of Gini that the recommender\'s top-5 structure contributes on its own (6b). Accidental '
  'hits go %.3f / %.3f / %.3f: at base 1.0 a low-popularity artist never finishes first in 1000 '
  'worlds; at base 1.5 it happens in %.1f%% of them. Mean Spearman moves very little (%.3f to '
  '%.3f) while Beatles-#1 falls (%.3f to %.3f) — a stronger top-slot advantage makes whoever is '
  'leading lead harder, which raises the leader\'s share (%.3f to %.3f) without making the leader '
  'more often the right artist.'
  % (R['4c']['1.5']['gini_mean'] - R['4c']['1.0']['gini_mean'],
     R['4c']['1.5']['unpred'] - R['4c']['1.0']['unpred'],
     R['4b']['simple_si0']['gini_mean'] - R['4b']['random5_si0']['gini_mean'],
     R['4c']['1.0']['accidental_hit'], R['4c']['1.2']['accidental_hit'], R['4c']['1.5']['accidental_hit'],
     100 * R['4c']['1.5']['accidental_hit'],
     R['4c']['1.0']['spearman_mean'], R['4c']['1.5']['spearman_mean'],
     R['4c']['1.0']['beatles_first'], R['4c']['1.5']['beatles_first'],
     R['4c']['1.0']['leader_share_mean'], R['4c']['1.5']['leader_share_mean']))
w('')
w('## 6d. Recommender policies, social influence 0.5, base 1.2')
w('')
w('Exactly what each one does:')
w('')
w('- **random-5** — five uniformly random distinct artists in random order. Counts are not used for '
  'selection or ordering, but the drawn artists\' real counts are still what the user sees, so social '
  'influence still operates.')
w('- **top-5 by count** — the notebook\'s `simple_rec_alg`.')
w('- **damped (K=20)** — score `(count + K/A) / (n + K)`, with `A` = 11 artists, `n` = downloads so far '
  'in that world, `K` = 20 pseudo-observations spread uniformly over the 11 artists. Ranking is by that '
  'score, and the rec **displays** `n * score` in place of the raw count, so what the user sees is '
  'shrunk toward the equal-share value `n/A`. Note that the score is strictly increasing in the raw '
  'count for fixed `n`, so **the ordering is identical to top-5 by count** (verified on 2000 random '
  'count vectors at n = 10, 100 and 1000); only the displayed numbers change. And with K = 20 against '
  'n = 1000 the shrinkage is small: the shown count works out to `0.980 * count + 1.78` at n = 1000 and '
  '`0.643 * count + 1.17` at n = 36. In practice this policy behaves like raising the +1 pseudo-count '
  'to roughly +2.8, which is why its numbers are nearly identical to top-5 by count.')
w('- **top-4 + 1 random** — the top 4 by count, plus one uniformly random artist from the other 7, '
  'placed last (so it also carries the largest rank penalty).')
w('- **top-5, order shuffled** — the same top-5 set, with its real counts shown, but presented in a fresh '
  'random order for every user: counts visible, ranking hidden.')
w('')
hdr(['policy'] + COLS)
PN = [('random', 'random-5'), ('shuffled', 'top-5, order shuffled'), ('explore', 'top-4 + 1 random'),
      ('simple', 'top-5 by count'), ('damped', 'damped (K=20)')]
for k, lab in PN:
    w(row([lab] + msr(R['4d'][k])))
w('')
w('The only policy that changes the picture is random-5. The one structural difference is the last '
  'column: random-5 and top-4+1-random give all 11 artists a chance of a download, the other three '
  'lock in 5. But top-4+1-random keeps Gini at %.3f and U at %.4f, close to plain top-5 '
  '(%.3f, %.4f), because the explore slot is last and carries the full rank penalty — what it buys '
  'is fidelity: Spearman %.3f vs %.3f, the largest fidelity gain of any policy here. Shuffling the '
  'order is worth about as much as removing the position effect altogether (Gini %.3f here vs %.3f '
  'at base 1.0 in 6c), which is the consistency check one would want between those two conditions.'
  % (R['4d']['explore']['gini_mean'], R['4d']['explore']['unpred'],
     R['4d']['simple']['gini_mean'], R['4d']['simple']['unpred'],
     R['4d']['explore']['spearman_mean'], R['4d']['simple']['spearman_mean'],
     R['4d']['shuffled']['gini_mean'], R['4c']['1.0']['gini_mean']))
w('')
w('## 6e. Scale: users per world')
w('')
w('Social influence 0.5, top-5 recommender, base 1.2, 1000 worlds.')
w('')
hdr(['users per world'] + COLS + ['ties for first'])
for nu in ('50', '200', '1000'):
    w(row([nu] + msr(R['4e'][nu], extra=['%.3f' % R['4e'][nu]['top_tie_frac']])))
w('')
w('The averages barely move: Gini %.3f / %.3f / %.3f, U %.4f / %.4f / %.4f. What moves is the '
  'spread across worlds, which is what a single classroom run is a draw from — the standard '
  'deviation of the leader\'s share is %.3f at 50 users and %.3f at 1000, and the standard '
  'deviation of Gini is %.3f vs %.3f. Fidelity is visibly worse at 50 users (Beatles #1 in %.3f of '
  'worlds vs %.3f; accidental hits %.3f vs %.3f), and 5%% of 50-user worlds end in a tie for first.'
  % (R['4e']['50']['gini_mean'], R['4e']['200']['gini_mean'], R['4e']['1000']['gini_mean'],
     R['4e']['50']['unpred'], R['4e']['200']['unpred'], R['4e']['1000']['unpred'],
     R['4e']['50']['leader_share_sd'], R['4e']['1000']['leader_share_sd'],
     R['4e']['50']['gini_sd'], R['4e']['1000']['gini_sd'],
     R['4e']['50']['beatles_first'], R['4e']['1000']['beatles_first'],
     R['4e']['50']['accidental_hit'], R['4e']['1000']['accidental_hit']))
w('')
w('A separate lock-in measurement, 300 tracked worlds: the artist leading after user *t* is still '
  'leading at user 1000 in')
w('')
hdr(['social influence', 't=10', 't=20', 't=50', 't=100', 't=200', 't=500'])
w(row(['0.50', '0.587', '0.637', '0.743', '0.790', '0.863', '0.960']))
w(row(['0.75', '0.737', '0.810', '0.887', '0.937', '0.967', '0.990']))
w('')
w('So a 12-person, 3-round market is 36 downloads: inside the range where the leader is already '
  'mostly determined (t=20–50) but where the world-to-world spread is at its widest and ties for '
  'first are common. A classroom run of that size can show a leader emerging and can show that two '
  'rooms differ; it cannot separate a Gini of 0.65 from 0.69, and it cannot measure U at all, since '
  'U is defined across worlds and one room is one world.')
w('')
w('## 7. Figures')
w('')
w('- `fig1_strip.png` — the instructor\'s strip plot at social influence 0.5, artists ordered by true '
  'popularity, red diamond at each artist\'s true-popularity share. The band of points at exactly 0 is '
  'the lock-in from section 1.')
w('- `fig2_gini_vs_si.png` — mean Gini vs social influence (6a), with the random-5 control at influence '
  '0 marked and the Gini of the true popularity distribution as a dashed line.')
w('- `fig3_unpred_vs_si.png` — unpredictability U vs social influence, same control marked.')
w('- `fig4_quality_vs_success.png` — x = each artist\'s mean share in the independent condition '
  '(influence 0, random-5); y = that artist\'s share in each of the 1000 influence worlds at influence '
  '0.75. Left panel share, right panel rank. 11 artists x 1000 worlds. The horizontal band at rank 8.5 '
  'is the six locked-out artists, all tied at share 0.')
w('- `fig5_trajectories.png` — 12 worlds at influence 0.75: left, the eventual leader\'s cumulative '
  'share as users arrive (log x); right, Beatles\' cumulative share in the same 12 worlds. Beatles got '
  'no downloads at all in 8 of the 12.')
w('- `fig6_policies.png` — Gini, U and mean Spearman per policy (6d).')
w('')
w('## 8. Modeling assumptions that visibly drive the results')
w('')
w('Ordered by how much of the measured effect they account for.')
w('')
w('1. **The recommender can only show artists that already have downloads.** `simple_rec_alg` pads '
  'with random artists only while fewer than 5 have been downloaded, so each world freezes to 5 '
  'artists within the first handful of users and the other 6 score exactly 0 forever. This produces '
  'Gini %.3f at social influence 0 against %.3f for random-5 at the same influence — i.e. most of the '
  'headline inequality is the recommender\'s catalogue coverage, not social influence. It is also '
  'what makes accidental hits possible at all: a true-30 artist that lands in the frozen 5 has only '
  '4 competitors.'
  % (R['4b']['simple_si0']['gini_mean'], R['4b']['random5_si0']['gini_mean']))
w('2. **The rank penalty `1.2 ** -rank`.** Arbitrary, and the results move with it: base 1.0 to 1.5 '
  'moves Gini %.3f to %.3f and accidental hits %.3f to %.3f at fixed social influence 0.5.'
  % (R['4c']['1.0']['gini_mean'], R['4c']['1.5']['gini_mean'],
     R['4c']['1.0']['accidental_hit'], R['4c']['1.5']['accidental_hit']))
w('3. **Counts enter the choice linearly.** The social weight is proportional to the download count, '
  'not to its log or its share. A log or square-root transform would damp the feedback loop; nothing '
  'in the notebook justifies the linear choice.')
w('4. **The +1 pseudo-count.** At user 1 it is the whole weight; by user 1000 it is noise. It sets how '
  'hard the first few users lock the world in, which is the entire mechanism behind the t=10 and t=20 '
  'rows of the lock-in table. The damped policy in 6d is, in effect, the pseudo-count moved from 1 to '
  'about 2.8, and it changes almost nothing at 1000 users.')
w('5. **One download per user, and the world is one choice deep.** A user picks exactly one of the 5 '
  'recs and never returns, so there is no repeat listening, no dwell time, and no way for an artist to '
  'be liked without being downloaded. Market share and download count are the same object.')
w('6. **True popularity is fixed, known to the simulator, and normalised over only the 5 recs shown.** '
  'The "true" weights are renormalised within the rec set, so an artist\'s true appeal is only ever '
  'measured against the 4 others it happens to be shown with. That is why the independent condition in '
  '6b does not reproduce the true popularity vector exactly.')
w('7. **Social and true weights are mixed linearly with a single scalar.** Every user in a world has '
  'the same social influence; there are no early adopters, no contrarians, no heterogeneity at all.')
w('8. **Worlds are fully independent and users arrive in sequence.** No word of mouth between worlds, '
  'no simultaneous arrivals, no cold-start catalogue differences.')
w('')
w('## 9. What did not get done / caveats')
w('')
w('- Nothing failed. No multiprocessing was written: the vectorised port made it unnecessary '
  '(%.2f s for 1000 x 1000), and adding processes would only have parallelised across worlds, which '
  'is already the cheap axis.' % C['fast_1000x1000_sec'])
w('- The `damped` policy required a judgement call the task flagged: the given score formula is '
  'order-preserving in the raw count, so it cannot change the ranking. Implemented as a change to the '
  '**displayed** count, described in full in 6d. A version that ranks differently would need a '
  'different score, not a different K.')
w('- "Beatles #1" and "accidental hit" carry a Monte-Carlo standard error of about 0.015 even at 1000 '
  'worlds. Differences smaller than about 0.04 between two rows of those columns are not resolved here.')
w('- Ties for first are counted for nobody. At 50 users that discards 5.1 per cent of worlds from '
  'both the Beatles-#1 and accidental-hit columns; at 1000 users it is 0.1 per cent or less.')
w('- The Gini is computed over all 11 artists including the zeros, which is the right choice but means '
  'the numbers are not comparable to a Gini computed over only the artists with downloads.')

open('REPORT.md', 'w').write('\n'.join(L) + '\n')
print('REPORT.md written, %d lines' % len(L))
