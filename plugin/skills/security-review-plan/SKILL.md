# security-review-plan

Reviews an implementation plan for security issues before implementation begins.

## Input

`plan-path`: path to the plan file (e.g. `docs/superpowers/plans/2026-05-20-feature-name.md`)

## Steps

**1. Read checklist**

Read `rules/security/security-checklist.md`.

**2. Review the plan**

Read the plan file. For each task, evaluate:

**Authentication & Authorisation:**
- Does every new API route specify who can call it (role check, session check)?
- Could any proposed logic allow privilege escalation?
- Is tenant isolation maintained?

**Data Exposure:**
- Do proposed API responses return only needed fields?
- Any PII or sensitive fields in client-facing responses?

**Input Handling:**
- Is user input validated at the boundary with a schema validator?
- Any raw SQL or unparameterised queries proposed?

**Business Logic:**
- Financial or state operations protected against double-submit?
- State transitions validate current state?

**External Integrations:**
- Webhook signatures verified before processing?
- Secrets read from env vars, never hardcoded?

**3. Output**

```
[security-review-plan] PASS

or

[security-review-plan] ISSUES FOUND

  [CRITICAL] Task 3 — Add admin route
  No auth check specified for POST /api/admin/reset
  → Add session check + role === 'ADMIN' guard before any DB write

  [MEDIUM] Task 5 — User export
  Proposed response includes full user object
  → Select only id, name, email fields
```

CRITICAL issues block the plan gate — the developer must resolve them before implementation begins. MEDIUM and LOW are presented for developer decision.
