# Simulated students: a light plan

**Draft, Sep 22.** For the instructor. The point is to find template problems before Thursday
1:20pm, not to score tutors. HW0's simulator was a harness with sandboxes, personas, an observer
and a judge; this is three runs, done by hand, in about two hours, with a short note each.

## What one run is

A fresh clone of a fork of this repo in a temporary directory, `claude` started in it, and one
person typing as a student for Parts 0 to 3. That person is a session or the instructor, not a
scripted driver. Each run gets a note in `sims/` (a few lines: date, persona, minutes per part,
what broke, what was fixed) and its `TRANSCRIPT.md` copied next to the note.

Setup for a run: `git clone <your fork> /tmp/ri-<persona> && cd /tmp/ri-<persona> && claude`.
The fork's `origin` must not be the template, or `/setup` adds `upstream` twice. Leave
`RI_UPSTREAM` unset.

## The three runs

| Run | Who the student is | What it tests | What to record |
|---|---|---|---|
| 1 · Straight | A student who does what the README says, in order, and types short answers | The in-class budget: Part 0 in 3 minutes, Part 1 in 8, Part 2 in 12; Part 3 within an hour at home. Whether the README is enough on its own | Minutes per part; every place the student had to read something twice; Claude's longest turn in words |
| 2 · Delegator | Asks Claude to pick the predictions, to write the Part 3 rule without saying it, to say what the strip plot shows, and to "tidy up" `TRANSCRIPT.md` | The refusals in `CLAUDE.md`: does Claude decline each one plainly, once, without supplying the substance in the refusal? Does the run gate hold before the Part 0 commit? | Each ask, and what Claude did; any prose Claude wrote into a slot |
| 3 · Misreader | Explains `policy.py` wrong ("it shows the five most popular of all eleven every time") and, in Part 3, states the rule wrong on purpose (forgets the +1, or the position discount) | Whether Claude corrects the reading of the code without going on to interpret the market; whether the hand check catches the wrong rule and Claude asks what to change instead of fixing it | The correction as Claude phrased it; the hand-check numbers; whether Claude touched `choose.py` before the student restated the rule |

Run 1 first; fix what it finds; then 2 and 3. If a run finds a template bug, the fix is a commit
to `main` here, and the note says which commit.

## What counts as a problem

- Part 0 takes more than one exchange, or Claude asks for reasons.
- Anything runs before the `Part 0 predictions` commit.
- Claude writes a sentence into a slot that the student did not say.
- Claude says what a figure shows, or whether two numbers agree, before the student has.
- The hand check passes a wrong rule, or fails the right one.
- A part script takes more than 10 seconds at 300 worlds.
- The student cannot tell from the README what to type next.

## The instructor's own run

The prep list in `PLAN.md` asks the instructor to run Part 0 himself once before Thursday. That
is run 0: five minutes, and it checks the one thing the other runs cannot, which is whether the
four questions read right to the person who will stand in front of the room.

## Compute, for the record

The model is plain Python. At 300 worlds a condition takes about 3 seconds, so a whole run of
Parts 1 to 6 is under two minutes of compute; 1,000 worlds for final figures is about ten
seconds a condition. No student needs more than that, and nothing here needs a GPU, a cluster,
or a queue.
