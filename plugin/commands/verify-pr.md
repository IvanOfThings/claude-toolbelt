# /verify-pr

Iteratively fixes failures in a verification document. Each run produces one **Fix iteration** per unresolved test; the tester re-checks, and if any iteration still fails, the developer runs `/verify-pr` again to append the next iteration. The loop continues until every test's latest iteration is `[x] ✅ OK`.

**Usage:** `/verify-pr [doc-path] [test-ids...]`

- `doc-path`: path to the verification document containing failing tests. If omitted, uses the most recent document in `docs/superpowers/verification/`.
- `test-ids`: optional list of specific test IDs to address (e.g. `P1.2 P3.1`). If omitted, addresses every unresolved test in the doc.

A test is **unresolved** when:
- It has no Fix iteration block and Initial status is `[x] ❌ FAIL` or `[x] ⚠️ PARTIAL`, **or**
- Its latest Fix iteration is marked `[x] ❌ STILL FAILING` or `[x] ⚠️ NEW ISSUE FOUND` by the tester.

(See `rules/workflow/verification-doc-format.md` for the full resolution rule and iteration block format.)

---

## Step 1 — Diagnose

Invoke `diagnose-pr-failures` with `doc-path` and `test-ids`.

For each unresolved test, the diagnosis includes the iteration history so the proposed fix does not repeat a previously failed attempt.

If any test is marked as "awaiting tester re-check" (latest iteration has no Tester re-check checkbox marked), the skill skips it and reports it at the end — those need the tester's input before they can be re-diagnosed.

**GATE:** Present the full diagnosis to the developer. Wait for confirmation before applying fixes.

---

## Step 2 — Fix

Invoke `apply-pr-fixes` with the confirmed diagnosis.

For each unresolved test, the skill writes a failing unit test, implements the minimum code to make it pass, runs the full suite, and appends a **Fix iteration N** block to the verification document. Iteration numbering is per test and computed automatically from the existing blocks.

The skill does **not** run `git add` or `git commit`. Changes are staged in the working tree for the developer to review.

---

## Step 3 — Hand back to the developer

`apply-pr-fixes` reports which iterations were appended and where. The developer:

1. Reviews the diff (source changes + the new iteration block in the verification doc).
2. Commits when ready, choosing the message and the commit boundary.
3. Optionally back-fills the iteration block's hash field (`pending` → short hash).
4. Returns the document to the tester for re-check.

---

## Step 4 — Iterate or archive

When the tester re-checks an iteration:

- **`[x] ✅ OK`** — the test is resolved for that iteration. Nothing to do here.
- **`[x] ❌ STILL FAILING`** or **`[x] ⚠️ NEW ISSUE FOUND`** — the developer re-runs `/verify-pr` on the same doc. Step 1 picks the test up, includes iteration N in the history, and Step 2 appends iteration N+1.

When **every** test in both verification documents (functional + technical) is resolved, `apply-pr-fixes` reports that the docs are ready to archive. The developer moves them to `docs/superpowers/verification/verified/` when they are sure no further review is needed — `/verify-pr` does **not** move the files automatically.

---

## Notes

- `/verify-pr` is safe to run repeatedly on the same document. Each run is idempotent for resolved tests (they are skipped) and incremental for unresolved ones (one new iteration appended).
- The Initial status and Comments are never modified — they are the historical record of the tester's original observation.
- Earlier iteration blocks are never edited. Every attempt is preserved so the developer and tester can see the full sequence of fixes and feedback.
