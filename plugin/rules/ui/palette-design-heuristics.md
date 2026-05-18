# Palette Design Heuristics

Best practices applied when `init-design-system` generates the three candidate colour palettes. These are **not** WCAG rules — they are taste/craft heuristics that prevent the "AI-generated palette" smell (clashing accents, generic mid-range hues, jarring focus rings).

`check-contrast` and `check-affordance` verify accessibility. This document codifies the layer above: **whether the palette actually looks like a designed system**.

## H1 — One dominant brand colour per palette

Each candidate palette has **one** primary brand colour. The accent supports it (analogous, complementary, or warm-cool partner) but is not a second brand. Status colours (`success` / `warning` / `danger`) live on their own axis and are not "third and fourth brands".

A palette with three competing brand-strength colours reads as confused. The eye cannot decide what to lock onto, calls-to-action lose hierarchy, and the design system feels like a swatch library rather than a brand.

**Wrong**: `primary` = green-600 and `accent` = pink-500 and a secondary "feature" colour = blue-500, all at full brand saturation.

**Right**: `primary` = forest-olive, `accent` = warm gold (a quieter partner), status colours desaturated to functional roles.

## H2 — Temperature-coherent focus ring

The `focus-ring` colour should be in **thermal sympathy** with the palette, not in opposition. A warm-tone palette (terracotta, olive, saffron) gets a warm focus ring (amber, saffron, ochre). A cool-tone palette (slate, ocean, indigo) gets a cool focus ring (cyan, lavender, sky).

The default Tailwind/shadcn focus ring is often a generic teal/cyan. Dropping a cyan ring onto a saffron-gold palette feels like a system-error popup, not a focus state. The focus ring is the most-seen interaction colour after `primary` — it must belong.

Constraint: the focus ring still needs ≥ 3:1 against every surface it overlays, including `button-primary-bg`. The colour-temperature rule narrows the candidates but the contrast requirement filters them.

## H3 — Lightest border that still passes 3:1

For `border-card`, `border-input`, `divider`, prefer the **lightest tone in the warm/cool family that still passes 3:1** against the surface — not "any tone that passes 3:1". Heavy borders look like wireframes; the goal is the subtlest visual separator that still meets the contrast threshold.

In practice: start with the lightest plausible neutral, compute the ratio, and only darken if it fails. Stop at the first passing value.

## H4 — Adjust the gradient, don't adjust the text

When the hero gradient cannot give the subtitle 4.5:1 contrast at the lightest stop, **darken the gradient** until it passes — do not switch the subtitle to a darker text colour or apply opacity tricks. The hero is the design element; the text is the message. Make the hero serve the message.

Anti-pattern: hero with bright primary at the top, subtitle rendered as `rgba(255,255,255,0.7)` "to make it softer". The contrast at the lightest stop fails 4.5:1; users with low vision see "vanishing text". Solid `hero-text` against a darker gradient ramp is the correct solution.

## H5 — Solid hero text, never opacity-modulated

`hero-text` is a solid colour (no `opacity`, no `rgba()` alpha). Opacity-on-white reads differently on each gradient stop, the contrast becomes position-dependent, and the value drifts as the gradient renders at different sizes. A single tested hex value validated against both stops is the contract.

## H6 — Status colours come from a separate axis

`success` / `warning` / `danger` are NOT derived from `primary` and `accent`. They live on their own functional axis (typically green / amber / red) regardless of the brand palette. A "Sage Olive" brand still has a red danger colour — using the brand olive for success and a darker olive for "warning" reads as a single state with shades, not as semantic distinction.

The exception is when `success` happens to coincide with the brand hue (an olive-green brand can use the brand green as `success` — they are perceptually the same colour). In that case make it explicit in the token table; do not silently overload.

## H7 — Three palettes, three distinct directions

When proposing three candidate palettes, each should represent a genuinely different design direction (not three saturations of the same hue). Example axes:

- **Tone**: classic / modern / playful
- **Temperature**: warm / cool / mixed
- **Brand colour family**: red-orange / green / yellow-gold (or whatever fits the product context)

Three "blue, slightly different blue, even more slightly different blue" palettes give the developer the illusion of choice with no real decision to make. The point of three candidates is to expose three viable identities; the developer picks the one that fits the brand, not the one with the prettiest header.

## H8 — Name each palette with a vibe + dominant colour

Every palette proposal carries a short name (2–4 words) that captures the vibe and dominant brand colour. Names like "Sage Olive", "Terracotta", "Saffron Gold" give the developer something to react to emotionally before they read the hex codes. Names like "Palette A" lose this signal.

## Where the heuristics apply

These run **inside `init-design-system` paso 3**, after the developer has provided any brand-colour hints, before the candidate `token_table`s are validated by `check-contrast` and `check-affordance`. The pipeline:

1. Read product context (`docs/plan.md`)
2. Read brand-colour hints from the developer (paso 3 prompt)
3. Apply heuristics H1–H8 to generate three distinct candidate palettes
4. Run `check-contrast` Mode 2 + `check-affordance` on each candidate
5. Drop candidates that fail accessibility; iterate generation
6. Present the surviving palettes with their vibe names and full audit results

The heuristics shape **which** candidates are generated. The contrast and affordance audits decide **which** are admissible.
