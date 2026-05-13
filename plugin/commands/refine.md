# /refine

Decomposes a change document into ordered work items and executes them as `/dev-cycle` runs.

**Usage:** `/refine <doc-path>`

`doc-path`: path to a document describing desired changes, a feature list, or a product brief.

---

## Phase 1 — Context + document read

Invoke `analyze-context`.

Read the input document at `doc-path`.

---

## Phase 2 — Decomposition

Invoke `decompose-refinement` with the document content and project context.

---

## Phase 3 — Clarification

`decompose-refinement` asks clarifying questions inline (one at a time, max 2 per item). Answer them before proceeding to spec generation.

---

## Phase 4 — Queue

`decompose-refinement` generates mini-spec files in `docs/superpowers/specs/refined/` and `queue.json`.

**GATE:** Present the queue to the developer. Wait for approval before execution begins.

---

## Phase 5 — Execution

For each item slug in `queue.json["pending"]`:

1. Run `/dev-cycle docs/superpowers/specs/refined/<item-slug>.md`
2. On completion: move the slug from `pending` to `done` in `queue.json`
3. Continue with the next pending item

If a `/dev-cycle` returns a blocker: stop the queue, report the blocker to the developer, and wait for resolution before resuming.
