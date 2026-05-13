# Dev Workflow Plugin — Phase 2: Commands & Skills

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add all workflow commands (dev-cycle, security-review, verify-pr, generate-verification, ui-contrast, refine) and their 13 supporting skills to the plugin.

**Architecture:** Pure markdown content — SKILL.md files in `plugin/skills/<name>/` subdirectories plus command orchestrators in `plugin/commands/`. No runtime code. Skills are instructional documents that Claude reads when invoked; commands are thin orchestrators that sequence skill invocations with gates. Phase 1 rules are already present and referenced by skills in this phase.

**Tech Stack:** Markdown, Claude Code plugin format (commands/ + skills/ directories), git

**Specs:** `docs/superpowers/specs/2026-05-13-dev-workflow-plugin-design.md` (main), `docs/superpowers/specs/2026-05-13-dev-workflow-plugin-ui-addendum-design.md` (addendum)

---

## File Structure

```
plugin/
├── commands/
│   ├── dev-cycle.md              ← 8-step workflow orchestrator
│   ├── generate-verification.md  ← thin 2-step orchestrator
│   ├── ui-contrast.md            ← WCAG contrast audit
│   ├── security-review.md        ← routes to plan or code mode
│   ├── verify-pr.md              ← diagnose + fix verification failures
│   └── refine.md                 ← decompose doc → dev-cycles
└── skills/
    ├── check-dependencies/SKILL.md     ← plugin + MCP availability check
    ├── analyze-context/SKILL.md        ← reads project state, produces summary
    ├── update-mockups/SKILL.md         ← frontend-design wrapper, mobile-first
    ├── write-plan/SKILL.md             ← superpowers:writing-plans wrapper
    ├── implement-agentic/SKILL.md      ← superpowers:subagent-driven-development wrapper
    ├── quality-review/SKILL.md         ← 5 quality gates post-implementation
    ├── update-docs/SKILL.md            ← features.md + consistency pass
    ├── generate-verification-doc/SKILL.md ← produces functional + technical docs
    ├── security-review-plan/SKILL.md   ← pre-implementation plan review
    ├── security-review-code/SKILL.md   ← post-implementation diff review
    ├── decompose-refinement/SKILL.md   ← change doc → mini-specs + queue.json
    ├── diagnose-pr-failures/SKILL.md   ← extract FALLO/PARCIAL → diagnosis
    └── apply-pr-fixes/SKILL.md         ← TDD fix per failure, archive when done
```

---

## Task 1: Core utility skills (check-dependencies, analyze-context)

**Files:**
- Create: `plugin/skills/check-dependencies/SKILL.md`
- Create: `plugin/skills/analyze-context/SKILL.md`

- [ ] **Step 1: Create skill subdirectories**

```bash
mkdir -p plugin/skills/check-dependencies plugin/skills/analyze-context
```

- [ ] **Step 2: Write plugin/skills/check-dependencies/SKILL.md**

```markdown
# check-dependencies

Checks that all plugins and MCPs required by the framework and project are installed. Run silently at the start of any command.

## Input

`scope`: `framework` | `project` | `all` (default: `all`)

## Steps

**1. Determine what to check**

- `framework` scope: read `plugin/dependencies.md` (installed at the plugin's path)
- `project` scope: read the project's `CLAUDE.md` → `## Dependencies` section
- `all` scope: both

**2. Check plugins**

Read `~/.claude/plugins/installed_plugins.json`.

For each required plugin, check if its key exists in the JSON object. If the file does not exist, all plugins are considered missing.

**3. Check MCPs**

Read the `<system-reminder>` deferred tools list present in the current context window.

An MCP is **present** if at least one of its expected tool names appears in the deferred tools list.

Known MCP → expected tool name prefix:
- Honeycomb → `mcp__claude_ai_Honeycomb__` (any tool starting with this prefix)

**4. Report**

If all present: output nothing. Continue silently.

If any missing, output exactly:

```
⚠️  Missing dependencies detected:

  PLUGIN  <name>   not installed
  → <install command from dependencies.md>

  MCP     <name>   not configured
  → <setup commands from dependencies.md>
```

Do not block execution — the invoking command decides whether to gate on missing dependencies.
```

- [ ] **Step 3: Write plugin/skills/analyze-context/SKILL.md**

```markdown
# analyze-context

Reads project state before any implementation work. Produces a summary the developer confirms before proceeding.

## Steps

**1. Read CLAUDE.md**

Identify: project name, tech stack, paths to rule files, paths to documentation files. Note which files are referenced — skills use these paths, not hardcoded assumptions.

**2. Read docs/README.md**

This file lists every documentation file the project has declared, one line per file. Use this list to decide which other docs to read — do not assume a fixed set.

**3. Read docs/features.md**

Understand the current feature inventory and their documented behaviours.

**4. Read IMPLEMENTATION.md**

Identify: active sprint name, tasks in progress, completion state.

**5. Read relevant mockups (if UI task)**

If the task involves a UI change, read the mockup files in `docs/mockups/` that relate to the affected area.

**6. Output summary**

Write 2–4 sentences covering:
- What exists in the relevant area
- What this task needs to change
- Key constraints (mobile-first, DB migration needed, i18n strings needed, new tracing spans needed)

Example:
```
Context: Availability feature exists in docs/features.md with weekly slot management. Mockup at docs/mockups/availability.html shows mobile card layout. IMPLEMENTATION.md Sprint 3 active, 2 tasks pending. This task adds recurring schedules — requires a new DB column on AvailabilitySlot (migration needed) and a new UI toggle (mobile-first, i18n strings required).
```

Present the summary. Wait for the developer to confirm before the invoking command proceeds to the next step.
```

- [ ] **Step 4: Verify files**

```bash
ls plugin/skills/check-dependencies/ plugin/skills/analyze-context/
```

Expected: `SKILL.md` in each directory.

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/check-dependencies/ plugin/skills/analyze-context/
git commit -m "feat(plugin/skills): add check-dependencies and analyze-context skills"
```

---

## Task 2: Dev cycle preparation skills (update-mockups, write-plan, implement-agentic)

**Files:**
- Create: `plugin/skills/update-mockups/SKILL.md`
- Create: `plugin/skills/write-plan/SKILL.md`
- Create: `plugin/skills/implement-agentic/SKILL.md`

- [ ] **Step 1: Create skill subdirectories**

```bash
mkdir -p plugin/skills/update-mockups plugin/skills/write-plan plugin/skills/implement-agentic
```

- [ ] **Step 2: Write plugin/skills/update-mockups/SKILL.md**

```markdown
# update-mockups

Creates or updates HTML mockups for UI changes. Enforces mobile-first design using the project's design tokens.

## Prerequisites

Requires the `frontend-design` plugin. Run `check-dependencies` if unsure.

## Steps

**1. Read design context**

Read the project's `.claude/rules/ui.md` to load the design token reference (colors, typography, spacing, component library).

Read `rules/ui/mobile-first.md` from the plugin to apply the 390px-first constraint.

**2. Generate or update mockup**

Use `superpowers:frontend-design` to create or update the HTML mockup at `docs/mockups/<feature-name>.html`.

Mockup requirements:
- Default viewport: 390px width. Desktop layout only at `sm:` breakpoint and above.
- All colors and spacing come from the project's design tokens (`.claude/rules/ui.md`), never ad-hoc values.
- Interactive elements carry a `data-invalidates` attribute noting their React Query cache scope:
  `data-invalidates="['team', teamId, 'members']"`

**3. Validate mobile layout**

Describe what the mockup looks like at 390px:
- No horizontal overflow
- Touch targets ≥ 44px
- Content stacks vertically
- Text readable at default font sizes (minimum 14px body)

**4. Output**

State: file path created/updated, and one sentence describing the key mobile layout decision.

Present to developer. Wait for approval before the invoking command proceeds to implementation.
```

- [ ] **Step 3: Write plugin/skills/write-plan/SKILL.md**

```markdown
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
```

- [ ] **Step 4: Write plugin/skills/implement-agentic/SKILL.md**

```markdown
# implement-agentic

Implements a plan task-by-task using fresh subagents with spec compliance and code quality review after each task.

Wraps `superpowers:subagent-driven-development`.

## Input

Plan file path from `write-plan` output.

## Steps

**1. Read quality checklist**

Read `rules/security/code-quality-checklist.md` from the plugin. This is the checklist used by code quality review subagents.

**2. Invoke subagent-driven-development**

Use `superpowers:subagent-driven-development`.

Per task:
- Implementer subagent: receives full task text + project context
- Spec compliance review: confirms code matches plan exactly
- Code quality review: checks against `code-quality-checklist.md`

**3. Context management**

If the plan has 4 or more tasks, instruct implementer subagents to run `/compact` after every 2–3 tasks to prevent context overflow during long runs.

**4. Output**

Report: tasks completed, any spec deviations caught in review, any quality issues found and fixed.
```

- [ ] **Step 5: Verify files**

```bash
ls plugin/skills/update-mockups/ plugin/skills/write-plan/ plugin/skills/implement-agentic/
```

Expected: `SKILL.md` in each directory.

- [ ] **Step 6: Commit**

```bash
git add plugin/skills/update-mockups/ plugin/skills/write-plan/ plugin/skills/implement-agentic/
git commit -m "feat(plugin/skills): add update-mockups, write-plan, implement-agentic skills"
```

---

## Task 3: Dev cycle quality and documentation skills (quality-review, update-docs)

**Files:**
- Create: `plugin/skills/quality-review/SKILL.md`
- Create: `plugin/skills/update-docs/SKILL.md`

- [ ] **Step 1: Create skill subdirectories**

```bash
mkdir -p plugin/skills/quality-review plugin/skills/update-docs
```

- [ ] **Step 2: Write plugin/skills/quality-review/SKILL.md**

```markdown
# quality-review

Runs all post-implementation quality gates before generating verification documents.

## Gates (run in order — stop if any gate FAILS)

**Gate 1: Architecture compliance**

Run the architecture check command defined in the project's `CLAUDE.md` (e.g. `npm run check:architecture`). If no check command is defined, skip this gate.

**Gate 2: Error observability**

Read `rules/observability/error-observability.md`. Scan every `catch` block in `git diff main`:
- Does it call `errorTracker.captureException(err)` before `console.error`?
- No fire-and-forget `.catch(console.error)`?
- Non-OK external API responses create and capture an error?

Output `[error-observability] PASS` or list violations with file:line references.

**Gate 3: Tracing conventions**

Read `rules/observability/tracing-conventions.md`. Scan every new span introduced in `git diff main`:
- Name follows `"<verb> <business object>"` format (lowercase, spaces)?
- `op` is from the approved list: `cron`, `function`, or `http.client`?
- Mandatory attributes present for the span type (entity IDs, outcome counts)?
- No generic outbound HTTP span name (e.g. bare `"sendMessage"`)?

Output `[tracing] PASS` or list violations classified MEDIUM or HIGH.

**Gate 4: React best practices** (skip if no `.tsx` files changed)

Use `vercel:react-best-practices` on changed `.tsx` files.

**Gate 5: Security**

Invoke `security-review-code` skill (reads `rules/security/security-checklist.md` against `git diff main`).

## Output format

```
[quality-review] PASS — all 5 gates passed

or

[quality-review] BLOCKED

  Gate 2 — Error observability
  src/services/poll.ts:45 — catch block missing captureException before console.error

  Gate 5 — Security
  [CRITICAL] src/api/admin.ts:12 — route handler missing auth check
```

CRITICAL security issues and architecture violations block proceeding. MEDIUM and LOW issues are presented to the developer who decides whether to fix before moving on.
```

- [ ] **Step 3: Write plugin/skills/update-docs/SKILL.md**

```markdown
# update-docs

Updates project documentation after implementation to reflect what was actually built.

## Steps

**1. Read docs/README.md**

This file lists every documentation file the project has declared. Use this list to know which docs exist — do not assume a fixed set. Skip any doc not declared here.

**2. Update docs/features.md**

For each feature added, modified, or removed in this cycle: update its entry to reflect current behaviour. Add new features, remove deleted ones, correct changed descriptions.

**3. Update the plan file**

Read the plan file used for this cycle (`docs/superpowers/plans/YYYY-MM-DD-<name>.md`). If the implementation deviated from the plan (different file structure, different approach chosen), note the deviation at the top under a `## Deviations` section.

**4. Consistency pass — architecture**

Read `docs/arch.md` if declared. Did this cycle introduce or change architectural layers, patterns, or service boundaries? If yes, update the relevant section.

**5. Consistency pass — database**

Read `docs/db.md` if declared. Did a DB migration run in this cycle? If yes, update the schema description and entity relationship notes.

**6. Consistency pass — API**

Read `docs/api.md` if declared. Were new endpoints added or existing ones changed? If yes, update the route list, request/response shapes, and auth requirements.

**7. Consistency pass — mockups**

If the implementation deviated from a mockup in `docs/mockups/`, do NOT silently update the mockup. Flag the discrepancy to the developer:

```
⚠ Mockup deviation detected: docs/mockups/availability.html
  Mockup shows inline date picker; implementation uses modal.
  → Update mockup with /init-design-system or /dev-cycle before next cycle.
```

**8. Verify docs/README.md**

Confirm every file listed in `docs/README.md` still exists. Remove entries for deleted files, add entries for newly created documentation files.
```

- [ ] **Step 4: Verify files**

```bash
ls plugin/skills/quality-review/ plugin/skills/update-docs/
```

Expected: `SKILL.md` in each directory.

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/quality-review/ plugin/skills/update-docs/
git commit -m "feat(plugin/skills): add quality-review and update-docs skills"
```

---

## Task 4: Verification skill + /generate-verification + /ui-contrast commands

**Files:**
- Create: `plugin/skills/generate-verification-doc/SKILL.md`
- Create: `plugin/commands/generate-verification.md`
- Create: `plugin/commands/ui-contrast.md`

- [ ] **Step 1: Create skill subdirectory**

```bash
mkdir -p plugin/skills/generate-verification-doc
```

- [ ] **Step 2: Write plugin/skills/generate-verification-doc/SKILL.md**

```markdown
# generate-verification-doc

Generates two verification documents for the current branch: a functional (UI-first) document and a technical (API/DB/permissions) document.

## Input

`slug`: kebab-case name for the PR (e.g. `telegram-notifications-fix`, `availability-ux`).

If not provided, derive from the current branch name or the most recent commit subject.

## Steps

**1. Read standards**

Read `rules/workflow/verification-doc-format.md` — the two-document structure, block/test numbering, routing rules, archiving rule.

Read `rules/workflow/ui-first-testing.md` — write test steps as user actions, not API calls.

**2. Read implementation context**

Run `git diff main --name-only` to identify changed files.

Read the plan file for this cycle from `docs/superpowers/plans/`.

For UI changes: read the relevant mockup from `docs/mockups/`.

**3. Generate functional document**

File: `docs/superpowers/verification/YYYY-MM-DD-<slug>.md`

Include:
- Header: branch, PR (pending), test date blank, tester blank
- How-to-use section with ✅/⚠️/❌ status legend
- Prerequisites table
- Blocks covering: complete UI flows, mobile viewport check (390px), visual regression, navigation, user-visible error messages
- Each test step written as a user action (role, URL, element, observable outcome)

Add cross-reference header note: *"Complementary doc: `<slug>-api.md`. This doc covers UI end-to-end flows only and can be archived independently when all its tests are ✅ OK."*

**4. Generate technical document**

File: `docs/superpowers/verification/YYYY-MM-DD-<slug>-api.md`

Include:
- Header note pointing back to the functional doc
- Tests requiring DevTools Console (`fetch()` calls), DB inspection (Prisma Studio / DB client), or API-level permission tests (403 responses for unauthorised callers)
- Each technical test includes: `**Unit coverage:** path/to/test.ts → "test name"`

**5. Output**

State both file paths created.
```

- [ ] **Step 3: Write plugin/commands/generate-verification.md**

```markdown
# /generate-verification

Generates verification documents for the current branch.

**Usage:** `/generate-verification [spec-path]`

`spec-path` is optional. If provided, `analyze-context` also reads this file for additional context about what was built.

---

## Step 1 — Context analysis

Invoke `analyze-context`. If `spec-path` was provided, include it in the context read.

---

## Step 2 — Generate documents

Invoke `generate-verification-doc`.

Show the developer both generated document paths.
```

- [ ] **Step 4: Write plugin/commands/ui-contrast.md**

```markdown
# /ui-contrast

Runs a WCAG AA contrast audit on changed UI files using the project's resolved design tokens.

**Usage:** `/ui-contrast`

---

## Step 1 — Read design tokens

Read the project's `.claude/rules/ui.md`. This file contains the resolved design token reference (color classes, hex values, light/dark variants) generated by `init-design-system`.

If `.claude/rules/ui.md` does not exist: report it and suggest running `/init-design-system` first.

---

## Step 2 — Find changed UI files

Run `git diff main --name-only` and filter for `.tsx`, `.html`, `.css`, `.scss` files.

If no UI files changed: output `[ui-contrast] No UI files changed — nothing to audit.` and stop.

---

## Step 3 — Audit contrast

For each changed UI file, identify every text-on-background combination (Tailwind classes, CSS variables, or inline styles). Look up the hex values in `.claude/rules/ui.md`.

Apply WCAG AA minimums:
- Normal text (< 18pt / < 14pt bold): **4.5:1**
- Large text (≥ 18pt or ≥ 14pt bold): **3:1**
- UI components and graphical objects (icons, borders): **3:1**

---

## Step 4 — Output

```
[ui-contrast] PASS — all combinations meet WCAG AA

or

[ui-contrast] ISSUES FOUND

  src/components/poll-card.tsx:23
  text-soft (#6B7280) on bg-page (#FFFFFF) — ratio 4.6:1 ✅

  src/components/status-badge.tsx:15
  text-faint (#D1D5DB) on bg-panel (#F9FAFB) — ratio 1.8:1 ❌
  Required: 4.5:1 (normal text)
  → Use text-soft (#6B7280) or text-strong (#111827) instead
```

This command does not gate — it provides information for the developer to act on.
```

- [ ] **Step 5: Verify files**

```bash
ls plugin/skills/generate-verification-doc/
ls plugin/commands/generate-verification.md plugin/commands/ui-contrast.md
```

- [ ] **Step 6: Commit**

```bash
git add plugin/skills/generate-verification-doc/ plugin/commands/generate-verification.md plugin/commands/ui-contrast.md
git commit -m "feat(plugin): add generate-verification-doc skill and generate-verification, ui-contrast commands"
```

---

## Task 5: Security skills + /security-review command

**Files:**
- Create: `plugin/skills/security-review-plan/SKILL.md`
- Create: `plugin/skills/security-review-code/SKILL.md`
- Create: `plugin/commands/security-review.md`

- [ ] **Step 1: Create skill subdirectories**

```bash
mkdir -p plugin/skills/security-review-plan plugin/skills/security-review-code
```

- [ ] **Step 2: Write plugin/skills/security-review-plan/SKILL.md**

```markdown
# security-review-plan

Reviews an implementation plan for security issues before implementation begins.

## Input

`plan-path`: path to the plan file (e.g. `docs/superpowers/plans/2026-05-20-feature-name.md`)

## Steps

**1. Read checklist**

Read `rules/security/security-checklist.md`.

**2. Review the plan**

Read the plan file. For each task, evaluate:

**Authentication & Authorisation:**
- Does every new API route specify who can call it (role check, session check)?
- Could any proposed logic allow privilege escalation?
- Is tenant isolation maintained?

**Data Exposure:**
- Do proposed API responses return only needed fields?
- Any PII or sensitive fields in client-facing responses?

**Input Handling:**
- Is user input validated at the boundary with a schema validator?
- Any raw SQL or unparameterised queries proposed?

**Business Logic:**
- Financial or state operations protected against double-submit?
- State transitions validate current state?

**External Integrations:**
- Webhook signatures verified before processing?
- Secrets read from env vars, never hardcoded?

**3. Output**

```
[security-review-plan] PASS

or

[security-review-plan] ISSUES FOUND

  [CRITICAL] Task 3 — Add admin route
  No auth check specified for POST /api/admin/reset
  → Add session check + role === 'ADMIN' guard before any DB write

  [MEDIUM] Task 5 — User export
  Proposed response includes full user object
  → Select only id, name, email fields
```

CRITICAL issues block the plan gate — the developer must resolve them before implementation begins. MEDIUM and LOW are presented for developer decision.
```

- [ ] **Step 3: Write plugin/skills/security-review-code/SKILL.md**

```markdown
# security-review-code

Reviews code changes (git diff main) for security issues after implementation.

## Steps

**1. Read checklist**

Read `rules/security/security-checklist.md`.

**2. Get the diff**

Run `git diff main` to get all code changes since branching from main.

**3. Review the diff**

Apply every checklist item to the changed code:

**Authentication & Authorisation:** every new route has auth check, no privilege escalation through proposed logic, tenant isolation maintained.

**Data Exposure:** responses shaped to minimal fields, no PII, list endpoints have pagination or limits.

**Input Handling:** user inputs validated with schema validator (Zod, Joi, etc.), no raw SQL.

**Business Logic:** financial operations protected against double-submit, state transitions guarded.

**External Integrations:** webhook signatures verified, no hardcoded secrets.

**Runtime:**
- No `console.log` printing sensitive data (tokens, passwords, full user objects)
- Error responses don't leak stack traces or internal details
- Rate limiting present on auth-adjacent endpoints
- Cron endpoints verify shared secret before executing

**4. Output**

```
[security-review-code] PASS

or

[security-review-code] ISSUES FOUND

  [CRITICAL] src/app/api/teams/[id]/members/route.ts:23
  Missing auth check — any authenticated user can add members to any team
  → Add: if (session.user.teamId !== params.id) return NextResponse.json({}, { status: 403 })

  [MEDIUM] src/services/team.ts:89
  Response includes full Prisma object — exposes internal fields
  → Select: { id, name, role } only
```

CRITICAL issues block merging. MEDIUM and LOW are presented to the developer.
```

- [ ] **Step 4: Write plugin/commands/security-review.md**

```markdown
# /security-review

Runs a security review on a plan (before implementation) or on code changes (after implementation).

**Usage:**
- `/security-review plan <path>` — reviews a plan file before starting implementation
- `/security-review code` — reviews `git diff main` after implementation

---

## Plan mode

`/security-review plan <path>`

Invoke `security-review-plan` with the provided plan file path.

---

## Code mode

`/security-review code`

Invoke `security-review-code` against the current `git diff main`.
```

- [ ] **Step 5: Verify files**

```bash
ls plugin/skills/security-review-plan/ plugin/skills/security-review-code/
ls plugin/commands/security-review.md
```

- [ ] **Step 6: Commit**

```bash
git add plugin/skills/security-review-plan/ plugin/skills/security-review-code/ plugin/commands/security-review.md
git commit -m "feat(plugin): add security-review-plan, security-review-code skills and security-review command"
```

---

## Task 6: PR verification skills + /verify-pr command

**Files:**
- Create: `plugin/skills/diagnose-pr-failures/SKILL.md`
- Create: `plugin/skills/apply-pr-fixes/SKILL.md`
- Create: `plugin/commands/verify-pr.md`

- [ ] **Step 1: Create skill subdirectories**

```bash
mkdir -p plugin/skills/diagnose-pr-failures plugin/skills/apply-pr-fixes
```

- [ ] **Step 2: Write plugin/skills/diagnose-pr-failures/SKILL.md**

```markdown
# diagnose-pr-failures

Reads a verification document, extracts failing tests, and produces a structured diagnosis before touching any code.

## Input

`doc-path`: path to the verification document (functional or technical).

`test-ids` (optional): specific test IDs to diagnose (e.g. `P1.2 P3.1`). If omitted, diagnoses all tests marked `❌ FAIL` or `⚠️ PARTIAL`.

## Steps

**1. Read the verification document**

Extract every test marked `❌ FAIL` or `⚠️ PARTIAL`. For each: note its ID, title, steps, and tester comments.

**2. Read relevant source files**

For each failing test, identify the source files likely responsible (routes, services, components, existing tests). Read them.

**3. Produce structured diagnosis**

For each failing test, output:

```
### P2.1 — [test title]

**What the tester sees:** [from tester comments]
**Root cause:** [your analysis of the source files]
**Affected files:** [list of files to change]
**Proposed fix:** [1-2 sentence description]
**Existing test coverage:** [path/to/test.ts → "test name" if a unit test covers this, otherwise "none"]
```

**4. Gate**

Present the full diagnosis. Do not touch any code. Wait for developer confirmation before `apply-pr-fixes` proceeds.
```

- [ ] **Step 3: Write plugin/skills/apply-pr-fixes/SKILL.md**

```markdown
# apply-pr-fixes

Applies TDD fixes for each diagnosed PR failure. Updates the verification document after each fix.

## Input

Diagnosis output from `diagnose-pr-failures` (confirmed by developer).

## Steps

For each diagnosed failing test (in dependency order — foundational fixes first):

**1. Write a failing unit test**

Write a test that reproduces the failure programmatically. Run it and confirm it fails with the expected error message.

**2. Implement the fix**

Implement the minimum code to make the test pass. Do not fix unrelated issues. Run the test and confirm it passes.

**3. Run the full test suite**

Run all tests. Confirm no regressions.

**4. Update the verification document**

Change the test's status line to:
```markdown
- [ ] 🔧 CORREGIDO — pendiente re-test
```

Add to the tester comments field:
```
> Fix: [what was changed] — [short commit hash]
```

**5. Commit**

```bash
git add <changed source files> <verification document>
git commit -m "fix: <description> (P<N>.<M>)"
```

**6. Archive if all resolved**

After all fixes in this batch are committed: check if every test in both verification documents (functional + technical) is either `[x] ✅ OK` or `🔧 CORREGIDO — pendiente re-test`.

If all are resolved: move both documents to `docs/superpowers/verification/verified/` and report the archive.
```

- [ ] **Step 4: Write plugin/commands/verify-pr.md**

```markdown
# /verify-pr

Diagnoses and fixes failures in a verification document.

**Usage:** `/verify-pr [doc-path] [test-ids...]`

- `doc-path`: path to the verification document containing failing tests. If omitted, uses the most recent document in `docs/superpowers/verification/`.
- `test-ids`: optional list of specific test IDs to address (e.g. `P1.2 P3.1`). If omitted, addresses all `❌ FAIL` and `⚠️ PARTIAL` tests.

---

## Step 1 — Diagnose

Invoke `diagnose-pr-failures` with `doc-path` and `test-ids`.

**GATE:** Present the full diagnosis to the developer. Wait for confirmation before applying fixes.

---

## Step 2 — Fix

Invoke `apply-pr-fixes` with the confirmed diagnosis.

---

## Step 3 — Archive (if complete)

After `apply-pr-fixes` completes: if both verification documents have all tests resolved, move them to `docs/superpowers/verification/verified/`.

Report the archive path to the developer.
```

- [ ] **Step 5: Verify files**

```bash
ls plugin/skills/diagnose-pr-failures/ plugin/skills/apply-pr-fixes/
ls plugin/commands/verify-pr.md
```

- [ ] **Step 6: Commit**

```bash
git add plugin/skills/diagnose-pr-failures/ plugin/skills/apply-pr-fixes/ plugin/commands/verify-pr.md
git commit -m "feat(plugin): add diagnose-pr-failures, apply-pr-fixes skills and verify-pr command"
```

---

## Task 7: Refinement skill + /refine command

**Files:**
- Create: `plugin/skills/decompose-refinement/SKILL.md`
- Create: `plugin/commands/refine.md`

- [ ] **Step 1: Create skill subdirectory**

```bash
mkdir -p plugin/skills/decompose-refinement
```

- [ ] **Step 2: Write plugin/skills/decompose-refinement/SKILL.md**

```markdown
# decompose-refinement

Reads a change document and decomposes it into discrete, ordered work items ready for `/dev-cycle`.

## Input

`doc-path`: path to the input document describing desired changes or features.

## Steps

**1. Read project context**

The invoking command has already run `analyze-context`. Use that output as project context.

**2. Read the input document**

Read every requirement, feature request, or change described in the document.

**3. Identify discrete items**

Decompose into items where each item:
- Can be completed in a single `/dev-cycle` (roughly ≤ 1 day of implementation work)
- Has a clear, testable acceptance criterion
- Touches one cohesive area of the codebase

Flag items that are oversized:
```
⚠ Item 3 is oversized: "Rewrite the entire notifications system"
  → Suggested split: (a) notification data model, (b) delivery service, (c) notification UI
```

**4. Check IMPLEMENTATION.md**

Read `IMPLEMENTATION.md`. Mark any items already implemented as `[DONE — skip]` in the decomposition.

**5. Order by dependency**

Sort items so foundational items (data model, service layer) come before items that depend on them (API routes, UI components).

**6. Ask clarifying questions**

For each item where the implementation approach is ambiguous: ask one clarifying question. Maximum 2 questions per item total. Ask them one at a time before writing specs.

**7. Generate mini-specs**

For each item, create `docs/superpowers/specs/refined/YYYY-MM-DD-<item-slug>.md` containing:

```markdown
# <Item title>

**Type:** feature | bugfix | refactor | migration
**Summary:** [1-2 sentences]

## Acceptance criteria
- [testable outcome]
- [testable outcome]

## Affected areas
- [files, services, routes, components]

## Dependencies
- [other item slugs that must be done first, or "none"]

## Constraints
- [ ] Mobile-first required
- [ ] i18n strings required
- [ ] DB migration needed
- [ ] New tracing spans needed
```

**8. Generate queue.json**

Create `docs/superpowers/specs/refined/queue.json`:
```json
{
  "pending": ["<slug-1>", "<slug-2>", "<slug-3>"],
  "done": []
}
```

Present the queue to the developer for approval before `/refine` begins execution.
```

- [ ] **Step 3: Write plugin/commands/refine.md**

```markdown
# /refine

Decomposes a change document into ordered work items and executes them as `/dev-cycle` runs.

**Usage:** `/refine <doc-path>`

`doc-path`: path to a document describing desired changes, a feature list, or a product brief.

---

## Phase 1 — Context + document read

Invoke `analyze-context`.

Read the input document at `doc-path`.

---

## Phase 2 — Decomposition

Invoke `decompose-refinement` with the document content and project context.

---

## Phase 3 — Clarification

`decompose-refinement` asks clarifying questions inline (one at a time, max 2 per item). Answer them before proceeding to spec generation.

---

## Phase 4 — Queue

`decompose-refinement` generates mini-spec files in `docs/superpowers/specs/refined/` and `queue.json`.

**GATE:** Present the queue to the developer. Wait for approval before execution begins.

---

## Phase 5 — Execution

For each item slug in `queue.json["pending"]`:

1. Run `/dev-cycle docs/superpowers/specs/refined/<item-slug>.md`
2. On completion: move the slug from `pending` to `done` in `queue.json`
3. Continue with the next pending item

If a `/dev-cycle` returns a blocker: stop the queue, report the blocker to the developer, and wait for resolution before resuming.
```

- [ ] **Step 4: Verify files**

```bash
ls plugin/skills/decompose-refinement/
ls plugin/commands/refine.md
```

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/decompose-refinement/ plugin/commands/refine.md
git commit -m "feat(plugin): add decompose-refinement skill and refine command"
```

---

## Task 8: /dev-cycle command

**Files:**
- Create: `plugin/commands/dev-cycle.md`

- [ ] **Step 1: Write plugin/commands/dev-cycle.md**

This is the main workflow command — the most frequently invoked command in the framework.

```markdown
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
```

- [ ] **Step 2: Verify file**

```bash
ls plugin/commands/dev-cycle.md
```

- [ ] **Step 3: Commit**

```bash
git add plugin/commands/dev-cycle.md
git commit -m "feat(plugin/commands): add dev-cycle command (8-step workflow orchestrator)"
```

---

## Task 9: Verify complete Phase 2 structure

- [ ] **Step 1: Verify all skill SKILL.md files**

```bash
find plugin/skills -name "SKILL.md" | sort
```

Expected (13 files):
```
plugin/skills/analyze-context/SKILL.md
plugin/skills/apply-pr-fixes/SKILL.md
plugin/skills/check-dependencies/SKILL.md
plugin/skills/decompose-refinement/SKILL.md
plugin/skills/diagnose-pr-failures/SKILL.md
plugin/skills/generate-verification-doc/SKILL.md
plugin/skills/implement-agentic/SKILL.md
plugin/skills/quality-review/SKILL.md
plugin/skills/security-review-code/SKILL.md
plugin/skills/security-review-plan/SKILL.md
plugin/skills/update-docs/SKILL.md
plugin/skills/update-mockups/SKILL.md
plugin/skills/write-plan/SKILL.md
```

- [ ] **Step 2: Verify all command files**

```bash
find plugin/commands -name "*.md" | sort
```

Expected (6 files):
```
plugin/commands/dev-cycle.md
plugin/commands/generate-verification.md
plugin/commands/refine.md
plugin/commands/security-review.md
plugin/commands/ui-contrast.md
plugin/commands/verify-pr.md
```

- [ ] **Step 3: Verify .gitkeep files are superseded (not blocking)**

```bash
ls -la plugin/commands/ plugin/skills/
```

Expected: `.gitkeep` files still present alongside new files (they are harmless).

- [ ] **Step 4: Verify package.json name**

```bash
grep '"name"' plugin/package.json
```

Expected: `"name": "dev-workflow"`

- [ ] **Step 5: Tag phase 2**

```bash
git tag phase2-commands
git log --oneline -8
```

Verify the last 8 commits include all Phase 2 tasks (Task 1 through Task 8 commits).

---

## Self-review notes

**Spec coverage:**
- ✅ check-dependencies — reads installed_plugins.json + deferred tools list for MCPs
- ✅ analyze-context — reads CLAUDE.md → docs/README.md → features.md → IMPLEMENTATION.md → mockups
- ✅ update-mockups — frontend-design wrapper, 390px-first, data-invalidates annotation
- ✅ write-plan — superpowers:writing-plans wrapper, TDD constraint, saves to docs/superpowers/plans/
- ✅ implement-agentic — subagent-driven-development wrapper, code-quality-checklist.md, /compact guidance
- ✅ quality-review — 5 gates: architecture + error-observability + tracing + react BP + security-review-code
- ✅ update-docs — features.md + plan deviations + consistency pass (arch/db/api/mockups) + docs/README.md verify
- ✅ generate-verification-doc — two-doc format, ui-first-testing rule, cross-reference headers
- ✅ security-review-plan — pre-implementation, reads security-checklist.md, CRITICAL blocks plan gate
- ✅ security-review-code — post-implementation git diff, same checklist, CRITICAL blocks merge
- ✅ decompose-refinement — oversized detection, DONE filtering, dependency ordering, queue.json
- ✅ diagnose-pr-failures — FALLO/PARCIAL extraction, structured diagnosis, no code touched before gate
- ✅ apply-pr-fixes — TDD fix per test, CORREGIDO status, archive when all resolved
- ✅ /dev-cycle — 8-step orchestrator with fast paths, gates, /clear after plan approval
- ✅ /generate-verification — thin 2-step orchestrator
- ✅ /ui-contrast — reads .claude/rules/ui.md, WCAG AA ratios, informational (no gate)
- ✅ /security-review — routes to plan or code mode
- ✅ /verify-pr — diagnose → gate → fix → archive
- ✅ /refine — 5-phase: context → decompose → clarify → queue gate → execute dev-cycles

**Not in this plan (Phase 3):**
- init-brainstorm, init-scaffold, init-generate-specs skills
- init-design-system, update-icons, i18n-compliance skills
- /init-project, /init-design-system, /update-icons commands
