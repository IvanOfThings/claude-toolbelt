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

If a test fails or is partial, `/verify-pr` will append a **Fix iteration** block below the test. The tester re-checks the iteration and either marks it ✅ OK (test resolved) or fills in a new comment so `/verify-pr` can append a further iteration. The loop continues until the latest iteration is ✅ OK.

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

**Initial status:**
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

## Fix iteration block

When `/verify-pr` (via `apply-pr-fixes`) fixes a failing test, it appends a **Fix iteration** block **below** the test's Initial status and Comments. The Initial status and Comments are never modified — they remain as the historical record of the original failure.

```markdown
#### 🔧 Fix iteration N — YYYY-MM-DD — `<short-hash-or-pending>`

**Diagnosis:** <root cause analysis from diagnose-pr-failures>

**Changes:**
- `path/to/file.ts:L1-L2` — <what changed and why>
- `path/to/another.ts:L3` — <what changed>

**Unit coverage:** `path/to/test.ts → "test name added or updated"`

**What to re-check:** <concrete steps the tester runs to verify the fix; refer to the original test steps and call out the specific outcome that should change>

**Tester re-check (iteration N):**
- [ ] ✅ OK
- [ ] ❌ STILL FAILING
- [ ] ⚠️ NEW ISSUE FOUND

**Comments (iteration N):**
>
```

The hash field is `pending` when the iteration is written before the developer commits, and is back-filled by the developer after committing (or left as `pending` if they prefer).

## Iteration rules

- **Numbering**: iterations are numbered per test (`Fix iteration 1`, `Fix iteration 2`, ...). When appending, `apply-pr-fixes` reads the previous iterations and picks the next integer.
- **History is preserved**: never edit a previous iteration block — append a new one. The full sequence of attempts must remain visible for review.
- **Resolution rule**: a test is considered resolved when its **latest iteration** has `[x] ✅ OK`. A test with no iteration block is resolved only if the Initial status is `[x] ✅ OK`.
- **Re-entry**: a test whose latest iteration is `[x] ❌ STILL FAILING` or `[x] ⚠️ NEW ISSUE FOUND` is picked up by the next `/verify-pr` run, which appends `Fix iteration N+1`.
- **Tester-only fields**: the "Tester re-check" checkboxes and "Comments (iteration N)" field are filled by the tester, never by `apply-pr-fixes`. The skill writes them as empty placeholders.
- **Diagnosis context**: when generating iteration N, `diagnose-pr-failures` reads iterations 1..N-1 so the new fix does not repeat a previously failed attempt.

## Archiving

When all tests in a doc are resolved per the resolution rule above, move it to `docs/superpowers/verification/verified/`.
