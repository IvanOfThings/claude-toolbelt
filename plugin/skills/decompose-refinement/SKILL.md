# decompose-refinement

Reads a change document and decomposes it into discrete, ordered work items ready for `/dev-cycle`.

## Input

`doc-path`: path to the input document describing desired changes or features.

## Steps

**1. Read project context**

The invoking command has already run `analyze-context`. Use that output as project context.

**2. Read the input document**

Read every requirement, feature request, or change described in the document.

**3. Identify discrete items**

Decompose into items where each item:
- Can be completed in a single `/dev-cycle` (roughly ≤ 1 day of implementation work)
- Has a clear, testable acceptance criterion
- Touches one cohesive area of the codebase

Flag items that are oversized:
```
⚠ Item 3 is oversized: "Rewrite the entire notifications system"
  → Suggested split: (a) notification data model, (b) delivery service, (c) notification UI
```

**4. Check IMPLEMENTATION.md**

Read `IMPLEMENTATION.md`. Mark any items already implemented as `[DONE — skip]` in the decomposition.

**5. Order by dependency**

Sort items so foundational items (data model, service layer) come before items that depend on them (API routes, UI components).

**6. Ask clarifying questions**

For each item where the implementation approach is ambiguous: ask one clarifying question. Maximum 2 questions per item total. Ask them one at a time before writing specs.

**7. Generate mini-specs**

For each item, create `docs/superpowers/specs/refined/YYYY-MM-DD-<item-slug>.md` containing:

```markdown
# <Item title>

**Type:** feature | bugfix | refactor | migration
**Summary:** [1-2 sentences]

## Acceptance criteria
- [testable outcome]
- [testable outcome]

## Affected areas
- [files, services, routes, components]

## Dependencies
- [other item slugs that must be done first, or "none"]

## Constraints
- [ ] Mobile-first required
- [ ] i18n strings required
- [ ] DB migration needed
- [ ] New tracing spans needed
```

**8. Generate queue.json**

Create `docs/superpowers/specs/refined/queue.json`:
```json
{
  "pending": ["<slug-1>", "<slug-2>", "<slug-3>"],
  "done": []
}
```

Present the queue to the developer for approval before `/refine` begins execution.
