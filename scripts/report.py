#!/usr/bin/env python3
"""Turn the validator's result.json into a report issue and proposed baselines.

Compares each skill with its approved baseline, flags regressions, writes
out/issue.md, and writes proposed baseline.json files into registry/tests/ so
the pipeline can open a pull request for a person to approve.

Environment: PROJECT, SHA, REPO, MIN_SCORE, REMOVED, OWNER, RUN_URL
"""
import json
import os
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
REGRESSION_DROP = 5  # a total drop of this many points or more counts as a regression


def load(path):
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def main():
    project = os.environ["PROJECT"]
    sha = os.environ["SHA"]
    repo = os.environ["REPO"]
    min_score = int(os.environ.get("MIN_SCORE", "60"))
    removed = os.environ.get("REMOVED", "").split()
    owner = os.environ.get("OWNER", "")
    run_url = os.environ.get("RUN_URL", "")

    result = load(OUT / "result.json")
    report = (OUT / "report.md").read_text() if (OUT / "report.md").exists() else ""
    commit_link = f"[`{sha[:7]}`](https://github.com/{repo}/commit/{sha})"

    if not result or not isinstance(result.get("skills"), list):
        body = (f"## Skill validation could not finish: {project}\n\n"
                f"Commit {commit_link}. The validator did not write a valid `out/result.json`.\n\n"
                f"Check the run log: {run_url}\n")
        (OUT / "issue.md").write_text(body)
        _set_output(status="error", changed_baselines="false")
        return

    rows, worst = [], "pass"
    rank = {"pass": 0, "new": 0, "fail": 2, "regression": 2, "critical": 3}
    for skill in result["skills"]:
        name = skill["skill"]
        total = int(skill.get("total", 0))
        base_path = ROOT / "registry" / "tests" / project / name / "baseline.json"
        base = load(base_path)

        if skill.get("critical"):
            status = "critical"
        elif total < min_score:
            status = "fail"
        elif base and int(base.get("total", 0)) - total >= REGRESSION_DROP:
            status = "regression"
        elif not base:
            status = "new"
        else:
            status = "pass"
        if rank[status] > rank[worst]:
            worst = status

        prev = base.get("total") if base else None
        delta = "" if prev is None else f"{total - int(prev):+d}"
        cases = skill.get("case_results", {})
        trig = skill.get("trigger_results", {})
        rows.append(
            f"| `{name}` | {skill.get('family', '?')} | **{total}** | "
            f"{prev if prev is not None else 'none'} | {delta or 'new'} | "
            f"{trig.get('should', '-')} / {trig.get('should_not', '-')} | "
            f"{cases.get('passed', 0)}/{cases.get('total', 0)} | {_badge(status)} |"
        )

        proposed = {
            "skill": name,
            "project": project,
            "commit": sha,
            "date": date.today().isoformat(),
            "total": total,
            "checks": skill.get("checks", {}),
            "family": skill.get("family", ""),
            "trigger_results": trig,
            "case_results": cases,
        }
        base_path.parent.mkdir(parents=True, exist_ok=True)
        base_path.write_text(json.dumps(proposed, indent=2) + "\n")

    collisions = result.get("collisions") or []
    lines = [
        f"## Skill validation: {project}",
        "",
        f"Commit {commit_link} · minimum score {min_score} · overall: {_badge(worst)}"
        + (f" · @{owner}" if owner and worst != "pass" else ""),
        "",
        "| Skill | Family | Score | Baseline | Change | Triggers (should / not) | Cases | Status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
        *rows,
    ]
    if removed:
        lines += ["", "**Removed skills:** " + ", ".join(f"`{r}`" for r in removed)]
    if collisions:
        lines += ["", "**Trigger collisions**", ""]
        lines += [f"- `{' / '.join(c.get('skills', []))}`: \"{c.get('phrase', '')}\". {c.get('fix', '')}"
                  for c in collisions]
    lines += [
        "",
        "New scores and any drafted tests are in the linked **baseline pull request**. "
        "Merging it approves them as the new baseline; closing it keeps the old one.",
        "",
        f"Run log: {run_url}",
        "",
        "<details><summary>Full report</summary>",
        "",
        report,
        "",
        "</details>",
    ]
    (OUT / "issue.md").write_text("\n".join(lines) + "\n")
    _set_output(status=worst, changed_baselines="true")
    print("\n".join(lines[:10 + len(rows)]))


def _badge(status):
    return {
        "pass": "✅ pass",
        "new": "🆕 new (no baseline yet)",
        "fail": "❌ below minimum",
        "regression": "⚠️ regression",
        "critical": "🚨 critical issue",
        "error": "⚠️ error",
    }[status]


def _set_output(**values):
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a") as fh:
            for key, value in values.items():
                fh.write(f"{key}={value}\n")


if __name__ == "__main__":
    main()
