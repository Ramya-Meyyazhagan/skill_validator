# Setup: automatic Skill Validator on GitHub

Every pull request that adds or changes a skill gets a scorecard comment, and the check fails if a skill scores below 60 or has a critical safety issue.

## Repo layout

```
your-repo/
├── .github/workflows/validate-skills.yml   ← the automation
├── skill-validator/SKILL.md                ← the validator's rules
└── skills/
    └── <your-skill>/SKILL.md               ← skills being validated
```

## One-time setup (about 15 minutes)

1. **Create a personal GitHub repo** (your own account, not your employer's).
2. **Upload these files** keeping the folder layout above.
3. **Get an Anthropic API key:** sign in at console.anthropic.com, add a small amount of credit, create a key.
4. **Add the key to GitHub:** repo → Settings → Secrets and variables → Actions → New repository secret.
   - Name: `ANTHROPIC_API_KEY`
   - Value: your key. Never paste the key into any file.
5. **Turn on Actions:** repo → Actions tab → enable workflows if asked.

## Test it

1. Create a branch, add a test skill at `skills/test-skill/SKILL.md`, and open a pull request.
2. Within a few minutes, the "Validate Skills" check runs and posts a scorecard comment.
3. Or run it by hand: Actions → Validate Skills → Run workflow (validates every skill, no PR comment; download the report from the run's artifacts).

## Settings you can change

- **Minimum score:** `MIN_SCORE` near the top of the workflow file (start at 60, raise to 75 later).
- **Which folders count as skills:** the `paths` list and the `grep` line in "Find changed skills".

## Cost and safety

- You pay per run through your Anthropic API credit. A few skills per PR is usually small; set a monthly spend limit in the Anthropic Console.
- The validator only reads files. It is never allowed to run scripts inside the skills it checks.
- Keep this repo personal: use public skills for testing, never employer code or internal plugins.

## Maintenance mode setup (watching other project repos)

1. **List the projects** in `registry/projects.yml` (repo, branch, skills folder, minimum score).
2. **Allow pull requests from Actions:** this repo → Settings → Actions → General → Workflow permissions → tick **"Allow GitHub Actions to create and approve pull requests"** → Save.
3. **Private project repos only:** create a fine-grained GitHub token with **Contents: Read-only** on those repos, and add it here as a secret named `PROJECTS_READ_TOKEN`. Public repos need nothing.
4. **First run:** Actions → Watch Skill Projects → Run workflow. The first run validates every skill and drafts tests for any skill that has none.
5. **Review the Baseline update pull request,** fix the drafted tests if needed, and merge it. From then on, only changed skills are re-validated, and each one is compared with this baseline.

Moving to an organization later: put this repo in the org, use an org-level `ANTHROPIC_API_KEY` secret, and replace `PROJECTS_READ_TOKEN` with a GitHub App or org-scoped read-only token.
