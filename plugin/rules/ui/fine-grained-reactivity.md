# Fine-Grained Reactivity

Every interaction must update only the minimum necessary UI — never trigger a full page reload or full navigation for a component-level action.

## Rules

- **Use your state management library's update mechanism** (e.g. React Query invalidation) after any mutation. Do not use `router.refresh()` for client-triggered data changes.
- **Optimistic updates by default** for any action the user expects to feel instant (toggles, status changes, form submissions). Implement rollback on error.
- **No `window.location.reload()`** — ever. If something seems to require a full reload, that is a design problem to fix.
- **No full-page navigation on form submit** — forms mutate via async function, update local cache, and stay on the current page unless the action explicitly requires navigating away.
- **Submit buttons disabled while pending** — every submit button and primary action button must be disabled during in-flight requests to prevent double-submissions. No exceptions.
- **Scope cache invalidations tightly** — invalidate the narrowest query key possible, not the entire cache. Prefer `['team', id, 'members']` over `['team']`.

## Optimistic update pattern

```ts
const prevState = currentData;
setData(applyOptimisticChange(currentData, ...args)); // instant UI update
const res = await submitChange(...);
if (res.ok) {
  refetchFromServer(); // rehydrate with authoritative data
} else {
  setData(prevState); // rollback on error
}
```

When a user action directly affects a displayed data section, immediately apply an optimistic local state update, fire the server request, and replace with the server response on success. Never wait for the round-trip before reflecting the user's own action.
