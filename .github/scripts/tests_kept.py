#!/usr/bin/env python3
"""Gate: fail if any test_* function that exists on the base branch is gone from this branch.

Guards against an agent "fixing" a failing suite by deleting tests. Usage: tests_kept.py BASE_SHA
"""
import re
import subprocess
import sys
from pathlib import Path

PATTERN = re.compile(r"^\s*def (test_\w+)", re.M)


def at_base(rev: str) -> set[str]:
    files = subprocess.run(["git", "ls-tree", "-r", "--name-only", rev, "tests/"], capture_output=True, text=True,
                           check=True).stdout.split()
    names = set()
    for f in (f for f in files if Path(f).name.startswith("test_") and f.endswith(".py")):
        text = subprocess.run(["git", "show", f"{rev}:{f}"], capture_output=True, text=True, check=True).stdout
        names |= {f"{Path(f).stem}.{m}" for m in PATTERN.findall(text)}
    return names


def now() -> set[str]:
    return {f"{p.stem}.{m}" for p in Path("tests").glob("test_*.py") for m in PATTERN.findall(p.read_text())}


if __name__ == "__main__":
    before, after = at_base(sys.argv[1]), now()
    missing = sorted(before - after)
    if missing or not before:
        print("tests_kept FAILED: " + (", ".join(missing) if missing else "no tests found at base (sensor sees nothing)"))
        sys.exit(1)
    print(f"tests_kept ok: all {len(before)} existing tests kept ({len(after)} now)")
