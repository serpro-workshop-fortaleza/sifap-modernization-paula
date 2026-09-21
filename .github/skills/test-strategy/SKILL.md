---
name: "test-strategy"
description: "Use when designing a test strategy, choosing the test pyramid shape, setting coverage targets, or assessing testing investments across unit, integration, and end-to-end (E2E) layers. Triggers include \"test strategy\", \"test pyramid\", \"coverage target\", \"E2E versus integration\", and \"testing investment\"."
---
# Test strategy

## When to Invoke

- "Design a test strategy for..."
- "What should the ratio of unit, integration, and end-to-end (E2E) tests be?"
- "What is the appropriate coverage target?"
- "Audit our test pyramid."

## Workflow

1. **Inventory** the code under test: modules, public APIs, external integrations, and critical paths.
2. **Classify risk** by module (P0 / P1 / P2) based on the blast radius of a failure.
3. **Distribute the pyramid**: start with 70% unit tests, 20% integration, and 10% E2E; justify deviations.
4. **Set coverage targets**: a baseline of 80% line coverage and 90% for P0 modules, tracking branch coverage separately.
5. **Set the flake budget**: a maximum rate of 1%; anything above triggers quarantine.
6. **Choose tools per layer**: unit (Vitest/JUnit/pytest), integration (Testcontainers), and E2E (Playwright).
7. **Produce the output**: a one-page strategy document with targets, tools, coverage thresholds, and quarantine rules per layer.

## Heuristics

- If an E2E test can be rewritten as integration and contract tests, do so. E2E tests are expensive and flaky.
- Contract tests are better than mocks for anything crossing service boundaries.
- Mutation testing (Stryker, PIT) is the only honest way to detect tests that prove nothing.

## Anti-patterns

- Inverted pyramid: many slow E2E tests on top of few unit tests.
- A single global coverage number, without a higher target for P0 modules.
- Mocked service boundaries that never detect a real integration failure.
- Coverage treated as a goal, not a confidence indicator.

## Output Template

```markdown
## Test strategy - <system or module>

| Layer | Target distribution | Tools | Coverage target |
|---|---|---|---|
| Unit | 70% | JUnit 5 / Vitest | 80% of lines (90% for P0) |
| Integration | 20% | Testcontainers | critical paths |
| E2E | 10% | Playwright | main user journeys |

**Flake budget**: <=1% (above that, quarantine)
**Risk classification**: P0 <modules> / P1 <modules> / P2 <modules>
```

## Quality Gate

- [ ] Each module is classified by risk (P0/P1/P2) and has a coverage target.
- [ ] The pyramid distribution is defined per layer, and deviations from 70/20/10 are justified.
- [ ] Each layer states its tool and threshold.
- [ ] A flake budget and quarantine rule are defined.

## References

- [Google Testing Blog - Test Sizes](https://testing.googleblog.com/2010/12/test-sizes.html)
- [ISTQB Foundation Syllabus](https://www.istqb.org/certifications/certified-tester-foundation-level)
- [Martin Fowler - Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
