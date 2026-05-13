# Dev Workflow Plugin — Design Spec

**Date:** 2026-05-13  
**Status:** Approved

---

## Overview

Create an installable Claude Code plugin in `claude-toolbelt` that packages a reusable development workflow framework. The plugin provides slash commands, focused skills, and canonical rules extracted from the `team-manager` project so they can be applied consistently across any new project.

The framework has three pillars:
1. **Commands** — thin orchestrators (slash commands)
2. **Skills** — focused, reusable units of work
3. **Rules** — canonical reference documents, single source of truth for standards

---

## Plugin Structure

```
claude-toolbelt/
├── CLAUDE.md
└── plugin/
    ├── package.json              ← name: "dev-workflow", version, type: "module"
    ├── README.md
    ├── dependencies.md          ← framework dependency manifest
    │
    ├── commands/
    │   ├── init-project.md
    │   ├── dev-cycle.md
    │   ├── refine.md
    │   ├── generate-verification.md
    │   ├── verify-pr.md
    │   ├── security-review.md
    │   └── ui-contrast.md
    │
    ├── skills/
    │   ├── check-dependencies/SKILL.md
    │   ├── analyze-context/SKILL.md
    │   ├── update-mockups/SKILL.md
    │   ├── write-plan/SKILL.md
    │   ├── implement-agentic/SKILL.md
    │   ├── quality-review/SKILL.md
    │   ├── update-docs/SKILL.md
    │   ├── generate-verification-doc/SKILL.md
    │   ├── security-review-plan/SKILL.md
    │   ├── security-review-code/SKILL.md
    │   ├── decompose-refinement/SKILL.md
    │   ├── diagnose-pr-failures/SKILL.md
    │   ├── apply-pr-fixes/SKILL.md
    │   ├── init-brainstorm/SKILL.md
    │   ├── init-scaffold/SKILL.md
    │   └── init-generate-specs/SKILL.md
    │
    └── rules/
        ├── process/
        │   ├── git-discipline.md
        │   ├── dev-prod-parity.md
        │   ├── tdd-cycle.md
        │   └── implementation-tracking.md
        ├── code-quality/
        │   ├── code-quality.md
        │   ├── database-patterns.md
        │   └── redis-cache-pattern.md
        ├── security/
        │   ├── security-checklist.md
        │   └── code-quality-checklist.md
        ├── ui/
        │   ├── mobile-first.md
        │   ├── skeleton-first.md
        │   └── fine-grained-reactivity.md
        ├── observability/
        │   ├── error-observability.md
        │   ├── background-tasks.md
        │   └── honeycomb-investigation.md
        ├── workflow/
        │   ├── project-structure.md
        │   ├── verification-doc-format.md
        │   └── ui-first-testing.md
        └── templates/
            ├── architecture-layers.md   ← filled per project by init-project
            └── ui-design-tokens.md      ← filled per project by init-project
```

---

## Commands (Orchestrators)

Each command is a thin markdown file that invokes skills in sequence with gates between phases. Commands do not contain workflow logic — they delegate entirely to skills.

### `/init-project <doc-path>`

Bootstraps a new project from a documentation file describing features and goals.

```
1. check-dependencies(framework)
2. init-brainstorm          ← brainstorming session → high-level design approval
3. init-scaffold            ← creates directory structure + CLAUDE.md + IMPLEMENTATION.md
4. write-plan               ← generates docs/plan.md (high-level design)
5. init-generate-specs      ← generates ordered refinement specs + queue.json
```

**Output**: a fully scaffolded project with CLAUDE.md index, standardized docs structure, `.claude/rules/` populated from templates, and a queue of refinement specs ready for `/refine`.

**Gate after step 2**: developer approves the high-level design before scaffolding begins.

---

### `/dev-cycle <description|spec-path>`

Full development cycle for a feature or bug fix.

```
1. check-dependencies(project)
2. analyze-context          ← reads docs/README.md, features.md, IMPLEMENTATION.md, mockups
   GATE: developer confirms analysis summary
3. [update-mockups]         ← optional, only if UI change needed
   GATE: developer approves mockup
4. write-plan               ← generates docs/superpowers/plans/YYYY-MM-DD-<name>.md
   + security-review-plan   ← HIGH issues block the gate
   GATE: developer approves plan → /clear
5. implement-agentic        ← subagent-driven implementation with per-task review
6. quality-review           ← architecture + Sentry + React BP + security-review-code
7. update-docs              ← updates docs/features.md, docs/README.md, plan file
8. generate-verification-doc← generates funcional + técnico/API verification docs
```

**Fast path**: tasks touching ≤2 files with no new UI or DB migration skip steps 3 and 4.

---

### `/refine <doc-path>`

Decomposes a change document into ordered work items and executes them.

```
Phase 1: analyze-context + read input doc
Phase 2: decompose-refinement → discrete items in dependency order
Phase 3: interactive clarification (one question at a time, max 2 per item)
Phase 4: generate mini-specs → docs/superpowers/specs/refined/ + queue.json
         GATE: developer approves queue
Phase 5: for each pending item → /dev-cycle <spec-path>
```

---

### `/generate-verification [spec-path]`

Generates verification documents for the current branch.

```
1. analyze-context (git diff, commits, optionally a spec file)
2. generate-verification-doc
```

---

### `/verify-pr [doc-path] [test-ids...]`

Diagnoses and fixes failures in verification documents.

```
1. diagnose-pr-failures   ← reads doc, extracts FALLO/PARCIAL, diagnoses root causes
   GATE: developer confirms diagnosis
2. apply-pr-fixes         ← TDD fix per failure, updates verification doc
3. [archive if all ✅ OK]
```

---

### `/security-review <plan|code> [path]`

```
plan <path>  →  security-review-plan
code         →  security-review-code (against git diff main)
```

---

### `/ui-contrast`

Reads the project's `.claude/rules/ui.md` (which contains the project's design tokens) and runs a WCAG AA contrast audit against changed UI files.

---

## Skills

### `check-dependencies`

**Input**: scope — `framework` | `project` | `all`  
**Reads**: `plugin/dependencies.md` (framework deps), project `CLAUDE.md` `## Dependencies` section  
**Checks**:
- Plugins: reads `~/.claude/plugins/installed_plugins.json` and checks each required plugin key exists
- MCPs: reads the system-reminder deferred tools list; an MCP is considered missing if none of its expected tool names appear in that list

**Output**: pass (silent) or a structured report with exact install commands for every missing item.

```
⚠️  Missing dependencies detected:

  PLUGIN  frontend-design   not installed
  → claude plugin install frontend-design

  MCP     honeycomb         not configured
  → claude mcp add honeycomb
  → Set HONEYCOMB_API_KEY in your environment
```

---

### `analyze-context`

Reads the project state before any implementation work:
- `CLAUDE.md` → discovers project paths and stack
- `docs/README.md` → feature inventory and documentation index
- `docs/features.md` → current feature behavior
- `IMPLEMENTATION.md` → sprint state
- Relevant mockups in `docs/mockups/`

Outputs a 2–4 sentence summary: what exists, what needs to change, constraints.

---

### `update-mockups`

Invokes `frontend-design` skill to create or update HTML mockups in `docs/mockups/`. Enforces mobile-first: reads `rules/ui/mobile-first.md`, validates at 390px before desktop. Annotates interactive elements with their React Query update scope.

---

### `write-plan`

Wraps `superpowers:writing-plans` with project context from `analyze-context`. Reads `rules/process/tdd-cycle.md`. Every plan task must follow the TDD structure. Saves to `docs/superpowers/plans/YYYY-MM-DD-<name>.md`.

---

### `implement-agentic`

Wraps `superpowers:subagent-driven-development`. Per task: implementer subagent → spec compliance review → code quality review. Reads `rules/security/code-quality-checklist.md` as the review checklist. Instructs `/compact` after every 2–3 tasks if plan has 4+ tasks.

---

### `quality-review`

Runs all post-implementation quality gates:
1. Architecture compliance scripts (`npm run check:architecture` or equivalent from CLAUDE.md)
2. Sentry instrumentation review (reads `rules/observability/error-observability.md`)
3. `vercel:react-best-practices` on changed TSX files
4. `security-review-code`

---

### `update-docs`

Updates `docs/features.md` with behavior changes. Corrects the plan file if assumptions were wrong. Verifies `docs/README.md` links are consistent.

---

### `generate-verification-doc`

Reads `rules/workflow/verification-doc-format.md` and `rules/workflow/ui-first-testing.md`. Produces two files:
- `docs/superpowers/verification/YYYY-MM-DD-<slug>.md` — functional (UI-first)
- `docs/superpowers/verification/YYYY-MM-DD-<slug>-api.md` — technical (API/DB/permissions)

---

### `security-review-plan` / `security-review-code`

Both read `rules/security/security-checklist.md`. Plan mode reviews a plan file; code mode reviews `git diff main`. Output: PASS or structured issue list with severity (CRITICAL/MEDIUM/LOW) and exact fix suggestions.

---

### `decompose-refinement`

Reads input document + project context. Decomposes into discrete items (one `/dev-cycle` per item), checks for already-done items in IMPLEMENTATION.md, flags oversized items, generates mini-spec files and `queue.json`.

---

### `diagnose-pr-failures`

Reads verification document, extracts FALLO and PARCIAL tests, reads relevant source files, produces structured diagnosis (what tester sees / root cause / affected files / proposed fix) before touching any code.

---

### `apply-pr-fixes`

TDD fix per failing test: write failing test → implement fix → green → commit. Updates verification doc with `🔧 CORREGIDO — pendiente re-test` status. Archives doc to `verified/` when all tests are ✅ OK.

---

### `init-brainstorm`

Invokes `superpowers:brainstorming` with the input documentation file as context. Explores: project goals, target users, key features, tech stack preferences, architecture style, design system direction. Produces high-level design approval before any file creation.

---

### `init-scaffold`

Creates the standardized project structure after brainstorm approval:

```
CLAUDE.md                    ← thin index (<100 lines)
IMPLEMENTATION.md            ← empty tracker with column headers
.claude/
  rules/
    coding.md                ← from brainstorm: TS config, linting, naming
    architecture.md          ← from template: layers filled for this stack
    testing.md               ← from brainstorm: test strategy, mock approach
    ui.md                    ← from template: design tokens, mobile-first
    observability.md         ← from brainstorm: error tracking, tracing setup
docs/
  README.md                  ← documentation index
  plan.md                    ← high-level design (from brainstorm)
  features.md                ← initial feature list
  arch.md                    ← architecture diagram (text/ASCII)
  db.md                      ← data model
  api.md                     ← API surface (empty, filled during development)
  mockups/                   ← empty, populated during dev-cycle
  superpowers/
    plans/
    specs/refined/
    verification/
```

Generates `CLAUDE.md` using the canonical template (index format, <100 lines, references thematic files).

---

### `init-generate-specs`

Takes the approved high-level design (features list from brainstorm) and generates:
- One mini-spec file per feature in `docs/superpowers/specs/refined/`
- Features ordered by implementation dependency (foundational features first)
- `queue.json` ready for `/refine`

Each spec includes: type, summary, acceptance criteria, affected areas, dependencies, constraints (mobile-first, design tokens, TDD).

---

## Rules Catalogue

### `rules/process/`

| File | Content extracted from |
|------|----------------------|
| `git-discipline.md` | CLAUDE.md "REGLA CRÍTICA — Commits y pushes" |
| `dev-prod-parity.md` | CLAUDE.md "Paridad dev/producción" |
| `tdd-cycle.md` | dev-cycle Step 5, verify-pr Step 3 |
| `implementation-tracking.md` | CLAUDE.md "Implementation Process" — 4-column tracker, gate rule |

### `rules/code-quality/`

| File | Content extracted from |
|------|----------------------|
| `code-quality.md` | CLAUDE.md "Code quality rules" (DRY, search-before-implementing, lean files, service-first principle) |
| `database-patterns.md` | CLAUDE.md "Database access principles" (singleton, parallel queries, server-side only) |
| `redis-cache-pattern.md` | CLAUDE.md "Redis read-through cache pattern" (9-step pattern: typed payload, validator, builder, versioned key, fallback) |

### `rules/security/`

| File | Content extracted from |
|------|----------------------|
| `security-checklist.md` | security-review.md (auth/authZ, data exposure, input handling, business logic, external integrations) |
| `code-quality-checklist.md` | dev-cycle.md Step 4 checklist (mobile, design tokens, Sentry, architecture R1-R6) |

### `rules/ui/`

| File | Content extracted from |
|------|----------------------|
| `mobile-first.md` | CLAUDE.md "Mobile-first" section |
| `skeleton-first.md` | CLAUDE.md "Skeleton-first, lazy loading" section |
| `fine-grained-reactivity.md` | CLAUDE.md "Fine-grained reactivity" section |

### `rules/observability/`

| File | Content extracted from |
|------|----------------------|
| `error-observability.md` | CLAUDE.md "Sentry instrumentation" (generalized: any error tracker) |
| `background-tasks.md` | CLAUDE.md "Background work in route handlers — waitUntil" |
| `honeycomb-investigation.md` | CLAUDE.md "Honeycomb MCP usage" |

### `rules/workflow/`

| File | Content extracted from |
|------|----------------------|
| `project-structure.md` | Canonical directory layout contract for this framework |
| `verification-doc-format.md` | generate-verification.md — exact two-doc format, numbering, partition rules |
| `ui-first-testing.md` | generate-verification.md — UI-first testing rules |

### `rules/templates/`

| File | Purpose |
|------|---------|
| `architecture-layers.md` | N-layer architecture template: layer names, paths, rules (R1..RN). Filled by `init-scaffold` during `init-project`. |
| `ui-design-tokens.md` | Design token reference template: color palette, light/dark values, contrast ratios. Filled by `init-scaffold` during `init-project`. |

---

## Dependency Manifest (`plugin/dependencies.md`)

```markdown
# Framework Dependencies

## Required Plugins

| Plugin | Marketplace | Used by | Install |
|--------|-------------|---------|---------|
| superpowers | claude-plugins-official | write-plan, implement-agentic, init-brainstorm | `claude plugin install superpowers` |
| frontend-design | claude-plugins-official | update-mockups | `claude plugin install frontend-design` |
| vercel | claude-plugins-official | quality-review | `claude plugin install vercel` |
| honeycomb | honeycomb-plugins | honeycomb-investigation rule | `claude plugin install honeycomb --from honeycomb-plugins` |

## Required MCPs

| MCP | Used by | Setup |
|-----|---------|-------|
| Honeycomb MCP | honeycomb-investigation rule | `claude mcp add honeycomb` + env var `HONEYCOMB_API_KEY` |

## Optional Plugins

| Plugin | Used by | Install |
|--------|---------|---------|
| code-review | dev-cycle requesting-code-review | `claude plugin install code-review` |
```

---

## Canonical CLAUDE.md template

Generated by `init-scaffold` for every new project. Always under 100 lines.

```markdown
# [Project Name]

[One sentence: what it does and for whom.]

## Stack
- [line per technology — filled during init-brainstorm]
- Architecture: [.claude/rules/architecture.md]

## Rules
- Code: [.claude/rules/coding.md]
- Tests: [.claude/rules/testing.md]
- UI: [.claude/rules/ui.md]
- Observability: [.claude/rules/observability.md]
- Commits: never automatic — only when the developer explicitly asks

## Documentation
- Plan: [docs/plan.md]
- Features: [docs/features.md]
- Architecture: [docs/arch.md]
- Database: [docs/db.md]
- API: [docs/api.md]
- Mockups: [docs/mockups/]
- Implementation tracker: [IMPLEMENTATION.md]

## Dev commands
\`\`\`bash
[build, dev, test commands — filled during init-brainstorm]
\`\`\`

## Workflow
- New feature or bugfix: `/dev-cycle <description>`
- Process a change document: `/refine <path>`
- Generate verification docs: `/generate-verification`

## Dependencies
### Required plugins
- superpowers, frontend-design, vercel, honeycomb

### Required MCPs
- honeycomb: `claude mcp add honeycomb` + env var `HONEYCOMB_API_KEY`
[project-specific MCPs added during init-project]
```

---

## What stays in team-manager and does NOT move to the plugin

The following sections of team-manager's CLAUDE.md are project-specific and will remain there after the plugin is introduced:

- Telegram message format conventions
- Redis wrapper implementation details (env vars, specific TTL defaults)
- Prisma schema and existing services list
- Deployment env vars and Vercel-specific configuration
- Specific Honeycomb dataset names and environment mapping

When the plugin is installed in team-manager, its CLAUDE.md will be refactored to the thin-index format, with the above remaining as project-specific `.claude/rules/` files.

---

## Migration path for team-manager

Once the plugin is implemented:

1. Install plugin: `claude plugin install /path/to/claude-toolbelt/plugin` (uses the `dev-workflow` name from package.json)
2. Refactor `CLAUDE.md` → thin index (<100 lines) referencing thematic files
3. Extract project-specific rules to `.claude/rules/`:
   - `architecture.md` ← the 5-layer Next.js architecture
   - `coding.md` ← TypeScript, Prisma, Zod patterns
   - `ui.md` ← design tokens (currently in ui-contrast command)
   - `observability.md` ← Sentry + Honeycomb project config
4. Move `mockups/` → `docs/mockups/`
5. Move `PLAN.md` → `docs/plan.md`
6. Copy existing `.claude/commands/` files are superseded by the plugin's commands
