# analyze-context

Reads project state before any implementation work. Produces a summary the developer confirms before proceeding.

## Steps

**1. Read CLAUDE.md**

Identify: project name, tech stack, paths to rule files, paths to documentation files. Note which files are referenced — skills use these paths, not hardcoded assumptions.

**2. Read docs/README.md**

This file lists every documentation file the project has declared, one line per file. Use this list to decide which other docs to read — do not assume a fixed set.

**3. Read docs/features.md**

Understand the current feature inventory and their documented behaviours.

**4. Read IMPLEMENTATION.md**

Identify: active sprint name, tasks in progress, completion state.

**5. Read relevant mockups (if UI task)**

If the task involves a UI change, read the mockup files in `docs/mockups/` that relate to the affected area.

**6. Output summary**

Write 2–4 sentences covering:
- What exists in the relevant area
- What this task needs to change
- Key constraints (mobile-first, DB migration needed, i18n strings needed, new tracing spans needed)

Example:
```
Context: Availability feature exists in docs/features.md with weekly slot management. Mockup at docs/mockups/availability.html shows mobile card layout. IMPLEMENTATION.md Sprint 3 active, 2 tasks pending. This task adds recurring schedules — requires a new DB column on AvailabilitySlot (migration needed) and a new UI toggle (mobile-first, i18n strings required).
```

Present the summary. Wait for the developer to confirm before the invoking command proceeds to the next step.
