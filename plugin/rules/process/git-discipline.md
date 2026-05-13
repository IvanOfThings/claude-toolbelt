# Git Discipline

**Never commit or push automatically.**

Commits and pushes must only happen when the developer explicitly requests them.

## Rules

- **Commits**: only when the developer explicitly asks (`"commit"`, `"make a commit"`, `/commit`)
- **Push**: only when the developer explicitly asks (`"push"`, `"push the changes"`)
- **PRs**: never create or close PRs without explicit instruction

## Rationale

Every push may trigger a deployment and its associated cost. Intermediate commits during exploratory work create noise in the history. The developer is always the decision-maker on when to record and share state.

## No exceptions

This rule has no exceptions: not at the end of a `/dev-cycle`, not when archiving a spec, not after completing a fix, not when "it's just a small change".
