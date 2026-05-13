# init-brainstorm

Leads an interactive brainstorming session to define the project's functional design, architecture, and technical setup before any scaffolding begins.

Wraps `superpowers:brainstorming` with project bootstrap context.

## Input

`doc-path` (optional): path to an input document describing features and goals. If provided, use it as starting context.

## Steps

**1. Invoke superpowers:brainstorming**

Use `superpowers:brainstorming` with the input document (if provided) as context.

Explore through conversation:
- Product goals and target users
- Key features (functional scope)
- Tech stack preferences (framework, database, auth, deployment)
- Architecture style (monolith vs services, API-first vs fullstack)
- Design system direction (minimalist, full-featured, brand-heavy)

Follow the brainstorming skill's process: explore → clarify → propose approaches → present design sections → approve.

**2. Technical setup questions (after functional design is approved)**

After the developer approves the high-level functional design, ask two technical questions before closing:

**Question 1 — i18n library:**
```
Which i18n library will this project use?
1. next-intl (recommended for Next.js)
2. i18next / react-i18next
3. LinguiJS
4. None — single language only
```

**Question 2 — Project languages:**
```
What locales will this project support?
- Default locale: [e.g. es, en, fr]
- Additional locales: [list, or "none"]
```

**3. Record technical setup**

Add a `## Technical Setup` section to `docs/plan.md` (the plan file produced by brainstorming):

```markdown
## Technical Setup

- **i18n library:** [chosen library or "none"]
- **Default locale:** [e.g. es]
- **Additional locales:** [list or "none"]
```

**4. Output**

Return:
- Approved high-level design summary (features, architecture, stack)
- i18n library and locales chosen
- Path to docs/plan.md
