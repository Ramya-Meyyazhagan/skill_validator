#!/usr/bin/env python3
"""Undo any file change the validator made outside the folders it is allowed to write.

Runs right after Claude, from a trusted copy saved before Claude started, so a
skill that tries to trick Claude (prompt injection) cannot change the scripts or
workflows that run next with write access.

Allowed:
  out/**                                         run outputs (report, result)
  target/**                                      the project checkout (never committed)
  registry/tests/<PROJECT>/<skill>/triggers.yml  drafted tests, only for skills
  registry/tests/<PROJECT>/<skill>/cases.yml     validated in this run
Everything else is restored from git or deleted, and listed in out/guard.txt.

Environment: PROJECT, SKILLS (space-separated)
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
project = os.environ["PROJECT"]
skills = set(os.environ.get("SKILLS", "").split())


def git(*args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout


def allowed(path):
    parts = Path(path).parts
    if not parts:
        return False
    if parts[0] in ("out", "target"):
        return True
    return (
        len(parts) == 5
        and parts[:3] == ("registry", "tests", project)
        and parts[3] in skills
        and parts[4] in ("triggers.yml", "cases.yml")
    )


reverted = []

# Tracked files that were changed or deleted
for path in git("diff", "--name-only", "HEAD").splitlines():
    if not allowed(path):
        git("checkout", "HEAD", "--", path)
        reverted.append(f"restored {path}")

# New files (no .gitignore exclusions, so nothing can be hidden from this check)
for path in git("ls-files", "--others").splitlines():
    if not allowed(path):
        target = root / path
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
        reverted.append(f"deleted {path}")

out = root / "out"
out.mkdir(exist_ok=True)
(out / "guard.txt").write_text("\n".join(reverted) + ("\n" if reverted else ""))

if reverted:
    print("Blocked writes outside allowed folders:")
    print("\n".join(f"  {r}" for r in reverted))
else:
    print("Workspace clean: no writes outside allowed folders.")
