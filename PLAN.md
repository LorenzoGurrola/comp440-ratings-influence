# Influence simulation activity · Thu Sep 24, 2026 · plan

**Draft, Sep 22.** A plan for the instructor to react to, not a build. It was written in
`comp440-main/docs/` and moved here the same day at the instructor's ask; this file is the copy to
edit. The repo holds this plan and the Sep 22 measurements (section 12) and nothing else yet, the
module plan in `comp440-main` is untouched, and the
Sep 24 deck is still the unedited copy of the S24 Feedback Effects deck. Section 9 lists the decisions the build needs; section 10 is the
work, dated.

**What it is.** Students simulate a cultural market in the shape of Salganik, Dodds and Watts
(the Thursday reading): many identical worlds, each with a hidden true popularity per item, a
recommender that shows each arriving user five items, and users whose choices mix the counts they
see with their own taste. They run it with Claude Code from a template repo, in HW1's shape, and
they produce the paper's two measures, inequality and unpredictability, from their own runs, as
figures. The class did this in Spring 2024 from a Colab notebook (section 2). This version keeps
that model, exposes its assumptions, adds the measures and a control condition, and asks for about
three times the work.

**What it replaces.** The 32-minute live four-world market in the current Sep 24 rows, its
12-minute debrief, and the five prep items that block on it (dry run, twelve items, form and
sheet, fallback, round count). Two reasons beyond the instructor's ask: the live market was
designed for about 25 people in four worlds, and the enrolled count is 12 (module plan, Sep 22), so
each world would hold three people; and a simulation gives every student the paper's actual
measures, which three rounds of hand-counted picks cannot. A 12-person, three-round market is 36
downloads, and the simulation says that is where the leader is already mostly settled while the
room-to-room spread is widest (section 12, item 5).

## 1. Learning outcomes

Each outcome names the evidence in the student's submission that shows it. The module's third
outcome ("a ratings system that shows counts is a participant in preference, not a measurement of
it; two different things get called simulation") is what the activity teaches; HW1's fourth goal
(direct Claude and keep the judgments yours) is how it is taught.

| # | By the end, a student can | Evidence |
|---|---|---|
| 1 | State the paper's two claims as quantities: inequality is the Gini coefficient of market shares within a world, unpredictability is how much an item's share differs between worlds that started identical | The Gini and unpredictability figures from their own runs, with one sentence each on what the axis means |
| 2 | Show, from their own runs, that both quantities rise with social influence, and that the best items still rarely fail and the worst rarely win | The social-influence sweep (figures 2 and 3) and the quality-versus-success figure (4), with the sentence comparing each to the paper's Figures 1, 2 and 3 |
| 3 | Explain why a download or rating count is partly a record of what earlier users were shown, and name the position in a real interface that does this | The write-up's sentence on the tags-and-ratings timing figure from HW1 Part 2, or on HW0's three rankings, or on the "Popular on Netflix" row shown Sep 22 |
| 4 | Treat a recommender policy as an intervention: compare at least two policies on inequality, unpredictability and fidelity to true preferences, and state the tradeoff | The policy figure (6) and the write-up's tradeoff sentence, with the policy they designed described in words before Claude wrote it |
| 5 | Say what a simulation is and is not evidence for: name one modeling assumption that drives the result, change it, and report whether the conclusion survived | The sensitivity part: which assumption they changed (position effect, pseudo-count, linear counts, coverage, users per world) and the before-and-after numbers |
| 6 | Direct Claude through an experiment: predict before every run, verify one of Claude's numbers by another route, and keep the interpretation their own | Part 0 predictions committed before any run; the verification slot; every "what it shows" sentence in their words, per the transcript |

Outcomes 1, 2 and 5 are new relative to Spring 2024. Outcome 4 existed as "create a recommendation
algorithm that is better in some way to you"; the measures make "better" answerable.

## 2. The previous activity, as it ran

- **Source:** the Colab "Simulation of Feedback Effects in Recommenders",
  <https://colab.research.google.com/drive/1B_DZK-Tlv6Duv5Al_r0Z7mdS8nwlFvx6>, the instructor's
  copy, shared anyone-with-link. It is not in `data/materials.json` and sits outside the course
  folder; five student copies are next to it in Drive (student work, not read).
- **When:** launched in class Thu Feb 1, 2024, the Salganik day, alongside the SVD Colab; due as
  "Feedback effects activity" by 8am Tue Feb 13, twelve days later (S24 daily schedule sheet).
- **The model:** 11 artists with a hidden true popularity (Beatles 100 down to John Coltrane 10).
  1000 worlds of 1000 users. Each user is shown five artists chosen by a recommender function
  from the world's download counts so far. The chance of choosing each shown artist is a mix:
  `social_influence` × (its count + 1, discounted by 1.2 per rank position) and
  `1 − social_influence` × its true popularity, each normalized over the five shown. One
  download per user. The shipped recommender is top-five by count, padded at random.
- **What students did:** run the shipped recommender at social influence 0.5; then two
  experiments: repeat at high and low social influence and explain; write a "better" recommender,
  test it, explain.
- **The one figure:** a strip plot, one column per artist, one dot per world at the artist's share.
- **What it could not do.** No measure: inequality and unpredictability were read off the strip
  plot by eye, so "explain your results" had no number to explain. No control condition. "Better"
  was undefined, so the second experiment could not be wrong. The constants that drive the result
  (the 1.2 position discount, the +1 pseudo-count, the linear effect of counts, one download per
  user) sit inside helpers labeled "not required" to read. Speed was not the obstacle: the
  notebook's own code runs 1000 × 1000 in about ten seconds (measured Sep 22). The notebook did
  not ask for a sweep and had nothing to measure one with.

## 3. Updates, Spring 2024 to Fall 2026

| | Spring 2024 | Fall 2026 | Why |
|---|---|---|---|
| Delivery | Colab notebook, copied per student | GitHub template repo run with Claude Code, HW1's shape: `CLAUDE.md`, `WRITEUP.md` slots, transcript hook, `run_all.py` | The course's established with-Claude pattern; gives a transcript and a run gate |
| Who writes code | The student, by hand | Claude, to the student's spec; the student verifies | Frees the time for experiments; matches HW1's division of labor |
| The model | Constants hidden in helpers | The same mechanics, every constant a named parameter with a default and a comment | Outcome 5 needs them visible |
| Measures | None | Gini (inequality), Salganik's cross-world share difference (unpredictability), rank correlation with true popularity (fidelity), accidental-hit rate. The paper had to split its one independent world in two to get an unpredictability number for the control; the simulation just runs many independent worlds | Outcomes 1, 2, 4 |
| Control | None | The independent condition: social influence 0 **and random exposure** (five random artists shown), not the top-5 policy at 0. Measured Sep 22: the top-5 policy with no social influence at all already gives Gini 0.64, because a user can only pick among the five shown (section 12) | The paper's design; the quality-versus-success figure needs it |
| Conditions | One: counts shown, sorted | Three: independent; counts visible in random order (the paper's experiment 1); sorted by count (experiment 2) | Outcome 2, the presentation-order result |
| Experiments | Two, open-ended | Six parts, each predict, run, verify, one sentence | Outcome 6 |
| Figures | One | Six, listed in section 5 | The instructor asked for visualizations; each figure answers one question |
| Scale | 1000 worlds × 1000 users, pure Python, about 10 seconds a run | Vectorized, under a second a run; Gini and unpredictability are stable at 100 worlds, the win-rate measures need 1000 | A six-point sweep takes seconds, so students can afford to try things |
| Grading | Take-home, weight not recorded here | Slots in `WRITEUP.md` plus figures; weight and category TBD (section 9) | |
| Time | About 2–3 hours, estimated | About 5–6 hours over twelve days | The instructor's ask: quite a bit more |

## 4. The activity, part by part

Every part runs the same loop, which is HW1's: the student says what they expect, Claude runs it,
the student checks one number by another route, the student says what it shows and Claude writes
that sentence down unchanged. Parts 0 and 1 happen in class Thursday. The rest is take-home.
Student time is an estimate.

| Part | The student does | Claude does | Output | Time |
|---|---|---|---|---|
| 0 · Predictions | Four predictions before any run: which artist wins most often at social influence 0.5; whether inequality rises or falls with social influence; whether the best artist ever loses a world; whether a recommender can lower inequality without lowering fidelity. A reason each | Writes them into `WRITEUP.md` unchanged; commits; refuses to run anything before that commit | The Part 0 commit | 10 min, in class |
| 1 · Baseline | Runs the shipped policy at social influence 0.5 and reads the strip plot; recomputes one world's Gini by hand from the printed shares and reports whether it matched | Runs it, prints the shares of one world, draws figure 1, describes the axes and stops | Figure 1, the verification slot, one sentence | 15 min, in class |
| 2 · The sweep | Chooses the social-influence levels; predicts the shape; reads the Gini and unpredictability curves against the paper's Figures 1 and 2 (direction, not size) | Runs the sweep, draws figures 2 and 3 | Figures 2 and 3, one sentence each | 45 min |
| 3 · What is shown | Runs the three conditions: independent, counts in random order, sorted by count; reads quality against success | Runs them, draws figure 4 in the paper's Figure 3 layout | Figure 4, one sentence on which condition moved success away from quality | 45 min |
| 4 · A policy | Describes a policy in words before any code (damped popularity, exploration, hiding counts, anything); predicts its effect on the three measures; compares it with the shipped policy and random | Implements exactly what was described, runs the comparison, draws figure 6; never proposes a policy first | Figure 6, the policy in the student's words, the tradeoff sentence | 60 min |
| 5 · One assumption | Picks one assumption (the position discount; the pseudo-count; counts entering the choice linearly rather than as a log; the recommender only ever showing artists that already have a download; users per world); predicts; changes it; reports whether the Part 2 conclusion survived; the users-per-world case is the classroom-scale run, 12 users and 3 rounds | Reruns, draws figure 5 for the trajectories | Figure 5, before-and-after numbers, one sentence | 45 min |
| 6 · Connections | Two sentences: where this shows up in data they have already handled (HW1 Part 2's tags-and-ratings timing figure, or HW0's three rankings), and where it shows up in an interface (the "Popular on Netflix" row from Sep 22); plus two of HW1's Part 4 questions on working with Claude | Writes their words; runs `/checkpoint`; commits and pushes on their yes | The last slots | 30 min |

**Why the simulation is a good fit for "with Claude".** The mechanical work is code and plots,
which Claude does well; the graded work is a prediction, a verification and a sentence, which
Claude is told not to supply. That division is cleaner here than in HW1, where the code itself
carries judgment.

## 5. The visualizations

Each figure answers one question and carries one student sentence. Plain matplotlib, labeled
axes, the question in the caption, no decoration; Claude draws them, the student reads them.

| # | Figure | Question it answers | Paper counterpart |
|---|---|---|---|
| 1 | Strip plot: one column per artist ordered by true popularity, one dot per world at its share, a marker at its true share | Do identical worlds end the same way? | none; the S24 figure, kept |
| 2 | Gini versus social influence, with the independent control marked | Does inequality rise with social influence? | Figure 1, inequality |
| 3 | Unpredictability versus social influence | Does unpredictability rise with it? | Figure 2 |
| 4 | Two panels: share, then rank, in the independent condition (x) against each influence world (y), per artist | Does quality still predict success, and where does it stop predicting? | Figure 3 |
| 5 | The leader's cumulative share as users arrive, twelve worlds overlaid; a second panel for the true best artist | When does a world lock in, and can a mediocre artist hold the lead? | none; the live-market "accidental hit", now visible per world |
| 6 | Gini, unpredictability and fidelity per policy, dots on three panels | What does the recommender's rule cost and buy? | none |

Figures 1 to 3 come from Parts 1 and 2; 4 from Part 3; 6 from Part 4; 5 from Part 5. The
Thursday debrief shows figures 2 and 3 from one pair's run next to the paper's Figures 1 and 2 on the
deck, which is the second Keshav pass the current rows already promise.

## 6. Claude's role, in the rules

`CLAUDE.md` is HW1's, cut to this activity. Claude is the analyst-intern; the student is the
senior analyst.

- **Freely:** write and run the simulation and the measure code; draw any figure asked for, axes
  labeled; explain Gini, the unpredictability measure, rank correlation, the mixing rule, as often
  as asked; vectorize slow code.
- **Never:** choose a social-influence level, a policy, a constant to change, or the artists;
  propose a policy before the student has described one (ask what their instinct is; then, if
  asked, name families in neutral order); say what a figure shows or means (describe the axes and
  stop); write or reword a prediction, a verification or a "what it shows" sentence; run a part
  before the previous part's slots are filled and committed; state a number it did not compute this
  turn.
- **Always:** ask what the student expects before the first run of each part; read `WRITEUP.md`
  in full at the start of a session; write the student's words into the slot in the same turn they
  say them and read the line back; offer a commit at the end of each part.
- **Not edited by anyone:** `TRANSCRIPT.md`, `run_all.py`, `measures.py`, `load_data.py` if there
  is one. The simulation file is the student's to change in Part 5, which is the point.

The class's own AI agreements (v1, Sep 10: transparency about AI use, keep your own agency, know
what AI is doing to your product and your learning) are consistent with this and can be cited on
the launch slide in the students' words, which are already in the shared doc. The syllabus floor
holds: the Salganik reading reflection, due 8:00am Thursday, is no-AI; the activity is AI-encouraged
for code and figures and no-AI for the sentences.

## 7. Delivery

**Recommended: a template repo in HW1's shape**, `shilad/comp440-ratings-influence`, public,
forked by each student, run with Claude Code. The instructor created the repo Sep 22; it holds
this plan and the Sep 22 measurements, and nothing student-facing yet. Ships:

| File | What | Written by |
|---|---|---|
| `sim.py` | The S24 mechanics, vectorized, every constant a named parameter with the S24 default | ships; the student changes one constant in Part 5 |
| `measures.py` | Gini, unpredictability, fidelity, accidental-hit rate, tested | ships, not edited |
| `plots.py` | The six figures as functions | ships; the student may ask Claude to change them |
| `part1_baseline.py` … `part5_assumption.py` | One script per part, docstring says what it prints | student and Claude |
| `WRITEUP.md` | The slots: four predictions, the verification, one sentence per figure, the policy in words, the tradeoff, the assumption before-and-after, the two connections, two working-with-Claude answers | the student's words, written by Claude |
| `run_all.py` | Reruns everything, lists blank slots | ships, not edited |
| `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/setup`, `/checkpoint` | Section 6; the transcript hook; the allow-list | ships |
| `figures/` | The six PNGs | Claude commits them |

**Alternative: the S24 Colab plus claude.ai.** Zero build; loses the transcript, the run gate,
the Part 0 gate and the measures, and the student writes the code. It is the fallback if the repo
is not ready by Thursday morning, in which case Thursday launches Parts 0 and 1 on the notebook and
the repo lands for the take-home parts.

**In-class access.** Same as HW0's launch: if Claude Code is not working for part of the room, the
instructor's screen is the shared session for Part 1 and everyone else predicts and verifies from
the printed shares. Nothing in Part 1 needs more than the printed numbers.

## 8. Thursday, proposed rows

For the instructor to paste into the Sep 24 section of `docs/modules/collective-traces.md` in
`comp440-main`, or to
ask for by name; this file does not change the module plan. The news discussion is the
instructor's own 20 minutes this week. The Generative Agents block and the comparison table (22
minutes in the current rows) do not fit alongside both the news discussion and a launch; the rows
below leave them out, and section 9 has the decision. Sum: 90.

| Min | Block | What happens | Slides |
|---|---|---|---|
| 5 | Opening | Brent Hecht visits Tue Sep 29, speaker questions due 8:00am that morning; HW1 due Thu Oct 1 8:00am; the Salganik reflection landed this morning; today launches a take-home activity, due [TBD: date] | |
| 20 | News discussion | The instructor's slot; format as the sign-up doc says | [TBD: instructor] |
| 3 | The day's question: what if ratings aren't independent? | HW0 ranked 1,682 movies by count, plain mean and shrunken mean and the top ten changed each time; every rule read ratings as a record of what people independently thought; today's question stays on the board: what if ratings are partly a record of what people saw other people rate; hands, who picked a restaurant, song or paper mostly for its count | Your rankings assume ratings are independent. What if they aren't? |
| 12 | The reading: what Salganik et al. did | Which Keshav pass did you do, pass 1 is enough today; four questions, answers taken before confirming: what the independent world is for (14,341 participants, 48 songs by unknown bands, one independent world and eight social-influence worlds in each of two experiments; experiment 1 showed the songs with their counts in a 16 × 3 grid in random order, experiment 2 in one column sorted by count; all checked against the PDF Sep 22); why eight parallel worlds; the two outcome measures and why two (inequality is the Gini coefficient of market shares within a world; unpredictability is a song's average share difference between pairs of worlds, averaged over songs); what quality did; land the sentence: the outcome is not recoverable from the songs alone, and showing people the counts is what does it; both measures on the board, they are the numbers you compute next | Which pass did you do? · The paper's four questions · Inequality and unpredictability: two measures, two claims |
| 8 | The simulation: the model and the rules | The S24 diagram: worlds, hidden true popularity, a recommender, users who see five items and mix the counts with their taste; the four constants on the slide, named; what Claude does and what is yours, in one line each; the class AI agreements, quoted from the shared doc; fork, clone, `uv sync`, `claude`, `/setup` | The model, on one slide [pull: 2026 Feedback Effects, 19] · What Claude does, what you do · Fork, clone, /setup |
| 10 | Part 0: four predictions | Everyone types four predictions with a reason into Claude; Claude commits; the run gate means nothing runs before that commit; hands: who predicted inequality falls | Four predictions, before any run |
| 15 | Part 1: the baseline, in pairs | Run the shipped policy at social influence 0.5; the strip plot; each pair recomputes one world's Gini by hand from the printed shares and posts match or diverge in Slack; one sentence per pair on the figure | The strip plot [empty: built live] · Match or diverge |
| 10 | Debrief: ours against theirs | Two pairs' figures 2 and 3 on screen next to the paper's Figures 1 and 2, if any pair got the sweep running, else the instructor's own run; same direction, different size, and why the size means nothing here; the take-home parts, two minutes each; where this is in HW1: the tags-and-ratings timing figure in Part 2 | Ours vs theirs · Where this is in your HW1 |
| 4 | Close | Parts 2 to 6 due [TBD]; Brent Hecht Tuesday, questions 8:00am; HW1 Oct 1; students photograph the slide | |
| 3 | Slack | Cut if behind: the HW1 questions thread | |

**A second shape, if Generative Agents stays.** Cut the launch to Part 0 only (10 minutes), run
Part 1 at home, and drop the debrief; the news discussion stays. That keeps the 22 minutes but the
room never sees a figure, and the debrief moves to Tue Oct 6 or to Slack.

**Corrections to the current Sep 24 rows, whichever shape runs.** "Where this is in your HW1: the
popularity baseline" is stale: the HW1 that shipped Sep 17 is tag-based and has no popularity
baseline. The live tie is HW1 Part 2 step 2, the figure of when a movie's tags and ratings arrived,
where the 2006 tag-suggestion spike is the interface, not the movie; and HW0's three rankings by
count, mean and shrunken mean. The paper's numbers in the module plan's reading row were checked against the PDF Sep 22 and
are right (section 11), so its VERIFY item on them can be closed.

## 9. Decisions for the instructor

- [ ] **Go or no go on the repo build**, and by when. The repo does not exist. Section 10 is the
  work; it is a session's day plus a dry run, and Thursday is in two days. If no go, the S24 Colab
  runs Parts 0 and 1 on Thursday and the repo follows for the take-home parts.
- [ ] **Due date.** Proposed Tue Oct 6, 8:00am: twelve days, as S24 gave, and after both HW1 (Oct
  1) and Brent Hecht's questions (Sep 29). Thu Oct 8 is Frank Schilder's tentative visit and the
  Retrieval module's last day. Earlier than Oct 1 stacks it on HW1.
- [ ] **Weight and category.** S24's weight is not recorded in the repo. The live syllabus has
  "reading reflections and activities" at 25% and homework at 30% with 6% each; this is more than
  a reflection and less than a homework. Two options: a fixed number of points in the 25% bucket,
  or an unweighted 0/1/2 like a reflection with the figures as the evidence.
- [ ] **Individual or pairs.** Parts 0 and 1 run in pairs in class; the take-home parts as one
  repo per pair or one per student. HW1 is individual.
- [ ] **Submission.** The assignment form's homework branch takes a repo URL; either that branch
  as is, or a new first-question option for activities. A Forms edit is the instructor's to make:
  <https://docs.google.com/forms/d/1nNjZ4z584ODWb8N-p2TLJAorHEqZTXHnfdR_MUJ1P88/edit>.
- [ ] **Generative Agents on Thursday, or later.** Section 8's rows leave it out; the second shape
  keeps it and cuts the launch to ten minutes. It can open the Agents module Nov 10 without loss.
- [ ] **The items.** Keep the eleven artists, or switch to obscure MovieLens titles for continuity
  with HW0 and HW1. The artists are the instructor's and students may recognize them, which does
  not matter here because true popularity is a number the model hides, not a belief in the room.
- [x] **Repo name and visibility.** Settled Sep 22: `shilad/comp440-ratings-influence`, public,
  created empty by the instructor.
- [ ] **The 1.2 position discount, the +1 pseudo-count and one download per user** stay the
  defaults, so that Part 5 has something to change. If the instructor wants different defaults,
  say so before the build, not after students have forked.
- [ ] **Exposure lock-in: keep it or fix it.** In the S24 model a user can only choose among the
  five artists shown, so the top-5 policy locks every world into whichever five got the first
  downloads, and that alone produces most of the measured inequality before social influence does
  anything (section 12). Two options: keep the model as it is and make the lock-in the point of
  Part 4, with the random-exposure control showing the cost; or add one parameter, the chance that
  a user picks outside the five shown, so that social influence and exposure can be varied
  separately. The second is closer to the paper, where every participant saw all 48 songs. Decide
  before the build; it changes what the sweep in Part 2 looks like.

## 10. Prep, dated

- [ ] Sep 22 — Instructor: the decisions in section 9, at least the first three, so the build can
  start. No build runs before a go (lecture-deck skill, stage 0, applies to the repo too).
- [ ] Sep 22–23 — Session, on the go: fill the `comp440-ratings-influence` repo in HW1's shape;
  port `sim.py` with named parameters (the Sep 22 measurement scripts in `measurements/` are the
  reference implementation); write and test
  `measures.py` against a hand-computed Gini; write `plots.py`;
  `CLAUDE.md` per section 6; `WRITEUP.md` slots; `run_all.py`; the hook and allow-list; the
  README with the six parts, the AI guidelines and the rubric. Estimate: 4–5 hours.
- [ ] Sep 23 — Session: dry-run Parts 0 and 1 as a student, cold, in a fresh fork; time them; fix
  what breaks. Estimate: 1 hour. Then the instructor runs Part 0 himself once.
- [ ] Sep 23 — Session, with the instructor's go: add the launch slides to the Sep 24 deck (the
  copied S24 deck, untouched since Sep 13): the model slide is its slide 19 already; add "What
  Claude does, what you do", "Fork, clone, /setup", "Four predictions", "Match or diverge", "Ours
  vs theirs", "Where this is in your HW1". Add, never rewrite; the deck is his copy.
- [ ] Sep 23 — Session, through the `schedule-change` skill: link the repo on the Sep 24 row and
  add the due date to `assignments:`; `build.py` before pushing. The Salganik reading row stays as
  it is.
- [ ] Sep 23 — Instructor: the form option, if a new one is wanted; announce in `#comp440-f26`
  that Thursday needs a laptop with Claude Code working, as HW0's launch did.
- [ ] Sep 24, morning — Session: process the Salganik reflections per the `process-reflections`
  skill; the four reading questions on the deck are already written and do not depend on them.
- [ ] Sep 24 — Instructor: the news discussion's 20 minutes are his; the sign-up doc was shared to
  the Macalester domain Sep 22 (module plan), so that item is closed.
- [ ] Sep 24 — If behind at minute 40, cut the reading block to the four questions, not the launch;
  Part 0 must happen in the room or the run gate has no meaning.

## 11. Verified and not

- **Verified Sep 22:** the S24 notebook's mechanics and student tasks (read from the instructor's
  copy); the S24 dates (daily schedule sheet); the deck's contents (the 2026 copy, 19 slides, slide
  19 is the model diagram, slide 10 is the paper's Figure 3, slides 12–14 are the Netflix paper);
  HW1 as published at `origin/main` (tag-based, Part 2 step 2 has the timing figure, Part 4 has the
  working-with-Claude questions); enrolled count 12 (module plan, Sep 22).
- **Measured Sep 22:** the S24 mechanics at the proposed defaults, 1000 worlds × 1000 users;
  section 12 has the numbers and what they change in the plan.
- **Verified Sep 22, against the paper's text** (Science 311, Feb 10 2006, pp. 854–856; the
  assigned PDF and the full version at princeton.edu both extract with `pypdf` in a clean virtual
  environment, so the module plan's note that the text does not extract is out of date): 14,341
  participants; 48 songs by unknown bands; two experiments, each with one independent world and
  eight social-influence worlds; experiment 1 a 16 × 3 grid in random order per participant with
  counts shown, experiment 2 a single column sorted by current popularity; the independent
  condition shows no counts, in random order. Inequality is the Gini coefficient of market shares
  (Figure 1). Unpredictability is, per song, the average absolute difference in market share
  between all pairs of worlds, averaged over songs (Figure 2); for the independent condition the
  authors split the one world into two random halves, 1000 times. Figure 3 plots share and rank
  in the independent world against the eight influence worlds, with more convexity in experiment
  2. "The best songs rarely did poorly, and the worst rarely did well, but any other result was
  possible" is the abstract's sentence.
- **Not verified:** the S24 activity's weight; the estimated student times.

## 12. The model at the defaults, measured Sep 22

The S24 notebook's mechanics were ported, unchanged, to a vectorized script and run at 1000
worlds × 1000 users with a fixed seed. The scripts, the raw numbers, the report and six draft
figures are in `measurements/` in this repo. They are the answer key to Parts 2 to 5; the
instructor decided Sep 22 that sharing it with an activity is fine, so it ships with the repo.
Every condition below ran in about one second, so the sweeps the activity asks for are cheap.

**The social-influence sweep**, top-5 policy, position discount 1.2, pseudo-count 1:

| Social influence | Gini | Unpredictability | Rank correlation with true popularity | True best artist finishes first | Winner has true popularity 30 or less |
|---|---|---|---|---|---|
| control: random exposure, 0 | 0.28 | 0.010 | 0.98 | 60% | 0% |
| 0 | 0.64 | 0.088 | 0.48 | 55% | 0% |
| 0.25 | 0.66 | 0.091 | 0.45 | 48% | 0% |
| 0.5 | 0.68 | 0.101 | 0.39 | 29% | 0.3% |
| 0.75 | 0.72 | 0.123 | 0.26 | 17% | 16% |
| 0.9 | 0.78 | 0.142 | 0.16 | 12% | 28% |
| 1.0 | 0.84 | 0.155 | 0.01 | 10% | 34% |

The Gini of the true popularity distribution itself is 0.30.

What the numbers say, and what each changes in the plan:

1. **Both measures rise with social influence, as in the paper.** Gini goes from 0.64 to 0.84
   and unpredictability from 0.088 to 0.155 between influence 0 and 1. The best artist still
   wins most often at low influence, and an artist with true popularity 30 or less wins a third
   of the worlds at full influence. Parts 2 and 3 will show what they are meant to show.
2. **The recommender alone produces most of the inequality.** With social influence 0, the
   top-5 policy already gives Gini 0.64 and unpredictability 0.088, against 0.28 and 0.010 for
   random exposure. Every world ends with exactly five artists downloaded and six at zero: a user
   can only pick among the five shown, and the top-5 rule never shows a sixth once five have a
   download. That is exposure lock-in, not social influence, and it is the feedback loop the
   Sep 22 reading named. Consequences: the independent control must be random exposure (section 3
   says so now), and the model mixes two effects the paper separates, which is a flaw to fix
   before the build or the activity's best teaching point. Section 9 has the decision.
3. **Presentation order matters less here than in the paper.** At social influence 0.5, turning
   the position discount from 1.0 (no order effect) to 1.2 to 1.5 moves Gini from 0.65 to 0.68
   to 0.71. Same direction as experiments 1 and 2, small size, so Part 3's sentence will be
   about direction.
4. **Policies at social influence 0.5** (Gini / unpredictability / rank correlation): random
   exposure 0.24 / 0.019 / 0.91; top-5 by count 0.68 / 0.101 / 0.39; damped popularity with
   K = 20, 0.68 / 0.102 / 0.35, that is, no change: shrinking counts toward a uniform prior is
   order-preserving, so it changes neither which five are shown nor their order, only the number
   displayed, and at 1000 users that shrink is about two percent; top-4 plus one random artist 0.66 /
   0.099 / 0.63, so one exploration slot leaves inequality and unpredictability where they were
   and restores most of the fidelity to true taste; the five shown in shuffled order 0.65 /
   0.098 / 0.39. A student who proposes damping, which Sep 15 made the answer to noisy means, will
   find it does nothing here; that is a result and should be graded as one. The README should say
   that some policies will not move the numbers, without saying which.
5. **A short run is noisier, not weaker.** At 50 users per world, unpredictability is 0.117 and
   an artist with true popularity 30 or less wins 8% of worlds; at 1000 users, 0.101 and 0.3%.
   Part 5's classroom-scale run will show more accidents, not fewer, and the current Sep 24
   debrief row's "expect a weaker effect" from three rounds is the wrong prediction for this
   model. The report's lock-in table says why: at social influence 0.5 the artist leading after
   20 downloads is still leading at 1,000 in 64% of worlds, and after 50 downloads in 74%. A
   12-person, three-round market is 36 downloads, so it lands where the leader is mostly settled
   but the world-to-world spread is widest, and it cannot measure unpredictability at all,
   because that is defined across worlds and one room is one world.
6. **The lock-out is visible per world.** At social influence 0.75, the true best artist got no
   downloads at all in 8 of 12 sample worlds, shut out of the five before its first download
   (figure 5). That is the accidental hit as a mechanism, which the live market could only have
   shown as a table.

**The port matches the original.** At 200 worlds and social influence 0.5, every measure from
the notebook's own code sits within 0.6 standard deviations of the port's spread over eight
seeds (Gini 0.6805 against 0.6792, unpredictability 0.1014 against 0.1012).

**Timing and stability.** The original runs 1000 worlds × 1000 users in about 10 seconds, the
port in 0.7. Gini and unpredictability move by 0.003 or less between seeds at 100 worlds. The
win-rate columns (true best first, accidental hit) carry a standard error of about 0.015 even at
1000 worlds, so a difference under 0.04 in those columns means nothing, and the README should say
so where it asks for them.

**The assumptions that drive the results**, in the report's order of size: the recommender only
shows artists that already have a download; the position discount; counts entering the choice
linearly; the pseudo-count; one download per user; true popularity normalized over only the five
shown; one scalar for everyone's social influence; independent worlds with sequential arrival.
Part 5 draws from the first five. The full report is `measurements/REPORT.md`.
