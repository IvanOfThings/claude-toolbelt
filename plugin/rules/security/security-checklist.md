# Security Review Checklist

Use this checklist when reviewing a plan (pre-implementation) or code (post-implementation).

## Authentication & Authorisation

- [ ] Every new API route specifies who can call it (role check, session check)
- [ ] No route skips auth middleware without explicit documented justification
- [ ] Privilege escalation is impossible through the proposed logic (e.g. a regular user cannot grant themselves admin)
- [ ] Tenant isolation: no query returns data across tenants unless the actor has explicit cross-tenant permission

## Data Exposure

- [ ] API responses return only the fields the caller needs — no full model dumps
- [ ] No PII or sensitive fields (passwords, tokens, internal IDs) exposed in client-facing responses
- [ ] Pagination or limits on list endpoints to prevent data enumeration

## Input Handling

- [ ] All user-supplied inputs are validated with a schema validator (Zod, Joi, etc.) before touching the database
- [ ] No raw SQL or unparameterised query calls
- [ ] File upload endpoints validate type and size before processing

## Business Logic

- [ ] Financial operations are protected against double-submit and replay
- [ ] State transitions validate current state before allowing the transition
- [ ] Soft-delete or archive operations cannot be triggered by unauthorised actors

## External Integrations

- [ ] Webhook endpoints verify the source signature before processing
- [ ] Secrets and tokens are read from environment variables, never hardcoded

## Runtime (code review only)

- [ ] No `console.log` printing sensitive data (tokens, passwords, full user objects)
- [ ] Error responses do not leak stack traces or internal details to the client
- [ ] Rate limiting exists on auth-adjacent endpoints
- [ ] Cron/scheduled job endpoints verify a shared secret before executing

## Severity classification

- **CRITICAL**: allows unauthorised access, data leakage, or integrity violation
- **MEDIUM**: increases attack surface or weakens a security control
- **LOW**: informational, defence-in-depth improvement

**CRITICAL issues block the PR.** MEDIUM and LOW are presented to the developer who decides.
