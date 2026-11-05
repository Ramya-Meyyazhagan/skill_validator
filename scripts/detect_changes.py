#!/usr/bin/env python3
"""Find which skills changed in each watched project since the last validated commit.

Reads registry/projects.yml and registry/state/<project>.json, clones each project
(metadata only, no file contents), and compares its current head with the last
validated commit. Writes a GitHub Actions matrix to $GITHUB_OUTPUT.

Environment:
  ONLY_PROJECT        validate just this project name (optional)
  FORCE_ALL           "true" = validate every skill, ignoring saved state
  PROJECTS_READ_TOKEN token for private repos (optional)
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"


def run(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed: {result.stderr.strip()}")
    return result


def clone_url(project):
    token = os.environ.get("PROJECTS_READ_TOKEN", "")
    if project.get("private") and not token:
        raise RuntimeError(f"{project['name']} is private but PROJECTS_READ_TOKEN is not set")
    auth = f"x-access-token:{token}@" if token else ""
    return f"https://{auth}github.com/{project['repo']}.git"


def skills_at(repo_dir, ref, skills_path):
    """Skill folder names that contain a SKILL.md at the given commit."""
    out = run(["git", "ls-tree", "-r", "--name-only", ref, "--", skills_path], cwd=repo_dir).stdout
    names = set()
    prefix = skills_path.rstrip("/") + "/"
    for line in out.splitlines():
        if line.startswith(prefix) and line.endswith("/SKILL.md"):
            rest = line[len(prefix):].split("/")
            if len(rest) == 2:  # exactly <skill>/SKILL.md, not nested deeper
                names.add(rest[0])
    return names


def changed_skills(repo_dir, base, head, skills_path):
    out = run(["git", "diff", "--name-only", base, head, "--", skills_path], cwd=repo_dir).stdout
    prefix = skills_path.rstrip("/") + "/"
    names = set()
    for line in out.splitlines():
        if line.startswith(prefix):
            parts = line[len(prefix):].split("/")
            if len(parts) >= 2:
                names.add(parts[0])
    return names


def main():
    config = yaml.safe_load((ROOT / "registry" / "projects.yml").read_text()) or {}
    only = os.environ.get("ONLY_PROJECT", "").strip()
    force = os.environ.get("FORCE_ALL", "false").lower() == "true"
    WORK.mkdir(exist_ok=True)

    matrix, notes = [], []
    for project in config.get("projects", []):
        name = project["name"]
        if only and name != only:
            continue
        skills_path = project.get("skills_path", "skills").strip("/")
        repo_dir = WORK / name
        try:
            run(["git", "clone", "--quiet", "--filter=blob:none", "--no-checkout",
                 "--branch", project.get("branch", "main"), clone_url(project), str(repo_dir)])
        except RuntimeError as err:
            notes.append(f"{name}: could not read repo ({err})")
            continue
        head = run(["git", "rev-parse", "HEAD"], cwd=repo_dir).stdout.strip()

        state_file = ROOT / "registry" / "state" / f"{name}.json"
        last = None
        if state_file.exists() and not force:
            last = json.loads(state_file.read_text()).get("last_checked_sha")
            known = run(["git", "cat-file", "-e", f"{last}^{{commit}}"], cwd=repo_dir, check=False)
            if known.returncode != 0:
                notes.append(f"{name}: saved commit {last} not found, validating all skills")
                last = None

        present = skills_at(repo_dir, head, skills_path)
        if last is None:
            targets, removed = present, set()
            reason = "first run" if not force else "forced"
        elif last == head:
            notes.append(f"{name}: no new commits since {head[:7]}")
            continue
        else:
            touched = changed_skills(repo_dir, last, head, skills_path)
            targets = touched & present
            removed = touched - present
            reason = f"changes since {last[:7]}"

        if not targets and not removed:
            notes.append(f"{name}: commits since {last[:7] if last else '-'} touched no skills")
            # still advance state so the same commits are not checked again
            matrix.append({"project": name, "sha": head, "skills": "", "removed": "",
                           "reason": "no skill changes", **_fields(project, skills_path)})
            continue

        matrix.append({
            "project": name,
            "sha": head,
            "skills": " ".join(sorted(targets)),
            "removed": " ".join(sorted(removed)),
            "reason": reason,
            **_fields(project, skills_path),
        })
        notes.append(f"{name}: validate [{', '.join(sorted(targets)) or 'none'}]"
                     f"{' removed [' + ', '.join(sorted(removed)) + ']' if removed else ''} ({reason})")

    for note in notes:
        print(note)

    output = os.environ.get("GITHUB_OUTPUT")
    payload = json.dumps({"include": matrix})
    if output:
        with open(output, "a") as fh:
            fh.write(f"matrix={payload}\n")
            fh.write(f"has_work={'true' if matrix else 'false'}\n")
    else:
        print(payload)


def _fields(project, skills_path):
    return {
        "repo": project["repo"],
        "branch": project.get("branch", "main"),
        "skills_path": skills_path,
        "min_score": int(project.get("min_score", 60)),
        "owner": project.get("owner", ""),
        "private": bool(project.get("private", False)),
    }


if __name__ == "__main__":
    try:
        main()
    except Exception as err:  # make failures readable in the Actions log
        print(f"detect_changes failed: {err}", file=sys.stderr)
        sys.exit(1)
