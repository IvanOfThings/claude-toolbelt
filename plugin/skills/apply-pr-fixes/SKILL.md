# apply-pr-fixes

Applies TDD fixes for each diagnosed PR failure. Updates the verification document after each fix.

## Input

Diagnosis output from `diagnose-pr-failures` (confirmed by developer).

## Steps

For each diagnosed failing test (in dependency order — foundational fixes first):

**1. Write a failing unit test**

Write a test that reproduces the failure programmatically. Run it and confirm it fails with the expected error message.

**2. Implement the fix**

Implement the minimum code to make the test pass. Do not fix unrelated issues. Run the test and confirm it passes.

**3. Run the full test suite**

Run all tests. Confirm no regressions.

**4. Update the verification document**

Change the test's status line to:
```markdown
- [ ] 🔧 CORREGIDO — pendiente re-test
```

Add to the tester comments field:
```
> Fix: [what was changed] — [short commit hash]
```

**5. Commit**

```bash
git add <changed source files> <verification document>
git commit -m "fix: <description> (P<N>.<M>)"
```

**6. Archive if all resolved**

After all fixes in this batch are committed: check if every test in both verification documents (functional + technical) is either `[x] ✅ OK` or `🔧 CORREGIDO — pendiente re-test`.

If all are resolved: move both documents to `docs/superpowers/verification/verified/` and report the archive.
