---
name: "refactor-safely"
description: "Use when refactoring legacy code, extracting a service, or making behavior-preserving changes. Triggers include \"refactor\", \"legacy code\", \"Strangler Fig pattern\", \"characterization test\", and \"Mikado Method\"."
---
# Safe refactoring

## When to Invoke

- When working on code without enough tests.
- When splitting a monolith or extracting a service.
- When a change is "one line" but affects a risky path.

## First rule

**Refactoring preserves behavior.** If you cannot prove behavior was preserved, it is not refactoring but rewriting. Implement characterization tests first.

## Workflow

1. **Characterize**: write tests that pin current behavior, including its quirks. Do not fix bugs yet. The goal is a safety net, not a fix.
2. **Take small, reversible steps**: apply one behavior-preserving transformation at a time. Commit after each one.
3. **Keep tests green**: run them after each step. Revert immediately if they turn red and you do not know why.
4. **Separate refactoring commits from behavior-changing commits**: reviewers can stay focused, and `git bisect` remains useful.
5. **Integrate frequently**: long-lived refactoring branches deteriorate.

## Patterns

### Strangler Fig pattern for systems

1. Place a facade (proxy, router, or feature flag) in front of the old system.
2. Route a small share of traffic to the new implementation.
3. Grow the new implementation incrementally while shrinking the old one.
4. Delete the old implementation when its traffic reaches zero.

### Mikado Method (for code)

1. Record the goal.
2. Try to achieve it directly and record what fails as a **prerequisite**.
3. Revert. Solve a prerequisite first. Repeat recursively.
4. Complete the leaves first and reach the original goal last.

### Branch by Abstraction

Introduce an interface, migrate callers to it, swap implementations, and retire the old one, all without a long-lived branch.

## How to create characterization tests

- Run the code with representative inputs and record the output (golden files or snapshot tests).
- Prefer external observation (HTTP, CLI, or database state). This approach withstands internal refactoring.
- Cover unusual cases too, as they often fail.
- Accept that some behaviors are *bugs now being preserved*. Flag them and fix them after the safety net is ready.

## Anti-patterns

- "Refactoring" pull requests that also fix bugs, change APIs, and rename files, making review and rollback impossible.
- Complete rewrites with no deliveries for months.
- Deleting old code before the new code handles 100% of traffic.
- Refactoring without tests, based only on manual happy-path checks.

## Output Template

```markdown
## Refactoring plan - <target>

| Field | Value |
|---|---|
| Goal | <behavior-preserving change> |
| Safety net | <characterization test path> |
| Pattern | Strangler Fig / Mikado / Branch by Abstraction |
| Steps | <ordered, reversible transformations> |

### Prerequisites (Mikado)
- <prerequisite discovered while trying to achieve the goal>

### Commits
- refactor: <one behavior-preserving step per commit>
```

## Quality Gate

- [ ] Characterization tests capture current behavior, including quirks, before any change.
- [ ] Refactoring commits are separate from behavior-changing commits.
- [ ] Tests stay green after each step; a red step is reverted, not forced through.
- [ ] Old code is deleted only after the new path handles all traffic.

## References

- [Martin Fowler - Refactoring (2nd ed.)](https://martinfowler.com/books/refactoring.html)
- [Michael Feathers - Working Effectively with Legacy Code](https://www.oreilly.com/library/view/working-effectively-with/0131177052/)
- [Mikado Method](https://mikadomethod.info/)
- [Fowler - Strangler Fig Application](https://martinfowler.com/bliki/StranglerFigApplication.html)
