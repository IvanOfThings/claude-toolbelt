# check-plugin-coherence

Verifies that the dev-workflow plugin is internally consistent — rules, skills, commands, templates, and the marketplace manifest all reference each other correctly and the executors stay aligned with their declarative doctrine. Combines a fast mechanical pass (the `scripts/check-plugin-coherence.py` script) with LLM-driven semantic checks that the script cannot mechanize.

Invoked by `/plugin-coherence`. Also runs automatically as a pre-commit hook on any change under `plugin/**` or `.claude-plugin/**` (the hook only runs the mechanical pass — semantic checks need this skill).

## Steps

**1. Run the mechanical script**

Execute `python3 scripts/check-plugin-coherence.py` from the repository root. Capture its full stdout + stderr + exit code.

The script's checks (subset that is fully automatable):

1. Backticked `rules/...md` references resolve to a real file under `plugin/rules/`.
2. Every `Invoke \`<name>\`` in a command points to an existing `plugin/skills/<name>/SKILL.md`.
3. Every `plugin/commands/<name>.md` is mentioned somewhere in the top-level `README.md` (soft warning if missing).
4. Skills not referenced by any command, skill, or rule are surfaced as orphan warnings.
5. Rule files not referenced by any other rule, skill, or command are surfaced as orphan warnings.
6. `plugin/package.json` `name` is declared in `.claude-plugin/marketplace.json` and the declared `source` paths resolve.
7. Every token referenced in `check-contrast`'s canonical matrix (Mode 2 table rows only) is declared in `rules/templates/ui-design-tokens.md`.

Exit code 0 = mechanical PASS (with optional warnings). Exit code 1 = mechanical FAIL (errors found, block).

**2. Run semantic checks (LLM-driven)**

The script cannot judge intent. This step adds the soft layer.

For each doctrine ↔ executor pair below, read both files and verify the executor's behaviour matches what the doctrine says. Report any divergence as a finding.

| Doctrine                                              | Executor                                            |
|-------------------------------------------------------|-----------------------------------------------------|
| `rules/ui/interactive-affordance.md`                  | `skills/check-affordance/SKILL.md`                  |
| `rules/ui/interactive-affordance.md` (contrast pairs) | `skills/check-contrast/SKILL.md` (canonical matrix) |
| `rules/ui/palette-design-heuristics.md`               | `skills/init-design-system/SKILL.md` paso 3         |
| `rules/security/security-checklist.md`                | `skills/security-review-code/SKILL.md`              |
| `rules/code-quality/transaction-coordinator.md`       | `skills/quality-review/SKILL.md` (Gate 5 / 7)       |
| `rules/code-quality/code-quality.md` magic-string section | `skills/quality-review/SKILL.md` Gate 7         |
| `rules/workflow/verification-doc-format.md`            | `skills/diagnose-pr-failures/SKILL.md` + `skills/apply-pr-fixes/SKILL.md` |

Concrete questions to ask per pair:

- Does the executor implement every check listed in the doctrine? (Add a finding when the doctrine mentions a rule that the executor does not enforce.)
- Does the executor enforce checks that the doctrine does not declare? (Add a finding so the doctrine catches up.)
- Are check numbers / table rows aligned? (e.g. `check-affordance` documents 11 checks; `ui-design-tokens.md` Affordance Audit table must show 11 rows.)

**3. Run narrative-consistency checks (LLM-driven)**

Read these three documents and verify they describe the same plugin:

- `README.md` (repo root) — the public face
- `plugin/README.md` (if it exists) — plugin-level overview
- `CLAUDE.md` (repo root) — internal guidance for Claude in this repo

Surface any narrative drift: command lists, version numbers, install commands, supported workflows.

**4. Report**

Combine the script output + semantic findings + narrative findings into a single report. Format:

```
[plugin-coherence] Mechanical pass
  <verbatim script output>

[plugin-coherence] Semantic alignment
  doctrine ↔ executor:
    rules/ui/interactive-affordance.md ↔ skills/check-affordance:
      ✅ all 11 doctrine checks have executor implementations
      ⚠️  doctrine mentions "ghost button default fill" — executor check #11 covers it but rule is not numbered in interactive-affordance.md; consider adding an explicit "rule 11" cross-reference

  narrative drift:
    README.md ↔ CLAUDE.md:
      ⚠️  README lists 9 commands; CLAUDE.md mentions only 7 (missing: /plugin-coherence, /update-icons)

[plugin-coherence] FINAL — PASS / FAIL with totals
```

PASS if the mechanical pass exited 0 and no semantic ERROR-level findings.
FAIL if the script exited non-zero, or any semantic finding is severity ERROR.

WARNING-level findings (semantic or mechanical) never fail the run — they are advisory.

## When to run

- **Always automatically** — the pre-commit hook at `.githooks/pre-commit` runs the mechanical pass on every commit that touches `plugin/**` or `.claude-plugin/**`. Activate it once per clone with `git config core.hooksPath .githooks`.
- **Manually before any non-trivial plugin change is merged** — invoke `/plugin-coherence` to run the full skill (mechanical + semantic + narrative). The mechanical pass alone is not enough when adding a new rule, executor check, or skill that wires existing pieces in a new way.
- **After resolving merge conflicts** that touched plugin files — semantic alignment is a frequent casualty of conflict resolution.

## Why two layers

Mechanical checks are cheap, deterministic, and run on every commit — they catch broken cross-references and orphan rules before they reach `main`. Semantic checks are expensive (need LLM reasoning) and probabilistic — they catch the kind of drift the script cannot see (doctrine adds a rule and forgets to update the executor, or vice versa). Running both as one skill keeps the report unified; running only the mechanical layer as a pre-commit hook keeps commits fast.
