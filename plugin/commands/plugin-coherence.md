# /plugin-coherence

Verifies that the dev-workflow plugin is internally consistent — rule references resolve, skill invocations point to real skills, executors stay aligned with their doctrine, marketplace manifest matches `plugin/package.json`, and the README narrative still describes the truth.

**Usage:** `/plugin-coherence`

No arguments — the command always audits the current working-tree state of the repository.

---

## Step 1 — Invoke the skill

Invoke `check-plugin-coherence`.

The skill runs in three stages:

1. **Mechanical pass** — `scripts/check-plugin-coherence.py`. Fast, deterministic; catches broken cross-references, orphans, marketplace ↔ package.json drift, template ↔ canonical-matrix drift.
2. **Semantic alignment** — LLM reads each doctrine ↔ executor pair (e.g. `interactive-affordance.md` ↔ `check-affordance` skill) and verifies the executor implements every doctrine rule and vice versa.
3. **Narrative consistency** — LLM checks that `README.md`, `plugin/README.md`, and `CLAUDE.md` describe the same plugin.

---

## Step 2 — Output

The skill returns a unified report. Errors block (anything that would prevent the plugin from working correctly when installed). Warnings are advisory.

---

## When this runs automatically

The mechanical pass (only) also runs as a **pre-commit hook** on any change under `plugin/**` or `.claude-plugin/**`. Activate it once per clone with:

```bash
git config core.hooksPath .githooks
```

The hook covers fast structural checks. The full skill (semantic + narrative) needs an LLM and runs only when you invoke `/plugin-coherence` manually — recommended after adding a new rule, skill, command, or non-trivial executor change, and before merging a plugin-evolution PR.
