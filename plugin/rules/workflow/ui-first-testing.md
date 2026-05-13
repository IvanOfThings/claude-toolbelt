# UI-First Testing

Verification tests describe user actions, not API calls. This rule applies to the functional verification document.

## The rule

**For every behaviour to verify: identify which UI page triggers it, then write the test steps as user actions.**

```
✅ Correct (UI-first):
  1. Sign in as `player`
  2. Navigate to /teams/my-team/polls
  3. DevTools → Network → filter by `polls/`
  4. Verify GET /api/teams/{id}/polls fires
  5. Confirm the response contains `status: "OPEN"`
  6. Confirm the "Open poll" badge appears on the card

❌ Wrong (API-first):
  1. Call GET /api/teams/{id}/polls
  2. Verify the response contains status: "OPEN"
```

## When a direct API call IS allowed

- The endpoint has no UI that triggers it (admin/cron endpoints, webhooks)
- The test covers an error case the UI deliberately prevents (e.g. submitting invalid payload, 409 conflict)
- Verifying internal state (database values, cache contents)

In those cases: document the exact `curl` or `fetch()` call. If a UI equivalent exists, include it as the primary path and the API call as a secondary verification.

## What makes a good test step

- The role used to sign in (`admin`, `player`, `manager`)
- The exact URL to navigate to
- The specific element to interact with
- The exact observable outcome (text visible, badge present, network request shape, redirect URL)

## What makes a bad test step

- Only verifies no error occurred, without describing what the user sees
- So generic it would pass even if a related feature broke
- Describes implementation details ("the service calls updateMany") rather than observable behaviour
