You are running the Skill Validator in maintenance mode for project "{{PROJECT}}".

Read `skill-validator/SKILL.md` and follow its rubric exactly. Keep its weights fixed.

## Inputs

- Project repo checked out (read-only) at: `target/` (commit {{SHA}})
- Skills folder in that repo: `target/{{SKILLS_PATH}}/`
- Skills to validate now: {{SKILLS}}
- Skills removed in this change (do not validate, just list them): {{REMOVED}}
- Stored tests for each skill: `registry/tests/{{PROJECT}}/<skill>/`
  - `triggers.yml`: should_trigger and should_not_trigger prompts
  - `cases.yml`: test inputs with plain-English `expect` checks
  - `baseline.json`: last approved result (may be missing for new skills)
- Minimum passing score: {{MIN_SCORE}}

## What to do for each skill in "Skills to validate now"

1. Run the full rubric on `target/{{SKILLS_PATH}}/<skill>/`.
2. Trigger tests: if `triggers.yml` exists, use ITS prompts instead of inventing new ones, so results stay comparable over time. Judge each prompt from the description alone.
3. Cases: if `cases.yml` exists, for each case judge whether following the skill's instructions on that input would meet every `expect` line. A case passes only if all its expect lines would be met. Quote the instruction that makes it pass or fail.
4. If `triggers.yml` or `cases.yml` is missing, write a DRAFT of the missing file into `registry/tests/{{PROJECT}}/<skill>/` (10 + 10 trigger prompts; 3 to 5 cases including one edge case). Put `# DRAFT - review before merging` on the first line. Then use the draft for this run.
5. If `baseline.json` exists, compare against it and say what got better or worse and why.

If more than one skill exists in `target/{{SKILLS_PATH}}/`, also run Collection mode across ALL skills in that folder (read them, but only score the ones listed above) and report trigger collisions.

## Rules

- Read files only. Never run, import or execute anything inside `target/`.
- Never modify anything inside `target/`.
- Do not write or edit any `baseline.json`. The pipeline writes baselines from your result file.
- Only write the files listed in Outputs and draft test files described above.

## Outputs (all required)

1. `out/report.md`: the human report. Start with a one-line summary, then for each skill: the scorecard table, critical issues, test results (triggers and cases), change vs baseline, and the top 3 fixes with rewritten text. End with the collection findings if any.

2. `out/result.json`: exactly this shape, one entry per validated skill:

```json
{
  "project": "{{PROJECT}}",
  "commit": "{{SHA}}",
  "skills": [
    {
      "skill": "<name>",
      "family": "<family>",
      "total": 0,
      "checks": {"structure": 0, "description": 0, "instructions": 0, "disclosure": 0,
                 "triggers": 0, "safety": 0, "family": 0},
      "critical": false,
      "critical_issues": [],
      "trigger_results": {"should": "x/10", "should_not": "x/10"},
      "case_results": {"passed": 0, "total": 0, "failed_ids": []},
      "tests_drafted": false,
      "top_fix": "<one line>"
    }
  ],
  "collisions": [{"skills": ["a", "b"], "phrase": "<overlapping words>", "fix": "<one line>"}]
}
```

Write valid JSON only in `out/result.json`, with no comments.
