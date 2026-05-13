# /security-review

Runs a security review on a plan (before implementation) or on code changes (after implementation).

**Usage:**
- `/security-review plan <path>` — reviews a plan file before starting implementation
- `/security-review code` — reviews `git diff main` after implementation

---

## Plan mode

`/security-review plan <path>`

Invoke `security-review-plan` with the provided plan file path.

---

## Code mode

`/security-review code`

Invoke `security-review-code` against the current `git diff main`.
