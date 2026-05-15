# Code Quality Rules

These rules apply to all implementation work regardless of language or framework.

## DRY — Don't Repeat Yourself

Before creating a new component, hook, utility function, or helper, check if a similar one already exists. Reuse or extend it. If the same logic appears in two places, extract it into a shared unit.

## Search before implementing

Before writing formatting logic, date handling, URL construction, list rendering, or any utility, grep the relevant library files for existing helpers. If an existing helper covers 80%+ of the need, use or extend it rather than duplicating inline.

## Refactor on discovery

If during implementation you find inline logic that matches an existing helper, refactor that callsite to use the helper — even if it's not the primary task. Keep the helper as the single source of truth.

## No over-engineering

Do not add abstractions for hypothetical future needs. Build exactly what the current task requires. Three similar lines is better than a premature abstraction.

## Lean files

A file that grows beyond ~200 lines is a signal to extract components or helpers. Each file should have one clear responsibility. If you can't describe what a file does in one sentence, it does too much.

## Consistent patterns

Follow the patterns already established in the codebase. Before introducing a new pattern, verify no equivalent pattern already exists.

## No magic strings for domain enums

Every finite set of values that crosses more than one file must come from a **single source**: a TypeScript `enum`, a `const` object with `as const` + a union type, or a type generated from the database schema (Prisma, Drizzle, Kysely, etc.). The string literal is declared once; every comparison, assignment, and persisted value references the source.

Applies to:
- **Status / state** values (`'active'`, `'pending'`, `'archived'`)
- **Role / permission** values (`'admin'`, `'editor'`, `'viewer'`)
- **Type / kind / category** discriminators
- **Domain error codes** (`'INSUFFICIENT_FUNDS'`, `'NOT_AUTHORISED'`)
- **HTTP-relevant constants** that the app interprets in logic (custom header names, well-known query parameters)

Examples — wrong vs right:

```ts
// ❌ magic string repeated across files
if (poll.status === 'open') { ... }                 // src/components/poll-card.tsx
return polls.filter(p => p.status !== 'archived')   // src/services/poll.ts
await prisma.poll.update({ data: { status: 'closed' } })  // src/services/poll.ts

// ✅ single source — generated type from schema
import { PollStatus } from '@/db/types'             // or local enum, or const + as const
if (poll.status === PollStatus.Open) { ... }
return polls.filter(p => p.status !== PollStatus.Archived)
await prisma.poll.update({ data: { status: PollStatus.Closed } })
```

**Refactor trigger:** if the same literal appears 3+ times across different files in a comparison, `switch case`, or assignment, an enum is waiting to be extracted. The third occurrence is when you extract — not the tenth.

**Exceptions** — magic strings are acceptable when:
- The literal is used in **a single file**, in **a single place**, and is not a state the system reasons about (e.g. a debug log label, a one-off test fixture).
- The value belongs to an **external API** the project does not own and is never interpreted in business logic (e.g. an upstream provider's status code passed straight through).
- The string **is the data** introduced by a user or external system (a tag, a label, a free-form category) — not a state the application defines.

When in doubt, extract. Three similar literals is the canonical signal.

## Service-first data access

Every database query introduced in an HTTP handler must go through a service layer function. There is no inline-complexity threshold, no "small one-off query" exception.

Workflow when adding a handler that needs data:
1. Find the service that owns the relevant entity
2. If the service has the method, use it
3. If the service exists but lacks the method, extend it
4. Only create a new service file if no service owns the entity yet

Business logic (state validation, error codes, transactions, cache invalidation) belongs in the service. Handlers do: auth check → input parsing → service call → error mapping → response serialisation. Handlers do not re-implement business rules.

All layers — including services — use domain subfolders when 2+ files share the same domain. See `architecture-layers.md` for the full rule.
