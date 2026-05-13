# Database Access Patterns

## Singleton client

Use a single shared database client instance across the application. Never instantiate the client multiple times. Export one instance from a dedicated module (e.g. `src/lib/db.ts`) and import it everywhere.

Rationale: prevents connection pool exhaustion on serverless environments and ensures consistent connection lifecycle management.

## Parallel queries

When a handler or service needs multiple independent queries, run them in parallel. Never chain `await` calls that are not dependent on each other:

```ts
// ✅ Correct — parallel
const [user, team] = await Promise.all([
  db.user.findUnique({ where: { id } }),
  db.team.findMany({ where: { memberId: id } }),
]);

// ❌ Wrong — sequential, wastes time
const user = await db.user.findUnique({ where: { id } });
const team = await db.team.findMany({ where: { memberId: id } });
```

## Server-side only

All database queries run in server-side code: API handlers, server components, server actions, background jobs. Never import the database client from client-side code. Never expose raw database objects or sensitive fields to the client — shape the response to include only what the caller needs.

## Migrations before deployment

Run schema migrations manually before deploying code that depends on them. Never deploy code expecting a schema change that hasn't been applied yet.
