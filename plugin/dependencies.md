# Framework Dependencies

## Required Plugins

| Plugin | Marketplace | Used by | Install |
|--------|-------------|---------|---------|
| superpowers | claude-plugins-official | write-plan, implement-agentic, init-brainstorm | `claude plugin install superpowers` |
| frontend-design | claude-plugins-official | update-mockups | `claude plugin install frontend-design` |
| vercel | claude-plugins-official | quality-review (react-best-practices) | `claude plugin install vercel` |
| honeycomb | honeycomb-plugins | honeycomb-investigation rule | `claude plugin install honeycomb --from honeycomb-plugins` |

## Required MCPs

| MCP | Used by | Setup |
|-----|---------|-------|
| Honeycomb MCP | honeycomb-investigation rule | `claude mcp add honeycomb` + env var `HONEYCOMB_API_KEY` |

## Optional Plugins

| Plugin | Used by | Install |
|--------|---------|---------|
| code-review | requesting-code-review in dev-cycle | `claude plugin install code-review` |
