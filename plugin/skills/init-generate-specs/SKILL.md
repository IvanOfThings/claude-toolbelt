# init-generate-specs

Generates ordered refinement specs for every feature in the approved high-level design. Creates a `/refine`-ready queue.

## Input

From `init-brainstorm` output: feature list with descriptions, tech stack, architecture layers.

## Steps

**1. Read docs/plan.md**

Extract the complete feature list from the approved design. Each feature becomes one mini-spec.

**2. Order by implementation dependency**

Group features into implementation layers before speccing:
- Layer 1: Data model / schema definitions
- Layer 2: Service layer / business logic
- Layer 3: API routes / server actions
- Layer 4: UI components / pages
- Layer 5: Cross-cutting integration features

Foundational features first. A UI feature cannot be specced before the API it depends on.

**3. Generate mini-spec files**

For each feature, create `docs/superpowers/specs/refined/YYYY-MM-DD-<feature-slug>.md`:

```markdown
# [Feature name]

**Type:** feature
**Summary:** [1-2 sentences from brainstorm description]

## Acceptance criteria
- [Specific, testable outcome from brainstorm]
- [Mobile-first: layout works at 390px]
- [i18n: all user-visible strings in locales/]

## Affected areas
- [Inferred from stack: e.g. src/app/api/..., src/components/..., src/services/...]

## Dependencies
- [Other feature slugs that must be completed first, or "none"]

## Constraints
- [ ] Mobile-first required
- [ ] i18n strings required
- [ ] DB migration needed
- [ ] New tracing spans needed
```

**4. Generate queue.json**

Create `docs/superpowers/specs/refined/queue.json`:

```json
{
  "pending": ["<slug-1>", "<slug-2>", "<slug-3>"],
  "done": []
}
```

Order of slugs in `pending` matches the dependency order from Step 2.

**5. Output**

Report: number of specs generated, path to queue.json, first slug in the queue (the first feature to build).
