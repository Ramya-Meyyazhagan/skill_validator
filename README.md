# Skill Validator

Automatically audits Claude Skills (SKILL.md folders) and scores them 0–100, with a plain-English report and the top 3 fixes.

It works for many skill families (documents, code, data, workflows, writing, integrations, research, skill tooling), checks collections of skills for trigger collisions, and compares a skill's score across versions.

## How it works

- `skill-validator/SKILL.md`: the validator's rubric and steps
- `.github/workflows/validate-skills.yml`: runs the validator on every pull request that changes anything under `skills/`, posts the scorecard as a PR comment, and fails the check if a skill scores below 60 or has a critical safety issue
- `skills/`: put the skills you want validated here, one folder per skill

## Scorecard

| Check | Points |
| --- | --- |
| Structure | 10 |
| Description quality | 25 |
| Instructions quality | 15 |
| Progressive disclosure | 10 |
| Trigger tests (10 should / 10 should not) | 20 |
| Safety | 10 |
| Family-specific checks | 10 |

Grades: A 90–100 · B 75–89 · C 60–74 · D below 60

## Setup

See [SETUP.md](SETUP.md). In short: add an `ANTHROPIC_API_KEY` repository secret, then open a pull request that adds or changes a skill.

## Use it without GitHub

Copy `skill-validator/` into your skills folder (for example `~/.claude/skills/`) or upload it to Claude, then ask: "Validate this skill."

The SKILL.md format is an open standard, so the validator also works in other agent tools that read it.

Built by Ramya Meyyazhagan.
