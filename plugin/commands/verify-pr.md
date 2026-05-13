# /verify-pr

Diagnoses and fixes failures in a verification document.

**Usage:** `/verify-pr [doc-path] [test-ids...]`

- `doc-path`: path to the verification document containing failing tests. If omitted, uses the most recent document in `docs/superpowers/verification/`.
- `test-ids`: optional list of specific test IDs to address (e.g. `P1.2 P3.1`). If omitted, addresses all `❌ FAIL` and `⚠️ PARTIAL` tests.

---

## Step 1 — Diagnose

Invoke `diagnose-pr-failures` with `doc-path` and `test-ids`.

**GATE:** Present the full diagnosis to the developer. Wait for confirmation before applying fixes.

---

## Step 2 — Fix

Invoke `apply-pr-fixes` with the confirmed diagnosis.

---

## Step 3 — Archive (if complete)

After `apply-pr-fixes` completes: if both verification documents have all tests resolved, move them to `docs/superpowers/verification/verified/`.

Report the archive path to the developer.
