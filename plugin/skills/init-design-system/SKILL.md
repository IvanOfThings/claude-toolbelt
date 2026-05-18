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

**3a. Ask for brand colour hints (optional)**

Before generating, ask the developer:

> *"Do you have any brand colours you want me to honour in the palettes? You can paste hex codes, name a colour family (e.g. 'forest olive', 'terracotta', 'navy'), or describe the brand vibe in words. Leave blank to generate from product context only."*

Parse the answer into a `brand_hints` structure:
- `hex_anchors: string[]` — explicit hex values the developer wants pinned
- `colour_family: string` — named family ("olive", "saffron", etc.) the brand belongs to
- `vibe: string` — free-form description ("warm Mediterranean restaurant", "calm modern cookbook")
- Or `null` if the developer left it blank

Brand hints are **inputs to the heuristic generator**, not hard constraints — if a provided hex cannot pass contrast in any plausible arrangement, surface the problem and ask the developer whether to relax it.

**3b. Generate three distinct candidates (heuristic stage)**

Apply `rules/ui/palette-design-heuristics.md` (H1–H8) when generating each candidate `token_table`. Key heuristics:

- **H1 One dominant brand colour per palette** — `primary` is the brand; `accent` is a quieter partner; status colours live on a separate functional axis.
- **H2 Temperature-coherent focus ring** — warm palette → warm `focus-ring` (amber/saffron/ochre); cool palette → cool ring (cyan/lavender/sky). Generic teal on a warm palette is forbidden.
- **H3 Lightest passing border** — `border-card`, `border-input`, `divider` use the lightest tone that still passes 3:1, not "any passing tone".
- **H4 Adjust the gradient, not the text** — if the hero gradient cannot give `hero-text` 4.5:1 at the lightest stop, darken the gradient ramp until it does.
- **H5 Solid `hero-text`** — never `opacity` or `rgba()` alpha for hero overlays.
- **H6 Status colours on a separate axis** — `success`/`warning`/`danger` are functional (green/amber/red typically), not derived from `primary`/`accent`.
- **H7 Three distinct directions** — the three candidates must represent meaningfully different design directions (different tone, temperature, or brand-colour family), not three saturations of the same hue.
- **H8 Vibe-named palettes** — each candidate carries a short evocative name (2–4 words: "Sage Olive", "Terracotta", "Saffron Gold") so the developer reacts emotionally before reading hex codes.

Each candidate is a **full `token_table`** matching the shape consumed by `check-contrast` Mode 2 and `check-affordance` — see `rules/templates/ui-design-tokens.md` for the complete list of categories (surfaces, text including `hero-text`, brand, status colours, buttons including ghost and danger, links, borders including `border-input-focus`, focus). Do not skip categories: a palette without `button-primary-bg` cannot be validated for affordance; a palette without `hero-text` cannot be validated against the gradient stops.

**3c. Validate each candidate**

For each candidate, invoke in order:

1. `check-contrast` in **Mode 2** with the candidate's `token_table`. The skill expands the canonical matrix (including the gradient pairs `hero-text` × `bg-hero-from`/`bg-hero-to`) and returns the full audit.
2. `check-affordance` with the same `token_table`, **omitting `rules_md_path`** (the file does not exist yet — token-level checks 1–7 and 11 run).

A candidate is presentable only if **both** skills return `PASS`. If a candidate fails:
- **Hero gradient pair fails at the lightest stop** → apply H4: darken `bg-hero-from` until the ratio passes. Do not change `hero-text`.
- **Border fails 3:1** → walk the border tone one step darker; keep it as light as possible (H3).
- **Button variant fails check #11 default-state distinction** → add a fill, border, or distinct text colour for that variant; never resolve by adding a hover-only style.

Discard candidates that cannot be repaired and regenerate to keep three valid options.

**3d. Present and select**

Show the developer the three palettes with:
- Vibe name (H8)
- Dominant brand colour described in words
- Hex preview of `primary`, `accent`, `focus-ring`, `hero-text`
- Full `check-contrast` table per palette
- `check-affordance` audit (10 token-level checks)

Ask the developer to choose one or describe custom colours.

If the developer describes custom colours, build the full `token_table` from their input, apply the heuristics, run both skills again before accepting. On any failure, surface it with the suggested adjustment and re-ask — do not silently proceed.

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
