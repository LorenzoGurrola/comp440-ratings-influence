---
name: checkpoint
description: The end-of-part ritual. Run it at the end of every part and before submission. Runs run_all.py, names the part's blank writeup slots, confirms this session is in TRANSCRIPT.md, and commits the part once the student says yes.
---

Four steps, in this order, every time. Stop at the first thing missing: that is the current
step, and the part is not done until it is filled.

1. Run `uv run python run_all.py --part N`, with N the part being checked, and paste its output
   in full. `--part N` stops after Part N, so a later part's results never appear before the
   student has said what they expect from it. Before submission, run it with no `--part`. Do
   not summarize the output and do not say whether the numbers look right.
2. Read `WRITEUP.md` in full and name, one line each, every slot in **this part's section** that
   is still `XXXX`. Name them and ask what each needs; do not suggest wording. A prediction slot
   that a result has contradicted is not reworded; the "Revisited" slot at the end of Part 3
   takes the later thought.
3. Run `uv run python dump_transcript.py` and paste its last line. It says how many sessions are
   in `TRANSCRIPT.md` and whether this session is one of them. If the script fails on their
   machine, say so and go on: it costs them nothing.
4. If they have not already said to commit this part, ask whether they are ready, and wait.
   Only on a yes, said now or earlier in the message that asked for this checkpoint, make the
   commit yourself:

   ```
   git add -A
   git commit -m "Part N done"
   ```

   On anything other than a yes, say what is still open and stop.

Nothing here is a judgment about the work. Presence and form only.
