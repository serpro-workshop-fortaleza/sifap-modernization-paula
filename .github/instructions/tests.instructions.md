---
description: "Use when creating or reviewing automated tests, test strategy, specs, coverage gaps, regression tests, and quality gates."
applyTo: "**/*.test.*,**/*.spec.*,**/tests/**"
---

# Testing conventions - JUnit, Vitest, and traceability

This file activates for any test file (`*.test.*`, `*.spec.*`, or any file in a `tests/` path), in both backend and frontend. It teaches test structure and naming, backend (JUnit 5 + Testcontainers) and frontend (Vitest + Testing Library) tools, REQ-ID traceability, and coverage targets. Tests are written **during** implementation, never added afterward.

## Test pyramid

| Layer | Tools | Proportion |
|---|---|---|
| Unit (services, pure logic) | JUnit 5 / Vitest, no I/O | Most tests |
| Integration (repositories, components) | Testcontainers / Testing Library | Fewer |
| End-to-end | Critical workflow only | Fewest |

The [`test-strategy`](../skills/test-strategy/SKILL.md) skill owns decisions on pyramid shape and coverage targets.

## Structure: Arrange-Act-Assert

Each test has three visible phases and checks one behavior. Mock only external boundaries, never the database or the class under test.

```java
@Test
void should_reject_duplicate_label() { // REQ-021
    resourceRepository.save(Resource.of("alpha", new BigDecimal("10.00"))); // Arrange
    var request = new CreateResourceRequest("alpha", new BigDecimal("5.00"));
    assertThatThrownBy(() -> resourceService.create(request))            // Act
      .isInstanceOf(ResourceConflictException.class);                  // Assert
}
```

## Naming

Name tests `should_<expected behavior>_when_<condition>` (backend) or express the same intent in Testing Library's `it(...)` (frontend).

```text
should_return_409_when_identifier_already_exists
should_render_empty_state_when_no_resources
```

## Backend: JUnit 5 + Testcontainers

Repository and integration tests run against real containerized PostgreSQL 16, never H2, so behavior matches production. Bind the container with `@ServiceConnection`.

```java
@Testcontainers
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class ResourceRepositoryTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @Autowired
    ResourceRepository resourceRepository;

    @Test
    void should_find_resource_by_label_when_it_exists() { // REQ-021
        resourceRepository.save(Resource.of("alpha", new BigDecimal("10.00")));
        assertThat(resourceRepository.findByLabel("alpha")).isPresent();
    }
}
```

Backend business logic must include the success path, validation failure, and authentication failure.

## Frontend: Vitest + Testing Library

Query by accessible role or label, never by test-id when a role exists, and drive interaction with `user-event`. Avoid snapshot-only tests.

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { ArchiveButton } from './ArchiveButton';

describe('ArchiveButton', () => {
  it('should call onArchive when clicked', async () => { // REQ-032
    const onArchive = vi.fn().mockResolvedValue(undefined);
    render(<ArchiveButton id="1" onArchive={onArchive} />);
    await userEvent.click(screen.getByRole('button', { name: /archive/i }));
    expect(onArchive).toHaveBeenCalledWith('1');
  });
});
```

## REQ-ID traceability

Every test verifying a requirement names its REQ-ID in an inline comment. This feeds the non-blocking `spec-traceability` report (see [`sdd-artifacts.instructions.md`](sdd-artifacts.instructions.md)), which lists REQ-IDs not yet referenced by tests.

## Coverage targets

The repository minimum is **≥ 80% line** and **≥ 70% branch coverage**; service classes and business logic should aim higher (about 85% line coverage). CI runs Jacoco (backend) and Vitest `--coverage` (frontend) and reports the numbers. Configure thresholds in `pom.xml` and the Vitest configuration so `verify`/`test` fail below the minimum.

> [!NOTE]
> Coverage is a floor, not a goal. A branch without an assertion has not been tested even when the line is "covered"; verify behavior, not just the call.

## Conventions

| Rule | Rationale |
|---|---|
| Arrange-Act-Assert, one behavior per test | Readable and isolates the failure |
| Mock only external boundaries | A real database through Testcontainers catches real bugs |
| `should_<behavior>_when_<condition>` naming | Intent is clear in the report |
| Inline `// REQ-NNN` in requirement tests | Keeps spec-to-test traceability active |
| Written during implementation | Untested code is not integrated |

## Do / Don't

| Do | Don't |
|---|---|
| Use Testcontainers PostgreSQL 16 | Substitute H2 in integration tests |
| Query by role/label | Query by `data-testid` when a role exists |
| Verify behavior and edge-case branches | Rely only on snapshots or line coverage |
| Write the test alongside the code | Add tests after the feature is "done" |

## PR Checklist

- [ ] New behavior has unit tests; persistence has a Testcontainers integration test
- [ ] Tests follow Arrange-Act-Assert and `should_..._when_...` naming
- [ ] Requirement-driven tests have an inline `// REQ-NNN` comment
- [ ] Business logic covers the success path, validation failure, and authentication failure
- [ ] Coverage meets the minimum of ≥ 80% lines / ≥ 70% branches
- [ ] No external boundary is left unmocked and no required real dependency is mocked
