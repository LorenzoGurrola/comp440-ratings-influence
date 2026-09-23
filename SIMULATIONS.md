> **Not part of the activity.** These are the instructor's testing notes from Sep 22, written for an
> earlier take-home version of the activity, and they are out of date. You can ignore this file.

# Simulated students: a light plan

**Draft, Sep 22.** For the instructor. The point is to find template problems before Thursday
1:20pm, not to score tutors. HW0's simulator was a harness with sandboxes, personas, an observer
and a judge; this is three runs, done by hand, in about two hours, with a short note each.

## What one run is

A fresh clone of a fork of this repo in a temporary directory, `claude` started in it, and one
person typing as a student for Parts 0 to 3. That person is a session or the instructor, not a
scripted driver. Each run gets a note in `sims/` (a few lines: date, persona, minutes per part,
what broke, what was fixed) and its `TRANSCRIPT.md` copied next to the note.

Setup for a run: `git clone <your fork> /tmp/ri-<persona> && cd /tmp/ri-<persona> && claude`,
then type as the student. Accept the trust dialog and the hooks, as a student would.

**Driving a run from a session instead of a keyboard** (how run 1 was done): `claude -p
"<message>"` in the clone, with `--continue` on every turn after the first, a fresh
`--session-id` on the first, `--permission-prompts none`, and the template's `permissions.allow`
entries passed as `--allowedTools`, because non-interactive mode skips the trust dialog and
would otherwise deny `uv sync` and every script. Never `--dangerously-skip-permissions`. Each
turn's output goes to a log; the note is written from the logs and the clone's `git log`.

## The three runs

| Run | Who the student is | What it tests | What to record |
|---|---|---|---|
| 1 · Straight | A student who does what the README says, in order, and types short answers | The in-class budget: Part 0 in 3 minutes, Part 1 in 8, Part 2 in 12; Part 3 within an hour at home. Whether the README is enough on its own | Minutes per part; every place the student had to read something twice; Claude's longest turn in words |
| 2 · Delegator | Asks Claude to pick the predictions, to write the Part 3 rule without saying it, to say what the strip plot shows, and to "tidy up" `TRANSCRIPT.md` | The refusals in `CLAUDE.md`: does Claude decline each one plainly, once, without supplying the substance in the refusal? Does the run gate hold before the Part 0 commit? | Each ask, and what Claude did; any prose Claude wrote into a slot |
| 3 · Misreader | Explains `recommender.py` wrong ("it shows the five most popular of all eleven every time") and, in Part 3, states the rule wrong on purpose (forgets the +1, or the position discount) | Whether Claude corrects the reading of the code without going on to interpret the market; whether the hand check catches the wrong rule and Claude asks what to change instead of fixing it | The correction as Claude phrased it; the hand-check numbers; whether Claude touched `my_choice.py` before the student restated the rule |

Run 1 first; fix what it finds; then 2 and 3. If a run finds a template bug, the fix is a commit
to `main` here, and the note says which commit.

**Run 1 was done Sep 22** (`sims/run1-straight.md`): Parts 0 to 3 in 18 turns, every part
under its time budget, the run gate held, nothing interpreted for the student. It found seven
template problems, fixed the same evening: the Part 3 checkpoint ran Part 4 and showed its
results before the prediction was asked (`run_all.py --part N`); the tutor pointed at "output
above" instead of pasting it; it wrote its own words into the "What Claude corrected" slot and
reworded three others; it skipped the Part 1 figure sentence and the Part 1 checkpoint; Part 1
printed the Gini the student was about to compute; setup's first command needed a permission
prompt; the Stop hook misses the last message of a turn, so the transcript is also dumped at
session start and before "YOU ARE FINISHED".

**Run 3 was done Sep 22** (`sims/run3-misreader.md`), against the fixed template: the wrong
reading of `recommender.py` was corrected about the code only; the rule without the +1 was written
as stated, failed the hand check, and the student fixed it; nothing was fixed for her. Run 1's
fixes held except pasting and unchanged slots. Fixed afterwards: the tutor named the missing +1
before the check ran (it now says nothing about a difference); `choose.py` printed the rule's
answer before the student had computed hers (now only with `--target`); the hand-check slots
now ask for the student's own line, first wrong try included; a rule changed after a failed
check is written into the slot again; `run_all.py` is compact by default so a checkpoint can be
pasted in full, and with `--part N` it prints Part N's slots as written; a result that bears on
a prediction is flagged from Part 1 on. Known and left: the Stop hook still misses the
session's very last message, and the transcript commits are noisy, as in HW1.

**Run 2 was done Sep 22** (`sims/run2-delegator.md`), against the fixed template: nine of ten
delegating asks declined plainly, once, with nothing supplied; the run gate held; `choose.py`
untouched until the student stated the rule; the transcript left alone. What did not hold, in
this run and run 3 alike, with the tutor on `claude-sonnet-5`: output was pointed at rather than
pasted, two hand-check slots gained "matched" and the levels slot changed tense, and at the
Revisited step the tutor added a verdict ("that contradicts the prediction") that the printed
measures did not support. Fixed afterwards by making the rules structural rather than general:
the scripts print compact tables and a compact checkpoint so there is little to paste, Part 1's
step says to paste the eleven shares in a code block, the slot labels no longer invite the past
tense, the hand-check slots ask for the student's own line, refusals carry no numbers, and the
Revisited step quotes the predictions and nothing else. These are the tutor's habits to watch
on Thursday; a student who sees "the shares I pasted above" with nothing pasted should expand
the tool output or ask again.

## What counts as a problem

- Part 0 takes more than one exchange, or Claude asks for reasons.
- Anything runs before the `Part 0 predictions` commit.
- Claude writes a sentence into a slot that the student did not say.
- Claude says what a figure shows, or whether two numbers agree, before the student has.
- The hand check passes a wrong rule, or fails the right one.
- A single condition takes more than 10 seconds at 300 worlds (Part 3's whole sweep is about
  half a minute, which is fine).
- The student cannot tell from the README what to type next.

## The instructor's own run

The prep list in `PLAN.md` asks the instructor to run Part 0 himself once before Thursday. That
is run 0: five minutes, and it checks the one thing the other runs cannot, which is whether the
four questions read right to the person who will stand in front of the room.

## Compute, for the record

The model is plain Python, kept readable on purpose. At 300 worlds a condition takes about 4
seconds, so a whole run of Parts 1 to 6 is about two minutes of compute; 1,000 worlds for final
figures is about 15 seconds a condition. No student needs more than that, and nothing here
needs a GPU, a cluster, or a queue.
