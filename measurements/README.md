# Influence simulation: measurements, Sep 22, 2026

Exploratory runs of the Spring 2024 "Simulation of Feedback Effects in Recommenders" model, made
while planning the Sep 24 activity (`../PLAN.md`, section 12 reads these numbers). They are the
answer key to the activity's Parts 2 to 5; the instructor decided Sep 22 that sharing it with an
activity is fine, so they live here.

| File | What |
|---|---|
| `sim_original.py` | The notebook's own functions, unchanged, for reference |
| `sim.py` | The same mechanics, vectorized, every constant a parameter |
| `check_agreement.py`, `check_agreement.json` | Distributional check that the port matches the original |
| `run_experiments.py`, `results.json` | The sweep, the control, the position-order conditions, the policies, the users-per-world scale; seed 20260922, 1000 worlds × 1000 users |
| `figures.py`, `fig1_strip.png` … `fig6_policies.png` | The six draft figures the activity plan describes |
| `make_report.py`, `REPORT.md` | The measurement report, generated from the JSON: agreement check, timings, stability, one table per experiment, the assumptions that drive the results |

Mechanics preserved from the notebook: 11 artists with a hidden true popularity; each user sees
five artists chosen by a policy from the world's download counts; the chance of picking a shown
artist mixes its count plus one, discounted by 1.2 per rank position, with its true popularity,
weighted by `social_influence`; one download per user; a user can only pick among the five shown.
