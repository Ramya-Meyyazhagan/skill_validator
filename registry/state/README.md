# Watcher state

One file per project, `<project>.json`, written automatically by the watcher:

```json
{"project": "project-a", "last_checked_sha": "<sha>", "last_checked_at": "2026-11-05T14:00:00Z"}
```

`last_checked_sha` is the newest project commit the watcher has already validated. The next run compares the project's current head against it and validates only skills whose files changed in between.

Delete a project's file to force a full re-validation of every skill in it.
