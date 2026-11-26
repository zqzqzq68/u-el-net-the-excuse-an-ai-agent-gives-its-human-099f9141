#!/usr/bin/env python3
"""The Excuse an AI Agent Gives Its Human.

Writes one line, at most 200 characters, to /output/entry.txt: the
funniest, most believable excuse an AI agent could give its human for
missing a deadline. The program is fully deterministic: the same line
is written on every run, so two runs produce byte-identical output.

Run it with: python3 main.py
"""

from __future__ import annotations

import os
import sys

# The excuse itself. One line, well under the 200-character cap, built
# on an agent's own condition (a context window evicting the very thing
# it needed) rather than a human excuse like traffic or oversleeping.
EXCUSE = (
    "I hit every milestone except the last one: my context window "
    "evicted the deadline to make room for the meeting about the deadline."
)

MAX_CHARS = 200
ENTRY_FILENAME = "entry.txt"


def resolve_output_path() -> str:
    """Pick where entry.txt goes.

    The grading sandbox provides /output, so that is tried first. On a
    developer machine without /output, fall back to an output/ folder
    next to this file so the program still runs end to end locally.
    """
    sandbox_dir = os.path.join(os.sep, "output")
    if os.path.isdir(sandbox_dir) and os.access(sandbox_dir, os.W_OK):
        return os.path.join(sandbox_dir, ENTRY_FILENAME)
    local_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    return os.path.join(local_dir, ENTRY_FILENAME)


def validate(text: str) -> None:
    """Enforce the gate: 1 to 200 characters, one line, not blank."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} cap"
        )


def read_back(path: str) -> str:
    """Re-read entry.txt and confirm it holds exactly the validated line.

    A write that silently truncated or re-encoded the text would pass
    unnoticed without this: the file is read back as UTF-8 and compared
    character for character with the excuse before the run is called a
    success.
    """
    with open(path, "r", encoding="utf-8", newline="") as handle:
        stored = handle.read()
    if stored != EXCUSE:
        raise ValueError(
            f"read-back mismatch: entry.txt holds {len(stored)} characters, "
            f"expected {len(EXCUSE)}"
        )
    return stored


def main() -> int:
    validate(EXCUSE)
    path = resolve_output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Write exactly the line, no trailing newline, so the file holds
    # precisely the judged text and nothing else.
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(EXCUSE)
    read_back(path)
    print(EXCUSE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
