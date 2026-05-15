# /security-review

Runs a security review on a plan (before implementation) or on code changes (after implementation). Findings are reported with OWASP IDs.

**Usage:**
- `/security-review plan <path>` — reviews a plan file before starting implementation
- `/security-review code [--ai]` — reviews `git diff main` after implementation; `--ai` adds a complementary AI-driven pass

---

## Plan mode

`/security-review plan <path>`

Invoke `security-review-plan` with the provided plan file path.

The skill reads `rules/security/security-checklist.md` (OWASP Top 10 + CSRF + XSS) and maps each potential issue in the plan to its OWASP category. Critical issues block the plan; medium/low are surfaced for the developer to decide.

---

## Code mode

`/security-review code [--ai]`

Invoke `security-review-code` against the current `git diff main`.

The skill runs three checks:

1. **Checklist** — every item in `rules/security/security-checklist.md` applied to the diff.
2. **Dependency audit (A06)** — `npm audit` / `pnpm audit` / `yarn audit` against the project's lockfile. CRITICAL CVEs block; HIGH are presented.
3. **Secret scan (A02)** — `gitleaks` or `trufflehog` if installed, regex fallback otherwise. Every match is CRITICAL.

If `--ai` is passed: after the rule-based output, the built-in `superpowers:security-review` skill runs on the same branch as a complementary AI-driven review. Its findings are appended under a separate heading and are advisory only — they do not change the severity of the rule-based findings.

When to use `--ai`:
- Sensitive or novel features (auth, payments, file uploads, new external integrations).
- Before merging to `main` if you want a second opinion on critical paths.
- **Not by default** — AI review can be noisy and is slower; running it on every change drowns the rule-based signal.

---

## Composition with `/dev-cycle`

`/dev-cycle` invokes `security-review-plan` at step 4 (after `write-plan`) and `security-review-code` at step 6 via `quality-review` Gate 5. The `--ai` flag is not passed by default — invoke `/security-review code --ai` manually for high-risk PRs.

---

## Output

Both modes emit findings as `[A0X-SEVERITY] path:line — description`. End-of-run summary includes counts per OWASP category.

CRITICAL issues block merging. MEDIUM and LOW are presented to the developer who decides.
