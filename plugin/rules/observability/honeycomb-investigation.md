# Honeycomb Investigation Protocol

When investigating production issues (latency, errors, missing data) using the Honeycomb MCP.

## Workflow

**1. Always start with workspace context**

Call `get_workspace_context` first to discover available environments and datasets. Never assume an environment name or dataset name — they change per project and per deployment environment.

**2. Discover columns before querying**

Use `find_columns` or `get_dataset_columns` to confirm field names before building a query. Field schemas evolve; querying a stale name returns empty results without error, leading to false conclusions.

**3. Use human-readable time ranges**

Use `"last 2 hours"`, `"24h"`, `"last 7 days"` in query parameters — avoid epoch timestamps unless you need a precise window. Human-readable ranges are less error-prone and easier to communicate.

**4. Specify environment and dataset explicitly**

Every query call must specify both the environment and the dataset. Never rely on defaults.

## Environment vs deployment attribute

The Honeycomb **environment** is determined by which API key was used to send the data — it's configured in your deployment platform (e.g. per Vercel environment). The **`deployment.environment` span attribute** is set by your instrumentation code from `NODE_ENV` or similar. They can disagree if the wrong key is configured.

When in doubt about whether a trace is from production: check `deployment.environment`, `http.host`, and any git reference attributes on the root span.

## Investigation pattern

```
1. get_workspace_context        → discover environments + default datasets
2. get_dataset_columns          → confirm field names
3. run_query (broad)            → identify the time window and affected traces
4. run_bubbleup                 → find differentiating attributes between failing/passing
5. get_trace (specific trace)   → drill into individual request
6. Form hypothesis → verify with targeted query
```

## Useful BubbleUp pattern

When a metric is anomalous (high error rate, high latency), use `run_bubbleup` to compare the anomalous window against baseline. BubbleUp surfaces which attribute values appear disproportionately in the bad window — e.g. a specific user ID, deployment version, or database host.
