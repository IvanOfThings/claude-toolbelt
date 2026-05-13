# diagnose-pr-failures

Reads a verification document, extracts failing tests, and produces a structured diagnosis before touching any code.

## Input

`doc-path`: path to the verification document (functional or technical).

`test-ids` (optional): specific test IDs to diagnose (e.g. `P1.2 P3.1`). If omitted, diagnoses all tests marked `❌ FAIL` or `⚠️ PARTIAL`.

## Steps

**1. Read the verification document**

Extract every test marked `❌ FAIL` or `⚠️ PARTIAL`. For each: note its ID, title, steps, and tester comments.

**2. Read relevant source files**

For each failing test, identify the source files likely responsible (routes, services, components, existing tests). Read them.

**3. Produce structured diagnosis**

For each failing test, output:

```
### P2.1 — [test title]

**What the tester sees:** [from tester comments]
**Root cause:** [your analysis of the source files]
**Affected files:** [list of files to change]
**Proposed fix:** [1-2 sentence description]
**Existing test coverage:** [path/to/test.ts → "test name" if a unit test covers this, otherwise "none"]
```

**4. Gate**

Present the full diagnosis. Do not touch any code. Wait for developer confirmation before `apply-pr-fixes` proceeds.
