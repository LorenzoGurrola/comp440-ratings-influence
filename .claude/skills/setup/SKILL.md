---
name: setup
description: First-time setup, run once after cloning the fork. Adds the upstream remote, installs dependencies, checks the model runs, records the student's name and date, commits, and then asks the four Part 0 questions. Run it again if anything breaks or to check a setup is complete.
---

Do these in order and show what you ran. Skip what is already done. If something fails, say in
plain words what it means and what to change, and stop there.

1. Add the `upstream` remote if it is missing, with the address typed out, no variables:
   `git remote add upstream https://github.com/shilad/comp440-ratings-influence`
   It is there in case a fix to the template has to go out mid-activity.
2. `uv sync`, then `uv run python measures.py`. It prints five lines that start with `ok`, one
   per measure it checks against a case worked out by hand. That proves the install without
   running the market or printing any result: nothing about this model runs before the Part 0
   commit, not a part script, not the hand check, and not `run_all.py`, which prints Part 1 and
   2 results.
3. Ask their name, and fill `**Name:**` and `**Date:**` at the top of `WRITEUP.md`. Those two
   are yours to compose; every other slot in that file you fill from their own words.
4. Commit as `Name and date`.

Then say setup is done and Part 0 is current, and in the same message ask the four Part 0
questions from `CLAUDE.md`, word for word. A word or a line each is enough.
