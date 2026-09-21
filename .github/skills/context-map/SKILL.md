---
name: "context-map"
description: "Produce a map of the files relevant to a task, including files to modify, dependencies, related tests, reference patterns, and risks, before writing any code. Use when someone wants to scope the impact, plan changes, or understand which files a task affects before implementation."
---
# Context map

Create a written map of everything a task affects before writing any code. The map turns an open-ended change into a bounded, reviewable plan. This lets implementers edit the correct files, update the right dependencies, write suitable tests, and identify risks early.

> [!IMPORTANT]
> Do not start implementation until the context map is written and reviewed. The map is the artifact produced by this skill. Coding starts only after the map is approved.

## When to Invoke

- "Scope the impact of adding a status field to the payments API before I code."
- "Which files does this refactoring affect and which tests cover them?"
- "Map the blast radius of changing this repository interface."
- "Plan the file changes for this Stage 3 feature before implementation."

## How to create the map

1. **Restate the task in one sentence.** Describe the observable outcome, not the implementation detail.
2. **Locate entry points.** Find the files responsible for the behavior, such as controllers, services, components, or migrations.
3. **Trace direct dependencies.** Follow each file's imports and exports to discover what breaks if a signature changes.
4. **Find tests.** Identify unit and integration tests that already cover the affected code and record missing coverage.
5. **Collect reference patterns.** Point to an existing file that already solves a similar problem so its structure can be followed.
6. **Assess risks.** Explicitly flag public application programming interface (API) changes, database migrations, and configuration or secret changes.

> [!NOTE]
> In this immersion, `backend/` and `frontend/` do not exist until Stage 3. Therefore, a new feature's map lists files to **create**, not just files to modify. `infra/` already exists. Treat everything in `01-archaeology/legacy-sifap/` as read-only evidence and never assert the contents of a legacy program or field. Instead, cite the reading criterion in [`01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`](../../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md).

## Scope signals

| Signal | Meaning | Action |
|---|---|---|
| The change affects a public `/api/v1` contract | The blast radius reaches all callers | List callers and plan an API compatibility note |
| The change modifies a JPA entity or schema | A migration is needed | Add a `db/migration` row to the map |
| No test covers the target code | Regression risk | Add a "test to write" row before coding |
| A similar feature already exists | Reuse opportunity | Record it as a reference pattern to follow |

## Output Template

```markdown
## Context map: add a status field to Payment

### Files to create or modify
| File | Create or modify | Purpose | Change |
|---|---|---|---|
| backend/src/main/java/com/sifap/payment/PaymentController.java | modify | REST entry point | Add PATCH `/api/v1/payments/{id}/status` |
| backend/src/main/java/com/sifap/payment/PaymentStatus.java | create | Status enumeration | Define allowed values and transitions |

### Dependencies to check
| File | Relationship |
|---|---|
| backend/src/main/java/com/sifap/payment/PaymentService.java | Calls the modified controller mapping |
| frontend/app/payments/page.tsx | Renders the status returned by the API |

### Tests
| Test | Status | Coverage |
|---|---|---|
| backend/src/test/java/com/sifap/payment/PaymentControllerTest.java | exists | Extend for the new endpoint |
| PaymentStatus transition test | to write | New state machine behavior |

### Reference patterns
| File | Pattern to follow |
|---|---|
| backend/src/main/java/com/sifap/benefit/BenefitController.java | Existing PATCH structure with `@Valid` |

### Risks
- [ ] Breaking change to a public `/api/v1` contract
- [ ] Database migration required
- [ ] Configuration or secret change required
- [ ] Legacy behavior must be confirmed with read-only evidence in `01-archaeology/legacy-sifap/`
```

## Quality Gate

- [ ] Every file affected by the task is listed as create or modify, with the concrete change described.
- [ ] Direct dependencies of each changed signature are listed.
- [ ] Existing tests are identified and missing tests are marked "to write".
- [ ] At least one reference pattern is cited or its absence is stated.
- [ ] Public API, migration, and configuration risks are flagged before coding starts.
- [ ] Every legacy-derived item cites read-only evidence and does not assert the contents of legacy programs.
