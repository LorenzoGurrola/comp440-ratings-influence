# COMP 440: Ratings and Social Influence, a simulated market with Claude

**Fall 2026 · Individual · [TBD: weight] of the course grade**
**Due [TBD: Tue Oct 6, 8:00am Central]**

Launched in class Thu Sep 24. Parts 0 to 2 happen in class; the rest is take-home, about four
hours. Questions go to `#comp440-f26`.

## Goals

* To turn the paper's two claims, inequality and unpredictability, into numbers you compute.
* To see what a recommender does to a market on its own, before anyone copies anyone.
* To put social influence into a model yourself and watch what it changes.
* To say what a simulation is and is not evidence for, by changing one assumption.
* To direct Claude through an experiment while every prediction and every reading stays yours.

## Overview

Salganik, Dodds and Watts built an artificial music market: 14,341 people downloaded songs by
unknown bands, in eight separate worlds where they could see each song's download count and one
world where they could not. The same song was a hit in one world and a flop in another.

You will run a small version of that market hundreds of times. Eleven artists have a hidden true
popularity. Each simulated user is shown five artists by a recommender and picks one. A world is
1,000 users in a row; you run hundreds of worlds from the same start and measure how unequal each
world ends up and how much the worlds differ from each other.

The model ships with users who ignore the download counts. You add the social influence.

## How this activity works

1. Claude does the mechanical work: it runs the model, computes the measures, draws the figures,
   and writes your words into `WRITEUP.md`.
2. Before every run you say what you expect. After every run you say what it shows. Claude never
   says what a figure means.
3. You check one of Claude's numbers by hand in Part 1, and one number from your own rule by hand
   in Part 3.

Claude records the transcript of your sessions to share with Shilad.

## The task

### Part 0. Predictions (in class)

Fork this repo, clone your fork, start `claude`, approve the hooks, and type `/setup`. Claude
asks your name, then four questions. Answer each in a word or a line. Claude commits your answers
before anything runs; that is what they are for.

### Part 1. Users on their own (in class)

`part1_independent.py` runs the market as it ships: each user sees five random artists and picks
by taste alone. Claude runs it, prints one world's shares, and draws the strip plot. Recompute
that world's Gini by hand (the formula is at the top of `measures.py`) and tell Claude whether it
matched. Then one sentence: what does the figure show?

### Part 2. The recommender (in class)

Open `policy.py`. It is short. Tell Claude, in your own words, what `top_five` shows each user and
what it can never show. Claude corrects you if you have the code wrong. Then have Claude run
`part2_policy.py`: the same users, still ignoring the counts, now see the five most downloaded
artists. What changed against Part 1, in one sentence?

### Part 3. Social influence

`choose.py` decides what a user picks from the five shown. As shipped it ignores the counts. The
rule to put in is the paper's idea, made specific:

* each artist shown gets a social weight of (its downloads + 1) × 1.2^−position, where the top
  of the list is position 0;
* normalize the social weights over the five shown, and the true popularities over the five
  shown, so each set sums to 1;
* the chance of picking an artist is `social_influence` × social + (1 − `social_influence`) × true.

Tell Claude the rule in your own words. Claude writes it into `choice_weights()` and runs the
two-artist hand check; work that case out yourself and say whether it matched. Then pick the
social-influence levels for `part3_influence.py`, say what shape you expect, and read the two
curves against the paper's Figures 1 and 2. One sentence each: direction, not size.

### Part 4. What is shown

Two markets at the same social influence: one where an artist's position on the list does not
matter and one where it does, the paper's experiments 1 and 2. `part4_shown.py` draws the
paper's Figure 3 for each: what an artist earned when nobody saw counts, against what it earned
in each world. One sentence: which market moved success further from quality?

### Part 5. Your policy

Describe a recommender rule in words before any code: damped counts, an exploration slot, hiding
the counts, anything. Say what you expect it to do to inequality, unpredictability and fidelity
to true taste. Claude writes `my_policy.py` from your description, and `part5_policy.py` compares
it with the shipped rule and with random. Some rules will not move the numbers; that is a result.
One sentence: what your rule buys and what it costs.

### Part 6. One assumption

Pick one thing the model assumes: the 1.2 position discount, the +1 pseudo-count, that counts
enter the choice linearly, that the recommender only ever shows artists that already have a
download, or 1,000 users per world. Say what you expect. Claude makes the change inside
`part6_assumption.py`, so the files Parts 1 to 5 ran stay as they were, and reruns Part 3's
sweep before and after. Did the conclusion survive? The script also draws twelve worlds
unfolding user by user. Two sentences.

### Part 7. Connections, and working with Claude

Where does this show up in data you have already handled: HW1's figure of when a movie's tags and
ratings arrived, or HW0's three rankings? Where does it show up in an interface, such as the
"Popular on Netflix" row in the Sep 22 reading? Then two questions about working with Claude, in
`WRITEUP.md`.

When everything runs, have Claude run `/checkpoint`; it walks through what is still missing.
Then ask Claude to commit and push, and fill in the form: https://forms.gle/mgKcnqzTGxNaGvteA.
Tell Claude when you have. It will say **YOU ARE FINISHED!** Due **[TBD]**.

## AI guidelines

**No AI**: every sentence in `WRITEUP.md` that says what you expect, what a figure shows, or why
you chose something; the rule in Part 3 and the policy in Part 5 as you describe them. Claude
writes down what you said, word for word.

**Never edited by anyone**: `TRANSCRIPT.md`, `run_all.py`, `measures.py`, `policy.py`,
`sim.py` and `artists.py`; and `choose.py` once its hand check has passed.

**AI encouraged**: all the code, the figures, the hand-check arithmetic once you have done it
yourself, and any extra experiment you want to run.

## Rubric

I grade your process (through your transcript), your code, and your answers.

| Part | Weight | Full credit |
|---|---|---|
| 0. Predictions | 5 | Four predictions committed before any run, revisited when a result contradicts one |
| 1–2. Users, then the recommender | 20 | The hand check reported honestly; `top_five` explained correctly in your words; the two sentences say what the figures show |
| 3. Social influence | 25 | The rule in your words; the hand check; the two curves read against the paper's, direction not size |
| 4. What is shown | 10 | The sentence names the market and how far success moved |
| 5. Your policy | 20 | A rule precise enough to code, a prediction, and the tradeoff you found, a null result included |
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
