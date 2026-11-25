"""One Line, No Deadline Met — make.fun entry.

Writes one single-line joke giving an excuse for a missed deadline to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR / $OUTPUT_PATH when set).

The line is a fixed string: the program's whole job is to deliver it
exactly, and to refuse to write anything that would fail the gate
(1-200 characters, exactly one line, non-whitespace UTF-8 text).
"""

import os
import sys

LINE = (
    "I treated the deadline like a software update \u2014 "
    "I kept clicking 'remind me later' until it gave up on me."
)

MAX_CHARS = 200


def _validate(text):
    """Mirror the sealed gate: 1-200 chars, one line, non-whitespace UTF-8."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    text.encode("utf-8")  # raises if the text is not valid UTF-8
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError("entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text)))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")


def _output_path():
    # MAKEFUN_OUTPUT_DIR names a directory; OUTPUT_PATH names the file.
    # The old version probed isdir() on MAKEFUN_OUTPUT_DIR, so a directory
    # that did not exist yet was mistaken for a file path.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    path = os.environ.get("OUTPUT_PATH")
    if path:
        return path
    return "/output/entry.txt"


def main():
    _validate(LINE)
    path = _output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Round-trip check: what is on disk must be exactly the line, and must
    # still pass the gate.
    with open(path, "r", encoding="utf-8", newline="") as f:
        on_disk = f.read()
    if on_disk != LINE:
        raise ValueError("round-trip mismatch: file does not hold the entry line")
    _validate(on_disk)
    print("wrote %s" % path)
    print("line: %s" % LINE)
    print("chars: %d" % len(LINE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
