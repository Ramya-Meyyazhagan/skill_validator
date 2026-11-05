---
name: story-ready
description: Use when a Product Owner, BA or Scrum team asks to review, check or improve a user story or its acceptance criteria against INVEST and Definition of Ready before refinement or sprint planning.
---

# Story Ready

Reviews one user story and its acceptance criteria, says whether it is ready for sprint planning, flags the gaps, and suggests a rewrite.

## Steps

1. Read the story and acceptance criteria. If either is missing, ask for it before reviewing.
2. Score each INVEST letter as Pass or Gap: Independent, Negotiable, Valuable, Estimable, Small, Testable.
3. Check the acceptance criteria: each one is measurable and testable, and uses Given / When / Then where possible.
4. Check Definition of Ready: a clear user and value, known dependencies, edge cases named, no open questions hidden in the text.
5. Give a verdict: Ready or Not ready.
6. For every gap, quote the exact words that caused it.
7. Suggest a rewrite that fixes the gaps without adding scope.

## Output format

```
Verdict: Ready / Not ready
INVEST: I Pass | N Pass | V Gap | E Pass | S Gap | T Pass
Gaps:
- <gap> — "<quoted words>"
Suggested rewrite:
<story + acceptance criteria>
```

## Example

Input: "As a user, I want a better dashboard so it's easier to use."
Verdict: Not ready. Gaps: no specific user ("a user"), no measurable value ("better", "easier"), no acceptance criteria.

## Rules

- The Product Owner makes the final call; this is a second opinion.
- Never invent requirements that are not in the story.
