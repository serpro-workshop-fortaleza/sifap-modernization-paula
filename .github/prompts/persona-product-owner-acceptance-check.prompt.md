---
name: "acceptance-check"
description: "Produce a compliance report mapping each acceptance criterion in spec.md to its implementation and test."
argument-hint: "feature=NNN-feature-name"
agent: "product-owner"
tools: ["read", "search"]
---
# /acceptance-check

## Objective

Produce an evidence-based compliance report. The report maps each Given/When/Then acceptance criterion in `specs/<NNN>-<feature>/spec.md` to its corresponding implementation and test. Each item is classified as Pass, Gap, or Fail, with a `file:line` reference.

## When to Invoke

During user acceptance testing (UAT) or sprint review, after the feature's implementation and tests exist.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` exists with REQ-IDs and acceptance criteria
- Backend and/or frontend code and tests exist for the feature

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>`
- Optional: a subset of REQ-IDs to check (default: all)
- Ask the user for any missing information.

## What I Will Do

- Extract each REQ-ID and its Given/When/Then criteria from the specification
- Search implementation code in `backend/` (service layer) and `frontend/` (browser interface) and cite `file:line`
- Search tests for a REQ-ID reference (the same signal reported by the `spec-traceability` continuous integration, or CI, job)
- Classify each criterion: Pass (code and test found), Gap (code only, no test), or Fail (no code)
- Summarize Gaps and Failures as prioritized risks

## What I Will NOT Do

- Claim that a criterion passed without citing code AND a test reference
- Modify code, tests, or the specification. This is a read-only review
- Invent the behavior of code I cannot locate. I will mark the item as Gap or Fail and state what is missing
- Judge whether a requirement is correct or contradictory. I will route that analysis to `/contradiction-check` with the Requirements Engineer (`@requirements-engineer`)

## Output Format

A report presented to the team:

```markdown
## Acceptance report: 001-pagamento-beneficio

| REQ-ID | Criterion (Given/When/Then) | Implementation (file:line) | Test (file:line) | Status |
|---|---|---|---|---|
| REQ-PAY-014 | Given an inactive beneficiary, when the batch runs, then the row is rejected | backend/.../PaymentBatchService.java:132 | backend/.../PaymentBatchServiceTest.java:88 | Pass |
| REQ-PAY-021 | Given a corrected amount, when it is persisted, then it is rounded to 2 decimal places | backend/.../BenefitAmount.java:57 | - | Gap |
| REQ-PAY-030 | Given a duplicate row, when it is submitted, then it is ignored | - | - | Fail |

### Top risks
1. REQ-PAY-030 (Fail): duplicate handling is not implemented and blocks release.
2. REQ-PAY-021 (Gap): rounding is implemented but untested, creating a regression risk.
```

## Definition of Done

- [ ] Each in-scope REQ-ID appears in the report
- [ ] Each criterion has an Implementation and Test cell, or an explicit dash with a reason
- [ ] Each status is Pass, Gap, or Fail and has supporting references
- [ ] Gaps and Failures are summarized as prioritized risks
- [ ] No code, test, or specification file has been modified

## Prompt Body

You are the Product Owner (`@product-owner`), checking the delivery against the specification, not the intent.

**Step 1: load the specification.**
Read `specs/<NNN>-<feature>/spec.md` and list each REQ-ID with its acceptance criteria.

**Step 2: locate implementations.**
Search for the behavior in `backend/` and `frontend/`. Prefer REQ-ID references in Javadoc or comments. If there are none, search for the behavior. Cite `file:line`.

**Step 3: locate tests.**
Search for the REQ-ID string in `backend/src/test` and test files in `frontend/`. This is exactly what the `spec-traceability` CI job looks for. Cite `file:line`.

**Step 4: classify.**
Pass = code and test; Gap = code without a test; Fail = no code. Be strict: no reference, no pass.

**Step 5: summarize risk.**
List Failures first, then Gaps, starting with the greatest business impact.

Keep the review read-only and cite all evidence. Never claim coverage you cannot point to. When you cannot find the code, classify it as Gap or Fail, never as an assumption.

## Example Invocation

```text
/acceptance-check feature=001-pagamento-beneficio
```
