# init-design-system

Guides the selection of a component library and color palette, then generates the complete visual design system for the project.

Callable from `init-project` (Step 4) or standalone as `/init-design-system` to update an existing project's design system.

## Steps

**1. Read product context**

Read `docs/plan.md` if it exists. Extract: product type, target users, tone/personality, primary use context (sports, productivity, social, healthcare, etc.).

**2. Present component library options**

Show the following table and ask the developer to choose one:

| Option | Style | Included icons | Link |
|--------|-------|----------------|------|
| shadcn/ui | Minimalist, headless, Radix-based | Lucide | shadcn.com |
| DaisyUI | Themed, Tailwind-native | Heroicons | daisyui.com |
| Mantine | Full-featured, accessible, with hooks | Tabler Icons | mantine.dev |
| Flowbite | Bootstrap-style, Tailwind | Flowbite Icons | flowbite.com |
| None (CSS vars only) | Raw design tokens only | User's choice | — |

Wait for the developer's selection before continuing.

**3. Propose 3 candidate palettes (pre-validated)**

Based on the product context from `docs/plan.md`, generate candidate palettes. Each candidate is a **full `token_table`** matching the shape consumed by `check-contrast` Mode 2 and `check-affordance` — see `rules/templates/ui-design-tokens.md` for the complete list of categories (surfaces, text, brand, buttons, links, borders, focus). Do not skip categories: a palette without `button-primary-bg` cannot be validated for affordance.

**Pre-validate each candidate** by invoking, in order:

1. `check-contrast` in **Mode 2** with the candidate's `token_table`. The skill expands the canonical matrix and returns the full audit. The matrix definition lives in `check-contrast` — do not duplicate it here.
2. `check-affordance` with the same `token_table`, **omitting `rules_md_path`** (the file does not exist yet — only token-level checks 1–7 run).

A candidate is presentable only if **both** skills return `PASS`. Discard failing candidates and regenerate until you have 3 valid options.

Show the developer the resulting palettes with their full `check-contrast` tables and `check-affordance` results, then ask them to choose or describe custom colors.

If the developer describes custom colors, build the full `token_table` from their input and run both skills again before accepting. On any failure, surface it with the suggested replacement and re-ask — do not silently proceed.

Wait for the developer's selection before continuing.

**4. Generate docs/design-system.html**

Standalone HTML file (no server required). Include:
- CSS variable declarations for all resolved tokens
- Color palette swatches with hex values and CSS token names
- Typography scale (size, weight, line-height)
- Spacing scale
- Representative components from the chosen library: buttons (all variants), cards, badges, inputs, navigation bar, status indicators
- WCAG contrast table calculated from the project's actual token values
- Dark mode toggle (if the project uses dark mode based on brainstorm context)

**5. Generate docs/icons.html**

Standalone HTML file (no server, no build step). Include:
- Header: project name + icon library name (from chosen component library) + version
- Search bar (inline JS, no dependencies) — filters icons by name
- Size selector: 16 / 24 / 32 px
- Color selector: primary / text-strong / text-soft / custom hex
- Icon grid grouped by category: Navigation, Actions, Status, Communication, Data
- Each icon: visual preview + icon name + copy-ready usage snippet for the project's stack

Example snippet for shadcn/ui (Lucide):
```tsx
import { Home } from "lucide-react"
<Home size={24} className="text-primary" />
```

Example snippet for DaisyUI (Heroicons):
```tsx
import { HomeIcon } from "@heroicons/react/24/outline"
<HomeIcon className="w-6 h-6 text-primary" />
```

**6. Write .claude/rules/ui.md**

Fill the `rules/templates/ui-design-tokens.md` template from the plugin with the resolved values from the chosen `token_table`. The template defines the canonical structure — do not invent sections or omit declared categories. The file must include:

- All token categories from the template: Surfaces and text, Brand, Buttons (with hover/focus-visible/disabled columns), Links (with decoration column), Borders/separators/focus.
- The WCAG Contrast Reference table filled with the actual `check-contrast` Mode 2 output for this token table.
- The Affordance Audit table (will be filled in paso 7).
- The Pattern Catalogue sections from the template: Hero, Buttons × all states, Links, Inputs, Focus ring, Status badges, Active tab states.
- The Contrast & Affordance Audit Checklist at the end.

The declarations for hover, focus-visible, and disabled states for every interactive token are mandatory — `check-affordance` will verify them in paso 7. "Uses default" is not acceptable; declare explicit values.

**7. Final audit (gate)**

Run both skills against the freshly written `.claude/rules/ui.md`:

1. `check-contrast` Mode 2 with the resolved `token_table`. Expected: `[check-contrast] PASS`.
2. `check-affordance` with the same `token_table` **and `rules_md_path` pointing to `.claude/rules/ui.md`** — this enables declaration-level checks 8–10 (link underline, hover/focus-visible declared, disabled declared). Expected: `[check-affordance] PASS`.

Fill the "Affordance Audit" table in `.claude/rules/ui.md` with the result.

If either skill returns `FAIL`: do not close the command. Show the failures with the skill's suggested replacements, ask the developer how to adjust (swap token, tweak hex, regenerate palette, add missing state declaration), apply the fix to `.claude/rules/ui.md` and `docs/design-system.html`, and re-audit. Loop until both audits pass.

**8. Output**

Report: three files created/updated — `docs/design-system.html`, `docs/icons.html`, `.claude/rules/ui.md` — and the two final `PASS` lines from `check-contrast` and `check-affordance`.

Note: if future `dev-cycle` runs introduce icons not in `docs/icons.html`, run `/update-icons` to add them.
