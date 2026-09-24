"""
The check Claude Code runs before every Bash command Claude runs (.claude/settings.json, a
PreToolUse hook). It stops a "Part N done" or "Part 0 predictions" commit while a slot under that
part's heading in WRITEUP.md still reads XXXX, and names those slots. Every other command passes
untouched.

It reads WRITEUP.md with run_all.py's slot parser, so the two always agree on what a blank slot
is. The optional follow-up slots are never checked. Exit code 2 stops the command and shows
Claude the message; exit code 0 lets it run. Nothing in this file changes.
"""

import json
import re
import sys

from run_all import WRITEUP, blank_slots

GIT_COMMIT = re.compile(r"\bgit\b[^;&|\n]*\bcommit\b")
PART_COMMIT = re.compile(r"\bPart (\d+) (?:done|predictions)\b")


def committed_part(command):
    """The part a command commits as done ("Part N done", or "Part 0 predictions"), or None."""
    if not GIT_COMMIT.search(command):
        return None
    part = PART_COMMIT.search(command)
    return int(part.group(1)) if part else None


def main():
    try:
        command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    except (ValueError, AttributeError):
        return 0
    part = committed_part(command)
    if part is None or not WRITEUP.exists():
        return 0
    labels = blank_slots().get(part, [])
    if not labels:
        return 0
    print(f"Not committed: these Part {part} slots in WRITEUP.md still read XXXX:", file=sys.stderr)
    for label in labels:
        print(f"  - {label}", file=sys.stderr)
    print("Ask the student for each missing answer, write it in, read WRITEUP.md back with the "
          "Read tool, then commit again.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
