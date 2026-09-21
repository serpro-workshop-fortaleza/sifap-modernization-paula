---
name: "playwright-generate-test"
description: "Generate a Playwright end-to-end test from a scenario using Playwright MCP, delegating the procedure to the playwright-generate-test skill."
argument-hint: "scenario=\"<user flow to test>\""
agent: "qa-engineer"
tools: ["read", "search", "edit", "execute", "playwright/*"]
---
# /playwright-generate-test

## Objective

Explore a described user flow with Playwright MCP and produce a passing TypeScript end-to-end test with `@playwright/test` for the SIFAP 2.0 frontend. The complete procedure is in the [`playwright-generate-test`](../skills/playwright-generate-test/SKILL.md) skill. This prompt applies it to the Next.js 15 frontend without repeating it.

> [!IMPORTANT]
> Do not write test code based solely on the scenario. First execute the flow step by step with Playwright MCP, then generate the test from the observed steps.

## When to Invoke

During Stages 3 or 4, when the team wants an end-to-end regression test for a user-visible flow in the Next.js 15 frontend.

## Preconditions

- The `frontend/` application is running and accessible
- Playwright and the Playwright MCP server are available
- The test scenario has been described or will be provided when requested

> [!NOTE]
> Prompt files run in the VS Code Local agent. In Agent Host sessions, invoke the `playwright-generate-test` skill through `@qa-engineer`; the agent exposes the same `playwright/*` toolset. If the toolset is unavailable, stop with a blocker instead of generating an unobserved test.

## Inputs the Team Must Provide

- `scenario`: the user flow to test; request it if missing
- The base URL of the running frontend
- Ask the user for any missing information.

## What I Will Do

- Follow the explore-then-generate procedure in the [`playwright-generate-test`](../skills/playwright-generate-test/SKILL.md) skill
- Drive the scenario one step at a time through Playwright MCP before writing code
- Produce a TypeScript spec with `@playwright/test` in the frontend's `tests/` directory
- Run and adjust the test until it passes

## What I Will NOT Do

- Generate test code prematurely based solely on the scenario
- Cover unit or component behavior here; that remains in Vitest + Testing Library
- Leave a failing or flaky test
- Hardcode secrets or environment-specific data in the spec

## Output Format

```markdown
### Generated
`frontend/tests/payment-approval.spec.ts` — @playwright/test

### Execution
`npx playwright test payment-approval` → 1 passed
```

## Definition of Done

- [ ] The flow was explored step by step with Playwright MCP before writing code
- [ ] The spec uses `@playwright/test` and is in the frontend's `tests/` directory
- [ ] The test passes and is not flaky
- [ ] Unit or component coverage remains in Vitest + Testing Library

## Prompt Body

The [`playwright-generate-test`](../skills/playwright-generate-test/SKILL.md) skill defines the MCP-driven exploration and generation procedure. Read it and apply it to the scenario.

**Step 1 — Get the scenario.**
If no scenario was provided, request one. Confirm the frontend URL.

**Step 2 — Apply the skill.**
Execute the scenario one step at a time with Playwright MCP and generate the `@playwright/test` spec from the recorded steps.

**Step 3 — Follow the kit's rules.**
Target the Next.js 15 frontend with App Router, save the spec in `frontend/tests/`, and keep secrets out of the file.

**Step 4 — Verify.**
Run the test and adjust it until it passes.

## Example Invocation

```text
/playwright-generate-test scenario="approve a pending payment as an analyst"
```
