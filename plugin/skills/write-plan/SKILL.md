# write-plan

Creates a detailed TDD implementation plan for the current task. Wraps `superpowers:writing-plans` with project context.

## Steps

**1. Collect context**

From the `analyze-context` output (already done if called from `/dev-cycle`):
- Task description
- Affected files and areas
- Tech stack and test runner (from `CLAUDE.md`)

**2. Read TDD rule**

Read `rules/process/tdd-cycle.md` from the plugin. Every task in the plan must follow: write failing test → run (confirm fail) → implement → run (confirm pass) → commit.

**3. Invoke superpowers:writing-plans**

Use the `superpowers:writing-plans` skill to generate the plan.

Key constraints to enforce in every plan task:
- Task starts with a failing test
- Exact file paths for every file created or modified
- Complete code in every step — no placeholders or "TBD"
- Commit at the end of every task

**4. Save plan**

The plan saves to `docs/superpowers/plans/YYYY-MM-DD-<kebab-task-name>.md`.

**5. Output**

Return the plan file path for use by `security-review-plan` and `implement-agentic`.
