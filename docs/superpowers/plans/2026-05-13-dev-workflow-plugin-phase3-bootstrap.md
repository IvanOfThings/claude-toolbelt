# Dev Workflow Plugin — Phase 3: Project Bootstrap

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the project bootstrap commands (init-project, init-design-system, update-icons) and their 6 supporting skills, plus wire i18n-compliance into the existing quality-review skill.

**Architecture:** Pure markdown content — SKILL.md files in `plugin/skills/<name>/` and command orchestrators in `plugin/commands/`. One existing skill (quality-review) gets a new Gate 6. All new skills reference Phase 1 rules already on disk. This completes the plugin; after Phase 3 the full framework is installable.

**Tech Stack:** Markdown, Claude Code plugin format, git

**Specs:** `docs/superpowers/specs/2026-05-13-dev-workflow-plugin-design.md` (main), `docs/superpowers/specs/2026-05-13-dev-workflow-plugin-ui-addendum-design.md` (addendum)

---

## File Structure

```
plugin/
├── commands/
│   ├── init-project.md          ← 6-step bootstrap orchestrator (NEW)
│   ├── init-design-system.md    ← standalone design system command (NEW)
│   └── update-icons.md          ← lightweight icon catalog update (NEW)
└── skills/
    ├── init-brainstorm/SKILL.md       ← superpowers:brainstorming wrapper + i18n questions (NEW)
    ├── init-scaffold/SKILL.md         ← creates full project structure + locales/ (NEW)
    ├── init-generate-specs/SKILL.md   ← ordered feature specs + queue.json (NEW)
    ├── init-design-system/SKILL.md    ← library + palette + design-system.html + icons.html (NEW)
    ├── update-icons/SKILL.md          ← scans branch for new icons, updates icons.html (NEW)
    ├── i18n-compliance/SKILL.md       ← scans modified files for i18n violations (NEW)
    └── quality-review/SKILL.md        ← MODIFIED: add Gate 6 (i18n-compliance)
```

---

## Task 1: Bootstrap conversation skills (init-brainstorm, init-scaffold)

**Files:**
- Create: `plugin/skills/init-brainstorm/SKILL.md`
- Create: `plugin/skills/init-scaffold/SKILL.md`

- [ ] **Step 1: Create skill subdirectories**

```bash
mkdir -p plugin/skills/init-brainstorm plugin/skills/init-scaffold
```

- [ ] **Step 2: Write plugin/skills/init-brainstorm/SKILL.md**

```markdown
# init-brainstorm

Leads an interactive brainstorming session to define the project's functional design, architecture, and technical setup before any scaffolding begins.

Wraps `superpowers:brainstorming` with project bootstrap context.

## Input

`doc-path` (optional): path to an input document describing features and goals. If provided, use it as starting context.

## Steps

**1. Invoke superpowers:brainstorming**

Use `superpowers:brainstorming` with the input document (if provided) as context.

Explore through conversation:
- Product goals and target users
- Key features (functional scope)
- Tech stack preferences (framework, database, auth, deployment)
- Architecture style (monolith vs services, API-first vs fullstack)
- Design system direction (minimalist, full-featured, brand-heavy)

Follow the brainstorming skill's process: explore → clarify → propose approaches → present design sections → approve.

**2. Technical setup questions (after functional design is approved)**

After the developer approves the high-level functional design, ask two technical questions before closing:

**Question 1 — i18n library:**
```
Which i18n library will this project use?
1. next-intl (recommended for Next.js)
2. i18next / react-i18next
3. LinguiJS
4. None — single language only
```

**Question 2 — Project languages:**
```
What locales will this project support?
- Default locale: [e.g. es, en, fr]
- Additional locales: [list, or "none"]
```

**3. Record technical setup**

Add a `## Technical Setup` section to `docs/plan.md` (the plan file produced by brainstorming):

```markdown
## Technical Setup

- **i18n library:** [chosen library or "none"]
- **Default locale:** [e.g. es]
- **Additional locales:** [list or "none"]
```

**4. Output**

Return:
- Approved high-level design summary (features, architecture, stack)
- i18n library and locales chosen
- Path to docs/plan.md
```

- [ ] **Step 3: Write plugin/skills/init-scaffold/SKILL.md**

```markdown
# init-scaffold

Creates the standardized project structure after brainstorm approval. Uses brainstorm answers to populate project-specific files.

## Input

From `init-brainstorm` output:
- Project name, stack, architecture layers
- i18n library and default/additional locales
- Feature list (for generating translation file stubs)

## Steps

**1. Create directory structure**

```bash
mkdir -p .claude/rules
mkdir -p docs/mockups
mkdir -p docs/superpowers/plans
mkdir -p docs/superpowers/specs/refined/done
mkdir -p docs/superpowers/verification/verified
mkdir -p locales/<default-locale>
# For each additional locale:
mkdir -p locales/<additional-locale>
```

Skip locales/ entirely if i18n library is "None".

**2. Create CLAUDE.md**

Generate using the canonical template — must stay under 100 lines:

```markdown
# [Project Name]

[One sentence: what it does and for whom.]

## Stack
- [line per technology from brainstorm]
- Architecture: [.claude/rules/architecture.md]

## Rules
- Code: [.claude/rules/coding.md]
- Tests: [.claude/rules/testing.md]
- UI: [.claude/rules/ui.md]
- Observability: [.claude/rules/observability.md]
- Commits: never automatic — only when the developer explicitly asks

## Documentation
- Plan: [docs/plan.md]
- Features: [docs/features.md]
- Architecture: [docs/arch.md]
- Database: [docs/db.md]
- API: [docs/api.md]
- Mockups: [docs/mockups/]
- Design system: [docs/design-system.html]
- Icon catalog: [docs/icons.html]
- Implementation tracker: [IMPLEMENTATION.md]

## i18n
- Library: [chosen library]
- Default locale: [locale]
- Additional locales: [list or "none"]
- Translation files: [locales/]
- Standard: [.claude/rules/ui/i18n.md]

## Dev commands
```bash
[build, dev, test commands from brainstorm]
```

## Workflow
- New feature or bugfix: `/dev-cycle <description>`
- Process a change document: `/refine <path>`
- Generate verification docs: `/generate-verification`

## Dependencies
### Required plugins
- superpowers, frontend-design, vercel, honeycomb

### Required MCPs
- honeycomb: `claude mcp add honeycomb` + env var `HONEYCOMB_API_KEY`
[project-specific MCPs from brainstorm]
```

**3. Create IMPLEMENTATION.md**

```markdown
# Implementation Tracker

🎯 **Current sprint:** Sprint 1

| Task | Impl. | Tests | Local | Prod |
|------|-------|-------|-------|------|
| [First feature from brainstorm] | ⬜ | ⬜ | ⬜ | ⬜ |
```

**4. Create .claude/rules/ files**

Populate from brainstorm answers:

- `coding.md` — TypeScript/language standards, linting config, naming conventions
- `architecture.md` — fill the `architecture-layers.md` template with project-specific layer definitions (paths, rules, forbidden patterns)
- `testing.md` — test strategy, mock approach, coverage expectations
- `ui.md` — start with the `ui-design-tokens.md` template (tokens will be filled in by `init-design-system`)
- `observability.md` — error tracker and tracing setup for this project (which library, env vars, dataset names)

**5. Create docs/ files**

- `docs/README.md` — documentation index, one line per declared doc:
  ```markdown
  ## Documentation index
  - [plan.md](plan.md) — high-level feature design and architecture decisions
  - [features.md](features.md) — current feature inventory with behaviour descriptions
  - [arch.md](arch.md) — system architecture diagram and layer descriptions
  - [db.md](db.md) — database schema and entity relationships
  - [api.md](api.md) — API routes, request/response shapes, auth requirements
  ```
- `docs/plan.md` — copy from brainstorm output (already produced by `init-brainstorm`)
- `docs/features.md` — initial feature list from brainstorm, each with a one-line description
- `docs/arch.md` — architecture description from brainstorm
- `docs/db.md` — initial data model stub: "Schema defined during Sprint 1 implementation"
- `docs/api.md` — empty stub: "API surface defined during development"

**6. Create locales/ structure** (skip if i18n is "None")

For the default locale, create `common.json` plus one JSON file per feature area from the brainstorm:

`locales/<default-locale>/common.json`:
```json
{
  "actions": {
    "save": "[Translation needed]",
    "cancel": "[Translation needed]",
    "delete": "[Translation needed]",
    "edit": "[Translation needed]"
  },
  "errors": {
    "generic": "[Translation needed]",
    "notFound": "[Translation needed]",
    "unauthorized": "[Translation needed]"
  }
}
```

For each feature from brainstorm, `locales/<default-locale>/<feature-slug>.json`:
```json
{
  "<feature-slug>": {
    "title": "[Translation needed]",
    "description": "[Translation needed]"
  }
}
```

Replicate the same file structure for each additional locale.

**7. Output**

Report all files and directories created. State that `init-design-system` will populate `docs/design-system.html`, `docs/icons.html`, and finalize `.claude/rules/ui.md`.
```

- [ ] **Step 4: Verify files**

```bash
ls plugin/skills/init-brainstorm/ plugin/skills/init-scaffold/
```

Expected: `SKILL.md` in each directory.

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/init-brainstorm/ plugin/skills/init-scaffold/
git commit -m "feat(plugin/skills): add init-brainstorm and init-scaffold skills"
```

---

## Task 2: Feature spec generation skill + /init-project command

**Files:**
- Create: `plugin/skills/init-generate-specs/SKILL.md`
- Create: `plugin/commands/init-project.md`

- [ ] **Step 1: Create skill subdirectory**

```bash
mkdir -p plugin/skills/init-generate-specs
```

- [ ] **Step 2: Write plugin/skills/init-generate-specs/SKILL.md**

```markdown
# init-generate-specs

Generates ordered refinement specs for every feature in the approved high-level design. Creates a `/refine`-ready queue.

## Input

From `init-brainstorm` output: feature list with descriptions, tech stack, architecture layers.

## Steps

**1. Read docs/plan.md**

Extract the complete feature list from the approved design. Each feature becomes one mini-spec.

**2. Order by implementation dependency**

Group features into implementation layers before speccing:
- Layer 1: Data model / schema definitions
- Layer 2: Service layer / business logic
- Layer 3: API routes / server actions
- Layer 4: UI components / pages
- Layer 5: Cross-cutting integration features

Foundational features first. A UI feature cannot be specced before the API it depends on.

**3. Generate mini-spec files**

For each feature, create `docs/superpowers/specs/refined/YYYY-MM-DD-<feature-slug>.md`:

```markdown
# [Feature name]

**Type:** feature
**Summary:** [1-2 sentences from brainstorm description]

## Acceptance criteria
- [Specific, testable outcome from brainstorm]
- [Mobile-first: layout works at 390px]
- [i18n: all user-visible strings in locales/]

## Affected areas
- [Inferred from stack: e.g. src/app/api/..., src/components/..., src/services/...]

## Dependencies
- [Other feature slugs that must be completed first, or "none"]

## Constraints
- [ ] Mobile-first required
- [ ] i18n strings required
- [ ] DB migration needed
- [ ] New tracing spans needed
```

**4. Generate queue.json**

Create `docs/superpowers/specs/refined/queue.json`:

```json
{
  "pending": ["<slug-1>", "<slug-2>", "<slug-3>"],
  "done": []
}
```

Order of slugs in `pending` matches the dependency order from Step 2.

**5. Output**

Report: number of specs generated, path to queue.json, first slug in the queue (the first feature to build).
```

- [ ] **Step 3: Write plugin/commands/init-project.md**

```markdown
# /init-project

Bootstraps a new project: brainstorming → scaffold → design system → feature specs.

**Usage:** `/init-project [doc-path]`

`doc-path` is optional. If provided, `init-brainstorm` uses it as input context for the brainstorming session. If omitted, brainstorming starts with open-ended questions.

---

## Step 1 — Dependency check

Invoke `check-dependencies` with scope `framework`.

If framework dependencies are missing: show the report and ask the developer to install them before continuing.

---

## Step 2 — Brainstorm

Invoke `init-brainstorm` with `doc-path` (if provided).

**GATE:** The brainstorming session ends with the developer approving the high-level design and answering the i18n setup questions. Do not proceed until explicit approval is received.

---

## Step 3 — Scaffold

Invoke `init-scaffold` with the brainstorm output (project name, stack, features, i18n library and locales).

---

## Step 4 — Design system

Invoke `init-design-system`.

This step is interactive: the developer selects a component library and approves a color palette. The step completes when `docs/design-system.html`, `docs/icons.html`, and `.claude/rules/ui.md` are generated.

---

## Step 5 — High-level plan

`docs/plan.md` was produced during `init-brainstorm`. If it does not exist, invoke `write-plan` to generate it from the brainstorm summary.

---

## Step 6 — Generate feature specs

Invoke `init-generate-specs`.

Output: ordered queue of mini-specs in `docs/superpowers/specs/refined/` and `queue.json`.

Show the developer the queue and the first item. The project is now ready — use `/refine docs/superpowers/specs/refined/queue.json` to begin building, or `/dev-cycle <description>` to start any individual feature.
```

- [ ] **Step 4: Verify files**

```bash
ls plugin/skills/init-generate-specs/
ls plugin/commands/init-project.md
```

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/init-generate-specs/ plugin/commands/init-project.md
git commit -m "feat(plugin): add init-generate-specs skill and init-project command"
```

---

## Task 3: Design system skill + /init-design-system command

**Files:**
- Create: `plugin/skills/init-design-system/SKILL.md`
- Create: `plugin/commands/init-design-system.md`

- [ ] **Step 1: Create skill subdirectory**

```bash
mkdir -p plugin/skills/init-design-system
```

- [ ] **Step 2: Write plugin/skills/init-design-system/SKILL.md**

```markdown
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

Fill the `ui-design-tokens.md` template with the resolved values for this project:

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
```

- [ ] **Step 3: Write plugin/commands/init-design-system.md**

```markdown
# /init-design-system

Generates or regenerates the project's visual design system: component library, color palette, design-system.html, icons.html, and .claude/rules/ui.md.

**Usage:** `/init-design-system`

Run this as part of `init-project` (Step 4) or standalone to update an existing design system — for example, to change the component library or refresh the color palette.

---

Invoke `init-design-system`.

The skill is interactive: it reads `docs/plan.md` for product context, presents component library options, proposes three contextualised color palettes, and generates all output files after developer selections.
```

- [ ] **Step 4: Verify files**

```bash
ls plugin/skills/init-design-system/
ls plugin/commands/init-design-system.md
```

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/init-design-system/ plugin/commands/init-design-system.md
git commit -m "feat(plugin): add init-design-system skill and command"
```

---

## Task 4: Icon update skill + /update-icons command

**Files:**
- Create: `plugin/skills/update-icons/SKILL.md`
- Create: `plugin/commands/update-icons.md`

- [ ] **Step 1: Create skill subdirectory**

```bash
mkdir -p plugin/skills/update-icons
```

- [ ] **Step 2: Write plugin/skills/update-icons/SKILL.md**

```markdown
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
```

- [ ] **Step 3: Write plugin/commands/update-icons.md**

```markdown
# /update-icons

Scans the current branch for icon imports not yet in `docs/icons.html` and adds them.

**Usage:** `/update-icons`

Use this after a `dev-cycle` that introduced new icons. The `update-docs` skill flags uncatalogued icons with a ⚠ notice — run this command to resolve it.

For a full regeneration of the icon catalog (e.g. after switching component library), use `/init-design-system` instead.

---

Invoke `update-icons`.
```

- [ ] **Step 4: Verify files**

```bash
ls plugin/skills/update-icons/
ls plugin/commands/update-icons.md
```

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/update-icons/ plugin/commands/update-icons.md
git commit -m "feat(plugin): add update-icons skill and command"
```

---

## Task 5: i18n-compliance skill + update quality-review (Gate 6)

**Files:**
- Create: `plugin/skills/i18n-compliance/SKILL.md`
- Modify: `plugin/skills/quality-review/SKILL.md` (add Gate 6)

- [ ] **Step 1: Create skill subdirectory**

```bash
mkdir -p plugin/skills/i18n-compliance
```

- [ ] **Step 2: Write plugin/skills/i18n-compliance/SKILL.md**

```markdown
# i18n-compliance

Scans files modified in the current branch for i18n violations. Called automatically by `quality-review` as Gate 6.

## Steps

**1. Read i18n standard**

Read `rules/ui/i18n.md` from the plugin.

**2. Find modified files**

Run `git diff main --name-only` and filter for source files (`.ts`, `.tsx`, `.js`, `.jsx`, `.vue`, `.svelte`).

If no source files modified: output `[i18n] PASS — no source files changed.` and stop.

**3. Scan for violations**

For each modified source file, check:

| Violation | Severity | Detection pattern |
|-----------|----------|-------------------|
| Hardcoded user-visible string in JSX or template | HIGH | String literal inside a JSX element or translatable attribute (e.g. `<p>"Guardar cambios"</p>`, `placeholder="Enter name"`) |
| Hardcoded locale in `Intl` API call | HIGH | `toLocaleDateString('es-ES')`, `new Intl.DateTimeFormat('en-US')` with literal locale string |
| Missing translation key (used in code, absent in `locales/`) | HIGH | `t('some.key')` where `some.key` does not appear in any JSON file under `locales/` |
| Inline plural ternary | MEDIUM | `` `${n} item${n === 1 ? '' : 's'}` `` or `n === 1 ? "jugador" : "jugadores"` |
| Date or number without locale parameter | LOW | `new Date().toLocaleDateString()` with no locale argument |

**4. Output**

```
[i18n] PASS

or

[i18n] VIOLATIONS FOUND

  [HIGH] src/components/poll-card.tsx:34
  Hardcoded string: "Encuesta abierta"
  → Move to locales/<default-locale>/polls.json: polls.status.open

  [MEDIUM] src/components/squad-list.tsx:67
  Inline plural: `${count} jugador${count === 1 ? '' : 'es'}`
  → Use: t('squad.players', { count })
```

Any HIGH violation blocks the PR. MEDIUM and LOW are presented to the developer who decides whether to fix before merge.
```

- [ ] **Step 3: Read the current quality-review SKILL.md**

Read `plugin/skills/quality-review/SKILL.md` to confirm the current content before editing.

- [ ] **Step 4: Add Gate 6 to quality-review SKILL.md**

The current SKILL.md has 5 gates ending with Gate 5 (Security) and an output format section. Add Gate 6 between Gate 5 and the output format section, and update the output format to reference 6 gates:

After the Gate 5 block (which ends with "CRITICAL issues block merging..."), add:

```markdown
**Gate 6: i18n compliance**

Invoke `i18n-compliance` skill (reads `rules/ui/i18n.md` against modified source files in `git diff main`).

Any HIGH violation blocks proceeding. MEDIUM and LOW are presented to the developer who decides.
```

Update the output format header from `PASS — all 5 gates passed` to `PASS — all 6 gates passed`.

- [ ] **Step 5: Verify**

```bash
ls plugin/skills/i18n-compliance/
grep "Gate 6" plugin/skills/quality-review/SKILL.md
```

Expected: `SKILL.md` exists and `Gate 6` appears in quality-review.

- [ ] **Step 6: Commit**

```bash
git add plugin/skills/i18n-compliance/ plugin/skills/quality-review/SKILL.md
git commit -m "feat(plugin): add i18n-compliance skill and wire into quality-review Gate 6"
```

---

## Task 6: Verify complete plugin structure

- [ ] **Step 1: Verify all skill SKILL.md files**

```bash
find plugin/skills -name "SKILL.md" | sort
```

Expected (19 files):
```
plugin/skills/analyze-context/SKILL.md
plugin/skills/apply-pr-fixes/SKILL.md
plugin/skills/check-dependencies/SKILL.md
plugin/skills/decompose-refinement/SKILL.md
plugin/skills/diagnose-pr-failures/SKILL.md
plugin/skills/generate-verification-doc/SKILL.md
plugin/skills/i18n-compliance/SKILL.md
plugin/skills/implement-agentic/SKILL.md
plugin/skills/init-brainstorm/SKILL.md
plugin/skills/init-design-system/SKILL.md
plugin/skills/init-generate-specs/SKILL.md
plugin/skills/init-scaffold/SKILL.md
plugin/skills/quality-review/SKILL.md
plugin/skills/security-review-code/SKILL.md
plugin/skills/security-review-plan/SKILL.md
plugin/skills/update-docs/SKILL.md
plugin/skills/update-icons/SKILL.md
plugin/skills/update-mockups/SKILL.md
plugin/skills/write-plan/SKILL.md
```

- [ ] **Step 2: Verify all command files**

```bash
find plugin/commands -name "*.md" | sort
```

Expected (9 files):
```
plugin/commands/dev-cycle.md
plugin/commands/generate-verification.md
plugin/commands/init-design-system.md
plugin/commands/init-project.md
plugin/commands/refine.md
plugin/commands/security-review.md
plugin/commands/ui-contrast.md
plugin/commands/update-icons.md
plugin/commands/verify-pr.md
```

- [ ] **Step 3: Verify all rule files still present**

```bash
find plugin/rules -name "*.md" | wc -l
```

Expected: `22`

- [ ] **Step 4: Check Gate 6 in quality-review**

```bash
grep -c "Gate 6" plugin/skills/quality-review/SKILL.md
```

Expected: `1`

- [ ] **Step 5: Check package.json**

```bash
cat plugin/package.json
```

Expected: `"name": "dev-workflow"`, `"version": "0.1.0"`

- [ ] **Step 6: Tag phase 3 and summarise**

```bash
git tag phase3-bootstrap
git log --oneline -6
```

Verify the last 6 commits cover all Phase 3 tasks.

---

## Self-review notes

**Spec coverage:**
- ✅ init-brainstorm — superpowers:brainstorming wrapper + i18n questions after functional approval
- ✅ init-scaffold — full directory structure, CLAUDE.md (<100 lines), locales/ with feature stubs
- ✅ init-generate-specs — ordered mini-specs per feature, dependency layering, queue.json
- ✅ init-design-system — interactive library + palette selection, design-system.html, icons.html, .claude/rules/ui.md
- ✅ update-icons — branch scan per icon library, catalog update, no full regen
- ✅ i18n-compliance — HIGH/MEDIUM/LOW violations, HIGH blocks PR, called from quality-review
- ✅ /init-project — 6-step orchestrator: check-deps → brainstorm → scaffold → design-system → plan → specs
- ✅ /init-design-system — standalone command wrapping init-design-system skill
- ✅ /update-icons — thin command wrapping update-icons skill
- ✅ quality-review Gate 6 — i18n-compliance added, output updated to "6 gates"
- ✅ CLAUDE.md template includes i18n section (library, default locale, additional locales)
- ✅ init-scaffold i18n questions → locales/ creation wired from init-brainstorm output

**Not in any phase (out of scope):**
- Actual HTML generation for design-system.html / icons.html (runtime work done by the skill when invoked)
- Migration of team-manager to use the plugin (separate task, documented in main spec)
