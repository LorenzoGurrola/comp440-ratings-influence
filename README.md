# COMP 440: Ratings and Social Influence, a simulated market with Claude

**Fall 2026 · Individual · [TBD: weight] of the course grade**
**Due [TBD: Tue Oct 6, 8:00am Central]**

Launched in class Thu Sep 24. Parts 0 to 2 happen in class; the rest is take-home, about four
hours. Questions go to `#comp440-f26`.

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

### Part 0. Predictions (in class)

Fork this repo, clone your fork, start `claude`, and type `/setup`. Claude asks your name, then
four questions. Answer each in a word or a line. Claude commits your answers before anything
runs; that is what they are for.

### Part 1. Users on their own (in class)

`part1_independent.py` runs the market as it ships: each user sees five random artists and picks
by taste with no social influence. Claude runs it, prints one world's shares, and draws a strip
plot: one column per artist, one dot per world. Type one sentence: what does the figure show?

### Part 2. The recommender (in class)

Open `recommender.py`. It is short. Tell Claude, in your own words, what `top_five` shows each
user and what it can never show. Claude corrects you if you have the code wrong, and you write
down what it corrected.

Then have Claude run `part2_recommender.py`: the same users, still ignoring the counts, now see
the five most downloaded artists. What changed against Part 1, in one sentence?

### Part 3. Social influence

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
   whether all three agree. Parts 3 to 5 do not run until your code gives the rule's numbers.
3. Pick the social-influence levels for `part3_influence.py` (it ships with 0, 0.25, 0.5, 0.75
   and 1; keep them or change them), and say what shape you expect the curves to have.
4. Claude runs it. Read the two curves against the paper's Figures 1 and 2, one sentence each:
   direction, not size.
5. Go back to your Part 0 predictions: the last slot in Part 3 asks which were wrong.

### Part 4. What is shown

Two markets at the same social influence, both showing the five most downloaded artists: one
shows them in a random order and one shows them sorted by count, the paper's experiments 1 and 2.
`part4_shown.py` draws the paper's Figure 3 for each: an artist's share when nobody saw counts
(the paper calls this its quality) against its share in each world (its success). Say what you
expect first. Then one sentence: which market moved success further from quality, and how far?

### Part 5. Your recommender

A recommender sees only the download counts, never true popularity, and returns the five
artists to show, in order. Describe a rule of your own in words before any code: for example,
keep one of the five spots for a random artist, or mix the most and least downloaded. Say what
you expect it to do to inequality, unpredictability and fidelity. Claude writes
`my_recommender.py` from your description, and `part5_recommender.py` compares it with
`top_five` and `random_five`, all three with your Part 3 rule at social influence 0.5. Some rules
will not move the numbers; that is a result. One sentence: what your rule buys and what it costs.

### Part 6. One assumption

Pick one thing the model assumes: the 1.2 position discount, the +1 added to every count, that
an artist's social weight grows in proportion to its downloads, that the recommender only ever
shows artists that already have a download, or 1,000 users per world. Say what you expect.
Claude makes the change in `part6_assumption.py`, so the files Parts 1 to 5 used stay as they
were, and reruns Part 3's levels without and with the change. Did the conclusion survive? The
script also plots twelve worlds' shares as users arrive, one user at a time. Two sentences.

### Part 7. Connections, and working with Claude

Where does this show up in data you have already handled: HW1's figure of when a movie's tags and
ratings arrived, or HW0's three rankings? Where does it show up in an interface, such as the
"Popular on Netflix" row in the Sep 22 reading? Then two questions about working with Claude, in
`WRITEUP.md`.

## Submitting

When everything runs, have Claude run `/checkpoint`; it lists what is still missing. Then ask
Claude to commit and push, and fill in the form: https://forms.gle/mgKcnqzTGxNaGvteA. Tell Claude
when you have. It will say **YOU ARE FINISHED!**

## AI guidelines

**No AI**: every sentence in `WRITEUP.md` that says what you expect, what a figure shows, or why
you chose something; the rule in Part 3 and the recommender in Part 5 as you describe them. Claude
writes down what you said, word for word.

**Never edited by anyone**: `TRANSCRIPT.md`, `run_all.py`, `measures.py`, `recommender.py`,
`sim.py`, `artists.py`, `choose.py` and `hand_check.py`; and `my_choice.py` once its hand check
has passed. Parts 5 and 6 write new functions of their own; neither changes the Part 3 rule.

**AI encouraged**: all the code, the figures, the hand-check arithmetic once you have done it
yourself, and any extra experiment you want to run.

## Rubric

I grade your process (through your transcript), your code, and your answers.

| Part | Weight | Full credit |
|---|---|---|
| 0. Predictions | 5 | Four predictions committed before any run, revisited when a result contradicts one |
| 1–2. Users, then the recommender | 20 | `top_five` explained correctly in your words; the two sentences say what the figures show |
| 3. Social influence | 25 | The rule in your words; the hand check; the two curves read against the paper's, direction not size |
| 4. What is shown | 10 | The sentence names the market and how far success moved |
| 5. Your recommender | 20 | A rule precise enough to code, a prediction, and the tradeoff you found, a null result included |
| 6. One assumption | 10 | Before-and-after numbers and a verdict on whether the conclusion survived |
| 7. Connections, working with Claude | 10 | A real connection, and candor about where Claude was wrong or overconfident |
| | **100** | |

## Talk to me if...

**You would rather not use Claude.** Talk to me; there is no grade effect.

**Claude, or something else, is down.** A reported problem never costs you points; post in
`#comp440-f26` or email me. An outage of more than about half a day extends the deadline by 48
hours.

**Claude refuses to predict, to pick your rule, or to say what a figure shows.** Working as
intended; those are the assignment.
