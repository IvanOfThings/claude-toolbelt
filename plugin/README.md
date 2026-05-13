# dev-workflow

A reusable development workflow plugin for Claude Code. Provides slash commands, focused skills, and canonical rules for consistent software development across projects.

## Install

```bash
claude plugin install /path/to/claude-toolbelt/plugin
```

## What's included

- **Commands**: `/init-project`, `/dev-cycle`, `/refine`, `/generate-verification`, `/verify-pr`, `/security-review`, `/ui-contrast`, `/init-design-system`, `/update-icons`
- **Skills**: 19 focused skills covering analysis, implementation, review, scaffolding
- **Rules**: 20 canonical standards covering process, code quality, security, UI, observability, and workflow

## Dependencies

See `dependencies.md` for required plugins and MCPs.

## Phases

- **Phase 1 (this)**: Plugin structure + all rules
- **Phase 2**: Workflow commands (dev-cycle, security-review, verify-pr, generate-verification, ui-contrast)
- **Phase 3**: Project bootstrap commands (init-project, init-design-system, update-icons)
