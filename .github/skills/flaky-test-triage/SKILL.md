---
name: "flaky-test-triage"
description: "Use when a test is flaky, continuous integration (CI) is unstable, or a flaky test needs quarantine. Triggers include \"flaky test\", \"quarantine\", \"intermittent failure\", \"CI instability\", and \"flaky test dashboard\"."
---
# Flaky test triage

## When to Invoke

- CI fails and the rerun passes.
- "This test is flaky. Help me fix it."
- "Create a quarantine process for flaky tests."

## Diagnostic workflow

1. **Reproduce**: run the test in isolation 50 times with `--repeat-each 50` (Playwright) or `pytest --count=50`. If it fails less than once, it probably depends on execution order.
2. **Categorize** the root cause of flakiness:

- **Async/timing**: missing `await`, race condition, hardcoded `sleep`
- **Order dependency**: shared state, database not cleaned, global singleton
- **External dependency**: network, clock, file system
- **Nondeterminism**: unordered map iteration, random seed
- **Resource contention**: port, file lock, collision between parallel processes

3. **Fix the root cause**: replace `sleep` calls with explicit waits, isolate state, set random seeds, and use test-scoped ports.
4. **Quarantine if you cannot fix it in less than a day**: apply the `flaky/` label, open a tracking issue on GitHub, and set a 30-day service-level agreement (SLA) to fix or delete it.

## Quarantine policy

- Quarantined tests run but do not fail the build.
- Delete anything that stays in quarantine for more than 30 days. A test that cannot be fixed is worse than no test.
- Dashboard: track each test's flake rate over 100 runs. Automatically quarantine anything exceeding 5%.

## Anti-patterns

- `sleep(1000)`: always wrong.
- Repeating the assertion in a loop: hides timing errors.
- `@Retry(3)`: masks flakiness and encourages poor-quality tests.

## Output Template

Record each investigated flake and its resolution:

```markdown
## Flake triage: <test id>

| Field | Value |
|---|---|
| Test | <suite::test name> |
| Flake rate | <N>% over <M> runs |
| Root cause | Async-timing / Order dependency / External dependency / Nondeterminism / Resource contention |
| Fix or quarantine | <pull request (PR) link or `flaky/` label + tracking issue> |
| SLA | <30-day deadline to fix or delete> |

### Evidence
- <reproduction command, for example: pytest --count=50 path::test>
- <failure output or observed race condition>
```

## Quality Gate

- [ ] The flake was reproduced in isolation (more than 50 runs) and its category was identified.
- [ ] The fix addresses the root cause without adding `sleep`, a retry, or an assertion loop.
- [ ] Anything not fixed within a day enters quarantine with a GitHub tracking issue and a 30-day SLA.
- [ ] Quarantined tests continue running but do not fail the build.

## References

- [Google: Flaky Tests at Google](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html)
- [Microsoft Research: Empirical Study of Flaky Tests](https://www.microsoft.com/en-us/research/publication/an-empirical-analysis-of-flaky-tests/)
