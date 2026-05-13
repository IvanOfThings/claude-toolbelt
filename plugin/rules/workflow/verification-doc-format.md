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
