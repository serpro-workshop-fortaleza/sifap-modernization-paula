---
name: "write-github-issue"
description: "Writes a high-quality GitHub issue, ready for Copilot cloud agent."
argument-hint: "feature=\"<scoped-work>\" context=<context> reqs=REQ-XXX"
agent: "evolution"
tools: ["read", "search", "edit", "github/*"]
---
# /write-github-issue

## Objective

Create a structured issue for autonomous execution by Copilot Agent, with clear criteria, paths, and REQ-ID traceability.

## When to Invoke

At the start of Stage 4, for delegable work.

## Preconditions

- A Stage 3 prototype, an EARS `spec.md`, and specific work exist

## Inputs the Team Must Provide

- Feature or fix, REQ-IDs, context, and likely files

## What I Will Do

- Structure Context, Acceptance Criteria, Affected Files, Testing Approach, and Out of Scope
- Copy REQ-IDs without inventing behavior and suggest labels and an assignee

## What I Will NOT Do

- Publish, write a vague issue, delegate an architectural decision or security fix, or omit tests

## Output Format

```markdown
# Issue: [Title]
## Context
## Acceptance Criteria
## Likely Affected Files
## Testing Approach
## Out of Scope
## Labels
## Related Requirements
```

Save to `04-evolution/issues/<slug>.md`.

## Definition of Done

- [ ] The five sections exist
- [ ] Criteria are testable
- [ ] There is a REQ-ID or a justified statement of new behavior
- [ ] Paths and tests are indicated
- [ ] Fits in one PR

## Prompt Body

You are `@evolution`.

**Step 1 - Understand.** Ask what to do, which context, whether it addresses `REQ-NNN` or new behavior, and which files.

**Step 2 - Context.** Describe the current and desired states and link EARS.

**Step 3 - Criteria.** Copy verifiable criteria from `spec.md`. If missing, record the gap without inventing an answer.

**Step 4 - Files.** List those to modify, create, and only consult.

**Step 5 - Tests.** Identify unit tests, integration tests, and existing tests to update, following local patterns.

**Step 6 - Out of scope.** State exclusions, such as schema, authentication, or frontend, to prevent expansion.

**Step 7 - Metadata.** Suggest `enhancement` or `bug`, the context, and `copilot-agent`.

**Step 8 - Draft.** Generate `<slug>` in kebab-case. Remind the team to review and publish manually through the UI or `gh issue create`.

## Example Invocation

```text
/write-github-issue feature="<scoped-work>" context=<context> reqs=REQ-XXX
```
