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

**Gate 6: i18n compliance**

Invoke `i18n-compliance` skill (reads `rules/ui/i18n.md` against modified source files in `git diff main`).

Any HIGH violation blocks proceeding. MEDIUM and LOW are presented to the developer who decides.

## Output format

```
[quality-review] PASS — all 6 gates passed

or

[quality-review] BLOCKED

  Gate 2 — Error observability
  src/services/poll.ts:45 — catch block missing captureException before console.error

  Gate 5 — Security
  [CRITICAL] src/api/admin.ts:12 — route handler missing auth check
```

CRITICAL security issues and architecture violations block proceeding. MEDIUM and LOW issues are presented to the developer who decides whether to fix before moving on.
