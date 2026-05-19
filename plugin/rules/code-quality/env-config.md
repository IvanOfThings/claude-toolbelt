# Environment Configuration

Environment variables are **read and validated once at startup** in a single typed config module, never inline at the call-site. The rest of the codebase imports a typed `config` (or `env`) object; no business logic ever touches `process.env` directly.

## Why this matters

Three problems with inline `process.env.X` reads:

1. **Failure is delayed.** A missing or malformed `AUTH_SECRET` doesn't surface until a user hits the route that uses it. With validation at boot, the server refuses to start with a clear error — the failure mode is loud, immediate, and never reaches production.
2. **No typing.** In TypeScript, `process.env.X` is `string | undefined`, always. Every call-site has to cast or assert. A validated config module exposes a typed `string`, `number`, or `URL` directly.
3. **The list of required vars is scattered.** A new contributor cannot answer "what env vars does this project need?" without grepping the whole tree. The config module is the single source of truth — operational setup and onboarding read one file.

A fourth, security-relevant: secrets leaked into logs, error messages, or traces are easier to redact when they have a single read-site — the config module — instead of being interspersed across handlers. Aligns with `rules/security/security-checklist.md` A02 and A09.

## The rule

> All application code reads configuration through a single typed module (`env.ts` / `config.ts`). That module is the **only** file in the project that calls `process.env.<NAME>` for application-defined variables. It validates every variable with a schema (Zod, valibot, or equivalent), throws on missing or malformed values at module load, and exports a typed object. Tests and the framework's own internals are the only exceptions — see below.

## Pattern — `env.ts` (Zod example)

```ts
// src/env.ts
import { z } from "zod";

const schema = z.object({
  // Required secrets
  AUTH_SECRET: z.string().min(32, "AUTH_SECRET must be at least 32 chars"),
  DATABASE_URL: z.string().url(),

  // Required public vars
  NEXT_PUBLIC_APP_URL: z.string().url(),

  // Optional with defaults
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
  PORT: z.coerce.number().int().positive().default(3000),
});

const parsed = schema.safeParse(process.env);

if (!parsed.success) {
  console.error("❌ Invalid environment variables:");
  console.error(parsed.error.flatten().fieldErrors);
  throw new Error("Environment validation failed — refusing to start");
}

export const env = parsed.data;
```

Then everywhere else:

```ts
// src/services/auth.ts
import { env } from "@/env";

export async function verifyToken(token: string) {
  return jwt.verify(token, env.AUTH_SECRET);  // typed: string, guaranteed at boot
}
```

## Per-framework recommended tooling

| Framework        | Recommended approach                                                                  |
|------------------|---------------------------------------------------------------------------------------|
| **Next.js**      | `@t3-oss/env-nextjs` — Zod-based, enforces `NEXT_PUBLIC_*` client/server separation, fails fast at module load. De-facto standard in the Next.js community. |
| **SvelteKit**    | Built-in `$env/static/private` and `$env/static/public`; layer a Zod schema on top in a `config.ts` for runtime validation of optional vars. |
| **Astro**        | `astro:env` (experimental) or a manual `env.ts` with Zod.                            |
| **Node (generic)** | Manual `env.ts` with Zod or valibot — same shape as the example above.             |
| **Python**       | `pydantic-settings` — equivalent ergonomics: schema validation, typed exports, fails fast at import. |

The principle is universal across stacks. Pick the lowest-friction validator that gives you fail-fast and typed exports.

## Client/server separation (Next.js + similar)

Server-only secrets must **never** be importable from a client bundle. The recommended Next.js pattern (`@t3-oss/env-nextjs`):

```ts
// src/env.ts
import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  server: {
    AUTH_SECRET: z.string().min(32),
    DATABASE_URL: z.string().url(),
  },
  client: {
    NEXT_PUBLIC_APP_URL: z.string().url(),
  },
  runtimeEnv: {
    AUTH_SECRET: process.env.AUTH_SECRET,
    DATABASE_URL: process.env.DATABASE_URL,
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
  },
});
```

Importing a server-only key from a `"use client"` file becomes a compile-time error.

## Allowed exceptions

`process.env.X` access outside the config module is allowed only in these cases:

1. **`NODE_ENV`** — bundlers (Webpack, Turbopack, Vite, esbuild) inline this value at build time; it is not a runtime env read. Use it in module-init code (`const isDev = process.env.NODE_ENV !== "production"`) without going through the config module.
2. **Build-time tooling** — `next.config.js`, `vite.config.ts`, codegen scripts. These run outside the application runtime; the config module may not be importable.
3. **Tests** — `vi.stubEnv("KEY", "value")` (Vitest) or `process.env.KEY = "value"` followed by an explicit reset in `afterEach`. Tests are intentionally outside the validated startup path.

Every other `process.env.X` in the application is a violation.

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                                  |
|-----------------------------------------------------------------------|--------------------------------------------------------------------------------|
| `const secret = process.env.AUTH_SECRET;` inside a handler            | Delayed failure; untyped (`string \| undefined`); duplicates the env read.    |
| `process.env.STRIPE_KEY ?? "sk_test_..."` as default                  | Silent fallback to a placeholder; the failure becomes a wrong-environment bug instead of a startup error. |
| `if (!process.env.X) throw ...` repeated in N files                   | The validation logic is the config module's job, not every consumer's.        |
| Reading a server secret in a client component (Next.js)                | Either it's `undefined` in the bundle, or it leaks the secret into the client. Use the `@t3-oss/env-nextjs` client/server split. |
| `new PrismaClient({ log: process.env.NODE_ENV === "development" ? [...] : [...] })` inline | Tolerable (bundler-inlined `NODE_ENV`) but the cleaner version is `config.databaseLog` from the config module — keeps the Prisma init free of env reads. |
| Test sets `process.env.X` without resetting                            | Bleeds into other tests; flakiness depends on test order.                     |

## Checklist for reviewing env usage

- [ ] Every `process.env.X` access outside `env.ts` / `config.ts` is justified by one of the three allowed exceptions
- [ ] Required secrets are declared in the schema with a sensible minimum constraint (`.min(32)`, `.url()`, etc.) — not just `.string()`
- [ ] The config module fails at module load with a readable error listing every malformed var, not the first one only
- [ ] Server-only secrets are not importable from client bundles (when the framework supports the split)
- [ ] No silent `?? "default"` fallbacks for secrets — defaults are acceptable only for non-sensitive, optional configuration
- [ ] Tests that override env vars do so via `vi.stubEnv` / equivalent with a reset in `afterEach`
