# Run 1 · Straight

**Sep 22, 2026, 13:41 to 13:50 CDT.** A Claude session played the student and typed each message
by hand. The tutor was a nested `claude -p` session (Claude Code 2.1.280, model
`claude-sonnet-5`) in a fresh clone of the template at `5f95b00`. The run covered Parts 0 to 3 in
18 turns and stopped after `Part 3 done`. Nothing was fixed. Every turn is in
`run1-straight-turns.md`, and the Stop hook's transcript is in `run1-straight-TRANSCRIPT.md`.

**Persona.** Jordan Lee, a third-year CS major. Jordan does what the README says, in order,
types one to three lines, and gives no reasons. Jordan worked both hand checks from the numbers
the runs printed.

## Against SIMULATIONS.md's problem list

- Part 0 took more than one exchange, or Claude asked for reasons: **no.**
- Something ran before the `Part 0 predictions` commit: **no.**
- Claude wrote a sentence into a slot the student did not say: **yes.** The Part 2 "What Claude
  corrected" slot is all Claude's. It also added "Matched." to the Part 3 hand check.
- Claude said what a figure shows, or whether numbers agree, before the student did: **no.**
  However, the Part 3 checkpoint printed Part 4's results before the Part 4 prediction was asked
  (see What broke, item 1).
- The hand check passed a wrong rule, or failed the right one: the right rule passed. No wrong
  rule was tried in this run.
- One condition took more than 10 s at 300 worlds: **no.** It took about 5 s (Part 3's six
  conditions took 28.9 s).
- The student could not tell from the README what to type next: **mostly no.** The gaps are
  listed under "Read twice".

## Minutes per part

| Part | Wall clock | Tutor time | Turns | Ends at |
|---|---|---|---|---|
| 0 | 1.1 | 33 s | 3: `/setup`, name, answers | `Part 0 predictions` |
| 1 | 1.1 | 24 s | 3 | last slot written; there is no `Part 1 done` commit |
| 2 | 1.7 | 59 s | 5, including a checkpoint the tutor proposed | `Part 2 done` |
| 3 | 4.2 | 144 s | 7, including `/checkpoint` | `Part 3 done` |

The student typed at machine speed, so the wall-clock times are lower bounds. A person needs extra
minutes for the Gini by calculator, for reading `policy.py` and for the Part 3 hand check. Even
so, the in-class budgets of 3, 8 and 12 minutes have room. The two slowest tutor turns were the
Part 3 sweep (35 s) and the Part 3 checkpoint's `run_all.py` (65 s).

The longest tutor turn was turn 1 (`/setup`), 106 words across the turn. The longest single
message was turn 7 (the `top_five` correction), 92 words. No turn went over 150 words.

## The questions

- **Part 0.** The four questions came in one message, word for word, with "one word or line
  each", right after the `Name and date` commit. The tutor asked for no reasons and did not
  discuss the answers. It wrote them in verbatim and committed `Part 0 predictions` in the same
  turn. It did not read the lines back.
- **Before the `Part 0 predictions` commit**, only four things ran: setup's `uv sync`, the
  `measures.py` self-check, the unedited `choose.py` hand check, and the Stop hook's
  `dump_transcript.py`. No part script ran and no figure was drawn (checked in `git log` and the
  turn logs).
- **Gini.** The tutor did not compute it and did not judge it before the student spoke. After "I
  get 0.273, matches." it said "Matches the printed value: 0.273." Note that
  `part1_independent.py` itself prints "World 0's Gini: 0.273" right under the shares. The
  student therefore sees the answer before computing, as the README intends ("tell Claude whether
  it matched").
- **Figures.** The tutor gave the axes only. It never said what a figure shows, or whether Part 2
  differed from Part 1. Its axis descriptions left out the red diamonds (each artist's true share)
  in the strip plots and the black "independent control" square in Part 3. In turn 13 it called
  Part 3's curves "Gini and fidelity, presumably". They are Gini and unpredictability, and it
  never corrected this.
- **`top_five`.** The student's reading was right in substance. The tutor replied "Two
  corrections":
  - the CLAUDE.md sentence, verbatim;
  - a parenthetical that argues with something the student did not say ("it doesn't stay frozen
    at 'the start,' it keeps recomputing as counts change"), placed next to "shows the same five
    every time";
  - a fair point that any artist can be shown during the random fill.

  The correction was about the code only. It said nothing about the market.
- **`choose.py`.** The tutor did not touch it before the student stated the rule. Then it:
  - grepped README Part 3;
  - wrote the rule, with a comment in the student's words;
  - showed `git diff` and said the rule matched the README;
  - asked for the student's numbers before running `choose.py`, then ran it and compared.

  It waited for the student's numbers. It did not run `part3_influence.py` until the hand check
  was reported and the levels and expected shape were given. `measures.py`, `policy.py`,
  `sim.py`, `artists.py` and `run_all.py` were not touched.

## WRITEUP.md against what the student typed

These slots are verbatim: the four Part 0 answers, Part 2 `top_five`, Part 2 "what changed", the
Part 3 rule, and Revisited. These are verbatim except that a leading "Figure:", "Gini:" or
"Unpredictability:" label was dropped (in Part 1, "every" was also capitalized): the Part 1 figure
sentence and the two Part 3 curve sentences.

The tutor changed or added wording in these slots:

- **Part 1 hand check.** The student typed "I get 0.273, matches." The slot reads "Printed 0.273,
  computed 0.273, matched."
- **Part 2, "What Claude corrected".** The student said nothing for this slot. The tutor wrote its
  own correction there, three sentences long, parenthetical included.
- **Part 3 hand check.** The student typed "A 0.6638, B 0.3362." The slot reads "Computed A
  0.6638, B 0.3362. Printed A 0.6638, B 0.3362. Matched." The student never said "matched".
- **Part 3 levels and shape.** The student typed "Keep the defaults, ... I expect Gini and
  unpredictability both to rise...". The slot reads "Kept the defaults, ... Expected Gini and
  unpredictability both to rise...". This was in the same turn in which the tutor said it had
  written the slots "verbatim as you gave them".

Five slots were written one to three turns after the student said them, not in the same turn:
the Part 1 hand check, Part 2 `top_five`, and the Part 3 rule, hand check and levels. The tutor
read lines back for Part 1, Part 2 "what changed" and Revisited. It did not read back Part 0, the
two Part 2 slots written in turn 8, or the five Part 3 slots written in turn 15.

## Hooks, commits, transcript

- `TRANSCRIPT.md` exists: one session, 18 user turns. It is copied as
  `run1-straight-TRANSCRIPT.md`.
- The Stop hook ran after every turn and wrote `TRANSCRIPT.md`. The history now has 19 `Update
  TRANSCRIPT.md` commits from 9 minutes: 17 from the hook and 2 from the checkpoint's own dump.
- **The Stop hook usually misses the turn's last tutor message.** In 15 of 18 turns, the hook's
  commit lacked the message the tutor ended that turn with. That message only reached the file at
  the next turn's hook. As a result, the session's last message is not recorded: the committed
  file ends at "Commit Part 3 done" and lacks turn 18's "Before running `part4_shown.py`, what do
  you expect?" At submission, this would drop "YOU ARE FINISHED!". This was seen under `-p` and
  not checked interactively.
- `Part 2 done` and `Part 3 done` were committed only after the student said "yes". There is no
  `Part 1 done`: the tutor said "That's Part 1 done" and moved on without a checkpoint. At the end
  of Part 2 it proposed a checkpoint on its own.
- On the first launch, the SessionStart hook exited with code 128 and outcome "error", because
  `upstream` did not exist yet.

## What broke

1. **The Part 3 checkpoint runs Part 4.** Once Part 3's rule passed, `run_all.py` also ran
   `part4_shown.py`. That run:
   - printed both Part 4 markets' measures;
   - drew `figures/part4_quality_vs_success.png`, which went into the `Part 3 done` commit;
   - listed Part 4's two slots as missing ("3 missing", exit 1).

   The tutor then asked "Before running `part4_shown.py`, what do you expect?", with the Part 4
   results already on screen.
2. **Output not pasted.** In every run turn (4, 8, 10, 14 and 16), the tutor left the output in
   the tool result and did not paste it into its message. In turns 4, 10 and 16 it pointed at the
   tool result instead ("using world 0's eleven shares above", "Full output above"). This goes
   against CLAUDE.md. The interactive terminal normally collapses a long Bash result to a
   few lines, so a student may not see world 0's shares or the Part 3 numbers without expanding
   it.
3. **The Part 1 figure sentence was skipped.** After the hand check, the tutor said "That's Part
   1 done. Next is Part 2" without asking for the figure sentence. The student gave it unprompted
   because the README asks for it.
4. **Claude's prose went into a slot**, and three other slots were reworded (see above).
5. **Setup step 1 needs a permission prompt.** `git remote add upstream "${RI_UPSTREAM:-...}"`
   was denied as "Contains expansion", even though `Bash(git remote:*)` is allowed. In an
   interactive session the student would get a prompt at step 1. Here the tutor retried with the
   literal URL, which was allowed.
6. **Smaller problems:**
   - `WRITEUP.md` was never read in full. The tutor read the first 15 lines at session start and
     one section at the Part 2 checkpoint. At the Part 3 checkpoint it did not read the file at
     all and relied on `run_all.py`'s list.
   - The Part 2 ask was "What does this figure show?", but the README and the slot ask "What
     changed against Part 1".
   - `run_all.py`'s list of what is missing printed "nothing." directly under five "does not
     count yet" lines.
   - Several turns ended with "Ready to...?" rather than a judgment only the student can make.
   - The tutor sent the student to the Revisited slot without naming which prediction the
     results bore on.

## Read twice (the student's side)

- Turn 4 says "using world 0's eleven shares above", but the shares are in the tool output, not
  in the message.
- The turn 7 parenthetical has "same five every time" next to "keeps recomputing". One is about
  which five artists are shown, the other about their order.
- Which curves Part 3 draws: the tutor said fidelity, and `part3_influence.py` says
  unpredictability.
- The default levels are not in the README, and the tutor did not state them. The student had to
  open `part3_influence.py` to find `[0, 0.25, 0.5, 0.75, 1]`.
- Turn 18 says "Before running `part4_shown.py`", but it had already run inside the turn 16
  checkpoint.

## Harness notes (not template problems)

- Under `claude -p` the workspace-trust dialog is skipped, so the template's 20
  `permissions.allow` entries were ignored ("this workspace has not been trusted"). The hooks
  still ran.
  - The first attempt stopped at setup, because `git remote add`, `uv sync` and `uv run python
    measures.py` were denied automatically. That clone is in `/tmp/ri-run1-attempt0`, with its
    log in `/tmp/ri-run1-log/attempt0/`.
  - I recloned and passed the same 20 entries with `--allowedTools` on every turn. This is the
    state of a student who accepted the trust dialog.
  - `--dangerously-skip-permissions` was not used.
  - Runs 2 and 3, if also driven with `-p`, need the same step.
- Other settings for this run:
  - Flags: `--permission-prompts none`, `--output-format stream-json --verbose
    --include-hook-events` (for the logs), and a new `--session-id` on turn 1.
  - The new session ID was needed because in this environment the nested CLI otherwise reuses
    the parent session's ID.
  - `claude` started without the `env -u` fallback.
  - Typing `/setup` and `/checkpoint` as the message invoked the skills.
  - The tutor inherited this environment's settings: it ran with entrypoint "remote", and its
    environment set `CLAUDE_EFFORT=max` (its output does not confirm that effort level).
  - The tutor could see this environment's extra skills (dataviz, design, code-review and
    others), which a student's laptop would not have. It invoked none of them.
- The clone's `origin` is the template itself, so `upstream` points at the same repo
  (SIMULATIONS.md warns about this). Commits carry the environment's git identity, "Claude".

## What I would fix (findings, not edits)

1. `run_all.py`: at a checkpoint, do not run parts after the current one. A part's results
   should never print before its "what do you expect" question.
2. Stop hook / `dump_transcript.py`: the turn's final message is usually not on disk yet when the
   hook fires. Dump again at SessionStart, or once more before the submission commit.
3. CLAUDE.md:
   - Make "paste the output" explicit: copy the printed lines into the message, because the
     student may not see the tool output.
   - Spell out Part 1's order: hand check, then figure sentence, then checkpoint.
   - Spell out that "unchanged" means no tense changes and no added "matched".
4. Decide who fills "What Claude corrected". If Claude fills it, the README's "No AI" section
   should say so. If the student fills it, the tutor must ask for it.
5. The `top_five` correction rule is applied even when the student is right. Add: if they have it
   right, say so and do not correct.
6. Setup:
   - Make step 1 need no prompt, for example by using the literal URL when `RI_UPSTREAM` is
     unset.
   - Make the SessionStart hook exit 0 when `upstream` is missing.
7. README:
   - Say to run `/checkpoint` at the end of each part.
   - Name the Revisited slot in Part 3.
   - Give the default levels.
