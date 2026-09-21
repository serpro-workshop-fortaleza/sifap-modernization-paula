# Testing patterns

## Core sections (required)

### 1) Testing stack and commands

- Primary test framework: [NAME + VERSION]
- Assertion/mocking tools: [TOOLS]
- Commands:

```bash
[run all tests]
[run unit tests]
[run integration/e2e tests]
[run coverage]
```

### 2) Test structure

- Test file location pattern: [colocated/test folder/etc.]
- Naming convention: [pattern]
- Setup files and where they run: [paths]

### 3) Test scope matrix

| Scope | Covered? | Typical target | Notes |
|-------|----------|----------------|-------|
| Unit | [yes/no] | [modules/services] | [notes] |
| Integration | [yes/no] | [API/data boundaries] | [notes] |
| End-to-end (E2E) | [yes/no] | [user flows] | [notes] |

### 4) Mocking strategy and isolation

- Primary mocking approach: [module/class/network]
- Isolation guarantees: [what resets and when]
- Common test failure mode: [brief note]

### 5) Coverage and quality signals

- Coverage tool + threshold: [value or TODO]
- Currently reported coverage: [value or TODO]
- Known gaps/flaky areas: [list]

### 6) Evidence

- [path/to/test-config]
- [path/to/representative-test-file]
- [path/to/ci-or-coverage-config]

## Extended sections (optional)

Add only when needed:

- Framework-specific suite patterns
- Detailed mocking recipes by dependency type
- Historical flaky test catalog
- Test performance bottlenecks and optimization ideas
