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

## Service-first data access

Every database query introduced in an HTTP handler must go through a service layer function. There is no inline-complexity threshold, no "small one-off query" exception.

Workflow when adding a handler that needs data:
1. Find the service that owns the relevant entity
2. If the service has the method, use it
3. If the service exists but lacks the method, extend it
4. Only create a new service file if no service owns the entity yet

Business logic (state validation, error codes, transactions, cache invalidation) belongs in the service. Handlers do: auth check → input parsing → service call → error mapping → response serialisation. Handlers do not re-implement business rules.

Services live flat at the service layer root, named `<domain>-service.ts`. Do not create subfolders for services — the file is already the domain boundary. Other layers (hooks, api-client, api-contracts) use domain subfolders when 2+ files share the same domain; see `architecture-layers.md`.
