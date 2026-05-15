# Test Conventions

Rules for **where test files live and how they are written**. These complement `process/tdd-cycle.md`, which governs *when* tests are written (red → green → refactor).

## File location: `__tests__/` sibling folder

Tests live in a `__tests__/` folder next to the production code they cover. One folder per module, never a top-level `tests/` tree mirroring `src/`.

```
src/services/user/
  user-service.ts
  user-repository.ts
  __tests__/
    user-service.test.ts
    user-repository.test.ts
```

## Naming

- **Suffix**: `*.test.ts` (or `*.test.tsx` for components). Never `*.spec.ts` — a single glob keeps the test runner config trivial.
- **One-to-one mapping**: one test file per production file, same base name. `user-service.ts` → `__tests__/user-service.test.ts`. Finding a module's tests is a mechanical operation, not a search.

## Fixtures and mocks live with the tests

Module-specific fixtures and mocks go inside the same `__tests__/` folder, not in a global `tests/` or `fixtures/` tree:

```
src/services/user/
  __tests__/
    user-service.test.ts
    __mocks__/
      auth-client.ts
    __fixtures__/
      sample-users.json
```

Shared fixtures used by more than one module are the exception — only then promote them to a higher-level `__fixtures__/`.

## Mock at the right boundary

- Mock **external dependencies**: HTTP clients, database drivers, the clock, the filesystem, third-party SDKs.
- **Do not mock internal collaborators** of the module under test. If you feel the need to mock another service in the same codebase, the test is likely written at the wrong layer — move it up to an integration test or refactor the seam.
- Aligns with `process/dev-prod-parity.md`: tests should exercise the same wiring production uses, mocking only what crosses the process boundary.

## Test names describe behaviour

Every test name reads as a specification of observable behaviour, not as a method label.

```ts
// ✅
it('returns 404 when the user does not exist', ...)
it('rejects with InvalidEmailError when the email is missing an @', ...)

// ❌
it('getUser test', ...)
it('works', ...)
```

If you cannot name the test in behavioural terms, the test probably isn't asserting behaviour — it's asserting implementation.

## No shared state between tests

- Every test must pass when run in isolation and in any order.
- Use `beforeEach` for setup; avoid `beforeAll` with mutable state.
- Reset module-level singletons, in-memory databases, mocked clocks, and spies between tests.
- A test that only passes after another test has run is a bug in the test, not a feature of the suite.
