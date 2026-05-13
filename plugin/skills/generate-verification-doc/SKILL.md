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
