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

**3. Propose 3 color palettes**

Based on the product context from `docs/plan.md`, generate 3 contextualised palette proposals. Each contains:
- `primary` — main brand color (hex value + Tailwind scale reference)
- `surface` — page and panel backgrounds (light / dark hex values)
- `accent` — secondary action color (hex value)
- WCAG AA contrast ratio for primary text on the light surface background

Example for a sports management app:
```
Palette A "Campo de juego"
  primary:  #16A34A (green-600)  contrast on white: 4.6:1 ✅
  surface:  #F0FDF4 (light) / #052E16 (dark)
  accent:   #FACC15 (yellow-400)

Palette B "Equipación"
  primary:  #2563EB (blue-600)   contrast on white: 5.9:1 ✅
  surface:  #EFF6FF (light) / #1E3A5F (dark)
  accent:   #F97316 (orange-500)

Palette C "Noche"
  primary:  #7C3AED (violet-600) contrast on white: 5.5:1 ✅
  surface:  #F5F3FF (light) / #1E1B4B (dark)
  accent:   #06B6D4 (cyan-500)
```

Present all three with names. Ask the developer to choose one or describe custom colors.

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

Fill the `rules/templates/ui-design-tokens.md` template from the plugin with the resolved values for this project:

```markdown
# UI Design Tokens — [Project Name]

## Component library: [chosen library]

## Token Reference (Light / Dark)
| Token | Light | Dark |
|-------|-------|------|
| bg-page     | [hex] | [hex] |
| bg-panel    | [hex] | [hex] |
| text-strong | [hex] | [hex] |
| text-soft   | [hex] | [hex] |
| text-faint  | [hex] | [hex] |
| text-primary| [hex] | [hex] |
| accent      | [hex] | [hex] |

## WCAG Contrast Reference
| Text token | Background token | Ratio | Status |
|-----------|-----------------|-------|--------|
| text-primary | bg-panel (light) | ?:1 | [✅/❌] |
| text-strong  | bg-page (light)  | ?:1 | [✅/❌] |
[additional combinations from the palette]

## Pattern Catalogue
### Hero / dark sections
[Correct and incorrect usage for hero backgrounds]

### Active tab / selector states
[Correct usage for interactive elements]

### Status badges
[Color assignments for open, closed, pending, error states]

## Contrast Audit Checklist
- [ ] Hero sections — all text uses light variants on dark gradient
- [ ] Active tabs/nav — use text-primary on light backgrounds
- [ ] Status badges — darker text variants in light mode with dark-mode overrides
- [ ] Normal text on panels — text-strong or text-soft; never text-faint for meaningful content
```

**7. Output**

Report: three files created/updated — `docs/design-system.html`, `docs/icons.html`, `.claude/rules/ui.md`.

Note: if future `dev-cycle` runs introduce icons not in `docs/icons.html`, run `/update-icons` to add them.
