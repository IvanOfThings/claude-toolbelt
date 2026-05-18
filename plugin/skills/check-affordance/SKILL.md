# check-affordance

Verifies that the project's design system makes interactive elements **evidently distinguishable** from informational content. Complements `check-contrast` — that skill measures WCAG ratios; this skill enforces structural rules from `rules/ui/interactive-affordance.md` that ratios alone cannot capture.

Called by `/init-design-system` (paso 3 pre-validación y paso 7 post-write) on the project's resolved token table.

## Input

```yaml
token_table:               # same shape as check-contrast Mode 2
  bg-page:               { light, dark }
  bg-panel:              { light, dark }
  text-strong:           { light, dark }
  text-soft:             { light, dark }
  link-text:             { light, dark }     # optional
  primary:               "#..."
  button-primary-bg:     "#..."              # optional
  button-primary-text:   "#..."              # optional
  button-outline-border: "#..."              # optional
  button-outline-text:   "#..."              # optional
  focus-ring:            "#..."
  border-card:           "#..."
  border-input:          "#..."

rules_md_path:           # optional — path to .claude/rules/ui.md
  string                 # if provided, skill verifies declarations within the file
```

## What this skill checks

### Token-level checks (always run)

| # | Check                                                                                          | Why                                                                |
|---|------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| 1 | At least **one button style** is defined (either `button-primary-bg` or `button-outline-border`) | A design system without button tokens cannot enforce affordance. |
| 2 | If `button-primary-bg` defined: hex ≠ `bg-page.light`, ≠ `bg-panel.light`, ≠ `bg-page.dark`, ≠ `bg-panel.dark` | A button that matches the surface camouflages with it.            |
| 3 | If `button-primary-bg` defined: `button-primary-text` is also defined                          | A button must declare its own text color, not inherit body text.   |
| 4 | If `button-outline-border` defined: `button-outline-text` is also defined                      | Same reasoning.                                                    |
| 5 | If `link-text` defined: hex ≠ `text-strong.light` (and dark variant ≠ `text-strong.dark`)       | A link indistinguishable from body text fails WCAG 1.4.1.          |
| 6 | `focus-ring` is defined                                                                        | Keyboard accessibility requires a visible focus indicator.         |
| 7 | `border-card` and `border-input` are defined                                                   | Containers and inputs need explicit boundaries — borrowing `text-faint` is not acceptable. |
| 11| **Default-state distinction** for every declared button variant (primary, outline, ghost, danger, custom). For each variant `V` that has any `button-V-*` token declared, at least one of the following must hold (in light **and** in dark mode separately):<br/>• `button-V-bg` is declared and its hex ≠ `bg-page` and ≠ `bg-panel`, **or**<br/>• `button-V-border` is declared (any non-transparent value), **or**<br/>• `button-V-text` is declared and its hex ≠ `text-strong` on the surface the button lives on. | A button that has none of these in its default state is invisible until `:hover` — fails the affordance rule. Hover-only buttons are not buttons. Ghost variants in particular often regress to `background: transparent + color: text-strong + border: none`; check #11 catches this. |

### Declaration-level checks (only when `rules_md_path` provided)

The skill reads the file at `rules_md_path` (typically `.claude/rules/ui.md`) and looks for textual declarations:

| # | Check                                                                                       | What to look for in the file                                                |
|---|---------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| 8 | Links are underlined by default                                                              | A line declaring `text-decoration: underline` for `link-text` / `a` element, or an explicit "Links are underlined" statement in the Pattern Catalogue. |
| 9 | Every interactive token declares `hover` and `focus-visible` variants                       | Each of `button-primary`, `button-outline`, `link-text` has rows or sub-sections declaring `:hover` and `:focus-visible` colors/styles. |
| 10| `disabled` state is declared for buttons                                                    | Each button token has a `disabled` variant (color + opacity rule).          |

If `rules_md_path` is not provided, checks 8–10 are returned as a **TODO checklist** for the caller to verify manually.

## Steps

**1. Validate input**

Require `token_table` with at least `bg-page`, `bg-panel`, `text-strong`. Reject otherwise.

**2. Run token-level checks 1–7 and 11**

For each failing check, record: check number, what failed, and the specific tokens involved. Check 11 runs per declared button variant (primary, outline, ghost, danger, plus any custom `button-*-*` family detected in the `token_table`) and emits one row per variant per mode.

**3. Run declaration-level checks 8–10** (if `rules_md_path` given)

For each, grep the file content. If a declaration is absent, record as failing.

**4. Output**

```
[check-affordance] Token-level checks
| # | Check                                                  | Status |
|---|--------------------------------------------------------|--------|
| 1 | At least one button style defined                       | ✅ |
| 2 | button-primary-bg distinguishable from surfaces         | ❌ matches bg-panel.light (#F9FAFB) |
| 3 | button-primary-text defined                             | ✅ |
| 5 | link-text ≠ text-strong                                 | ✅ |
| 6 | focus-ring defined                                      | ✅ |
| 7 | border-card and border-input defined                    | ❌ border-input missing |

[check-affordance] Declaration-level checks  (rules_md_path: .claude/rules/ui.md)
| #  | Check                                                 | Status |
|----|-------------------------------------------------------|--------|
| 8  | Links underlined by default                            | ✅ |
| 9  | Hover + focus-visible declared for all interactives   | ❌ link-text:focus-visible missing |
| 10 | Disabled state declared for buttons                    | ✅ |
```

End with `[check-affordance] PASS — N checks satisfied.` or `[check-affordance] FAIL — X of N checks unsatisfied.`.

Like `check-contrast`, this skill does not gate — the caller decides.

## Notes for callers

- **`/init-design-system` step 3**: run on each candidate palette's projected token table. Discard candidates failing token-level checks (declarations come later — the file does not exist yet). Skip checks 8–10.
- **`/init-design-system` step 7**: run again with `rules_md_path` pointing to the freshly written `.claude/rules/ui.md`. Run all 10 checks. Gate on PASS together with `check-contrast`.
- The doctrine behind these checks lives in `plugin/rules/ui/interactive-affordance.md`. If the rule changes, update this skill so the executor stays in sync with the spec.
