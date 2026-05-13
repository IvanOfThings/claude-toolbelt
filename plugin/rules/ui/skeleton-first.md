# Skeleton-First Loading

Every screen must feel structured and complete from the very first paint. Users must never see a blank white area or a "Loading..." / "Cargando..." text string.

## The pattern: Suspense + skeleton, always

Every section that fetches data must be wrapped in a `<Suspense fallback={<XxxSkeleton />}>` boundary.

Skeleton components must:
- Match the **exact dimensions** (height, width, spacing) of the real content — no layout shift when data arrives
- Use animated placeholder shapes (e.g. `animate-pulse` divs) that mimic the shape of cards, rows, or text blocks
- Live in the same directory as the real component: `foo-card.tsx` → `foo-card-skeleton.tsx`

## Progressive top-to-bottom hydration

Decompose every page into independent sections, each with its own Suspense boundary and data fetch. Do not wait for the entire page's data before rendering anything.

```
Page
├── <HeroSection />             ← no data, renders immediately
├── <Suspense fallback={<StatsSkeleton />}>
│     <StatsSection />          ← fetches its own data independently
│   </Suspense>
└── <Suspense fallback={<ListSkeleton />}>
      <ItemList />               ← fetches its own data independently
    </Suspense>
```

## Non-negotiable rules

- **No "Loading..." text** — ever. Every loading state is a skeleton that mirrors the content shape.
- **No full-page loading gates** — do not block the entire page on a single `isLoading` flag.
- **Skeleton dimensions are fixed** — the page must not jump or reflow when data arrives.
- **One Suspense boundary per independent data source**.
- **Skeleton components are first-class** — they are tested and reviewed like any other component.
