# /generate-verification

Generates verification documents for the current branch.

**Usage:** `/generate-verification [spec-path]`

`spec-path` is optional. If provided, `analyze-context` also reads this file for additional context about what was built.

---

## Step 1 — Context analysis

Invoke `analyze-context`. If `spec-path` was provided, include it in the context read.

---

## Step 2 — Generate documents

Invoke `generate-verification-doc`.

Show the developer both generated document paths.
