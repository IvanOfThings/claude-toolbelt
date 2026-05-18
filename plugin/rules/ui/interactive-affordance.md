# Interactive Affordance

Users must be able to tell, at a glance, what is clickable and what is informational. A design system that achieves WCAG contrast on text but leaves buttons indistinguishable from their surroundings fails the user just as much as one with grey-on-grey labels.

This rule is the **declarative doctrine**. The `check-affordance` skill is the executor.

## The two principles

> **Principle 1 — Distinct signal.** Every interactive element must signal its interactivity through **at least one** of: a distinct fill, a contrasting border, or an explicit non-color cue (underline, icon). Color alone is never sufficient — WCAG 1.4.1.

> **Principle 2 — Default-state distinction.** The distinct signal must be present **in the default state**, not only on `:hover` or `:focus`. A button that reveals its fill or border on hover is invisible to a user who has not yet moved the cursor; on touch devices it has no default state to reveal. *Hover-only buttons are not buttons.*

The second principle is what `check-affordance` check #11 enforces: for every declared button variant, at least one of `button-V-bg ≠ surfaces`, `button-V-border` declared, or `button-V-text ≠ text-strong` must be true in both light and dark mode.

## Required token categories

Every project's `.claude/rules/ui.md` must declare these categories in addition to the standard text/background tokens:

### Buttons

At least one of these styles must be fully defined:

| Style       | Required tokens                                                    | Default-state distinction must come from |
|-------------|--------------------------------------------------------------------|-------------------------------------------|
| **Primary** | `button-primary-bg`, `button-primary-text`                         | Fill (`-bg` ≠ surfaces) — usually 3:1+ vs `bg-page`/`bg-panel` |
| **Outline** | `button-outline-border`, `button-outline-text`                     | Border (`-border` ≥ 3:1 vs surface)       |
| **Ghost**   | `button-ghost-bg`, `button-ghost-text`                             | A real default fill (e.g. `bg-panel-hover`) — **never `background: transparent`** |
| **Danger**  | `button-danger-bg`, `button-danger-text` (typically reuses `danger` status colour) | Fill — same rule as primary               |

**Ghost variant clause**: the default `button-ghost-bg` cannot be transparent. It must be at minimum `bg-panel-hover` or any fill ≥ 3:1 vs `bg-page`/`bg-panel`. A ghost button without a default fill, border, or distinct text color is the canonical hover-only-affordance failure and is rejected by check #11.

### Links

If text links appear in the product, `link-text` must be defined and must satisfy **both**:

1. `link-text.light` ≠ `text-strong.light` (and same for dark) — color must visibly differ from body text.
2. Links are underlined by default. The default rule must be declared in `.claude/rules/ui.md`'s Pattern Catalogue. Removing the underline is allowed only on hover (or explicitly per-component for navigation tabs).

### Inputs

Input fields require a **compound focus signal**: the `focus-ring` outline overlay alone is not enough — the input itself must visually change at the border. Required tokens:

| Token                  | Used for                                                         |
|------------------------|------------------------------------------------------------------|
| `border-input`         | Default border colour, ≥ 3:1 against `bg-panel`                  |
| `border-input-focus`   | Border colour applied when the input is `:focus-visible`. Typically the same hue family as `focus-ring`. |
| `focus-ring`           | The outline overlay drawn around the input on `:focus-visible`   |

In the project's CSS:

```css
input:focus-visible {
  border-color: var(--border-input-focus);
  outline: 3px solid var(--focus-ring);
  outline-offset: 1px;
}
```

A single signal (only the outline, or only the border colour change) is too easy to miss in scan reading.

### Focus, borders, separators

| Token                | Required because                                                  |
|----------------------|-------------------------------------------------------------------|
| `focus-ring`         | Keyboard users need a visible focus indicator (WCAG 2.4.7).       |
| `border-input-focus` | Inputs need a compound focus signal — see "Inputs" above.         |
| `border-card`        | Cards need explicit boundaries against the page background.       |
| `border-input`       | Inputs must look different from static labels.                    |
| `divider`            | Section separators that are not borders of a container.           |

## Contrast requirements

Enforced by `check-contrast` Mode 2 using its canonical matrix. The non-negotiable subset for affordance:

| Pair                                    | Threshold |
|-----------------------------------------|-----------|
| `button-primary-bg` vs `bg-page` / `bg-panel`  | 3:1   |
| `button-outline-border` vs `bg-page`           | 3:1   |
| `button-ghost-bg` vs `bg-page`                 | 3:1   |
| `button-danger-bg` vs `bg-page` / `bg-panel`   | 3:1   |
| `border-card` vs `bg-page`                     | 3:1   |
| `border-input` vs `bg-panel`                   | 3:1   |
| `focus-ring` vs every surface it overlays      | 3:1   |
| `button-primary-text` vs `button-primary-bg`   | 4.5:1 |
| `button-danger-text` vs `button-danger-bg`     | 4.5:1 |
| `hero-text` vs `bg-hero-from` (lightest stop)  | 4.5:1 |
| `hero-text` vs `bg-hero-to` (darkest stop)     | 4.5:1 |

## States — required for every interactive token

Each interactive token must declare:

- **`:hover`** — visual change (lightness shift, fill swap, or border emphasis).
- **`:focus-visible`** — typically the `focus-ring` token, but the rule needs an explicit declaration per token. For inputs, also declare `border-input-focus` as the compound border change.
- **`:disabled`** — reduced opacity is the conventional cue, but the disabled state must remain distinguishable from active body text.

Declaring "uses default" is not acceptable. The framework's CSS reset is not the project's design system.

## Visual separation: interactive vs informational

- **Informational sections** (cards, hero blocks, callouts) must not adopt button-shaped affordances: pill-radius fills, ring outlines, or hover-coloured backgrounds.
- **Interactive elements** must not look like passive labels: no buttons styled with only `text-strong` and no border or fill (this is the default-state principle).
- **Status badges are non-interactive — full stop.** Badges may share visual language with buttons (rounded shape, status colour fill) only if they:
  - Have **no `:hover` style**
  - Have **no `:focus-visible` style**
  - Use `cursor: default`, never `cursor: pointer`
  - Carry no `aria-label` of an action and no click handler

  Badges convey state (Pending, Approved, Rejected); buttons trigger actions. Conflating the two is the most common reported usability bug in this framework's reviews.

## Anti-patterns

| Anti-pattern                                                                | Why it fails                                                                |
|-----------------------------------------------------------------------------|------------------------------------------------------------------------------|
| Button with `bg` equal to `bg-panel` and no border                           | Invisible against the panel — user cannot find it.                          |
| Ghost button with `background: transparent`, no border, `color: text-strong` | The canonical default-state failure: indistinguishable from body text until hover. |
| Link styled only as `text-primary` with no underline                         | Fails WCAG 1.4.1 — relies on colour alone.                                  |
| Card with `border-color` equal to `text-faint`                               | Borrowing a text token for structural use; usually < 3:1.                  |
| Focus ring identical to `primary`                                            | Fails when focus lands on a primary-filled button (no contrast).            |
| Disabled button using `text-soft` on `button-primary-bg`                     | Disabled state must not look like active body text on the surface.          |
| Section/callout with `border-radius` and fill that match a button            | Users will try to click it.                                                 |
| Badge with `:hover` background change or `cursor: pointer`                   | Looks interactive, is not. Frustration and broken expectation.              |
| Input focus that changes only the outline (no border-colour change)          | The input itself looks identical; users miss the focus state in scan reading. |
| Hero text rendered as `text-strong-dark` at `opacity: 0.85` on a gradient    | Validated against the gradient average, not the lightest stop — fails 4.5:1 at the top of the gradient. Use a solid `hero-text` token. |

## Pattern Catalogue contract

`.claude/rules/ui.md`'s Pattern Catalogue must include sections covering:

- Buttons — every declared variant × every declared state (primary, outline, ghost, danger)
- Links — default + hover + focus-visible
- Inputs — default + focus (compound signal: border change + outline) + disabled + error
- Focus ring — illustrated on at least three surface combinations (`bg-page`, `bg-panel`, `button-primary-bg`)
- Status badges — illustrated alongside buttons with an explicit note: "non-interactive, no hover, no focus"
- Active tab / selector states

`init-design-system` generates these sections. `check-affordance` verifies their textual presence when `rules_md_path` is supplied.
