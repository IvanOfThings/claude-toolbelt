# update-icons

Scans the current branch for icon imports not yet catalogued in `docs/icons.html` and adds them. Lightweight — does not regenerate the full design system.

## Steps

**1. Read current catalog**

Read `docs/icons.html`. Extract the list of icon names currently in the catalog (from the icon name labels in the grid).

If `docs/icons.html` does not exist: report it and suggest running `/init-design-system` first. Stop.

**2. Scan branch for new icon imports**

Run `git diff main --name-only` to find changed source files.

For each changed file, scan for icon imports matching the project's icon library pattern. Determine which library is in use from `.claude/rules/ui.md`:

- **Lucide** (shadcn/ui): `import { IconName } from "lucide-react"`
- **Heroicons** (DaisyUI): `import { IconNameIcon } from "@heroicons/react/..."`
- **Tabler Icons** (Mantine): `import { IconName } from "@tabler/icons-react"`
- **Flowbite Icons**: `<Icon name="icon-name" />`

Collect all icon names not present in the current catalog.

**3. Add new icons**

For each uncatalogued icon:
- Determine the appropriate category (Navigation, Actions, Status, Communication, Data — or add to a "Domain-specific" section if none fits)
- Add a grid cell to `docs/icons.html` in the correct category section with:
  - Visual preview
  - Icon name
  - Copy-ready usage snippet matching the project's library

**4. Output**

Report: number of icons added, their names, and which categories they landed in.

If no new icons found: output `[update-icons] No uncatalogued icons found in this branch.`
