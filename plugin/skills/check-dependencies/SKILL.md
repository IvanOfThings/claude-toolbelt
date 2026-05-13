# check-dependencies

Checks that all plugins and MCPs required by the framework and project are installed. Run silently at the start of any command.

## Input

`scope`: `framework` | `project` | `all` (default: `all`)

## Steps

**1. Determine what to check**

- `framework` scope: read `plugin/dependencies.md` (installed at the plugin's path)
- `project` scope: read the project's `CLAUDE.md` → `## Dependencies` section
- `all` scope: both

**2. Check plugins**

Read `~/.claude/plugins/installed_plugins.json`.

For each required plugin, check if its key exists in the JSON object. If the file does not exist, all plugins are considered missing.

**3. Check MCPs**

Read the `<system-reminder>` deferred tools list present in the current context window.

An MCP is **present** if at least one of its expected tool names appears in the deferred tools list.

Known MCP → expected tool name prefix:
- Honeycomb → `mcp__claude_ai_Honeycomb__` (any tool starting with this prefix)

**4. Report**

If all present: output nothing. Continue silently.

If any missing, output exactly:

```
⚠️  Missing dependencies detected:

  PLUGIN  <name>   not installed
  → <install command from dependencies.md>

  MCP     <name>   not configured
  → <setup commands from dependencies.md>
```

Do not block execution — the invoking command decides whether to gate on missing dependencies.
