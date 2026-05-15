# Interactive Affordance

Users must be able to tell, at a glance, what is clickable and what is informational. A design system that achieves WCAG contrast on text but leaves buttons indistinguishable from their surroundings fails the user just as much as one with grey-on-grey labels.

This rule is the **declarative doctrine**. The `check-affordance` skill is the executor.

## The principle

> Every interactive element must signal its interactivity through **at least one** of: a distinct fill, a contrasting border, or an explicit non-color cue (underline, icon). Color alone is never sufficient — WCAG 1.4.1.

## Required token categories

Every project's `.claude/rules/ui.md` must declare these categories in addition to the standard text/background tokens:

### Buttons

At least one of these styles must be fully defined:

| Style       | Required tokens                                            |
|-------------|------------------------------------------------------------|
| **Primary** | `button-primary-bg`, `button-primary-text`                 |
| **Outline** | `button-outline-border`, `button-outline-text`             |

A project may declare both. A project may declare a `button-ghost-text` if it uses a text-only button variant — but ghost buttons need an additional non-color cue (icon, underline on hover) because they have neither fill nor border.

### Links

If text links appear in the product, `link-text` must be defined and must satisfy **both**:

1. `link-text.light` ≠ `text-strong.light` (and same for dark) — color must visibly differ from body text.
2. Links are underlined by default. The default rule must be declared in `.claude/rules/ui.md`'s Pattern Catalogue. Removing the underline is allowed only on hover (or explicitly per-component for navigation tabs).

### Focus, borders, separators

| Token         | Required because                                                  |
|---------------|-------------------------------------------------------------------|
| `focus-ring`  | Keyboard users need a visible focus indicator (WCAG 2.4.7).       |
| `border-card` | Cards need explicit boundaries against the page background.      |
| `border-input`| Inputs must look different from static labels.                    |
| `divider`     | Section separators that are not borders of a container.           |

## Contrast requirements

Enforced by `check-contrast` Mode 2 using its canonical matrix. The non-negotiable subset for affordance:

| Pair                                    | Threshold |
|-----------------------------------------|-----------|
| `button-primary-bg` vs `bg-page` / `bg-panel` | 3:1   |
| `button-outline-border` vs `bg-page`         | 3:1   |
| `border-card` vs `bg-page`                   | 3:1   |
| `border-input` vs `bg-panel`                 | 3:1   |
| `focus-ring` vs every surface it overlays    | 3:1   |
| `button-primary-text` vs `button-primary-bg` | 4.5:1 |

## States — required for every interactive token

Each interactive token must declare:

- **`:hover`** — visual change (lightness shift, fill swap, or border emphasis).
- **`:focus-visible`** — typically the `focus-ring` token, but the rule needs an explicit declaration per token.
- **`:disabled`** — reduced opacity is the conventional cue, but the disabled state must remain distinguishable from active body text.

Declaring "uses default" is not acceptable. The framework's CSS reset is not the project's design system.

## Visual separation: interactive vs informational

- **Informational sections** (cards, hero blocks, callouts) must not adopt button-shaped affordances: pill-radius fills, ring outlines, or hover-colored backgrounds.
- **Interactive elements** must not look like passive labels: no buttons styled with only `text-strong` and no border or fill.
- **Status badges** are informational — they may share visual language with buttons (rounded, colored) only when they are clearly non-clickable (no hover state, no cursor change).

## Anti-patterns

| Anti-pattern                                                      | Why it fails                                                  |
|-------------------------------------------------------------------|---------------------------------------------------------------|
| Button with `bg` equal to `bg-panel` and no border                | Invisible against the panel — user cannot find it.            |
| Link styled only as `text-primary` with no underline              | Fails WCAG 1.4.1 — relies on color alone.                     |
| Card with `border-color` equal to `text-faint`                    | Borrowing a text token for structural use; usually < 3:1.    |
| Focus ring identical to `primary`                                 | Fails when focus lands on a primary-filled button (no contrast). |
| Disabled button using `text-soft` on `button-primary-bg`          | Disabled state must not look like active body text on the surface. |
| Section/callout with `border-radius` and fill that match a button | Users will try to click it.                                   |

## Pattern Catalogue contract

`.claude/rules/ui.md`'s Pattern Catalogue must include sections covering:

- Buttons (all declared variants × all declared states)
- Links (default + hover)
- Inputs (default + focus + disabled + error)
- Focus ring (illustrated on at least two surface combinations)
- Status badges (and how they differ visually from buttons)

`init-design-system` generates these sections. `check-affordance` verifies their textual presence when `rules_md_path` is supplied.
