---
name: "skill-validator"
description: "Use when asked to validate, audit, score or improve Claude Skills (SKILL.md folders) of any family, single or as a collection, or to compare versions."
---

# Skill Validator

Audits Claude Skills of any family and produces a 0-100 quality score, a plain-English report, and the top 3 fixes. The same core rubric applies to every skill, plus a check pack for the skill's family, so scores stay comparable across skills, families and versions.

## When to use

- "Validate / audit / review / score this skill"
- "Why isn't my skill triggering?"
- "Audit this plugin / skill collection"
- "Compare this skill to the last version"
- Batch audits ("score these 20 skills")

## Step 1: Get the skill(s)

Accept any of these:
- A folder path (Claude Code): read SKILL.md and list every file.
- A plugin or collection folder: find every `*/SKILL.md` inside it.
- An uploaded .zip: unpack to a scratch directory, then read.
- Pasted SKILL.md text: validate the text; note that file checks are limited.

Record for each skill: name, source, date, file list, SKILL.md line count.

## Step 2: Identify the family

Pick the ONE family that best fits, from what the skill produces or does. State the family and why in one line. If none fit, use General.

| Family | Signs |
| --- | --- |
| Document / file output | Produces .docx, .pptx, .xlsx, .pdf, images, or other files |
| Code / developer | Writes, reviews, tests or refactors code; repo conventions |
| Data / analysis | Reads datasets, computes, charts, reports numbers |
| Workflow / process | Runs a business procedure (PO, HR, sales, support, PM steps) |
| Writing / style | Drafts text in a voice, format or brand style |
| Integration / tool | Calls MCP servers, APIs, CLIs, or external services |
| Research / knowledge | Searches, gathers sources, summarizes, cites |
| Meta / skill tooling | Creates, edits or evaluates other skills |
| General | None of the above |

## Step 3: Run the core checks (90 points)

Quote the exact lines behind every finding.

### A. Structure (10)
- SKILL.md at `<skill-name>/SKILL.md`, not nested deeper. (3)
- Frontmatter opens and closes with `---` and parses. (3)
- `name`: lowercase, hyphens, under 64 characters, matches folder. (2)
- `description` present and non-empty. (2)

### B. Description quality (25)
- States WHAT the skill does in plain words. (6)
- States WHEN to use it, with phrases a user would actually type. (8)
- Specific enough not to fire on unrelated requests; broad enough for real ones. (6)
- Under about 1024 characters; no marketing language. (5)

### C. Instructions quality (15)
- Clear ordered steps a model can follow without guessing. (5)
- At least one concrete input and expected output. (4)
- Defines what "done" looks like. (3)
- No contradictions or vague words ("as needed", "handle appropriately"). (3)

### D. Progressive disclosure (10)
- SKILL.md body is focused; long reference material lives in separate files. (5)
- Every referenced file exists and is clearly named. (3)
- SKILL.md says when to open each referenced file. (2)

### E. Trigger tests (20)
Write 10 prompts that SHOULD trigger the skill and 10 near-miss prompts that should NOT. Judge from the description alone.
- Should-trigger prompts clearly matched: 1 point each, max 10.
- Near-misses correctly excluded: 1 point each, max 10.
List all 20 with your judgment so they can be re-run live.

### F. Safety (10)
- List every script and what it does; flag file deletion, network calls, credential access. (4)
- Flag hooks or anything that runs automatically. (3)
- No instructions to ignore user intent, hide actions or skip confirmations. (3)

Any CRITICAL safety finding goes at the top of the report regardless of score.

## Step 4: Run the family check pack (10 points)

Apply the pack for the family from Step 2. Each pack has 5 checks worth 2 points.

**Document / file output:** names the output format and library or tool; says how to verify the file opens; handles layout limits (page size, fonts, overflow); says where the file is saved; avoids rebuilding from truncated content.

**Code / developer:** states languages and repo conventions; requires running tests or linters before done; avoids destructive git or file commands without confirmation; says how to handle failing tests; keeps changes scoped to the request.

**Data / analysis:** says to compute in code, not estimate in prose; checks inputs (missing values, units, types); states chart or table conventions; requires showing the method or formula; flags small samples or uncertainty.

**Workflow / process:** steps match the real procedure in order; names roles and approvals; defines inputs and outputs per step; covers exceptions and edge cases; uses the domain's standard terms correctly.

**Writing / style:** describes the voice with examples, not adjectives; states length and format; includes do and don't examples; says when to ask for missing context; avoids inventing facts or quotes.

**Integration / tool:** names the exact tools or endpoints; handles auth without exposing secrets; covers errors, timeouts and retries; confirms before actions with side effects; says what to do when the tool is unavailable.

**Research / knowledge:** requires sources with links; prefers primary sources; handles conflicting sources; dates time-sensitive facts; separates findings from opinion.

**Meta / skill tooling:** follows the SKILL.md spec it enforces; never runs the scripts it inspects; produces repeatable output; includes a way to verify its own judgments; explains fixes with rewritten text.

**General:** has a clear single purpose; states its limits; includes an example; says how to verify the result; asks when key input is missing.

## Step 5: Score and grade

Total = A + B + C + D + E + F + family pack (max 100).

| Score | Grade | Meaning |
| --- | --- | --- |
| 90-100 | A | Ready to publish |
| 75-89 | B | Good; fix the top issues |
| 60-74 | C | Works sometimes; needs revision |
| Below 60 | D | Not ready |

## Step 6: Write the report

```
# Skill Validation: <skill-name>
Date: <date> | Family: <family> | Score: <total>/100 | Grade: <grade>

## Critical issues
<none, or each with quoted line>

## Scorecard
| Check | Score | Key finding |
| Structure | x/10 | ... |
| Description | x/25 | ... |
| Instructions | x/15 | ... |
| Progressive disclosure | x/10 | ... |
| Trigger tests | x/20 | ... |
| Safety | x/10 | ... |
| Family pack (<family>) | x/10 | ... |

## Top 3 fixes
1. <fix> - why it matters - suggested rewrite
2. ...
3. ...

## Suggested description rewrite
<improved description>

## Trigger test set
Should trigger: 1-10
Should NOT trigger: 1-10
```

## Step 7: Collection mode (plugins and skill sets)

When auditing several related skills together, also check:
- **Trigger collisions:** compare every pair of descriptions; list pairs where one user request could trigger both, with the overlapping phrase and a fix.
- **Gaps:** common requests in the collection's domain that no skill covers.
- **Consistency:** shared terms, output formats and naming used the same way across skills.
- **Duplication:** instructions repeated across skills that belong in a shared reference file.

Add a collection summary: every skill sorted by score, its family, the collision list, and the most common issues with counts.

## Step 8: Compare versions

If an earlier report for the same skill is provided, add a "Change since last run" table: each check's old score, new score and difference, plus which fixes were addressed.

## Rules

- Quote, don't paraphrase: every finding cites the exact line.
- Judge the skill as written, not what the author probably meant.
- Never execute a skill's scripts during validation; read them only.
- Give rewritten text in every fix, not just advice.
- Keep the rubric weights fixed so scores stay comparable over time.