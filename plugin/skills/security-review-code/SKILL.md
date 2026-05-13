# security-review-code

Reviews code changes (git diff main) for security issues after implementation.

## Steps

**1. Read checklist**

Read `rules/security/security-checklist.md`.

**2. Get the diff**

Run `git diff main` to get all code changes since branching from main.

**3. Review the diff**

Apply every checklist item to the changed code:

**Authentication & Authorisation:** every new route has auth check, no privilege escalation through proposed logic, tenant isolation maintained.

**Data Exposure:** responses shaped to minimal fields, no PII, list endpoints have pagination or limits.

**Input Handling:** user inputs validated with schema validator (Zod, Joi, etc.), no raw SQL.

**Business Logic:** financial operations protected against double-submit, state transitions guarded.

**External Integrations:** webhook signatures verified, no hardcoded secrets.

**Runtime:**
- No `console.log` printing sensitive data (tokens, passwords, full user objects)
- Error responses don't leak stack traces or internal details
- Rate limiting present on auth-adjacent endpoints
- Cron endpoints verify shared secret before executing

**4. Output**

```
[security-review-code] PASS

or

[security-review-code] ISSUES FOUND

  [CRITICAL] src/app/api/teams/[id]/members/route.ts:23
  Missing auth check — any authenticated user can add members to any team
  → Add: if (session.user.teamId !== params.id) return NextResponse.json({}, { status: 403 })

  [MEDIUM] src/services/team.ts:89
  Response includes full Prisma object — exposes internal fields
  → Select: { id, name, role } only
```

CRITICAL issues block merging. MEDIUM and LOW are presented to the developer.
