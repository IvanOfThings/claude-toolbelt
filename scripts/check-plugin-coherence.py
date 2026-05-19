#!/usr/bin/env python3
"""Plugin coherence checker — fast, deterministic subset.

Runs as a pre-commit hook against the working-tree state of plugin/** and
.claude-plugin/**. Exits 0 on PASS, 1 on FAIL. WARN entries are reported but
do not fail. The list of checks is intentionally mechanical — pattern matches,
file existence, JSON alignment.

For deeper semantic checks (doctrine ↔ executor alignment, narrative
consistency), invoke /plugin-coherence interactively. That command uses the
check-plugin-coherence skill which layers LLM reasoning on top of this output.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import defaultdict

REPO = pathlib.Path(__file__).resolve().parent.parent
PLUGIN = REPO / "plugin"
MARKETPLACE = REPO / ".claude-plugin" / "marketplace.json"
README = REPO / "README.md"

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def rel(p: pathlib.Path) -> str:
    return str(p.relative_to(REPO))


def list_skills() -> set[str]:
    return {p.parent.name for p in (PLUGIN / "skills").rglob("SKILL.md")}


def list_commands() -> set[str]:
    return {p.stem for p in (PLUGIN / "commands").glob("*.md") if p.stem != "README"}


def list_rule_files() -> set[pathlib.Path]:
    return set((PLUGIN / "rules").rglob("*.md"))


def list_all_md_under_plugin() -> list[pathlib.Path]:
    return list(PLUGIN.rglob("*.md"))


# ---------------------------------------------------------------------------
# Check 1: backticked rule-file references resolve
# ---------------------------------------------------------------------------

RULE_REF = re.compile(r"`(rules/[A-Za-z0-9_/-]+\.md)`")


def check_rule_references() -> None:
    for md in list_all_md_under_plugin():
        try:
            lines = md.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(lines, 1):
            for m in RULE_REF.finditer(line):
                ref = m.group(1)
                target = PLUGIN / ref
                if not target.is_file():
                    err(f"{rel(md)}:{n} references `{ref}` → no file at {rel(target)}")


# ---------------------------------------------------------------------------
# Check 2: skill invocations in commands resolve to real skills
# ---------------------------------------------------------------------------

# Matches "Invoke `name`", "invokes `name`", "invoke the `name` skill", etc.
SKILL_INVOKE = re.compile(r"[Ii]nvoke(?:s)?\s+(?:the\s+)?`([a-z][a-z0-9-]*)`")


def check_skill_invocations() -> None:
    skills = list_skills()
    for md in (PLUGIN / "commands").rglob("*.md"):
        try:
            lines = md.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(lines, 1):
            for m in SKILL_INVOKE.finditer(line):
                name = m.group(1)
                # External skills look like "namespace:name"; SKILL_INVOKE
                # already excludes them because ':' is not in the char class.
                if name in skills:
                    continue
                # Heuristic skip: very short names ("the", "a") slip through
                if len(name) < 3:
                    continue
                err(
                    f"{rel(md)}:{n} invokes skill `{name}` → no "
                    f"plugin/skills/{name}/SKILL.md"
                )


# ---------------------------------------------------------------------------
# Check 3: every plugin/commands/<name>.md exists in README mentions (soft)
# ---------------------------------------------------------------------------

README_CMD = re.compile(r"/([a-z][a-z0-9-]*)\b")


def check_commands_in_readme() -> None:
    if not README.exists():
        warn("no README.md at repo root")
        return
    mentioned = set(README_CMD.findall(README.read_text(encoding="utf-8")))
    for cmd in list_commands():
        if cmd not in mentioned:
            warn(f"command `/{cmd}` is not mentioned anywhere in README.md")


# ---------------------------------------------------------------------------
# Check 4: orphan skills (not referenced from any command, skill, or rule)
# ---------------------------------------------------------------------------


def check_orphan_skills() -> None:
    skills = list_skills()
    referenced: set[str] = set()
    for md in list_all_md_under_plugin():
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        # Exclude self-references (a skill mentioning its own name in its own SKILL.md)
        self_skill = md.parent.name if md.name == "SKILL.md" else None
        for skill in skills:
            if skill == self_skill:
                continue
            if re.search(r"`" + re.escape(skill) + r"`", text):
                referenced.add(skill)
                continue
            # Also match unquoted bare name inside path-like context, e.g. "plugin/skills/<name>/"
            if f"plugin/skills/{skill}/" in text:
                referenced.add(skill)
    orphans = skills - referenced
    for skill in sorted(orphans):
        warn(
            f"skill `{skill}` is not referenced by any command, other skill, or rule"
            " — orphan or only invoked dynamically?"
        )


# ---------------------------------------------------------------------------
# Check 5: orphan rules (rule files not referenced anywhere in the plugin)
# ---------------------------------------------------------------------------


def check_orphan_rules() -> None:
    rules = list_rule_files()
    referenced: set[pathlib.Path] = set()
    for md in list_all_md_under_plugin():
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for rule in rules:
            ref = rule.relative_to(PLUGIN).as_posix()
            if ref in text and md != rule:
                referenced.add(rule)
    orphans = rules - referenced
    for rule in sorted(orphans, key=lambda p: p.as_posix()):
        warn(
            f"rule `{rel(rule)}` is not referenced by any other rule, skill, or command"
        )


# ---------------------------------------------------------------------------
# Check 6: marketplace.json alignment with plugin/package.json
# ---------------------------------------------------------------------------


def check_marketplace_alignment() -> None:
    pkg_path = PLUGIN / "package.json"
    if not pkg_path.is_file():
        err(f"missing {rel(pkg_path)}")
        return
    pkg = json.loads(pkg_path.read_text(encoding="utf-8"))

    if not MARKETPLACE.is_file():
        warn(f"no {rel(MARKETPLACE)} — plugin not installable as a marketplace")
        return
    try:
        mk = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"{rel(MARKETPLACE)} is not valid JSON: {e}")
        return

    plugins = mk.get("plugins", [])
    if not plugins:
        err(f"{rel(MARKETPLACE)} has no `plugins` array")
        return

    declared = {p.get("name") for p in plugins}
    if pkg.get("name") not in declared:
        err(
            f"{rel(pkg_path)} name `{pkg.get('name')}` is not in"
            f" {rel(MARKETPLACE)} plugins ({sorted(declared)})"
        )

    for p in plugins:
        src = p.get("source")
        if isinstance(src, str):
            target = (REPO / src.lstrip("./")).resolve()
            if not target.is_dir():
                err(
                    f"{rel(MARKETPLACE)} plugin `{p.get('name')}` source `{src}`"
                    f" → directory not found"
                )


# ---------------------------------------------------------------------------
# Check 7: template ↔ check-contrast canonical-matrix token alignment
# ---------------------------------------------------------------------------


def check_template_token_alignment() -> None:
    """Every token referenced in check-contrast's canonical matrix is declared
    in the ui-design-tokens template (and vice versa, as a warning)."""
    matrix_path = PLUGIN / "skills" / "check-contrast" / "SKILL.md"
    template_path = PLUGIN / "rules" / "templates" / "ui-design-tokens.md"
    if not matrix_path.is_file() or not template_path.is_file():
        return

    matrix_text = matrix_path.read_text(encoding="utf-8")
    template_text = template_path.read_text(encoding="utf-8")

    # Restrict the search to the "Canonical matrix" section.
    canonical_match = re.search(
        r"## Canonical matrix \(Mode 2\)(.*?)(?=\n## |\Z)",
        matrix_text,
        flags=re.DOTALL,
    )
    if not canonical_match:
        return
    canonical = canonical_match.group(1)

    # Only look at table rows (lines starting with `|`) — avoids picking up
    # tokens mentioned in the prose around the table.
    table_rows = "\n".join(
        line for line in canonical.splitlines() if line.lstrip().startswith("|")
    )
    matrix_tokens = set(re.findall(r"`([a-z][a-z0-9-]*)`", table_rows))
    # Only consider design-token-shaped names (kebab with at least one dash or
    # one of the well-known single-word tokens).
    design_tokens = {
        t for t in matrix_tokens if "-" in t or t in {"primary", "accent", "divider"}
    }

    template_tokens = set(re.findall(r"`([a-z][a-z0-9-]*)`", template_text))

    missing_in_template = design_tokens - template_tokens
    for t in sorted(missing_in_template):
        err(
            f"check-contrast canonical matrix references token `{t}` but the"
            f" ui-design-tokens template does not declare it"
        )


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


CHECKS = [
    ("Rule references resolve", check_rule_references),
    ("Skill invocations resolve", check_skill_invocations),
    ("Commands mentioned in README", check_commands_in_readme),
    ("Orphan skills", check_orphan_skills),
    ("Orphan rules", check_orphan_rules),
    ("Marketplace ↔ package.json alignment", check_marketplace_alignment),
    ("Template ↔ check-contrast token alignment", check_template_token_alignment),
]


def main() -> int:
    print("[plugin-coherence] Running mechanical checks against working tree...")
    for label, fn in CHECKS:
        before_err = len(errors)
        before_warn = len(warnings)
        fn()
        added_err = len(errors) - before_err
        added_warn = len(warnings) - before_warn
        status = "✅"
        if added_err:
            status = f"❌ {added_err} error{'s' if added_err != 1 else ''}"
        elif added_warn:
            status = f"⚠️  {added_warn} warning{'s' if added_warn != 1 else ''}"
        print(f"  {status:<25} {label}")

    print()
    if errors:
        print(
            f"[plugin-coherence] FAIL — {len(errors)} error(s),"
            f" {len(warnings)} warning(s)"
        )
        print()
        print("Errors (block commit):")
        for e in errors:
            print(f"  ❌ {e}")
        if warnings:
            print()
            print("Warnings (review, optional fix):")
            for w in warnings:
                print(f"  ⚠️  {w}")
        return 1
    print(
        f"[plugin-coherence] PASS — 0 errors, {len(warnings)} warning(s)"
    )
    if warnings:
        print()
        print("Warnings (review, optional fix):")
        for w in warnings:
            print(f"  ⚠️  {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
