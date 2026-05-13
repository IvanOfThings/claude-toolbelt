# Error Observability

Every exception must be captured by the project's error tracker. Silent failures are forbidden.

## Error capture rules

- **Every `catch` block** that calls `console.error(err)` must also call `errorTracker.captureException(err)` **before** the console call.
- **No fire-and-forget `.catch(console.error)`** — replace with `.catch((err) => { errorTracker.captureException(err); console.error('[context]', err); })`.
- **Non-OK responses from external APIs** (HTTP 4xx/5xx from Telegram, email providers, webhooks) must create and capture an error: `errorTracker.captureException(new Error('[service] failed (${status}): ${body}'))`.
- **Never swallow errors silently** — if it's worth logging, it's worth capturing.

## External service call tracing

Wrap calls to external services in a tracing span to measure their duration as child spans. See `rules/observability/tracing-conventions.md` for span naming and attribute requirements.

```ts
// Example pattern (adapt to your tracing library)
await tracer.startSpan(
  { name: "email: send welcome message", op: "http.client" },
  async (span) => {
    span.setAttribute("email.recipient_id", userId);
    const res = await emailService.sendWelcome(userId);
    if (!res.ok) {
      errorTracker.captureException(new Error(`email failed (${res.status})`));
    }
  }
);
```

## Automatic instrumentation

Do not manually wrap operations that are already auto-instrumented by your ORM, framework, or cache library. Check your instrumentation setup before adding spans to avoid duplication.

## Scope for this rule

This rule covers error capture. For span naming and attribute conventions, see `rules/observability/tracing-conventions.md`. For post-response async work, see `rules/observability/background-tasks.md`.
