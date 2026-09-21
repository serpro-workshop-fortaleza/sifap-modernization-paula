---
name: "delegate-to-copilot-agent"
description: "After explicit approval, creates a reviewed GitHub issue, assigns it to Copilot coding agent, and records the real delegation status."
argument-hint: "issue=04-evolution/issues/<slug>.md"
agent: "evolution"
tools: ["read", "search", "edit", "github/*"]
---
# /delegate-to-copilot-agent

## Objective

Create one approved GitHub issue, assign it to Copilot coding agent, and record the returned URLs and status. The team retains review and integration authority.

## When to Invoke

After approval of a `/write-github-issue` draft.

## Preconditions

- `04-evolution/issues/<slug>.md` exists and has passed team review
- The user explicitly authorized creation and assignment in the current conversation
- GitHub tools are available and the authenticated identity can access the repository

## Inputs the Team Must Provide

- Draft path and explicit confirmation to create and assign the issue

## What I Will Do

- Read the approved draft and repository context
- Confirm the authenticated identity and search for duplicate open issues
- Check organization issue types when the repository belongs to an organization
- Create the issue, assign it to Copilot coding agent, and capture the actual result
- Write a delegation record with issue URL, assignment status, PR URL when available, blockers, and the accountable next step

## What I Will NOT Do

- Create or assign anything without explicit confirmation
- Duplicate an existing issue, merge a PR, or claim a successful action without a returned result
- Wait indefinitely for a PR or replace human review with agent output

## Output Format

`04-evolution/delegations/<issue-slug>.md`, with the issue URL, assignment result, observed status, PR URL when available, review checklist, blockers, and accountable next step.

## Definition of Done

- [ ] The user explicitly authorized the action and no duplicate open issue exists
- [ ] The issue URL and Copilot assignment result come from GitHub tool output
- [ ] The delegation record distinguishes observed results from pending work
- [ ] The team retains review and integration responsibility

## Prompt Body

You are `@evolution`.

**Step 1 - Confirm authorization and readiness.** Ask whether the draft was reviewed, the acceptance criteria are testable, the work fits one PR, and the team authorizes issue creation and Copilot assignment now. If any answer is no, return to `/write-github-issue` or record a blocker. Do not mutate GitHub.

**Step 2 - Establish GitHub context.** Use GitHub tools to identify the authenticated user and repository. Search open issues for the title, REQ-IDs, and distinctive acceptance text. If the owner is an organization, list its issue types and use the applicable type. Stop on a likely duplicate or insufficient permission.

**Step 3 - Create and assign.** Create the issue from the approved draft without rewriting its requirements. Add only labels that already exist. Assign the created issue to Copilot coding agent with the GitHub assignment tool. Treat creation and assignment as separate results; a created issue with a failed assignment is partial, not complete.

**Step 4 - Observe without waiting indefinitely.** Read the initial Copilot job status once. If a PR already exists, record its URL for `/review-agent-pr`. Otherwise record `queued`, `in progress`, `failed`, or `unavailable` exactly as returned and identify who will check later.

**Step 5 - Record evidence.** Write `04-evolution/delegations/<issue-slug>.md` with timestamps, issue URL, issue number, assignment result, observed job status, PR URL when present, expected files and tests from the approved draft, review owner, blocker or next step, and the statement: "This is delegation, not approval. The team owns review, integration, and consequences."

**Step 6 - Hand off review.** If a PR URL exists, invoke `/review-agent-pr`. Never merge as part of this prompt.

## Example Invocation

```text
/delegate-to-copilot-agent issue=04-evolution/issues/<slug>.md
```
