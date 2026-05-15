# check-contrast

Computes WCAG AA contrast ratios for text/background and UI-component pairs, reports pass/fail with suggested replacements. Single source of truth for the contrast logic used by `/init-design-system` (design-system audit) and `/ui-contrast` (changed-file audit).

## Input modes

The skill accepts **one of two inputs**:

### Mode 1 — ad-hoc pairs

For callers that already know which pairs to check (e.g. `/ui-contrast` scanning changed files).

```yaml
pairs:                      # required, non-empty
  - label: string           # human-readable identifier shown in output
    text_hex: "#RRGGBB"
    bg_hex:   "#RRGGBB"
    kind: normal | large | ui   # default: normal

available_tokens:           # optional — used to suggest replacements when a pair fails
  - name: string            # e.g. "text-strong"
    hex:  "#RRGGBB"
```

### Mode 2 — design-system token table

For callers auditing a full design system (e.g. `/init-design-system`). Caller passes the resolved token table; **the skill internally expands the canonical matrix** below and audits it.

```yaml
token_table:
  # Surfaces (each has light + dark variants)
  bg-page:              { light: "#...", dark: "#..." }
  bg-panel:             { light: "#...", dark: "#..." }

  # Text
  text-strong:          { light: "#...", dark: "#..." }
  text-soft:            { light: "#...", dark: "#..." }
  text-faint:           { light: "#...", dark: "#..." }   # optional, decorative only
  link-text:            { light: "#...", dark: "#..." }   # optional

  # Brand
  primary:              "#..."
  accent:               "#..."

  # Buttons (any subset that the project uses)
  button-primary-bg:    "#..."
  button-primary-text:  "#..."
  button-outline-border:"#..."
  button-outline-text:  "#..."

  # Borders / separators / focus
  border-card:          "#..."
  border-input:         "#..."
  divider:              "#..."
  focus-ring:           "#..."
```

Tokens marked optional are skipped silently if absent. Tokens with `{ light, dark }` variants produce one pair per variant.

## WCAG AA thresholds

| `kind`   | What it covers                                  | Minimum ratio |
|----------|-------------------------------------------------|---------------|
| `normal` | Body text, labels, anything below 18pt regular  | **4.5:1**     |
| `large`  | Text ≥ 18pt regular, or ≥ 14pt bold             | **3:1**       |
| `ui`     | Icons, borders, focus rings, graphical objects  | **3:1**       |

## Ratio formula

For each pair:

1. Convert each hex to sRGB channels (0..1).
2. Linearise each channel: `c <= 0.03928 ? c/12.92 : ((c+0.055)/1.055)^2.4`.
3. Relative luminance: `L = 0.2126*R + 0.7152*G + 0.0722*B`.
4. Ratio: `(max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)`. Round to 2 decimals.

## Canonical matrix (Mode 2)

When `token_table` is provided, the skill generates pairs as follows. Each row produces one pair per declared variant (light/dark) when applicable.

| Pair                              | text token          | background token       | kind   |
|-----------------------------------|---------------------|------------------------|--------|
| Body text on page                 | `text-strong`       | `bg-page`              | normal |
| Body text on page                 | `text-soft`         | `bg-page`              | normal |
| Body text on panel                | `text-strong`       | `bg-panel`             | normal |
| Body text on panel                | `text-soft`         | `bg-panel`             | normal |
| Link on panel                     | `link-text`         | `bg-panel`             | normal |
| Brand text on page                | `primary`           | `bg-page`              | normal |
| Button text on primary fill       | `button-primary-text` | `button-primary-bg`  | normal |
| Outline button text on page       | `button-outline-text` | `bg-page`            | normal |
| Primary button vs page            | `button-primary-bg` | `bg-page`              | ui     |
| Primary button vs panel           | `button-primary-bg` | `bg-panel`             | ui     |
| Outline button border vs page     | `button-outline-border` | `bg-page`          | ui     |
| Card border vs page               | `border-card`       | `bg-page`              | ui     |
| Input border vs panel             | `border-input`      | `bg-panel`             | ui     |
| Divider vs page                   | `divider`           | `bg-page`              | ui     |
| Focus ring vs page                | `focus-ring`        | `bg-page`              | ui     |
| Focus ring vs panel               | `focus-ring`        | `bg-panel`             | ui     |
| Focus ring vs primary button      | `focus-ring`        | `button-primary-bg`    | ui     |

This is the **canonical definition** of "complete design-system contrast audit". Adding a new token category (e.g. `button-disabled-bg`) means extending this table once — every caller using Mode 2 picks it up automatically.

## Steps

**1. Validate input**

Reject if neither `pairs` nor `token_table` is provided (or both are). In Mode 1, ensure each entry has `text_hex` and `bg_hex`. In Mode 2, ensure at least `bg-page`, `bg-panel`, `text-strong`, `text-soft` are present.

**2. Build pair list**

- Mode 1: use `pairs` as-is.
- Mode 2: expand the canonical matrix above against the provided `token_table`. Skip pairs whose tokens are absent. Generate one pair per declared light/dark variant.

**3. Compute ratios**

For each pair, compute the ratio using the formula above and compare against the threshold for its `kind`.

**4. Suggest replacements (only for failing pairs)**

When a pair fails:

- Mode 1: iterate `available_tokens` (text-tokens for text failures, all tokens otherwise). Pick the candidate with the **smallest passing ratio above the threshold** (least drastic change).
- Mode 2: use `token_table` itself as the candidate pool. For a failing text pair, try other text-* tokens against the same background. For a failing UI pair, do not auto-suggest — surface the failure so the developer picks an adjustment.
- If no candidate passes, say so explicitly. Do not invent a hex.

**5. Output**

Markdown table:

```
| Pair | Ratio | Required | Status |
|------|-------|----------|--------|
| text-soft (#6B7280) on bg-page (#FFFFFF)     | 4.83:1 | 4.5:1 | ✅ |
| border-card (#E5E7EB) on bg-page (#FFFFFF)   | 1.30:1 | 3.0:1 | ❌ |
| text-faint (#D1D5DB) on bg-panel (#F9FAFB)   | 1.79:1 | 4.5:1 | ❌ → use text-soft (#6B7280) — 4.61:1 |
```

End with `[check-contrast] PASS — N pairs audited.` or `[check-contrast] FAIL — X of N pairs below WCAG AA.`.

This skill does not gate — the caller decides what to do with failures.

## Notes for callers

- **`/ui-contrast`**: use Mode 1. Scan changed files, resolve tokens to hex via `.claude/rules/ui.md`, classify each pair's `kind` (`large` if class is `text-xl`/`text-2xl`/etc., `ui` if it's a border/outline/ring, otherwise `normal`).
- **`/init-design-system` step 3**: use Mode 2 on each candidate palette before showing it to the developer. Only show palettes where all pairs pass.
- **`/init-design-system` step 7**: use Mode 2 again on the resolved token table written to `.claude/rules/ui.md`. Gate the command on PASS.
