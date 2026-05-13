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
- Standard: [.claude/rules/ui.md]

## Dev commands
```bash
[build, dev, test commands from brainstorm]
```
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
- `architecture.md` — read `rules/templates/architecture-layers.md` from the plugin and fill in project-specific layer definitions (paths, rules, forbidden patterns)
- `testing.md` — test strategy, mock approach, coverage expectations
- `ui.md` — read `rules/templates/ui-design-tokens.md` from the plugin and fill in the token names (values will be completed by `init-design-system`)
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
- `docs/plan.md` — already created by `init-brainstorm`; do not recreate or overwrite
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
