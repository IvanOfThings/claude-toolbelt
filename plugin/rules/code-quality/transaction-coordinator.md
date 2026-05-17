# Transaction Coordinator Pattern

When a service operation spans **two or more database writes that must succeed or fail together**, split the implementation into atomic actions + a coordinator. Never bundle validations, the transaction wrapper, and all writes into one super-function.

This rule applies inside the service layer (see `rules/code-quality/code-quality.md` → "Service-first data access"). It does not change layering — handlers still call services, services still own business logic. It changes the **internal shape** of a transactional service.

## The pattern

### 1. Atomic actions

Each atomic action performs **exactly one CRUD operation**. It accepts the database client as a parameter so it works inside or outside a transaction.

- Signature: `async function <verb><Entity>(db: DbClient, args): Promise<...>`
- **No business validations** — those belong in the coordinator.
- **No tracing span** — the ORM's instrumentation already emits a query-level span, and the coordinator owns the operation-level span.
- **Private by default** — keep them un-exported until a second coordinator legitimately reuses them (YAGNI). Promote to exported when the second consumer arrives, not before.
- One file per coordinator is the default — atomic actions live alongside the coordinator they support. If a promoted atomic action is reused across files, extract it to a dedicated module.

### 2. Coordinator

The coordinator is the **public** function the handler calls. It:

1. Owns the operation-level tracing span (`Sentry.startSpan` or equivalent, following `rules/observability/tracing-conventions.md`).
2. Runs business validations **outside** the transaction — reads current state, throws typed domain errors, fails fast before any write.
3. Opens the transaction (`$transaction` / `transaction` / `db.transaction(async tx => ...)`).
4. Calls the atomic actions inside the transaction, passing `tx` as the `db` parameter.
5. Returns the result shape the handler maps to a response.

### 3. The `DbClient` type alias

Declare a shared alias so atomic actions accept both the regular client and the transaction client:

```ts
// @/lib/db
import { PrismaClient, Prisma } from "@prisma/client";
export type DbClient = PrismaClient | Prisma.TransactionClient;
```

Cross-ORM equivalents:

| ORM      | Atomic action parameter type                                          |
|----------|------------------------------------------------------------------------|
| Prisma   | `PrismaClient \| Prisma.TransactionClient`                            |
| Drizzle  | `NodePgDatabase<typeof schema> \| PgTransaction<...>` (or generic `Database` type) |
| Kysely   | `Kysely<DB> \| Transaction<DB>`                                        |
| TypeORM  | `EntityManager` (the same type works in both contexts)                 |
| Raw SQL  | A small interface `{ query(text, params): Promise<...> }` that both the pool and a `PoolClient` satisfy |

The principle is the same regardless of ORM: **one parameter type that accepts both clients**.

## Example (Prisma)

```ts
// services/admin/invitation-acceptance-service.ts
import { Sentry } from "@/lib/observability";
import { prisma, type DbClient } from "@/lib/db";
import { InvitationAcceptanceError } from "./errors";

// ── Atomic actions (private; one CRUD op each; no validations; no span)

async function setUserRoleToAdmin(db: DbClient, userId: string) {
  return db.user.update({ where: { id: userId }, data: { role: "ADMIN" } });
}

async function markInvitationUsed(db: DbClient, invitationId: string) {
  return db.adminInvitation.update({
    where: { id: invitationId },
    data: { usedAt: new Date() },
  });
}

async function recordPermissionChange(db: DbClient, args: {
  userId: string;
  invitationId: string;
}) {
  return db.auditLog.create({
    data: { kind: "ADMIN_GRANTED", userId: args.userId, refId: args.invitationId },
  });
}

// ── Coordinator (public; owns span + validations + transaction)

export async function acceptAdminInvitation(args: {
  token: string;
  userId: string;
}): Promise<{ ok: true }> {
  return Sentry.startSpan(
    { name: "accept admin invitation", op: "function" },
    async () => {
      // 1. Validations — outside the transaction
      const inv = await prisma.adminInvitation.findUnique({
        where: { token: args.token },
      });
      if (!inv) throw new InvitationAcceptanceError("NOT_FOUND");
      if (inv.usedAt) throw new InvitationAcceptanceError("ALREADY_USED");
      if (inv.expiresAt < new Date()) throw new InvitationAcceptanceError("EXPIRED");

      // 2. Transaction — atomic actions only
      await prisma.$transaction(async (tx) => {
        await setUserRoleToAdmin(tx, args.userId);
        await markInvitationUsed(tx, inv.id);
        await recordPermissionChange(tx, {
          userId: args.userId,
          invitationId: inv.id,
        });
      });

      return { ok: true };
    },
  );
}
```

## What this gives you

- **Testability per step.** Each atomic action is testable in isolation against the regular client; the coordinator gets a focused test that verifies validations + ordering + that `$transaction` was used.
- **Reuse without duplication.** When a second flow needs "mark invitation used" (e.g. `revokeAdminInvitation`, a cleanup cron), promote the atomic action to exported instead of copy-pasting.
- **Clean span hierarchy.** One operation-level span + N ORM-emitted query spans inside it. No double-instrumentation.
- **Lower cognitive load.** The coordinator reads as a 5-line orchestration; details of each write live in their named function.

## Anti-patterns

| Anti-pattern                                                                | Why                                                                 |
|-----------------------------------------------------------------------------|---------------------------------------------------------------------|
| Super-function: validations + `$transaction(async tx => { ...50 lines... })` in one body | Cannot test steps in isolation; cannot reorder; cannot reuse.       |
| Atomic action that **performs its own validation** (read + throw)            | Belongs in the coordinator; otherwise validations run inside the transaction and lock rows unnecessarily. |
| Atomic action that **opens its own transaction**                             | Defeats the point — the coordinator can no longer wrap multiple actions atomically. |
| Atomic action that **emits its own tracing span**                            | Double instrumentation; the coordinator's span already covers it.   |
| Atomic action **exported from day one** "in case someone needs it later"    | YAGNI. Export only when the second consumer is real.                |
| Coordinator runs validations **inside** `$transaction`                       | Holds row locks while reading + throwing; latency and lock contention. |
| Handler opening a transaction                                                | Transactions are a service-layer concern. Handlers do auth + parse + service call + serialise. |

## Trade-offs (honest)

- **Lines of code grow.** A 3-write transaction goes from ~15 lines (super-function) to ~40 lines (3 atomic actions + coordinator). For one-shot operations this is overhead; it pays off the moment a step needs reuse or independent testing.
- **Risk of misuse:** an exported atomic action can be called outside any transaction. Mitigation: a docstring `// must be called inside a transaction with peer actions` on every exported atomic action, plus a rule of thumb that **exporting an atomic action requires a coordinator review**.
- **When to skip this pattern:** a service operation that performs **one** write (no atomicity requirement) does not need a coordinator. Write it as a normal service function and move on.

## Checklist for reviewing a transactional service

- [ ] Multiple writes are inside a single `$transaction` (or ORM equivalent) — no implicit auto-commit between steps
- [ ] Validations run **before** the transaction is opened
- [ ] No atomic action contains an `if (notFound) throw` or other business validation
- [ ] No atomic action opens its own transaction
- [ ] No atomic action emits its own tracing span
- [ ] The coordinator's tracing span name follows `rules/observability/tracing-conventions.md`
- [ ] Atomic actions are private to the file unless a real second consumer requires export
- [ ] The transaction wrapper lives in the service, not the handler
