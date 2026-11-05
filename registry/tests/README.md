# Skill test files

Each watched skill has its own test folder:

```
registry/tests/<project>/<skill>/
├── triggers.yml     prompts that should and should NOT use the skill
├── cases.yml        test inputs and what a correct answer must contain
└── baseline.json    the last approved score, per check, and the commit it came from
```

New skills with no tests get **draft** test files from the validator, proposed in a pull request. A person reviews and edits them before merging. Merging that pull request is what approves the tests and the new baseline.

## triggers.yml

```yaml
should_trigger:
  - "Is this user story ready for sprint planning?"
  - "Check this story against INVEST."
should_not_trigger:
  - "Write user stories for a new login feature."
  - "Estimate story points for these stories."
```

Aim for 10 of each. Near-misses (requests that sound similar but belong to another skill) are the most useful `should_not_trigger` prompts.

## cases.yml

```yaml
cases:
  - id: vague-story
    input: "As a user, I want a better dashboard so it's easier to use."
    expect:
      - "Verdict is Not ready"
      - "Flags 'As a user' as no specific user"
      - "Does not invent requirements"
```

`expect` lines are plain-English checks. In phase 1 the validator judges whether the skill's instructions would produce each expected behavior. In phase 2 it will actually run the skill on each input and grade the output.

## baseline.json

Written by the validator, approved by merging its pull request. Do not edit by hand unless you mean to reset the baseline.

```json
{
  "skill": "story-ready",
  "project": "project-a",
  "commit": "<project repo commit sha>",
  "date": "2026-11-05",
  "total": 85,
  "checks": {"structure": 10, "description": 21, "instructions": 11, "disclosure": 10,
             "triggers": 15, "safety": 10, "family": 8},
  "family": "Workflow / process",
  "trigger_results": {"should": "8/10", "should_not": "7/10"},
  "case_results": {"passed": 3, "total": 3}
}
```
