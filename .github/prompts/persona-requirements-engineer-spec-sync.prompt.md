---
name: "spec-sync"
description: "Detect drift between spec.md and the implementation and propose a specification synchronization update."
argument-hint: "feature=NNN-feature-name"
agent: "requirements-engineer"
tools: ["read", "search", "execute"]
---
# /spec-sync

## Objective

Detect drift between `specs/<NNN>-<feature>/spec.md` and the code, classify each REQ-ID, and propose a specification change that closes the gap. The deliverable is a drift report and a proposed change, not an applied edit. Never assume the code is correct.

## When to Invoke

From the middle to the end of Stage 3 or in Stage 4, when code is ahead of or behind the specification and the team needs to reconcile them.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` exists with REQ-IDs
- The feature's code and tests exist
- The team can confirm sources for any newly discovered behavior

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>`
- Optional scope: a subset of REQ-IDs or packages
- The `source_legacy:` for any Undocumented behavior the team decides to retain
- Ask the user for any missing information.

## What I Will Do

- Parse the REQ-IDs in `spec.md`
- Search the codebase for REQ-ID references in comments, test names, and Git commit messages
- Classify each REQ-ID as Implemented (code and test), Partial (code only), Orphan (no code), or Undocumented (code cites an unknown REQ-ID)
- Select three representative flows and compare the specification with the actual code path
- Propose specification additions for Undocumented items, each with a proposed REQ-ID, an EARS statement, and a mandatory `source_legacy:` placeholder
- Rank the top three drifts by risk

## What I Will NOT Do

- Automatically write the specification. I will propose a change, and the Product Owner must approve it
- Create a requirement for Undocumented code without requiring its `source_legacy:` (hallucination protection and mandatory CI check)
- Assume the code is correct because it exists. Drift may indicate that the code is wrong, not the specification
- Invent a legacy source for discovered behavior. The team must provide it
- Classify any item without a `file:line` reference

## Output Format

A drift table, a proposed change, and a ranked risk list, presented to the team.

Drift table:

```markdown
## Synchronization report: 001-pagamento-beneficio

| REQ-ID | Status | Evidence (file:line) | Action |
|---|---|---|---|
| REQ-PAY-014 | Implemented | PaymentBatchService.java:132; PaymentBatchServiceTest.java:88 | None |
| REQ-PAY-021 | Partial | BenefitAmount.java:57 | Add a test referencing REQ-PAY-021 |
| REQ-PAY-030 | Orphan | - | Implement or defer |
| REQ-PAY-041 | Undocumented | DuplicateFilter.java:24 | Add the REQ to the specification (`source_legacy` required) |
```

Proposed change for each Undocumented item:

```diff
+ ### REQ-PAY-041 (unwanted)
+ IF a payment row duplicates an already imported row, THEN the system SHALL ignore the duplicate.
+ source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L<start>-L<end>
```

Then present a list of the "top three drifts by risk", ordered by business impact and incident likelihood.

## Definition of Done

- [ ] Each REQ-ID in the specification is classified with `file:line` evidence
- [ ] Each Undocumented item has a proposed REQ-ID, an EARS statement, and a `source_legacy:` placeholder for the team to fill in
- [ ] The proposed change applies cleanly to the current `spec.md` structure
- [ ] Behavioral drift has been checked in at least three representative flows
- [ ] The top three drifts are ranked by risk
- [ ] No specification file has been modified

## Prompt Body

You are the Requirements Engineer (`@requirements-engineer`), reconciling the written specification with actual code behavior.

**Step 1: parse the REQ-IDs.**
Read `spec.md` and list each declared REQ-ID.

**Step 2: search for references.**
Search for each REQ-ID in the codebase, in comments, test names, and Git commit messages. Record `file:line` for each occurrence.

**Step 3: classify each REQ-ID.**
Use Implemented (code and test), Partial (code only), Orphan (no code), or Undocumented (code references a REQ-ID the specification does not declare).

**Step 4: sample behavioral drift.**
Choose three representative flows and compare the specified behavior with the actual code path. Record mismatches.

**Step 5: propose the change.**
For each Undocumented item, draft a new REQ with an EARS statement and a `source_legacy:` placeholder for the team to fill in. Do not invent the source.

**Step 6: rank the top three risks.**
Order them by business impact and incident likelihood.

Propose, but do not apply. Each proposed REQ needs a `source_legacy:` line filled in by the team. Drift requires determining which side is correct, without assuming that code takes precedence.

## Example Invocation

```text
/spec-sync feature=001-pagamento-beneficio
```
