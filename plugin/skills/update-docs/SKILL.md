# update-docs

Updates project documentation after implementation to reflect what was actually built.

## Steps

**1. Read docs/README.md**

This file lists every documentation file the project has declared. Use this list to know which docs exist — do not assume a fixed set. Skip any doc not declared here.

**2. Update docs/features.md**

For each feature added, modified, or removed in this cycle: update its entry to reflect current behaviour. Add new features, remove deleted ones, correct changed descriptions.

**3. Update the plan file**

Read the plan file used for this cycle (`docs/superpowers/plans/YYYY-MM-DD-<name>.md`). If the implementation deviated from the plan (different file structure, different approach chosen), note the deviation at the top under a `## Deviations` section.

**4. Consistency pass — architecture**

Read `docs/arch.md` if declared. Did this cycle introduce or change architectural layers, patterns, or service boundaries? If yes, update the relevant section.

**5. Consistency pass — database**

Read `docs/db.md` if declared. Did a DB migration run in this cycle? If yes, update the schema description and entity relationship notes.

**6. Consistency pass — API**

Read `docs/api.md` if declared. Were new endpoints added or existing ones changed? If yes, update the route list, request/response shapes, and auth requirements.

**7. Consistency pass — mockups**

If the implementation deviated from a mockup in `docs/mockups/`, do NOT silently update the mockup. Flag the discrepancy to the developer:

```
⚠ Mockup deviation detected: docs/mockups/availability.html
  Mockup shows inline date picker; implementation uses modal.
  → Update mockup with /init-design-system or /dev-cycle before next cycle.
```

**8. Verify docs/README.md**

Confirm every file listed in `docs/README.md` still exists. Remove entries for deleted files, add entries for newly created documentation files.
