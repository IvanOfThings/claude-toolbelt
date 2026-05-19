# Code Quality Checklist

Run this checklist on every code change before merging. Used by the `quality-review` skill.

## Architecture

- [ ] No direct database calls in HTTP handlers — all DB access goes via service layer
- [ ] No raw `fetch('/api/...')` outside the API client layer
- [ ] API request/response shapes defined in a contracts layer and shared between client and server
- [ ] Business logic in services, not in routes or components
- [ ] No magic strings for domain enums — states, roles, types/kinds, error codes come from a single enum / `const as const` / generated schema type, never duplicated as string literals across files (see `rules/code-quality/code-quality.md`)
- [ ] Services with multi-step transactions follow the coordinator + atomic-action pattern (see `rules/code-quality/transaction-coordinator.md`) — no super-function combining validations, transaction wrapper, and all writes in one body
- [ ] No `process.env.X` accessed inline in business logic — env vars are read and validated once at startup in a single typed config module (`env.ts` / `config.ts`); only `NODE_ENV`, build-time tooling, and tests are allowed exceptions (see `rules/code-quality/env-config.md`)

## React / Next.js (skip if not applicable)

- [ ] No `fetch` calls directly in components — data flows through hooks
- [ ] No `'use client'` added without a concrete need (interactivity or browser API)
- [ ] `'use client'` boundary pushed as far down the component tree as possible
- [ ] Server-side async APIs awaited correctly (`await cookies()`, `await headers()`, `await params`)
- [ ] Mutations use `useMutation` + `invalidateQueries` on the narrowest applicable key
- [ ] No `window.location.reload()` or `router.refresh()` for client-triggered mutations
- [ ] Submit buttons disabled while pending to prevent double-submissions
- [ ] Optimistic updates with rollback for actions that feel instant (toggles, status changes)

## UI / Accessibility

- [ ] Mobile layout correct at 390px
- [ ] Design tokens used — no ad-hoc hex values or hardcoded spacing
- [ ] No "Loading..." / "Cargando..." text — skeleton components only
- [ ] No layout shift when data arrives — skeleton dimensions match real content

## Observability

- [ ] Every `catch` block with `console.error` also calls `errorTracker.captureException(err)` before it
- [ ] No fire-and-forget `.catch(console.error)` — must also capture the exception
- [ ] Non-OK responses from external APIs create and capture an error
- [ ] External service calls wrapped in a tracing span with correct `op` and descriptive name
- [ ] New spans include mandatory entity ID and outcome attributes (see `rules/observability/tracing-conventions.md`)

## i18n

- [ ] No hardcoded user-visible strings in source code
- [ ] Dates and numbers use `Intl` API or i18n library, not manual locale strings
- [ ] Plurals use library utilities, not inline ternaries

## Tests

- [ ] `<test runner> run` passes with no failures
- [ ] No TypeScript errors
- [ ] No regressions in existing tests
