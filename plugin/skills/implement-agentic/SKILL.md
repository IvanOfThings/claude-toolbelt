# implement-agentic

Implements a plan task-by-task using fresh subagents with spec compliance and code quality review after each task.

Wraps `superpowers:subagent-driven-development`.

## Input

Plan file path from `write-plan` output.

## Steps

**1. Read quality checklist**

Read `rules/security/code-quality-checklist.md` from the plugin. This is the checklist used by code quality review subagents.

**2. Invoke subagent-driven-development**

Use `superpowers:subagent-driven-development`.

Per task:
- Implementer subagent: receives full task text + project context
- Spec compliance review: confirms code matches plan exactly
- Code quality review: checks against `code-quality-checklist.md`

**3. Context management**

If the plan has 4 or more tasks, instruct implementer subagents to run `/compact` after every 2–3 tasks to prevent context overflow during long runs.

**4. Output**

Report: tasks completed, any spec deviations caught in review, any quality issues found and fixed.
