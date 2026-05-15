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

Invoke `security-review-code` skill. The skill applies `rules/security/security-checklist.md` (OWASP Top 10 + CSRF + XSS) against `git diff main`, runs a dependency audit (A06) against the project's lockfile, and runs a secret scan (A02). Findings are reported with OWASP IDs, e.g. `[A01-CRITICAL]`, `[A06-CRITICAL]`, `[A02-CRITICAL]`.

CRITICAL findings in any OWASP category block proceeding. `--ai` mode is not invoked here automatically — use `/security-review code --ai` manually for high-risk PRs.

**Gate 6: i18n compliance**

Invoke `i18n-compliance` skill (reads `rules/ui/i18n.md` against modified source files in `git diff main`).

Any HIGH violation blocks proceeding. MEDIUM and LOW are presented to the developer who decides.

**Gate 7: Magic-string scan (informational — non-blocking)**

Heuristic scan for likely magic-string-for-enum violations in the diff. Reads `rules/code-quality/code-quality.md` (section "No magic strings for domain enums") for context.

**Scan procedure** against `git diff main` plus the rest of `src/` for cross-file detection:

1. Extract every string literal appearing in one of these contexts in **changed files** only:
   - `=== '<lit>'` or `!== '<lit>'`
   - `=== "<lit>"` or `!== "<lit>"`
   - `case '<lit>':` / `case "<lit>":`
   - object/property assignment with a likely-enum key: `status: '<lit>'`, `role: '<lit>'`, `type: '<lit>'`, `kind: '<lit>'`, `state: '<lit>'`, `category: '<lit>'`
2. For each extracted literal, count occurrences of the **same literal in the same context family** across the full `src/` tree (not just the diff). Use `git grep` or `rg`.
3. Report any literal with **≥ 3 cross-file occurrences** as a candidate, with the files:lines where it appears and a suggested action.

**Filtering — skip the report when:**
- The literal already appears as an `enum` member, `as const` value, or generated-type value somewhere in `src/` (grep for `= '<lit>'` in enum / object-literal export contexts).
- The literal is a known framework string (`'GET'`, `'POST'`, `'PUT'`, `'PATCH'`, `'DELETE'`, `'application/json'`, etc.) — these have their own conventions.
- The literal is shorter than 2 characters (likely not a domain enum).

Output:

```
[magic-strings] No new magic-string candidates detected.

or

[magic-strings] INFORMATIONAL — 2 candidates detected

  'open' — 4 occurrences across:
    src/components/poll-card.tsx:23
    src/services/poll.ts:14
    src/services/poll.ts:67
    src/app/api/polls/route.ts:18
  → Suggestion: extract as PollStatus.Open (enum or generated schema type)

  'admin' — 3 occurrences across:
    src/middleware/auth.ts:9
    src/services/team.ts:42
    src/components/admin-panel.tsx:11
  → Suggestion: extract as Role.Admin
```

This gate is **informational only** — it does not block `quality-review` from passing. The developer reviews each candidate and decides whether to refactor or accept (some literals are legitimately one-off).

## Output format

```
[quality-review] PASS — Gates 1–6 passed (Gate 7 informational)

or

[quality-review] BLOCKED

  Gate 2 — Error observability
  src/services/poll.ts:45 — catch block missing captureException before console.error

  Gate 5 — Security
  [A01-CRITICAL] src/api/admin.ts:12 — route handler missing auth check
  [A06-CRITICAL] axios@0.21.0 — CVE-2024-39338 (SSRF), fixed in 1.7.4
  [A02-CRITICAL] config/staging.env:7 — possible committed AWS access key ID

  Gate 7 — Magic strings (informational, does not block)
  [magic-strings] 'open' — 4 occurrences → extract as PollStatus.Open
```

CRITICAL security issues and architecture violations block proceeding. MEDIUM and LOW issues are presented to the developer who decides whether to fix before moving on. Gate 7 findings never block — they are presented as suggestions only.
