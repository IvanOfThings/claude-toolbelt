# /dev-cycle

Full development cycle for a feature or bug fix.

**Usage:** `/dev-cycle <description or spec-path>`

The argument can be a plain description ("add player availability toggle") or a path to a mini-spec file from `/refine` (`docs/superpowers/specs/refined/2026-05-20-availability-toggle.md`).

---

## Step 1 — Dependency check

Invoke `check-dependencies` with scope `project`.

If dependencies are missing: show the report and ask the developer to install them before continuing.

---

## Step 2 — Context analysis

Invoke `analyze-context`.

**GATE:** Present the context summary to the developer. Wait for confirmation before continuing.

---

## Step 3 — Mockup (conditional)

**Skip this step if:** the task touches ≤ 2 files with no new UI surface.

If the task involves UI changes:

Invoke `update-mockups`.

**GATE:** Present the mockup to the developer. Wait for approval before continuing.

---

## Step 4 — Plan + security pre-check (conditional)

**Skip this step if:** the task touches ≤ 2 files with no DB migration.

Invoke `write-plan` with the task description and context.

Immediately after the plan is generated, invoke `security-review-plan` on the generated plan file path.

If `security-review-plan` finds CRITICAL issues: show them and stop. Do not proceed until the developer resolves them and you re-run security-review-plan with the corrected plan.

**GATE:** Show the plan to the developer. Wait for approval.

Run `/clear` after approval to free context before implementation begins.

---

## Step 5 — Implementation

Invoke `implement-agentic` with the approved plan file path.

If no plan was generated (fast path), invoke `implement-agentic` with the task description directly.

---

## Step 6 — Quality review

Invoke `quality-review`.

If `quality-review` returns BLOCKED: show the issues. Do not proceed until CRITICAL security issues and architecture violations are resolved.

---

## Step 7 — Documentation update

Invoke `update-docs`.

---

## Step 8 — Verification documents

Invoke `generate-verification-doc`.

Show the developer both verification document paths. The cycle is complete.
