# /update-icons

Scans the current branch for icon imports not yet in `docs/icons.html` and adds them.

**Usage:** `/update-icons`

Use this after a `dev-cycle` that introduced new icons. The `update-docs` skill flags uncatalogued icons with a ⚠ notice — run this command to resolve it.

For a full regeneration of the icon catalog (e.g. after switching component library), use `/init-design-system` instead.

---

Invoke `update-icons`.
