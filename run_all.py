"""
Run every part, start to finish, and say what is still missing.

    uv run python run_all.py

Runs measures.py's self-check, then Parts 1 to 5, then Part 6 once the line ending "delete this
line when you start" is gone from part6_assumption.py. A part that stops, because it failed or
because what it needs is not done yet (Part 3's rule in choose.py, your policy in my_policy.py),
does not stop the others.

Then it lists what is missing: the slots in WRITEUP.md still holding XXXX, under each part's
"## Part N" heading, and the figures a part promises that are not in figures/. A part counts
once it, or any later part, has run to the end; the name and date and Part 0 always count, and
Part 7 counts once Part 6 has run. A part that does not count yet is listed but never held
against you, so this is safe to run from the first day. The exit code is 0 when nothing that
counts is missing, and 1 otherwise. Presence and form only: nothing here says whether an answer
is right.
"""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent
WRITEUP = REPO / "WRITEUP.md"
FIGURES = REPO / "figures"
SENTINEL = "# delete this line when you start"

# part number -> (its script, the figures its docstring promises)
PARTS = {
    1: ("part1_independent.py", ["part1_strip.png"]),
    2: ("part2_policy.py", ["part2_strip.png"]),
    3: ("part3_influence.py", ["part3_gini.png", "part3_unpredictability.png"]),
    4: ("part4_shown.py", ["part4_quality_vs_success.png"]),
    5: ("part5_policy.py", ["part5_policies.png"]),
    6: ("part6_assumption.py", ["part6_trajectories.png"]),
}


def run(script):
    """Run one script with this Python, printing its output as it comes. Returns its exit code
    and its last line of output, which says why when a part stops."""
    print(f"\n== {script} ==", flush=True)
    start, last = time.perf_counter(), ""
    process = subprocess.Popen([sys.executable, script], cwd=REPO, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               env={**os.environ, "PYTHONUNBUFFERED": "1"})
    for line in process.stdout:
        print(line, end="", flush=True)
        last = line.strip() or last
    code = process.wait()
    print(f"-- {script}: exit code {code}, {time.perf_counter() - start:.1f} s", flush=True)
    return code, last


def blank_slots():
    """Part number -> the labels of the WRITEUP.md slots still holding XXXX. Part None is the
    lines above the first "## Part" heading. A slot is a bold label followed by XXXX, on the
    same line or alone on a line below; a label may wrap over lines."""
    slots, part, label, pending = {}, None, "", ""
    for line in WRITEUP.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"##\s+Part\s+(\d+)", line)
        if heading:
            part = int(heading.group(1))
        if not line.strip():
            pending = ""
            continue
        text = f"{pending} {line}" if pending else line
        if text.startswith("**"):
            close = text.rfind("**")
            if close == 0:   # the label goes on past this line
                pending = text
                continue
            pending = ""
            label = " ".join(text[2:close].replace("**", " ").split()).rstrip(": ")
            answer = text[close + 2:].strip()
        else:
            answer = line.strip()
        if answer == "XXXX":
            slots.setdefault(part, []).append(label)
    return slots


def main():
    self_check, _ = run("measures.py")
    finished, stopped = set(), {}   # parts that ran to the end; part -> why one did not
    for part, (script, _) in PARTS.items():
        if part == 6 and SENTINEL in (REPO / script).read_text(encoding="utf-8"):
            print(f"\n== {script} ==\nnot started: it still has the line ending "
                  f"\"{SENTINEL}\".")
            stopped[part] = "not started"
            continue
        code, last = run(script)
        if code == 0:
            finished.add(part)
        else:
            stopped[part] = f"{script} stopped: {last.rstrip('.')}"

    counted = {None, *range(max(finished, default=0) + 1)}
    if 6 in finished:
        counted.add(7)
    else:
        stopped[7] = "it counts once Part 6 has run"
    slots = blank_slots() if WRITEUP.exists() else {}
    missing = 0

    print("\n== what is missing ==")
    if self_check != 0:
        print("  measures.py's self-check failed: the measures are wrong. Tell your instructor.")
        missing += 1
    if not WRITEUP.exists():
        print("  WRITEUP.md is missing, so its slots were not checked.")
        missing += 1
    for part in [None, *range(8)]:
        name = "name and date" if part is None else f"part {part}"
        labels = slots.get(part, [])
        if part not in counted:
            count = f"{len(labels)} slot{'' if len(labels) == 1 else 's'} still XXXX"
            print(f"  {name}: does not count yet ({stopped.get(part, 'not reached')}); {count}.")
            continue
        if part in stopped:
            print(f"  {name}: {stopped[part]}.")
            missing += 1
        for figure in PARTS.get(part, ("", []))[1]:
            if not (FIGURES / figure).exists():
                print(f"  {name}: figures/{figure} is missing.")
                missing += 1
        for label in labels:
            print(f"  {name}: still XXXX: {label}")
            missing += 1
    if not missing:
        print("  nothing.")
    print(f"\n{missing} missing in the parts that count so far.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
