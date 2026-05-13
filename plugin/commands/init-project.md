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
