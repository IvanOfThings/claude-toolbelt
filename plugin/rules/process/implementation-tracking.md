# Implementation Tracking

Every project using this framework maintains `IMPLEMENTATION.md` at the project root as the single source of truth for implementation progress.

## Tracker format

Each task has four status columns:

| Column | Meaning |
|--------|---------|
| **Impl.** | Code written and functional (includes DB migration if applicable) |
| **Tests** | Tests written and passing |
| **Local** | Manually verified in local environment |
| **Prod** | Deployed and verified on production or preview URL |

Status values: `⬜` pending · `🔄` in progress · `✅` done · `—` not applicable

## Gate rule

**Do not start the next sprint until ALL tasks in the current sprint have ✅ in every applicable column.**

The `🎯 Current sprint` indicator always points to the active sprint. Update it when moving forward.

## Workflow per task

```
1. Set Impl. = 🔄
2. Write failing test → implement → tests green
3. Set Impl. = ✅, Tests = ✅
4. Verify locally
5. Set Local = ✅
6. Push branch → verify on preview/staging deployment
7. Set Prod = ✅
8. When all sprint tasks are ✅ on all columns → advance sprint indicator
```
