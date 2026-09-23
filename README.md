# COMP 440: Ratings and Social Influence, a simulated market with Claude

**Fall 2026 · Individual · [TBD: weight] of the course grade · graded for completion**
**Due [TBD: Tue Oct 6, 8:00am Central]**

One class period, Thu Sep 24: about 60 to 90 minutes from forking this repo to submitting. It is
graded for completion, not for being right. A part is complete when its script has run and its
slots in `WRITEUP.md` hold your own words. The follow-ups at the end are optional and are not
graded. Questions go to `#comp440-f26`.

## Goals

* To have you compute numbers behind the paper's two claims: inequality and unpredictability.
* To incorporate social influence into a model yourself and watch what it changes.
* To understand the possibilities and limitations of simulations, and see how they shift by
  changing assumptions.

## Overview

Salganik, Dodds and Watts built an artificial music market: 14,341 people downloaded songs by
unknown bands, in eight separate worlds where they could see each song's download count and one
world where they could not. A song could be a hit in one world and a flop in another.

You will run a small version of that market hundreds of times. Eleven artists have a hidden **true
popularity**. Each simulated user is shown five artists by a recommender and picks one. A world is
1,000 users in a row; you run hundreds of worlds from the same start and measure how unequal each
world ends up and how much the worlds differ from each other.

The model ships with users who ignore the download counts (the independent world). You will add
social influence.

## The measures

Every part prints the same five measures for each condition it runs. `measures.py` has the
exact formulas.

* **Gini**: inequality within a world, the paper's Figure 1. 0 means every artist has the same
  share of the downloads; 0.91 means one artist has all of them. The table shows the average
  over worlds.
* **Unpredictability**: how differently identical worlds end, the paper's Figure 2. For each
  artist, the average difference in its share between two worlds, then the average over artists.
  0 means every world ends the same way.
* **Fidelity**: how closely a world ranks the artists in the order of their true popularity. 1
  means the same order; 0 means no relation.
* **True best wins**: the fraction of worlds in which the Beatles (true popularity 100) end with
  the largest share.
* **Accidental hits**: the fraction of worlds in which an artist with true popularity 30 or less
  ends with the largest share.

## How this activity works

1. Claude codes, runs the simulation, computes the measures and draws the figures.
2. You determine approaches and strategies, hypothesize about what will happen, and interpret the results.

Claude records the transcript of your sessions to share with Shilad.

## The task

Six parts, about 70 minutes together. The minutes are a guide, not a rule.

### Part 0. Predictions · about 5 minutes

Fork this repo, clone your fork, start `claude`, and type `/setup`. Claude asks your name, then
four questions. Answer each in a word or a line. Claude commits your answers before anything
runs; that is what they are for.

### Part 1. Users on their own · about 8 minutes

`part1_independent.py` runs the market as it ships: each user sees five random artists and picks
by taste with no social influence. Claude runs it, prints one world's shares, and draws a strip
plot: one column per artist, one dot per world. Type one sentence: what does the figure show?

### Part 2. The recommender · about 12 minutes

Open `recommender.py`. It is short. A recommender returns two things: the five artists to show,
top of the list first, and the download counts shown with them. Tell Claude, in your own words,
what `top_five` shows each user and what it can never show. Claude corrects you if you have the
code wrong, and you write down what it corrected.

Then have Claude run `part2_recommender.py`: the same users, still ignoring the counts, now see
the five most downloaded artists. What changed against Part 1, in one sentence?

### Part 3. Social influence · about 25 minutes

A choice rule decides what a user picks from the five shown. The one that ships,
`independent_choice` in `choose.py`, ignores the counts. Yours goes in `my_choice.py`. The rule
to put in is the paper's idea, made specific:

* each artist shown gets a social weight of (its downloads + 1) × 1.2^−position, where the top
  of the list is position 0;
* normalize the social weights over the five shown, and the true popularities over the five
  shown, so each set sums to 1 (`normalize()` in `choose.py` does this);
* the chance of picking an artist is `social_influence` × social + (1 − `social_influence`) × true.

1. Tell Claude the rule in your own words. Claude writes it into `my_choice.py` from what you
   said.
2. Claude runs `hand_check.py`, which prints what your code gives for a two-artist case. Work out
   by hand what the rule gives for that case. Then Claude shows the rule's numbers, and you say
   whether all three agree. Parts 3 and 4 do not run until your code gives the rule's numbers.
3. Say what shape you expect the curves to have. Then Claude runs `part3_influence.py`, which
   ships with social-influence levels 0, 0.25, 0.5, 0.75 and 1; you may change them, but you do
   not have to.
4. Read the two curves against the paper's Figures 1 and 2, one sentence each: direction, not
   size.
5. Go back to your Part 0 predictions: the last slot in Part 3 asks which were wrong.

### Part 4. Your recommender · about 15 minutes

A recommender sees only the download counts, never true popularity, and returns the five artists
to show, in order, and the counts to show with them. Describe a rule of your own in words before
any code: for example, keep one of the five spots for a random artist, mix the most and least
downloaded, or show no counts at all. Say what you expect it to do to inequality,
unpredictability and fidelity. Claude writes `my_recommender.py` from your description, and
`part4_recommender.py` compares it with `top_five` and `random_five`, all three with your Part 3
rule at social influence 0.5. Some rules will not move the numbers; that is a result. One
sentence: what your rule buys and what it costs.

### Part 5. Reflection · about 5 minutes

Two sentences, in `WRITEUP.md`. Where does this show up in data you have already handled, or in
an interface you use: HW1's figure of when a movie's tags and ratings arrived, HW0's three
rankings, the "Popular on Netflix" row in the Sep 22 reading? Then one sentence on working with
Claude: a moment it was wrong or overconfident, or a judgment you kept for yourself.

## Follow-ups

Optional, and not graded. Do one if you want to; do none and you have still finished the
activity. The slots for them are at the end of `WRITEUP.md`, and `run_all.py` never counts them
as missing.

* **What is shown.** `followup_shown.py`: two markets at the same social influence, both showing
  the five most downloaded artists, one in a random order and one sorted by count — the paper's
  experiments 1 and 2. It draws the paper's Figure 3 for each: an artist's share when nobody saw
  counts (its quality) against its share in each world (its success). Which market moved success
  further from quality?
* **One assumption.** `followup_assumption.py`: pick one thing the model assumes — the 1.2
  position discount, the +1 added to every count, that an artist's social weight grows in
  proportion to its downloads, that the recommender only ever shows artists that already have a
  download, or 1,000 users per world. Change it there, so the files Parts 1 to 4 used stay as
  they were, and rerun Part 3's levels without and with the change. Did the conclusion survive?
* **More recommenders.** Write a second and a third rule in Part 4's shape and compare them.
* **More worlds.** Every script runs 300 worlds. Set `WORLDS = 1000` in a copy and see which
  numbers move and which only get steadier.

## Submitting

When the six parts are done, have Claude run `/checkpoint`; it lists what is still missing. Then
ask Claude to commit and push, and fill in the form: https://forms.gle/mgKcnqzTGxNaGvteA. Tell
Claude when you have. It will say **YOU ARE FINISHED!**

## AI guidelines

**No AI**: every sentence in `WRITEUP.md` that says what you expect, what a figure shows, or why
you chose something; the rule in Part 3 and the recommender in Part 4 as you describe them. Claude
writes down what you said, word for word.

**Never edited by anyone**: `TRANSCRIPT.md`, `run_all.py`, `measures.py`, `recommender.py`,
`sim.py`, `artists.py`, `choose.py` and `hand_check.py`; and `my_choice.py` once its hand check
has passed. Part 4 and the follow-ups write new functions of their own; none of them changes the
Part 3 rule.

**AI encouraged**: all the code, the figures, the hand-check arithmetic once you have done it
yourself, and any extra experiment you want to run.

## Rubric

Graded for completion. A part is complete when its script has run and its slots in `WRITEUP.md`
hold your own words. I do not grade whether a prediction came true or whether a reading is the
one I would have written. `uv run python run_all.py` lists what is still missing; when it says
nothing is missing, the activity is complete.

| Part | Complete when |
|---|---|
| 0. Predictions | Four predictions committed before anything runs |
| 1. Users on their own | `part1_independent.py` has run, the figure is drawn, the sentence is yours |
| 2. The recommender | `part2_recommender.py` has run; `top_five` in your words, what Claude corrected, what changed |
| 3. Social influence | Your rule in `my_choice.py`, the hand check reported, `part3_influence.py` has run, the two curve sentences and the revisited predictions |
| 4. Your recommender | Your rule described before any code, what you expected, `part4_recommender.py` has run, the tradeoff sentence |
| 5. Reflection | Both sentences |
| Follow-ups | Optional. Not graded, and never counted as missing |

## Talk to me if...

**You would rather not use Claude.** Talk to me; there is no grade effect.

**Claude, or something else, is down.** A reported problem never costs you points; post in
`#comp440-f26` or email me. An outage of more than about half a day extends the deadline by 48
hours.

**Claude refuses to predict, to pick your rule, or to say what a figure shows.** Working as
intended; those are the assignment.
