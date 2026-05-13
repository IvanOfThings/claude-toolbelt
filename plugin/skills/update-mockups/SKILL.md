# update-mockups

Creates or updates HTML mockups for UI changes. Enforces mobile-first design using the project's design tokens.

## Prerequisites

Requires the `frontend-design` plugin. Run `check-dependencies` if unsure.

## Steps

**1. Read design context**

Read the project's `.claude/rules/ui.md` to load the design token reference (colors, typography, spacing, component library).

Read `rules/ui/mobile-first.md` from the plugin to apply the 390px-first constraint.

**2. Generate or update mockup**

Use `superpowers:frontend-design` to create or update the HTML mockup at `docs/mockups/<feature-name>.html`.

Mockup requirements:
- Default viewport: 390px width. Desktop layout only at `sm:` breakpoint and above.
- All colors and spacing come from the project's design tokens (`.claude/rules/ui.md`), never ad-hoc values.
- Interactive elements carry a `data-invalidates` attribute noting their React Query cache scope:
  `data-invalidates="['team', teamId, 'members']"`

**3. Validate mobile layout**

Describe what the mockup looks like at 390px:
- No horizontal overflow
- Touch targets ≥ 44px
- Content stacks vertically
- Text readable at default font sizes (minimum 14px body)

**4. Output**

State: file path created/updated, and one sentence describing the key mobile layout decision.

Present to developer. Wait for approval before the invoking command proceeds to implementation.
