---
name: "playwright-generate-test"
description: "Generate an end-to-end Playwright test in TypeScript from a described scenario, driving Playwright MCP step by step and running the test until it passes. Use when someone requests creating or recording a Playwright browser or E2E test for a web flow."
---
# Playwright end-to-end test generation

Generate an end-to-end (E2E) Playwright test in TypeScript by exploring the described user flow with the Playwright MCP server, one step at a time. Then produce an `@playwright/test` spec and run it until it passes. This skill covers browser-level regression tests for the SIFAP 2.0 Next.js 15 UI. Unit and component behavior remains in Vitest + Testing Library (see [`tests.instructions.md`](../../instructions/tests.instructions.md)).

> [!NOTE]
> This skill drives the **Playwright MCP server**, which must be available against an accessible UI. The owning agent or prompt must expose the `playwright/*` toolset. If the toolset is unavailable, report the workflow as blocked and identify the missing prerequisite. Do not install tools implicitly or write the test manually based only on the scenario.

## When to Invoke

- "Generate a Playwright test for the payment approval flow."
- "Record an end-to-end test that logs in and opens the dashboard."
- "Create a browser regression test for this scenario."
- "Turn this user journey into a Playwright spec."

## Explore-then-generate workflow

Never write test code based only on the scenario description. First observe the real DOM through MCP, then generate the test.

1. **Get the scenario.** If the user does not describe a flow, ask for it. Confirm the running UI's base URL.
2. **Verify the tool boundary.** Confirm that `playwright/*` is available. If it is absent, stop and report a blocker; terminal HTTP requests are not equivalent to observed browser interaction.
3. **Explore step by step.** Drive the flow, one action at a time, with Playwright MCP tools (navigate, click, fill, and verify). Use each observed page state to guide the next step.
4. **Prefer accessible locators.** Select elements by role, label, or text (`getByRole`, `getByLabel`), not brittle CSS or `data-testid` when a role exists. This follows the Testing Library convention used throughout the kit.
5. **Generate the spec.** Only after confirming every step, produce a TypeScript test with `@playwright/test` based on the recorded interactions. Structure it as Arrange-Act-Assert and add an inline `// REQ-NNN` comment when the flow traces to a requirement.
6. **Save it** in the UI's `tests/` directory as `<feature>.spec.ts`.
7. **Run and refine.** Run `npx playwright test <name>` and fix locators or waits until the test passes reliably. Never leave a failing or flaky spec.

> [!WARNING]
> Do not include secrets or environment-specific data in the spec. Read base URLs and credentials from environment variables or Playwright configuration. Never hardcode them.

## Scope boundaries

| Layer | Tool | Owner |
|---|---|---|
| End-to-end (browser) | Playwright | this skill |
| Component / interaction | Vitest + Testing Library | [`tests.instructions.md`](../../instructions/tests.instructions.md) |
| Unit / pure logic | Vitest (frontend) or JUnit 5 (backend) | [`test-strategy`](../test-strategy/SKILL.md) |

## Output Template

```typescript
import { test, expect } from '@playwright/test';

// REQ-XXX: an analyst approves a pending payment
test('analyst approves a pending payment', async ({ page }) => {
  await page.goto('/payments');                                    // Arrange

  await page
    .getByRole('row', { name: /pending/i })
    .first()
    .getByRole('link', { name: /review/i })
    .click();

  await page.getByRole('button', { name: /approve/i }).click();    // Act

  await expect(page.getByRole('status')).toHaveText(/approved/i);  // Assert
});
```

Execution result to report:

```text
npx playwright test payment-approval
  1 passed (2.1s)
```

## Quality Gate

- [ ] The flow was explored step by step through Playwright MCP before writing code.
- [ ] The owning prompt or agent exposed `playwright/*`; unavailable tooling was reported as a blocker.
- [ ] The spec uses `@playwright/test` and is in the UI's `tests/` directory.
- [ ] Elements are selected by accessible role or label, not brittle selectors.
- [ ] Requirement-driven flows contain an inline `// REQ-NNN` comment.
- [ ] The test passes and is not flaky; no secrets are hardcoded.
- [ ] Unit and component coverage remains in Vitest + Testing Library.
