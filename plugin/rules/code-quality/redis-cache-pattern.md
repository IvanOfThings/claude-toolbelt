# Redis Read-Through Cache Pattern

Use this pattern whenever adding server-side caching. Do not deviate from it.

## The 9-step pattern

**1. Typed payload interface** — define what goes into the cache:
```ts
type FooCachePayload = { data: FooRow; relatedIds: string[] };
```

**2. Validator** — verify cache shape on read:
```ts
function parseFooCachePayload(raw: unknown): FooCachePayload {
  if (typeof raw !== "object" || raw === null) throw new Error("Not an object");
  const r = raw as Record<string, unknown>;
  if (typeof r.data !== "object" || r.data === null) throw new Error("Missing data");
  if (!Array.isArray(r.relatedIds)) throw new Error("Invalid relatedIds");
  return raw as FooCachePayload;
}
```
Never use `as FooCachePayload` directly on `JSON.parse` output.

**3. Builder** — construct the cache payload from DB results:
```ts
function buildFooCachePayload(data: FooRow, ids: Set<string>): FooCachePayload {
  return { data, relatedIds: [...ids] };
}
```

**4. Versioned cache key** — export from a central key module:
```ts
export const fooCacheKey = (id: string) => `foo:v1:${id}`;
```
Use a version prefix (`v1`, `v2`) to allow cache-bust on schema changes.

**5. Read path** — with fallback:
```ts
try {
  const cached = await cache.get(fooCacheKey(id));
  if (cached) {
    const payload = parseFooCachePayload(JSON.parse(cached));
    return payload; // cache hit
  }
} catch (err) {
  errorTracker.captureException(err);
  console.error("[foo/cache] Read failed, falling back to DB:", err);
  // fall through to DB
}
```

**6. Write path** — non-blocking:
```ts
try {
  await cache.set(fooCacheKey(id), JSON.stringify(buildFooCachePayload(data, ids)));
} catch (err) {
  errorTracker.captureException(err);
  console.error("[foo/cache] Write failed:", err);
  // never block the response on a cache write failure
}
```

**7. Invalidation** — after successful DB write:
```ts
try {
  await cache.del(fooCacheKey(id));
} catch (err) {
  errorTracker.captureException(err);
  console.error("[foo/cache] Invalidation failed:", err);
}
```

**8. Auth before cache** — always check authentication and authorisation BEFORE any cache call. A cache hit must never bypass a permission check.

**9. Graceful degradation is non-negotiable** — every cache operation is in its own try/catch. Redis being down must degrade to the database, never return a 500 to the user.
