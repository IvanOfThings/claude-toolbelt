# TDD Cycle

Every code change follows this cycle without exception:

```
1. Write a failing test that describes the desired behaviour
2. Run it — confirm it fails with the expected error
3. Write the minimum code to make the test pass
4. Run the test — confirm it passes
5. Refactor if needed, keeping tests green
6. Commit
```

## Rules

- **No implementation without a failing test first.** If you can't write a test that fails before the implementation, reconsider whether the test is meaningful.
- **Minimum code principle.** Write only enough code to make the failing test pass. Do not add behaviour not covered by a test.
- **One failing test at a time.** Do not write multiple failing tests before implementing. Fix the failing test before adding the next one.
- **Never skip the red step.** Running the test before implementing confirms the test is actually testing what you think it's testing.
- **Commit at green.** Each commit represents a working state. Never commit with failing tests.

## What counts as a test

- Unit tests for pure functions and service layer logic
- Integration tests for API routes (using test database or mocks at the correct boundary)
- Component tests for UI behaviour
- E2E tests for critical user flows

The appropriate test type depends on what is being changed. Prefer the fastest test that gives real confidence.
