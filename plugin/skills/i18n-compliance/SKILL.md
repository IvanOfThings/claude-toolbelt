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
