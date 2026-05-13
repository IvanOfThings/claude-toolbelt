# /init-design-system

Generates or regenerates the project's visual design system: component library, color palette, design-system.html, icons.html, and .claude/rules/ui.md.

**Usage:** `/init-design-system`

Run this as part of `init-project` (Step 4) or standalone to update an existing design system — for example, to change the component library or refresh the color palette.

---

Invoke `init-design-system`.

The skill is interactive: it reads `docs/plan.md` for product context, presents component library options, proposes three contextualised color palettes, and generates all output files after developer selections.
