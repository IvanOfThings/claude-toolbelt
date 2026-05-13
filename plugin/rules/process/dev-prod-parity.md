# Dev/Production Parity

**The code that runs locally must be identical to the code that runs in production.**

No conditional code paths based on `NODE_ENV` that use different libraries, drivers, or systems between environments. If such a branch exists, local tests don't cover production code and any bug in the production branch reaches deployment undetected.

## Rules

- **Single execution path** for database access, authentication, cache, and external services in both local and production. Environment variables change values (connection URLs, credentials), never the implementation.
- **If something doesn't work the same locally and in production, it's an architecture bug**, not an acceptable special case.
- **Tests must exercise exactly the same code that reaches production.** If production uses a different driver or adapter than local, tests provide no guarantee.
- **Forbidden**: `if (process.env.NODE_ENV === 'production') { require('other-library') }` to switch systems between environments. If different behaviour is needed, control it exclusively with environment variables that configure the same system.

## Accepted exceptions

- Configuration values: URLs, API keys, timeouts
- Log level: verbose locally, errors-only in production
- Auth mocking in local development (`MOCK_AUTH=true`)

Never the system implementation itself.
