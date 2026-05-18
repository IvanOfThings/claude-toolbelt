# Security Review Checklist

Reviewed against the **OWASP Top 10 (2021)** plus CSRF and XSS as standalone categories. Use this checklist when reviewing a plan (pre-implementation) or code (post-implementation). Every finding is reported with its OWASP ID (e.g. `[A01-CRITICAL]`) so reviewers can map directly to OWASP terminology.

---

## A01 — Broken Access Control

- [ ] Every new API route specifies who can call it (role check, session check, ownership check)
- [ ] No route skips auth middleware without explicit documented justification
- [ ] Privilege escalation is impossible through the proposed logic (e.g. a regular user cannot grant themselves admin, cannot edit `role` in their own profile payload)
- [ ] Tenant isolation: no query returns data across tenants unless the actor has explicit cross-tenant permission
- [ ] Object-level authorisation: `GET /resources/:id` verifies the caller can see that specific resource — not just that they are authenticated (IDOR)
- [ ] State transitions validate current state **and** caller permission before allowing the transition
- [ ] Soft-delete or archive operations cannot be triggered by unauthorised actors
- [ ] Direct object references (`/users/123`) cannot be enumerated to access neighbouring records

## A02 — Cryptographic Failures

- [ ] Passwords are hashed with a modern KDF (`bcrypt`, `argon2`, `scrypt`) — never MD5/SHA-1/SHA-256
- [ ] Sensitive data at rest is encrypted (PII, tokens, secrets)
- [ ] TLS enforced end-to-end — no HTTP for authenticated endpoints
- [ ] Cookies storing session / auth tokens set `Secure`, `HttpOnly`, and `SameSite` (Strict or Lax — not None unless cross-site is required and CSRF mitigated separately)
- [ ] No deprecated ciphers, weak random number generators, or hardcoded IVs
- [ ] Secrets and tokens are read from environment variables, never hardcoded or committed
- [ ] Secrets are loaded from a **validated config module at boot** (see `rules/code-quality/env-config.md`), never via inline `process.env.X` lookups inside handlers or services — fail-fast at startup, not on first user request

## A03 — Injection

- [ ] All user-supplied inputs are validated with a schema validator (Zod, Joi, etc.) before touching the database
- [ ] No raw SQL or unparameterised query calls — ORM or parameterised statements only
- [ ] No dynamic-code-eval APIs or shell-executing APIs invoked with user input
- [ ] NoSQL queries built from objects, not concatenated strings
- [ ] Command-line invocations use argument-array APIs (e.g. `execFile`, `spawn`), never shell-form APIs with concatenated strings
- [ ] File path operations validate against directory traversal (`..`, absolute paths)

## A04 — Insecure Design

- [ ] Financial / mutating operations are protected against double-submit and replay (idempotency keys, nonces)
- [ ] Rate limiting exists on auth-adjacent endpoints (login, signup, password reset, OTP)
- [ ] Account lockout or progressive delays on repeated auth failures
- [ ] Sensitive workflows (password change, email change, payment) require re-authentication

## A05 — Security Misconfiguration

- [ ] CORS configured to a specific allowlist — no `Access-Control-Allow-Origin: *` on credentialed endpoints
- [ ] Security headers present: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options` (or CSP `frame-ancestors`), `X-Content-Type-Options: nosniff`, `Referrer-Policy`
- [ ] Debug endpoints, profiler routes, admin panels not exposed in production
- [ ] Default credentials changed / removed in all environments
- [ ] Error responses do not leak stack traces or internal details to the client
- [ ] Directory listing disabled; no source maps in production
- [ ] `NODE_ENV=production` (or equivalent) set; dev-only middleware not active in prod

## A06 — Vulnerable & Outdated Components

- [ ] `npm audit` / `pnpm audit` / `yarn audit` shows no HIGH or CRITICAL vulnerabilities (run automatically by `security-review-code`)
- [ ] Lockfile committed and matches `package.json`
- [ ] No use of deprecated packages with known security history without explicit justification
- [ ] Direct dependencies kept on supported major versions

## A07 — Identification & Authentication Failures

- [ ] Sessions have an expiration; long-lived tokens are refreshable, not eternal
- [ ] Session ID is rotated on privilege change (login, role escalation)
- [ ] Logout invalidates the server-side session, not just the client-side cookie
- [ ] Password reset flow uses single-use, time-limited tokens delivered to a verified channel
- [ ] MFA is offered for accounts with elevated privileges, where the product context allows it
- [ ] Login error messages do not disclose whether an account exists ("invalid credentials" — not "user not found")

## A08 — Software & Data Integrity Failures

- [ ] Webhook endpoints verify the source signature (HMAC, JWT, etc.) before processing the payload
- [ ] Third-party scripts loaded with Subresource Integrity (`integrity` attribute) and `crossorigin`
- [ ] GitHub Actions / CI pipelines pin third-party actions to a commit SHA, not a moving tag
- [ ] Auto-update mechanisms verify signatures of downloaded artefacts
- [ ] Deserialisation of untrusted data is avoided or uses a safe parser — never unsafe binary deserialisers (Python's binary object format, Java's `ObjectInputStream`, etc.)

## A09 — Security Logging & Monitoring Failures

- [ ] Security-relevant events are logged: login success/failure, MFA challenges, privilege changes, password reset, admin actions
- [ ] Logs do not contain sensitive data: passwords, full tokens, full credit card numbers (mask or omit)
- [ ] Errors in security paths (auth check failures, permission denials) capture an exception via `errorTracker.captureException` (see `rules/observability/error-observability.md`)
- [ ] Alerts exist on anomalous patterns: brute force, sudden permission grants, mass data export

## A10 — Server-Side Request Forgery (SSRF)

- [ ] Outbound HTTP calls do not accept arbitrary user-controlled URLs without an allowlist
- [ ] When user-controlled URLs are required: DNS resolution validated against private/loopback IP ranges (`127.0.0.0/8`, `10/8`, `172.16/12`, `192.168/16`, `169.254/16`, `::1`)
- [ ] Cloud metadata endpoints (`169.254.169.254`) blocked at the egress layer or in the HTTP client
- [ ] Redirects followed only within an allowlist of hosts

## CSRF

- [ ] State-changing endpoints (POST/PUT/PATCH/DELETE) protected against CSRF when using cookie-based auth — via `SameSite=Strict|Lax` cookies, anti-CSRF tokens, or custom-header check
- [ ] No state-changing operation accepts `GET` requests
- [ ] OAuth flows include `state` parameter to prevent CSRF on the callback

## XSS

- [ ] No raw-HTML injection APIs (React's unsafe-HTML escape-hatch prop, Vue's `v-html`, plain DOM `inner-HTML` assignment) with unsanitised user content; if required, content passes through a sanitiser (DOMPurify or equivalent)
- [ ] HTML rendering uses framework's default escaping; never bypassed for user data
- [ ] User-supplied URLs validated against `javascript:` / `data:` schemes before use in `href` / `src`
- [ ] `Content-Security-Policy` restricts inline scripts and external script sources (covered by A05; called out here because CSP is the primary XSS mitigation)

---

## Data Exposure (cross-cutting)

- [ ] API responses return only the fields the caller needs — no full model dumps
- [ ] No PII or sensitive fields (passwords, tokens, internal IDs) in client-facing responses
- [ ] Pagination or limits on list endpoints to prevent data enumeration
- [ ] File upload endpoints validate type and size before processing; uploaded files served with `Content-Disposition: attachment` or from a separate origin

## Runtime (code review only)

- [ ] No `console.log` printing sensitive data (tokens, passwords, full user objects)
- [ ] Cron / scheduled job endpoints verify a shared secret before executing

---

## Severity classification

- **CRITICAL**: allows unauthorised access, data leakage, integrity violation, or remote code execution
- **MEDIUM**: increases attack surface or weakens a security control
- **LOW**: informational, defence-in-depth improvement

**CRITICAL issues block the PR.** MEDIUM and LOW are presented to the developer who decides.

Findings are reported as `[A0X-SEVERITY] path:line — description`, e.g. `[A01-CRITICAL] src/api/teams/route.ts:23 — missing ownership check`.
