# Background Tasks (Post-Response Async Work)

Any async operation launched inside a request handler that must complete **after** the HTTP response is returned must be wrapped with the platform's lifecycle extension mechanism.

## Why this matters

Without lifecycle extension, two things break silently:
1. The runtime may recycle the serverless function before the Promise resolves — notifications, emails, and background updates are lost with no error.
2. Tracing child spans (DB queries, external calls) appear in your observability tool *after* the parent span has already closed, making trace analysis impossible.

## Pattern

```ts
// Vercel: use waitUntil from @vercel/functions
import { waitUntil } from "@vercel/functions";

waitUntil(
  someAsyncFn(args).catch((err) => {
    errorTracker.captureException(err);
    console.error("[context] someAsyncFn failed:", err);
  })
);
return response; // return immediately

// Cloudflare Workers: use ctx.waitUntil(promise)
// Node.js long-running process: ensure the process stays alive until the work completes
```

## Rules

- **Never use bare `.catch(...)` fire-and-forget before returning a response** — always wrap with the lifecycle extension mechanism.
- The `.catch` handler must still call `errorTracker.captureException` (see `rules/observability/error-observability.md`).
- When there are multiple independent background operations, call the lifecycle extension separately for each — do not combine into `Promise.all` unless they are logically a single atomic unit.

## Testing

Mock the lifecycle extension in tests so the Promise executes immediately:
```ts
vi.mock("@vercel/functions", () => ({ waitUntil: vi.fn((p) => p) }));
```
