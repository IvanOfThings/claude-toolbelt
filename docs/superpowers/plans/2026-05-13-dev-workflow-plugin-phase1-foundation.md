# Dev Workflow Plugin — Phase 1: Foundation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the installable `plugin/` directory in `claude-toolbelt` with package metadata, dependency manifest, and all 20 canonical rule files that skills will reference.

**Architecture:** Pure markdown content. No runtime code. The plugin follows Claude Code's plugin format (commands/ and skills/ directories, package.json). All rules are self-contained reference documents read by skills at invocation time. Content is generalized from team-manager's CLAUDE.md and slash commands.

**Tech Stack:** Markdown, Claude Code plugin format, git

**Specs:** `docs/superpowers/specs/2026-05-13-dev-workflow-plugin-design.md` (main), `docs/superpowers/specs/2026-05-13-dev-workflow-plugin-ui-addendum-design.md` (addendum)

---

## File Structure

```
plugin/
├── package.json
├── README.md
├── dependencies.md
├── commands/              ← empty stubs (filled in Phase 2 & 3)
│   └── .gitkeep
├── skills/                ← empty stubs (filled in Phase 2 & 3)
│   └── .gitkeep
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
    │   ├── fine-grained-reactivity.md
    │   └── i18n.md
    ├── observability/
    │   ├── error-observability.md
    │   ├── tracing-conventions.md
    │   ├── background-tasks.md
    │   └── honeycomb-investigation.md
    ├── workflow/
    │   ├── project-structure.md
    │   ├── verification-doc-format.md
    │   └── ui-first-testing.md
    └── templates/
        ├── architecture-layers.md
        └── ui-design-tokens.md
```

---

## Task 1: Plugin scaffold (package.json, README, dependencies manifest, empty stubs)

**Files:**
- Create: `plugin/package.json`
- Create: `plugin/README.md`
- Create: `plugin/dependencies.md`
- Create: `plugin/commands/.gitkeep`
- Create: `plugin/skills/.gitkeep`

- [ ] **Step 1: Create plugin/ directory structure**

```bash
mkdir -p plugin/commands plugin/skills plugin/rules/process plugin/rules/code-quality \
  plugin/rules/security plugin/rules/ui plugin/rules/observability \
  plugin/rules/workflow plugin/rules/templates
touch plugin/commands/.gitkeep plugin/skills/.gitkeep
```

- [ ] **Step 2: Write plugin/package.json**

```json
{
  "name": "dev-workflow",
  "version": "0.1.0",
  "type": "module",
  "description": "Reusable development workflow framework for Claude Code projects"
}
```

- [ ] **Step 3: Write plugin/README.md**

```markdown
# dev-workflow

A reusable development workflow plugin for Claude Code. Provides slash commands, focused skills, and canonical rules for consistent software development across projects.

## Install

```bash
claude plugin install /path/to/claude-toolbelt/plugin
```

## What's included

- **Commands**: `/init-project`, `/dev-cycle`, `/refine`, `/generate-verification`, `/verify-pr`, `/security-review`, `/ui-contrast`, `/init-design-system`, `/update-icons`
- **Skills**: 19 focused skills covering analysis, implementation, review, scaffolding
- **Rules**: 20 canonical standards covering process, code quality, security, UI, observability, and workflow

## Dependencies

See `dependencies.md` for required plugins and MCPs.

## Phases

- **Phase 1 (this)**: Plugin structure + all rules
- **Phase 2**: Workflow commands (dev-cycle, security-review, verify-pr, generate-verification, ui-contrast)
- **Phase 3**: Project bootstrap commands (init-project, init-design-system, update-icons)
```

- [ ] **Step 4: Write plugin/dependencies.md**

```markdown
# Framework Dependencies

## Required Plugins

| Plugin | Marketplace | Used by | Install |
|--------|-------------|---------|---------|
| superpowers | claude-plugins-official | write-plan, implement-agentic, init-brainstorm | `claude plugin install superpowers` |
| frontend-design | claude-plugins-official | update-mockups | `claude plugin install frontend-design` |
| vercel | claude-plugins-official | quality-review (react-best-practices) | `claude plugin install vercel` |
| honeycomb | honeycomb-plugins | honeycomb-investigation rule | `claude plugin install honeycomb --from honeycomb-plugins` |

## Required MCPs

| MCP | Used by | Setup |
|-----|---------|-------|
| Honeycomb MCP | honeycomb-investigation rule | `claude mcp add honeycomb` + env var `HONEYCOMB_API_KEY` |

## Optional Plugins

| Plugin | Used by | Install |
|--------|---------|---------|
| code-review | requesting-code-review in dev-cycle | `claude plugin install code-review` |
```

- [ ] **Step 5: Verify structure**

```bash
find plugin/ -type f | sort
```

Expected output:
```
plugin/commands/.gitkeep
plugin/dependencies.md
plugin/package.json
plugin/README.md
plugin/skills/.gitkeep
```

- [ ] **Step 6: Commit**

```bash
git add plugin/
git commit -m "feat(plugin): add dev-workflow plugin scaffold"
```

---

## Task 2: Process rules

**Files:**
- Create: `plugin/rules/process/git-discipline.md`
- Create: `plugin/rules/process/dev-prod-parity.md`
- Create: `plugin/rules/process/tdd-cycle.md`
- Create: `plugin/rules/process/implementation-tracking.md`

- [ ] **Step 1: Write plugin/rules/process/git-discipline.md**

```markdown
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
```

- [ ] **Step 2: Write plugin/rules/process/dev-prod-parity.md**

```markdown
# Dev/Production Parity

**The code that runs locally must be identical to the code that runs in production.**

No conditional code paths based on `NODE_ENV` that use different libraries, drivers, or systems between environments. If such a branch exists, local tests don't cover production code and any bug in the production branch reaches deployment undetected.

## Rules

- **Single execution path** for database access, authentication, cache, and external services in both local and production. Environment variables change values (connection URLs, credentials), never the implementation.
- **If something doesn't work the same locally and in production, it's an architecture bug**, not an acceptable special case.
- **Tests must exercise exactly the same code that reaches production.** If production uses a different driver or adapter than local, tests provide no guarantee.
- **Forbidden**: `if (process.env.NODE_ENV === 'production') { require('other-library') }` to switch systems between environments. If different behaviour is needed, control it exclusively with environment variables that configure the same system.

## Accepted exceptions

- Configuration values: URLs, API keys, timeouts
- Log level: verbose locally, errors-only in production
- Auth mocking in local development (`MOCK_AUTH=true`)

Never the system implementation itself.
```

- [ ] **Step 3: Write plugin/rules/process/tdd-cycle.md**

```markdown
# TDD Cycle

Every code change follows this cycle without exception:

```
1. Write a failing test that describes the desired behaviour
2. Run it — confirm it fails with the expected error
3. Write the minimum code to make the test pass
4. Run the test — confirm it passes
5. Refactor if needed, keeping tests green
6. Commit
```

## Rules

- **No implementation without a failing test first.** If you can't write a test that fails before the implementation, reconsider whether the test is meaningful.
- **Minimum code principle.** Write only enough code to make the failing test pass. Do not add behaviour not covered by a test.
- **One failing test at a time.** Do not write multiple failing tests before implementing. Fix the failing test before adding the next one.
- **Never skip the red step.** Running the test before implementing confirms the test is actually testing what you think it's testing.
- **Commit at green.** Each commit represents a working state. Never commit with failing tests.

## What counts as a test

- Unit tests for pure functions and service layer logic
- Integration tests for API routes (using test database or mocks at the correct boundary)
- Component tests for UI behaviour
- E2E tests for critical user flows

The appropriate test type depends on what is being changed. Prefer the fastest test that gives real confidence.
```

- [ ] **Step 4: Write plugin/rules/process/implementation-tracking.md**

```markdown
# Implementation Tracking

Every project using this framework maintains `IMPLEMENTATION.md` at the project root as the single source of truth for implementation progress.

## Tracker format

Each task has four status columns:

| Column | Meaning |
|--------|---------|
| **Impl.** | Code written and functional (includes DB migration if applicable) |
| **Tests** | Tests written and passing |
| **Local** | Manually verified in local environment |
| **Prod** | Deployed and verified on production or preview URL |

Status values: `⬜` pending · `🔄` in progress · `✅` done · `—` not applicable

## Gate rule

**Do not start the next sprint until ALL tasks in the current sprint have ✅ in every applicable column.**

The `🎯 Current sprint` indicator always points to the active sprint. Update it when moving forward.

## Workflow per task

```
1. Set Impl. = 🔄
2. Write failing test → implement → tests green
3. Set Impl. = ✅, Tests = ✅
4. Verify locally
5. Set Local = ✅
6. Push branch → verify on preview/staging deployment
7. Set Prod = ✅
8. When all sprint tasks are ✅ on all columns → advance sprint indicator
```
```

- [ ] **Step 5: Verify files**

```bash
ls -la plugin/rules/process/
```

Expected: 4 files (git-discipline.md, dev-prod-parity.md, tdd-cycle.md, implementation-tracking.md)

- [ ] **Step 6: Commit**

```bash
git add plugin/rules/process/
git commit -m "feat(plugin/rules): add process rules (git-discipline, dev-prod-parity, tdd, tracking)"
```

---

## Task 3: Code quality rules

**Files:**
- Create: `plugin/rules/code-quality/code-quality.md`
- Create: `plugin/rules/code-quality/database-patterns.md`
- Create: `plugin/rules/code-quality/redis-cache-pattern.md`

- [ ] **Step 1: Write plugin/rules/code-quality/code-quality.md**

```markdown
# Code Quality Rules

These rules apply to all implementation work regardless of language or framework.

## DRY — Don't Repeat Yourself

Before creating a new component, hook, utility function, or helper, check if a similar one already exists. Reuse or extend it. If the same logic appears in two places, extract it into a shared unit.

## Search before implementing

Before writing formatting logic, date handling, URL construction, list rendering, or any utility, grep the relevant library files for existing helpers. If an existing helper covers 80%+ of the need, use or extend it rather than duplicating inline.

## Refactor on discovery

If during implementation you find inline logic that matches an existing helper, refactor that callsite to use the helper — even if it's not the primary task. Keep the helper as the single source of truth.

## No over-engineering

Do not add abstractions for hypothetical future needs. Build exactly what the current task requires. Three similar lines is better than a premature abstraction.

## Lean files

A file that grows beyond ~200 lines is a signal to extract components or helpers. Each file should have one clear responsibility. If you can't describe what a file does in one sentence, it does too much.

## Consistent patterns

Follow the patterns already established in the codebase. Before introducing a new pattern, verify no equivalent pattern already exists.

## Service-first data access

Every database query introduced in an HTTP handler must go through a service layer function. There is no inline-complexity threshold, no "small one-off query" exception.

Workflow when adding a handler that needs data:
1. Find the service that owns the relevant entity
2. If the service has the method, use it
3. If the service exists but lacks the method, extend it
4. Only create a new service file if no service owns the entity yet

Business logic (state validation, error codes, transactions, cache invalidation) belongs in the service. Handlers do: auth check → input parsing → service call → error mapping → response serialisation. Handlers do not re-implement business rules.
```

- [ ] **Step 2: Write plugin/rules/code-quality/database-patterns.md**

```markdown
# Database Access Patterns

## Singleton client

Use a single shared database client instance across the application. Never instantiate the client multiple times. Export one instance from a dedicated module (e.g. `src/lib/db.ts`) and import it everywhere.

Rationale: prevents connection pool exhaustion on serverless environments and ensures consistent connection lifecycle management.

## Parallel queries

When a handler or service needs multiple independent queries, run them in parallel. Never chain `await` calls that are not dependent on each other:

```ts
// ✅ Correct — parallel
const [user, team] = await Promise.all([
  db.user.findUnique({ where: { id } }),
  db.team.findMany({ where: { memberId: id } }),
]);

// ❌ Wrong — sequential, wastes time
const user = await db.user.findUnique({ where: { id } });
const team = await db.team.findMany({ where: { memberId: id } });
```

## Server-side only

All database queries run in server-side code: API handlers, server components, server actions, background jobs. Never import the database client from client-side code. Never expose raw database objects or sensitive fields to the client — shape the response to include only what the caller needs.

## Migrations before deployment

Run schema migrations manually before deploying code that depends on them. Never deploy code expecting a schema change that hasn't been applied yet.
```

- [ ] **Step 3: Write plugin/rules/code-quality/redis-cache-pattern.md**

```markdown
# Redis Read-Through Cache Pattern

Use this pattern whenever adding server-side caching. Do not deviate from it.

## The 9-step pattern

**1. Typed payload interface** — define what goes into the cache:
```ts
type FooCachePayload = { data: FooRow; relatedIds: string[] };
```

**2. Validator** — verify cache shape on read:
```ts
function parseFooCachePayload(raw: unknown): FooCachePayload {
  if (typeof raw !== "object" || raw === null) throw new Error("Not an object");
  const r = raw as Record<string, unknown>;
  if (typeof r.data !== "object" || r.data === null) throw new Error("Missing data");
  if (!Array.isArray(r.relatedIds)) throw new Error("Invalid relatedIds");
  return raw as FooCachePayload;
}
```
Never use `as FooCachePayload` directly on `JSON.parse` output.

**3. Builder** — construct the cache payload from DB results:
```ts
function buildFooCachePayload(data: FooRow, ids: Set<string>): FooCachePayload {
  return { data, relatedIds: [...ids] };
}
```

**4. Versioned cache key** — export from a central key module:
```ts
export const fooCacheKey = (id: string) => `foo:v1:${id}`;
```
Use a version prefix (`v1`, `v2`) to allow cache-bust on schema changes.

**5. Read path** — with fallback:
```ts
try {
  const cached = await cache.get(fooCacheKey(id));
  if (cached) {
    const payload = parseFooCachePayload(JSON.parse(cached));
    return payload; // cache hit
  }
} catch (err) {
  errorTracker.captureException(err);
  console.error("[foo/cache] Read failed, falling back to DB:", err);
  // fall through to DB
}
```

**6. Write path** — non-blocking:
```ts
try {
  await cache.set(fooCacheKey(id), JSON.stringify(buildFooCachePayload(data, ids)));
} catch (err) {
  errorTracker.captureException(err);
  console.error("[foo/cache] Write failed:", err);
  // never block the response on a cache write failure
}
```

**7. Invalidation** — after successful DB write:
```ts
try {
  await cache.del(fooCacheKey(id));
} catch (err) {
  errorTracker.captureException(err);
  console.error("[foo/cache] Invalidation failed:", err);
}
```

**8. Auth before cache** — always check authentication and authorisation BEFORE any cache call. A cache hit must never bypass a permission check.

**9. Graceful degradation is non-negotiable** — every cache operation is in its own try/catch. Redis being down must degrade to the database, never return a 500 to the user.
```

- [ ] **Step 4: Commit**

```bash
git add plugin/rules/code-quality/
git commit -m "feat(plugin/rules): add code quality rules (quality, database patterns, redis cache)"
```

---

## Task 4: Security rules

**Files:**
- Create: `plugin/rules/security/security-checklist.md`
- Create: `plugin/rules/security/code-quality-checklist.md`

- [ ] **Step 1: Write plugin/rules/security/security-checklist.md**

```markdown
# Security Review Checklist

Use this checklist when reviewing a plan (pre-implementation) or code (post-implementation).

## Authentication & Authorisation

- [ ] Every new API route specifies who can call it (role check, session check)
- [ ] No route skips auth middleware without explicit documented justification
- [ ] Privilege escalation is impossible through the proposed logic (e.g. a regular user cannot grant themselves admin)
- [ ] Tenant isolation: no query returns data across tenants unless the actor has explicit cross-tenant permission

## Data Exposure

- [ ] API responses return only the fields the caller needs — no full model dumps
- [ ] No PII or sensitive fields (passwords, tokens, internal IDs) exposed in client-facing responses
- [ ] Pagination or limits on list endpoints to prevent data enumeration

## Input Handling

- [ ] All user-supplied inputs are validated with a schema validator (Zod, Joi, etc.) before touching the database
- [ ] No raw SQL or unparameterised query calls
- [ ] File upload endpoints validate type and size before processing

## Business Logic

- [ ] Financial operations are protected against double-submit and replay
- [ ] State transitions validate current state before allowing the transition
- [ ] Soft-delete or archive operations cannot be triggered by unauthorised actors

## External Integrations

- [ ] Webhook endpoints verify the source signature before processing
- [ ] Secrets and tokens are read from environment variables, never hardcoded

## Runtime (code review only)

- [ ] No `console.log` printing sensitive data (tokens, passwords, full user objects)
- [ ] Error responses do not leak stack traces or internal details to the client
- [ ] Rate limiting exists on auth-adjacent endpoints
- [ ] Cron/scheduled job endpoints verify a shared secret before executing

## Severity classification

- **CRITICAL**: allows unauthorised access, data leakage, or integrity violation
- **MEDIUM**: increases attack surface or weakens a security control
- **LOW**: informational, defence-in-depth improvement

**CRITICAL issues block the PR.** MEDIUM and LOW are presented to the developer who decides.
```

- [ ] **Step 2: Write plugin/rules/security/code-quality-checklist.md**

```markdown
# Code Quality Checklist

Run this checklist on every code change before merging. Used by the `quality-review` skill.

## Architecture

- [ ] No direct database calls in HTTP handlers — all DB access goes via service layer
- [ ] No raw `fetch('/api/...')` outside the API client layer
- [ ] API request/response shapes defined in a contracts layer and shared between client and server
- [ ] Business logic in services, not in routes or components

## React / Next.js (skip if not applicable)

- [ ] No `fetch` calls directly in components — data flows through hooks
- [ ] No `'use client'` added without a concrete need (interactivity or browser API)
- [ ] `'use client'` boundary pushed as far down the component tree as possible
- [ ] Server-side async APIs awaited correctly (`await cookies()`, `await headers()`, `await params`)
- [ ] Mutations use `useMutation` + `invalidateQueries` on the narrowest applicable key
- [ ] No `window.location.reload()` or `router.refresh()` for client-triggered mutations
- [ ] Submit buttons disabled while pending to prevent double-submissions
- [ ] Optimistic updates with rollback for actions that feel instant (toggles, status changes)

## UI / Accessibility

- [ ] Mobile layout correct at 390px
- [ ] Design tokens used — no ad-hoc hex values or hardcoded spacing
- [ ] No "Loading..." / "Cargando..." text — skeleton components only
- [ ] No layout shift when data arrives — skeleton dimensions match real content

## Observability

- [ ] Every `catch` block with `console.error` also calls `errorTracker.captureException(err)` before it
- [ ] No fire-and-forget `.catch(console.error)` — must also capture the exception
- [ ] Non-OK responses from external APIs create and capture an error
- [ ] External service calls wrapped in a tracing span with correct `op` and descriptive name
- [ ] New spans include mandatory entity ID and outcome attributes (see `rules/observability/tracing-conventions.md`)

## i18n

- [ ] No hardcoded user-visible strings in source code
- [ ] Dates and numbers use `Intl` API or i18n library, not manual locale strings
- [ ] Plurals use library utilities, not inline ternaries

## Tests

- [ ] `<test runner> run` passes with no failures
- [ ] No TypeScript errors
- [ ] No regressions in existing tests
```

- [ ] **Step 3: Commit**

```bash
git add plugin/rules/security/
git commit -m "feat(plugin/rules): add security checklist and code quality checklist"
```

---

## Task 5: UI rules (mobile-first, skeleton-first, fine-grained reactivity)

**Files:**
- Create: `plugin/rules/ui/mobile-first.md`
- Create: `plugin/rules/ui/skeleton-first.md`
- Create: `plugin/rules/ui/fine-grained-reactivity.md`

- [ ] **Step 1: Write plugin/rules/ui/mobile-first.md**

```markdown
# Mobile-First UI Development

Applications are used primarily from mobile devices. Every UI change must be designed and validated mobile-first.

## Rules

- **Default viewport target**: 390px width (iPhone SE). Design at this width first.
- **Progressive enhancement**: use responsive breakpoints (`sm:`, `lg:`) only to enhance on larger screens — never to fix broken mobile layouts.
- **Touch targets**: minimum 44 × 44 px for all interactive elements.
- **No horizontal overflow**: the page must never scroll horizontally on mobile.
- **Validate before declaring done**: resize the browser to 390px and verify the layout before marking a UI task complete.

## Layout principles

Stack content vertically by default. Horizontal layouts are the exception, only introduced at larger breakpoints. Prioritise vertical space efficiency — users scroll, not pan.

## Typography

Base font size must remain readable at mobile width without pinch-to-zoom. Minimum body text: 14px (16px preferred). Never use `font-size` below 12px for any visible text.
```

- [ ] **Step 2: Write plugin/rules/ui/skeleton-first.md**

```markdown
# Skeleton-First Loading

Every screen must feel structured and complete from the very first paint. Users must never see a blank white area or a "Loading..." / "Cargando..." text string.

## The pattern: Suspense + skeleton, always

Every section that fetches data must be wrapped in a `<Suspense fallback={<XxxSkeleton />}>` boundary.

Skeleton components must:
- Match the **exact dimensions** (height, width, spacing) of the real content — no layout shift when data arrives
- Use animated placeholder shapes (e.g. `animate-pulse` divs) that mimic the shape of cards, rows, or text blocks
- Live in the same directory as the real component: `foo-card.tsx` → `foo-card-skeleton.tsx`

## Progressive top-to-bottom hydration

Decompose every page into independent sections, each with its own Suspense boundary and data fetch. Do not wait for the entire page's data before rendering anything.

```
Page
├── <HeroSection />             ← no data, renders immediately
├── <Suspense fallback={<StatsSkeleton />}>
│     <StatsSection />          ← fetches its own data independently
│   </Suspense>
└── <Suspense fallback={<ListSkeleton />}>
      <ItemList />               ← fetches its own data independently
    </Suspense>
```

## Non-negotiable rules

- **No "Loading..." text** — ever. Every loading state is a skeleton that mirrors the content shape.
- **No full-page loading gates** — do not block the entire page on a single `isLoading` flag.
- **Skeleton dimensions are fixed** — the page must not jump or reflow when data arrives.
- **One Suspense boundary per independent data source**.
- **Skeleton components are first-class** — they are tested and reviewed like any other component.
```

- [ ] **Step 3: Write plugin/rules/ui/fine-grained-reactivity.md**

```markdown
# Fine-Grained Reactivity

Every interaction must update only the minimum necessary UI — never trigger a full page reload or full navigation for a component-level action.

## Rules

- **Use your state management library's update mechanism** (e.g. React Query invalidation) after any mutation. Do not use `router.refresh()` for client-triggered data changes.
- **Optimistic updates by default** for any action the user expects to feel instant (toggles, status changes, form submissions). Implement rollback on error.
- **No `window.location.reload()`** — ever. If something seems to require a full reload, that is a design problem to fix.
- **No full-page navigation on form submit** — forms mutate via async function, update local cache, and stay on the current page unless the action explicitly requires navigating away.
- **Submit buttons disabled while pending** — every submit button and primary action button must be disabled during in-flight requests to prevent double-submissions. No exceptions.
- **Scope cache invalidations tightly** — invalidate the narrowest query key possible, not the entire cache. Prefer `['team', id, 'members']` over `['team']`.

## Optimistic update pattern

```ts
const prevState = currentData;
setData(applyOptimisticChange(currentData, ...args)); // instant UI update
const res = await submitChange(...);
if (res.ok) {
  refetchFromServer(); // rehydrate with authoritative data
} else {
  setData(prevState); // rollback on error
}
```

When a user action directly affects a displayed data section, immediately apply an optimistic local state update, fire the server request, and replace with the server response on success. Never wait for the round-trip before reflecting the user's own action.
```

- [ ] **Step 4: Commit**

```bash
git add plugin/rules/ui/mobile-first.md plugin/rules/ui/skeleton-first.md plugin/rules/ui/fine-grained-reactivity.md
git commit -m "feat(plugin/rules): add UI rules (mobile-first, skeleton-first, fine-grained reactivity)"
```

---

## Task 6: i18n rule

**Files:**
- Create: `plugin/rules/ui/i18n.md`

- [ ] **Step 1: Write plugin/rules/ui/i18n.md**

```markdown
# Internationalisation (i18n)

i18n is mandatory for all projects built with this framework. Every project supports at least the default locale defined during `init-project`, with infrastructure in place to add more.

## Rules

- **No hardcoded user-visible strings** in source code. Every text the user sees belongs in a translation file under `locales/`.
- **Dates, times, and numbers** must use `Intl.DateTimeFormat` / `Intl.NumberFormat` or the equivalent API of the project's chosen i18n library. Never string concatenation with locale assumptions.
- **Plurals and grammatical gender** use the library's plural utilities. Never inline ternaries: `n === 1 ? "item" : "items"`.
- **The default locale** is defined during `init-project` and read from config at runtime. Code never assumes a fixed locale.
- **Key naming convention**: `namespace.feature.element` — e.g. `polls.status.open`, `common.actions.save`, `errors.notFound`.
- **Namespace per feature**: each major feature area has its own translation file. Shared strings go in `common`.

## Accepted exceptions

- Log messages and error strings that only appear in server console output
- Code identifiers, enum values, URL slugs
- Dates or numbers in non-user-visible contexts (internal computations, API request params)

## Project setup

`init-project` creates the `locales/` structure and configures the chosen i18n library. Each project's CLAUDE.md declares the library and default locale.

## Enforcement

The `i18n-compliance` skill (part of `quality-review`) scans modified files for:

| Violation | Severity |
|-----------|----------|
| Hardcoded user-visible string in JSX or template | HIGH |
| Hardcoded locale in `Intl` API call | HIGH |
| Missing translation key (used in code, absent in locales/) | HIGH |
| Inline plural ternary | MEDIUM |
| Date arithmetic assuming locale | LOW |

Any HIGH violation blocks the PR.
```

- [ ] **Step 2: Commit**

```bash
git add plugin/rules/ui/i18n.md
git commit -m "feat(plugin/rules): add mandatory i18n rule"
```

---

## Task 7: Observability rules (error tracking and background tasks)

**Files:**
- Create: `plugin/rules/observability/error-observability.md`
- Create: `plugin/rules/observability/background-tasks.md`

- [ ] **Step 1: Write plugin/rules/observability/error-observability.md**

```markdown
# Error Observability

Every exception must be captured by the project's error tracker. Silent failures are forbidden.

## Error capture rules

- **Every `catch` block** that calls `console.error(err)` must also call `errorTracker.captureException(err)` **before** the console call.
- **No fire-and-forget `.catch(console.error)`** — replace with `.catch((err) => { errorTracker.captureException(err); console.error('[context]', err); })`.
- **Non-OK responses from external APIs** (HTTP 4xx/5xx from Telegram, email providers, webhooks) must create and capture an error: `errorTracker.captureException(new Error('[service] failed (${status}): ${body}'))`.
- **Never swallow errors silently** — if it's worth logging, it's worth capturing.

## External service call tracing

Wrap calls to external services in a tracing span to measure their duration as child spans. See `rules/observability/tracing-conventions.md` for span naming and attribute requirements.

```ts
// Example pattern (adapt to your tracing library)
await tracer.startSpan(
  { name: "email: send welcome message", op: "http.client" },
  async (span) => {
    span.setAttribute("email.recipient_id", userId);
    const res = await emailService.sendWelcome(userId);
    if (!res.ok) {
      errorTracker.captureException(new Error(`email failed (${res.status})`));
    }
  }
);
```

## Automatic instrumentation

Do not manually wrap operations that are already auto-instrumented by your ORM, framework, or cache library. Check your instrumentation setup before adding spans to avoid duplication.

## Scope for this rule

This rule covers error capture. For span naming and attribute conventions, see `rules/observability/tracing-conventions.md`. For post-response async work, see `rules/observability/background-tasks.md`.
```

- [ ] **Step 2: Write plugin/rules/observability/background-tasks.md**

```markdown
# Background Tasks (Post-Response Async Work)

Any async operation launched inside a request handler that must complete **after** the HTTP response is returned must be wrapped with the platform's lifecycle extension mechanism.

## Why this matters

Without lifecycle extension, two things break silently:
1. The runtime may recycle the serverless function before the Promise resolves — notifications, emails, and background updates are lost with no error.
2. Tracing child spans (DB queries, external calls) appear in your observability tool *after* the parent span has already closed, making trace analysis impossible.

## Pattern

```ts
// Vercel: use waitUntil from @vercel/functions
import { waitUntil } from "@vercel/functions";

waitUntil(
  someAsyncFn(args).catch((err) => {
    errorTracker.captureException(err);
    console.error("[context] someAsyncFn failed:", err);
  })
);
return response; // return immediately

// Cloudflare Workers: use ctx.waitUntil(promise)
// Node.js long-running process: ensure the process stays alive until the work completes
```

## Rules

- **Never use bare `.catch(...)` fire-and-forget before returning a response** — always wrap with the lifecycle extension mechanism.
- The `.catch` handler must still call `errorTracker.captureException` (see `rules/observability/error-observability.md`).
- When there are multiple independent background operations, call the lifecycle extension separately for each — do not combine into `Promise.all` unless they are logically a single atomic unit.

## Testing

Mock the lifecycle extension in tests so the Promise executes immediately:
```ts
vi.mock("@vercel/functions", () => ({ waitUntil: vi.fn((p) => p) }));
```
```

- [ ] **Step 3: Commit**

```bash
git add plugin/rules/observability/error-observability.md plugin/rules/observability/background-tasks.md
git commit -m "feat(plugin/rules): add observability rules (error capture, background tasks)"
```

---

## Task 8: Observability rules (tracing conventions and Honeycomb)

**Files:**
- Create: `plugin/rules/observability/tracing-conventions.md`
- Create: `plugin/rules/observability/honeycomb-investigation.md`

- [ ] **Step 1: Write plugin/rules/observability/tracing-conventions.md**

This rule was derived from a real production incident: Telegram notifications were not sent when closing polls. Investigation in Honeycomb was blocked because all routes had zero business-level spans — only autogenerated framework spans. It was impossible to answer "how many polls were closed?" or "was a Telegram send even attempted?".

```markdown
# Tracing Conventions

Business-level spans make traces answerable. Autogenerated framework spans (ORM queries, HTTP handlers) describe *what the framework did*, not *what the business did*. You need both.

## Span naming format

```
name:  "<verb> <business object>"   (lowercase, spaces, English)
op:    "<semantic category>"
```

| Example | ✅ Correct | ❌ Incorrect |
|---------|-----------|-------------|
| Closing polls cron | `"close expired polls"` | `"closeDuePolls"`, `"api/cron/close-polls"` |
| Telegram notification | `"telegram: send group reminder"` | `"telegram.sendMessage"` (too generic) |
| Service function | `"poll service: find polls needing reminder"` | `"findPollsNeedingReminder"` |

## Approved `op` categories

| Category | `op` value | When to use |
|----------|-----------|-------------|
| Cron job / background task | `"cron"` | Scheduled handlers |
| Business logic (service layer) | `"function"` | Functions in the service/domain layer |
| Outbound HTTP call | `"http.client"` | External APIs (notifications, webhooks, email) |
| Inbound HTTP | — | Do not use — autogenerated by the framework |

## Mandatory attributes by span type

**Cron / batch spans** — must include quantifiable outcome so a trace explains why no work happened:
```ts
span.setAttribute("poll.closed_count", count);   // how many items were processed
span.setAttribute("poll.candidates_found", n);   // how many candidates were found
```

**Service function spans** — must include entity IDs:
```ts
span.setAttribute("poll.id", pollId);
span.setAttribute("team.id", teamId);
span.setAttribute("user.id", requestingUserId);  // who triggered this
```

**Outbound HTTP spans** — must be specific per message type, never generic:
```ts
span.setAttribute("telegram.message_type", "group_poll_reminder");  // what was sent
span.setAttribute("poll.id", pollId);
span.setAttribute("poll.pending_count", pendingCount);              // why it was sent
```

## General attribute conventions

| Attribute | Required when |
|-----------|--------------|
| `user.id` | Any span triggered by a user action |
| `<owning-entity>.id` | Span operates on tenant-scoped data |
| `<primary-entity>.id` | The entity being read or mutated |
| `<entity>.<outcome>_count` | Span processes N items (closed, reminded, created, failed) |
| `<service>.message_type` | Outbound messaging spans |

## What NOT to instrument manually

- **Framework autogenerated spans** (HTTP handler names, route resolution) — cannot be renamed; add business spans as children
- **ORM autogenerated spans** (query method names, connection events) — handled by ORM instrumentation; business spans become their semantic parent
- **Cache operations** — if the project uses a cache wrapper with built-in tracing, do not add spans manually

## Position in the trace tree

```
GET /api/cron/close-polls              ← framework (autogenerated)
└── close expired polls [op=cron]      ← your business span
    ├── poll service: close due polls [op=function]
    │   └── Poll.updateMany            ← ORM (autogenerated)
    └── telegram: send close notice [op=http.client]
```

## Enforcement

`quality-review` checks every new span introduced in the branch:
- Name follows `"<verb> <business object>"` format → MEDIUM if violated
- `op` is from the approved list → MEDIUM if violated
- Mandatory attributes present for the span type → MEDIUM if missing
- No generic outbound HTTP span name (e.g. `"sendMessage"` with no context) → HIGH
```

- [ ] **Step 2: Write plugin/rules/observability/honeycomb-investigation.md**

```markdown
# Honeycomb Investigation Protocol

When investigating production issues (latency, errors, missing data) using the Honeycomb MCP.

## Workflow

**1. Always start with workspace context**

Call `get_workspace_context` first to discover available environments and datasets. Never assume an environment name or dataset name — they change per project and per deployment environment.

**2. Discover columns before querying**

Use `find_columns` or `get_dataset_columns` to confirm field names before building a query. Field schemas evolve; querying a stale name returns empty results without error, leading to false conclusions.

**3. Use human-readable time ranges**

Use `"last 2 hours"`, `"24h"`, `"last 7 days"` in query parameters — avoid epoch timestamps unless you need a precise window. Human-readable ranges are less error-prone and easier to communicate.

**4. Specify environment and dataset explicitly**

Every query call must specify both the environment and the dataset. Never rely on defaults.

## Environment vs deployment attribute

The Honeycomb **environment** is determined by which API key was used to send the data — it's configured in your deployment platform (e.g. per Vercel environment). The **`deployment.environment` span attribute** is set by your instrumentation code from `NODE_ENV` or similar. They can disagree if the wrong key is configured.

When in doubt about whether a trace is from production: check `deployment.environment`, `http.host`, and any git reference attributes on the root span.

## Investigation pattern

```
1. get_workspace_context        → discover environments + default datasets
2. get_dataset_columns          → confirm field names
3. run_query (broad)            → identify the time window and affected traces
4. run_bubbleup                 → find differentiating attributes between failing/passing
5. get_trace (specific trace)   → drill into individual request
6. Form hypothesis → verify with targeted query
```

## Useful BubbleUp pattern

When a metric is anomalous (high error rate, high latency), use `run_bubbleup` to compare the anomalous window against baseline. BubbleUp surfaces which attribute values appear disproportionately in the bad window — e.g. a specific user ID, deployment version, or database host.
```

- [ ] **Step 3: Commit**

```bash
git add plugin/rules/observability/tracing-conventions.md plugin/rules/observability/honeycomb-investigation.md
git commit -m "feat(plugin/rules): add tracing conventions and Honeycomb investigation protocol"
```

---

## Task 9: Workflow rules

**Files:**
- Create: `plugin/rules/workflow/project-structure.md`
- Create: `plugin/rules/workflow/verification-doc-format.md`
- Create: `plugin/rules/workflow/ui-first-testing.md`

- [ ] **Step 1: Write plugin/rules/workflow/project-structure.md**

```markdown
# Project Structure Contract

Every project initialised with this framework follows this directory layout. Skills navigate it by reading the project's `CLAUDE.md` index — they do not hardcode paths.

## Root

```
CLAUDE.md                      ← thin index (<100 lines), auto-loaded by Claude
IMPLEMENTATION.md              ← active sprint tracker (root for easy access)
.claude/
  commands/                    ← slash commands (contributed by installed plugins)
  settings.json
  rules/                       ← project-specific behavioural rules
    coding.md                  ← TypeScript/language standards, linting, naming
    architecture.md            ← layer definitions for this project (from template)
    testing.md                 ← test strategy, mock approach, coverage expectations
    ui.md                      ← design tokens, contrast rules (from template)
    observability.md           ← error tracker and tracing setup for this project
docs/
  README.md                    ← documentation index (lists all docs with one-line descriptions)
  plan.md                      ← high-level feature design (generated by init-project)
  features.md                  ← current feature inventory with behaviour descriptions
  arch.md                      ← architecture diagram (text/ASCII or linked diagram)
  db.md                        ← data model / schema description
  api.md                       ← API surface reference
  design-system.html           ← visual design system (generated by init-design-system)
  icons.html                   ← icon catalog (generated by init-design-system)
  mockups/                     ← HTML mockup files, one per screen/feature
  superpowers/
    plans/                     ← implementation plans (YYYY-MM-DD-<name>.md)
    specs/
      refined/                 ← refinement mini-specs + queue.json
        done/                  ← archived specs after completion
    verification/              ← verification documents (funcional + -api variants)
      verified/                ← archived after all tests ✅
locales/
  <default-locale>/            ← translation files (common.json + per-feature)
  <additional-locale>/
```

## CLAUDE.md structure

The project's CLAUDE.md is always under 100 lines. It contains:
- 1-2 sentence project description
- Stack list with link to `.claude/rules/architecture.md`
- Links to thematic rule files in `.claude/rules/`
- Links to documentation files in `docs/`
- Dev commands (build, dev, test) in a code block
- Workflow shortcuts (`/dev-cycle`, `/refine`)
- Dependencies section (required plugins and MCPs)

## docs/README.md

A one-line entry per documentation file declaring its purpose. Skills read this index to discover which docs exist rather than assuming a fixed set.

```markdown
## Documentation index
- [plan.md](plan.md) — high-level feature design and architecture decisions
- [features.md](features.md) — current feature inventory with behaviour descriptions
- [arch.md](arch.md) — system architecture diagram and layer descriptions
- [db.md](db.md) — database schema and entity relationships
- [api.md](api.md) — API routes, request/response shapes, auth requirements
```
```

- [ ] **Step 2: Write plugin/rules/workflow/verification-doc-format.md**

```markdown
# Verification Document Format

Every PR produces two verification documents. They are complementary — the functional doc can be archived independently when its tests pass, even if the technical doc still has open items.

## Two-document structure

**Functional doc** — `docs/superpowers/verification/YYYY-MM-DD-<slug>.md`
- Tests a tester can execute **from the UI** without DevTools Console or database access
- Covers: complete UI flows, mobile-first validation, visual regression, navigation, user-visible error messages
- Header note: *"Complementary doc: `<slug>-api.md`. This doc covers UI end-to-end flows only and can be archived independently when all its tests are ✅ OK."*

**Technical doc** — `docs/superpowers/verification/YYYY-MM-DD-<slug>-api.md`
- Tests requiring **DevTools Console** (direct API calls), **database inspection** (Prisma Studio / DB client), or **API-level permission testing** (403s for unauthorised callers)
- Each technical test includes a reference to the unit test covering the same rule: `**Unit coverage:** path/to/test.ts → "test name"`
- Header note pointing back to the functional doc

## File naming

- `YYYY-MM-DD` = date of creation
- `<slug>` = kebab-case of the PR's main topic (e.g. `telegram-notifications-fix`, `availability-ux`)
- Technical doc: `<slug>-api.md`

## Document structure

```markdown
# Local verification — <Descriptive title>

**Branch:** `<branch-name>`
**PR:** <link or "pending">
**Test date:** ___________
**Tester:** ___________

---

## How to use this document

Mark each test by placing `x` in the checkbox and filling in comments:
- [x] ✅ OK
- [ ] ⚠️ PARTIAL
- [ ] ❌ FAIL

**Comments** — always write something:
- ✅ OK → what worked well
- ⚠️ PARTIAL → what works and what doesn't
- ❌ FAIL → what happens vs what should happen

---

## Prerequisites

| Requirement | Status | Comments |
|-------------|--------|----------|
| Local server running | | |
[additional rows as needed]

---

## Block N — <Functional area name>

### PN.1 — <Test title>

**Steps:**
1. <User action>
2. <User action>

**Status:**
- [ ] ✅ OK
- [ ] ⚠️ PARTIAL
- [ ] ❌ FAIL

**Comments:**
>

---
```

## Numbering

- Blocks: `Block 1`, `Block 2`, ...
- Tests: `P1.1`, `P1.2`, `P2.1`, ... (unique across the whole document)

## Routing tests between docs

| Goes to functional | Goes to technical |
|-------------------|------------------|
| UI action + Network panel verification | `fetch()` from console |
| Mobile viewport check | Prisma Studio / DB inspection |
| Visual regression | Permission rejection at API level (403) |
| Form submit + visible result | Payload validation (invalid body → 422) |

## Archiving

When all tests in a doc are `[x] ✅ OK`, move it to `docs/superpowers/verification/verified/`.
```

- [ ] **Step 3: Write plugin/rules/workflow/ui-first-testing.md**

```markdown
# UI-First Testing

Verification tests describe user actions, not API calls. This rule applies to the functional verification document.

## The rule

**For every behaviour to verify: identify which UI page triggers it, then write the test steps as user actions.**

```
✅ Correct (UI-first):
  1. Sign in as `player`
  2. Navigate to /teams/my-team/polls
  3. DevTools → Network → filter by `polls/`
  4. Verify GET /api/teams/{id}/polls fires
  5. Confirm the response contains `status: "OPEN"`
  6. Confirm the "Open poll" badge appears on the card

❌ Wrong (API-first):
  1. Call GET /api/teams/{id}/polls
  2. Verify the response contains status: "OPEN"
```

## When a direct API call IS allowed

- The endpoint has no UI that triggers it (admin/cron endpoints, webhooks)
- The test covers an error case the UI deliberately prevents (e.g. submitting invalid payload, 409 conflict)
- Verifying internal state (database values, cache contents)

In those cases: document the exact `curl` or `fetch()` call. If a UI equivalent exists, include it as the primary path and the API call as a secondary verification.

## What makes a good test step

- The role used to sign in (`admin`, `player`, `manager`)
- The exact URL to navigate to
- The specific element to interact with
- The exact observable outcome (text visible, badge present, network request shape, redirect URL)

## What makes a bad test step

- Only verifies no error occurred, without describing what the user sees
- So generic it would pass even if a related feature broke
- Describes implementation details ("the service calls updateMany") rather than observable behaviour
```

- [ ] **Step 4: Commit**

```bash
git add plugin/rules/workflow/
git commit -m "feat(plugin/rules): add workflow rules (project structure, verification format, UI-first testing)"
```

---

## Task 10: Templates

**Files:**
- Create: `plugin/rules/templates/architecture-layers.md`
- Create: `plugin/rules/templates/ui-design-tokens.md`

- [ ] **Step 1: Write plugin/rules/templates/architecture-layers.md**

```markdown
# Architecture Layers — [PROJECT NAME]

> **This file is a template.** It is generated by `init-project` during the brainstorming phase and filled with the layer definitions for this specific project. The principle is universal; the layers are project-specific.

---

## Layers (data flow, top to bottom)

```
┌─────────────────────────────────────────────────┐
│ Layer N: [Name]                                  │
│   [file paths]                                   │
│   • [what it does]                               │
│   • [what it must NOT do]                        │
└─────────────────────────────────────────────────┘
                  ↓ calls
[repeat for each layer]
```

## Layer rules — non-negotiable

| Rule | Forbids | Requires |
|------|---------|----------|
| R1 [Layer] | [what is forbidden] | [what is required] |

## Architecture compliance checks

```bash
# Commands that verify layer boundaries (defined in project CLAUDE.md)
[project-specific check commands]
```

## Rationale

[Why this layering was chosen for this project. What problems it solves. Written during init-project brainstorm.]
```

- [ ] **Step 2: Write plugin/rules/templates/ui-design-tokens.md**

```markdown
# UI Design Tokens — [PROJECT NAME]

> **This file is a template.** It is generated by `init-design-system` during `init-project` and filled with the resolved token values for this project's design system.

---

## Component library: [LIBRARY NAME]

## Token Reference (Light / Dark)

| Token class | Light value | Dark value |
|-------------|-------------|------------|
| `bg-page`        | #... | #... |
| `bg-panel`       | #... | #... |
| `bg-panel-hover` | #... | #... |
| `text-strong`    | #... | #... |
| `text-soft`      | #... | #... |
| `text-faint`     | #... | #... |
| `text-primary`   | #... | #... |
| `bg-hero-from`   | #... | #... |
| `bg-hero-to`     | #... | #... |

## WCAG Contrast Reference

| Text | Background | Ratio | Status |
|------|-----------|-------|--------|
| `text-primary` | `bg-panel` (light) | ?:1 | [✅ / ❌] |
| `text-white` | hero gradient | ?:1 | [✅ / ❌] |
[filled by init-design-system]

## Pattern Catalogue

### Hero / dark sections
[filled by init-design-system based on chosen palette]

### Active tab / selector states
[filled by init-design-system]

### Status badges
[filled by init-design-system]

## Contrast Audit Checklist

- [ ] Hero sections — all text uses light variants on dark gradient
- [ ] Active tabs/nav — use `text-primary` (not a low-contrast variant) on light backgrounds
- [ ] Status badges — use darker text variants in light mode with dark-mode overrides
- [ ] Normal text on panels — use `text-strong` or `text-soft`; never `text-faint` for meaningful content
```

- [ ] **Step 3: Commit**

```bash
git add plugin/rules/templates/
git commit -m "feat(plugin/rules): add architecture-layers and ui-design-tokens templates"
```

---

## Task 11: Verify complete plugin structure

- [ ] **Step 1: Verify all rule files exist**

```bash
find plugin/rules -name "*.md" | sort
```

Expected (20 files):
```
plugin/rules/code-quality/code-quality.md
plugin/rules/code-quality/database-patterns.md
plugin/rules/code-quality/redis-cache-pattern.md
plugin/rules/observability/background-tasks.md
plugin/rules/observability/error-observability.md
plugin/rules/observability/honeycomb-investigation.md
plugin/rules/observability/tracing-conventions.md
plugin/rules/process/dev-prod-parity.md
plugin/rules/process/git-discipline.md
plugin/rules/process/implementation-tracking.md
plugin/rules/process/tdd-cycle.md
plugin/rules/security/code-quality-checklist.md
plugin/rules/security/security-checklist.md
plugin/rules/templates/architecture-layers.md
plugin/rules/templates/ui-design-tokens.md
plugin/rules/ui/fine-grained-reactivity.md
plugin/rules/ui/i18n.md
plugin/rules/ui/mobile-first.md
plugin/rules/ui/skeleton-first.md
plugin/rules/workflow/project-structure.md
plugin/rules/workflow/ui-first-testing.md
plugin/rules/workflow/verification-doc-format.md
```

- [ ] **Step 2: Verify plugin scaffold files exist**

```bash
ls plugin/package.json plugin/README.md plugin/dependencies.md
```

- [ ] **Step 3: Verify plugin can be referenced by Claude Code**

Check that the package.json has a valid name:
```bash
cat plugin/package.json | grep '"name"'
```
Expected: `"name": "dev-workflow"`

- [ ] **Step 4: Final commit with summary tag**

```bash
git tag phase1-foundation
git log --oneline -10
```

Verify 10 commits exist covering all tasks. If any task commits are missing, commit their files now before tagging.

---

## Self-review notes

**Spec coverage:**
- ✅ Plugin scaffold (package.json, README, dependencies manifest)
- ✅ All 4 process rules
- ✅ All 3 code quality rules (including redis-cache-pattern)
- ✅ Both security rules
- ✅ All 4 UI rules including i18n
- ✅ All 4 observability rules including tracing-conventions (from production incident)
- ✅ All 3 workflow rules
- ✅ Both templates

**Not in this plan (Phase 2 & 3):**
- commands/ files (dev-cycle, security-review, verify-pr, generate-verification, ui-contrast)
- skills/ files (analyze-context, write-plan, implement-agentic, quality-review, etc.)
- init-project command and skills
- init-design-system, update-icons, i18n-compliance skills
