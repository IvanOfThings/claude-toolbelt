# diagnose-pr-failures

Reads a verification document, extracts tests that need attention, and produces a structured diagnosis before touching any code. Aware of the iterative fix loop: it picks up both initial failures and tests where the tester rejected a previous fix.

## Input

`doc-path`: path to the verification document (functional or technical).

`test-ids` (optional): specific test IDs to diagnose (e.g. `P1.2 P3.1`). If omitted, diagnoses every test currently unresolved (see resolution rule below).

## Resolution rule (recap from `rules/workflow/verification-doc-format.md`)

A test is **resolved** when its latest iteration has `[x] ✅ OK`. A test is **unresolved** if any of the following hold:
- It has **no** Fix iteration block and Initial status is `[x] ❌ FAIL` or `[x] ⚠️ PARTIAL`.
- It has Fix iteration blocks and the latest one has `[x] ❌ STILL FAILING` or `[x] ⚠️ NEW ISSUE FOUND`.
- It has Fix iteration blocks but the latest one has **no** Tester re-check checkbox marked (the tester has not yet responded — do not diagnose; report it as "awaiting tester re-check" and skip).

## Steps

**1. Read the verification document**

Parse every test. For each unresolved test, record:
- ID and title
- Steps
- Initial status and Comments (the original failure description from the tester)
- Every previous Fix iteration block (iteration number, diagnosis, changes, what-to-re-check, tester re-check outcome, tester comments) — in order

**2. Read relevant source files**

For each unresolved test, identify the source files likely responsible (routes, services, components, existing tests). Read them. For tests with prior iterations, also read the files those iterations touched — the failure may be in a different layer than previously assumed.

**3. Produce structured diagnosis**

For each unresolved test, output:

```
### P2.1 — [test title]   (iteration N — to be appended)

**What the tester sees:**
- Original failure: [from Initial Comments]
- After iteration N-1: [from latest "Comments (iteration N-1)" — if any]

**Previous attempts:**     (only when prior iterations exist)
- Iteration 1 (a1b2c3d) — [one-line summary of that diagnosis + outcome marked by tester]
- Iteration 2 (pending) — [...]

**Root cause:** [your analysis, explicitly accounting for why the previous fixes did not resolve it]

**Affected files:** [list of files to change in this iteration]

**Proposed fix:** [1-2 sentence description; must differ meaningfully from prior iterations unless the tester's new comment points to a missed sub-case of the same root cause]

**Existing test coverage:** [path/to/test.ts → "test name" if a unit test covers this, otherwise "none — will be added"]
```

If a prior iteration's diagnosis already covers the tester's new comment word-for-word, surface this explicitly: do not propose the same fix twice. Ask the developer how to proceed before continuing.

**4. Gate**

Present the full diagnosis. Do not touch any code. Wait for developer confirmation before `apply-pr-fixes` proceeds.

If any tests were skipped as "awaiting tester re-check", list them at the end of the diagnosis so the developer knows they exist but were not addressed.
