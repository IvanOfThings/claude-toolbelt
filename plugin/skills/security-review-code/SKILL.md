# security-review-code

Reviews code changes (`git diff main`) for security issues after implementation. Combines three sources of findings:

1. **Checklist review** — applies every item in `rules/security/security-checklist.md` against the diff (OWASP Top 10 + CSRF + XSS).
2. **Dependency audit** — runs `npm audit` / `pnpm audit` / `yarn audit` to surface known CVEs (A06).
3. **Secret scan** — scans the diff for committed secrets (A02).

Every finding is reported with an OWASP ID prefix (e.g. `[A01-CRITICAL]`).

## Input

`ai`: optional boolean flag. When `true`, after producing the checklist/audit/secret-scan output, also invoke the built-in `superpowers:security-review` skill on the same branch and append its findings as a complementary AI-driven review.

## Steps

**1. Read checklist**

Read `rules/security/security-checklist.md`.

**2. Get the diff**

Run `git diff main` to get all code changes since branching from main. Also run `git diff main --name-only` to know which files changed.

**3. Apply checklist (categories A01–A10 + CSRF + XSS + Data Exposure + Runtime)**

For each category in the checklist, scan the diff for violations. Map every finding to its OWASP ID and severity:

| Category                                              | Prefix          |
|-------------------------------------------------------|-----------------|
| Broken Access Control                                 | `[A01-...]`     |
| Cryptographic Failures                                | `[A02-...]`     |
| Injection                                             | `[A03-...]`     |
| Insecure Design                                       | `[A04-...]`     |
| Security Misconfiguration                             | `[A05-...]`     |
| Vulnerable Components                                 | `[A06-...]`     |
| Authentication Failures                               | `[A07-...]`     |
| Integrity Failures                                    | `[A08-...]`     |
| Logging & Monitoring                                  | `[A09-...]`     |
| SSRF                                                  | `[A10-...]`     |
| CSRF                                                  | `[CSRF-...]`    |
| XSS                                                   | `[XSS-...]`     |
| Data Exposure (cross-cutting)                         | `[DATA-...]`    |
| Runtime                                               | `[RUNTIME-...]` |

**4. Dependency audit (A06)**

Detect the package manager from the lockfile in the repo root:

| Lockfile found       | Command to run                                  |
|----------------------|--------------------------------------------------|
| `pnpm-lock.yaml`     | `pnpm audit --prod --audit-level high --json`    |
| `yarn.lock`          | `yarn npm audit --severity high --json` (Yarn 3+) / `yarn audit --level high --json` (Yarn 1) |
| `bun.lockb`          | `bun audit --json` (if available; otherwise skip with note) |
| `package-lock.json`  | `npm audit --omit=dev --audit-level=high --json` |
| none                 | skip; report `[A06-INFO] no lockfile detected — dependency audit skipped` |

Parse the JSON output. For each advisory with severity `high` or `critical`, emit:

```
[A06-CRITICAL] <package>@<version> — <advisory title>
  CVE: <id>, fixed in <version>
  Path: <dependency path from output>
```

`high` maps to `[A06-MEDIUM]` for the purposes of our gating: dependency vulnerabilities rarely block a PR (the fix may not exist yet), but `critical` blocks. The developer can override.

**5. Secret scan (A02)**

Scan the diff for committed secrets. Strategy:

1. If `gitleaks` is on PATH: run `gitleaks protect --staged --no-banner --redact -v` (or against the diff with `--source` if not staged). Parse output.
2. Else if `trufflehog` is on PATH: run `trufflehog git --since-commit main --no-update --json file://.`. Parse output.
3. Else fall back to regex grep against `git diff main`:

| Pattern (case-insensitive)                                       | Example match                          |
|------------------------------------------------------------------|----------------------------------------|
| `(api[_-]?key\|secret[_-]?key\|access[_-]?token)\s*[:=]\s*["']\S+["']` | `apiKey: "sk_live_..."`                |
| `-----BEGIN (RSA \|EC \|DSA \|OPENSSH \|)PRIVATE KEY-----`       | Private key blocks                     |
| `AKIA[0-9A-Z]{16}`                                               | AWS access key ID                      |
| `aws_secret_access_key\s*=\s*\S+`                                | AWS secret                             |
| `xox[abprs]-[0-9a-zA-Z-]{10,48}`                                 | Slack tokens                           |
| `gh[ps]_[A-Za-z0-9]{36,255}`                                     | GitHub PATs                            |
| `sk-[a-zA-Z0-9]{32,}`                                            | Generic API key format (OpenAI, etc.)  |

For each match, emit:

```
[A02-CRITICAL] <file>:<line> — possible committed secret (<pattern name>)
  → Rotate the credential immediately and remove from history before merging
```

Always treat secret findings as CRITICAL — even a regex false positive is worth confirming.

**6. Optional — AI complementary review**

If `ai: true` was passed: invoke the built-in `superpowers:security-review` skill on the current branch. Append its findings to the output under a heading `[security-review-code] AI complementary review`. AI findings are advisory; they do not change severity classification of the rule-based findings above.

**7. Output**

```
[security-review-code] PASS

or

[security-review-code] ISSUES FOUND

  [A01-CRITICAL] src/app/api/teams/[id]/members/route.ts:23
  Missing auth check — any authenticated user can add members to any team
  → Add: if (session.user.teamId !== params.id) return NextResponse.json({}, { status: 403 })

  [A03-CRITICAL] src/services/search.ts:14
  Raw SQL concatenation with user input — SQL injection risk
  → Use parameterised query or ORM filter

  [A06-CRITICAL] axios@0.21.0 — Server-Side Request Forgery
  CVE-2024-39338, fixed in 1.7.4
  Path: > axios > follow-redirects

  [A02-CRITICAL] config/staging.env:7
  Possible committed secret (AWS access key ID)
  → Rotate the credential immediately and remove from history before merging

  [DATA-MEDIUM] src/services/team.ts:89
  Response includes full Prisma object — exposes internal fields
  → Select: { id, name, role } only
```

End with a count summary:

```
[security-review-code] FAIL — 2 CRITICAL, 1 MEDIUM (A01: 1, A03: 1, DATA: 1)
```

CRITICAL issues block merging. MEDIUM and LOW are presented to the developer who decides.

This skill does not commit or fix anything — it reports. The developer addresses findings, then re-runs `/security-review code`.
