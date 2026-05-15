# apply-pr-fixes

Applies TDD fixes for each diagnosed PR failure and appends a **Fix iteration** block to the verification document so the tester can re-check. Does not commit — the developer reviews and commits when ready.

## Input

Diagnosis output from `diagnose-pr-failures` (confirmed by developer).

## Steps

For each diagnosed unresolved test (in dependency order — foundational fixes first):

**1. Determine the iteration number**

Read the test entry in the verification document. Count existing `#### 🔧 Fix iteration N` blocks under it. The new block is iteration `N+1` (or `1` if there are none).

**2. Write a failing unit test**

Write a test that reproduces the failure programmatically. Run it and confirm it fails with the expected error message.

If a prior iteration already added a unit test, extend or add a new test that covers the specific sub-case the tester surfaced — do not replace the old one.

**3. Implement the fix**

Implement the minimum code to make the test pass. Do not fix unrelated issues. Run the test and confirm it passes.

**4. Run the full test suite**

Run all tests. Confirm no regressions.

**5. Append the Fix iteration block to the verification document**

Insert the block **below** the test's Initial status, Comments, and any previous iteration blocks — never above and never modifying earlier content. Use the exact format from `rules/workflow/verification-doc-format.md`:

```markdown
#### 🔧 Fix iteration N — YYYY-MM-DD — `pending`

**Diagnosis:** <root cause from diagnose-pr-failures, written so the tester can understand why the original behaviour happened>

**Changes:**
- `path/to/file.ts:L1-L2` — <what changed and why>
- `path/to/another.ts:L3` — <what changed>

**Unit coverage:** `path/to/test.ts → "test name added or updated"`

**What to re-check:** <concrete steps the tester runs to verify; reference the original test steps and call out the specific outcome that should change>

**Tester re-check (iteration N):**
- [ ] ✅ OK
- [ ] ❌ STILL FAILING
- [ ] ⚠️ NEW ISSUE FOUND

**Comments (iteration N):**
>
```

- The hash field is written as `pending` — the developer back-fills it after committing (or leaves it as `pending`).
- The "Tester re-check" checkboxes and "Comments (iteration N)" field are written as empty placeholders. Never pre-mark a status.
- Never edit the Initial status, the original Comments, or any earlier iteration block.

**6. Report and hand off to the developer**

After all diagnosed tests have their iteration blocks appended, output:

```
[apply-pr-fixes] N iterations appended to <doc-path>

  P2.1 — iteration 2 — src/.../poll-form.tsx + 1 unit test
  P3.4 — iteration 1 — src/.../availability-service.ts + 1 unit test

Changes are staged in the working tree. Review and commit when ready, then return the document to the tester for re-check.

If, after re-check, the tester marks a "STILL FAILING" or "NEW ISSUE FOUND" outcome, run `/verify-pr` again on the same doc to append the next iteration.
```

Do **not** run `git add` or `git commit`. The developer reviews diffs, picks the commit boundary, and writes the message.

## Archival check

After applying fixes, check whether every test in both verification documents (functional + technical) is now resolved per the rule in `rules/workflow/verification-doc-format.md` (latest iteration `[x] ✅ OK`, or Initial status `[x] ✅ OK` with no iteration).

If all are resolved: report this fact to the developer with the suggestion to archive (move to `docs/superpowers/verification/verified/`). Do **not** move the files automatically — archival is a state change the developer should confirm, especially because the documents may still be open in their editor or referenced by an open PR.
