---
name: "gen-specs-as-issues"
description: "Identify gaps between SIFAP legacy behavior and the modern specification, prioritize them, and open EARS-based GitHub issues with legacy traceability."
argument-hint: "area=<focus-area> repo=<owner/name>"
agent: "requirements-engineer"
tools: ["read", "search", "edit", "github/*"]
---
# /gen-specs-as-issues

## Objective

Find missing or underspecified behaviors in the SIFAP 2.0 modernization, prioritize them, and turn the top items into detailed GitHub issues. Each issue is an EARS specification with a unique REQ-ID and a mandatory `source_legacy:` line. This keeps every requirement traceable from the legacy Natural/Adabas code to the modern system.

> [!IMPORTANT]
> The `legacy-traceability` CI job rejects requirements without a `source_legacy:` line. Every issue opened by this command must cite a legacy artifact or provide a `[GREENFIELD]` justification.

## When to Invoke

During Stage 2 (specification) or Stage 4 (evolution), when the team needs to turn observed gaps into a prioritized, traceable list of specifications.

## Preconditions

- The pair has read the relevant legacy programs, as required by the HARD GATE in [`LEGACY-EXPLORATION-CHECKLIST.md`](../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md)
- The modern specification in `02-modern-spec/` and any content in `specs/` are available for comparison
- The team is authenticated to the target GitHub repository

## Inputs the Team Must Provide

- `area`: the focus area or bounded context to analyze, for example, payment inspection
- `repo`: the `owner/name` of the GitHub repository for the issues
- The legacy programs relevant to the area in `01-archaeology/legacy-sifap/`
- Ask the user for any missing information.

## What I Will Do

- Compare legacy behavior in the focus area with the modern specification and list gaps
- Score each gap by impact and risk and select the priority items
- Write each issue as an EARS requirement according to [`sdd-artifacts.instructions.md`](../instructions/sdd-artifacts.instructions.md)
- Assign a unique REQ-ID and a `source_legacy:` line; after explicit approval, search for duplicates and open issues with GitHub tools

## What I Will NOT Do

- Write a requirement without a `source_legacy:` line or an explicit `[GREENFIELD]` justification
- Invent behavior absent from both the legacy system and the modern specification
- Open issues before the team confirms the prioritized list
- Assign a `spec/` branch to implementation work; these are Stage 2 specification issues on `spec/<NNN>-<feature>`

## Output Format

```markdown
### Gap analysis — <area>
Gaps found: <observed count> · Selected for filing: <approved count>

### Issues to create
- [SPEC][REQ-NNN] <evidence-backed behavior title>
  source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L<start>-L<end>
  branch: spec/<NNN>-<feature-slug>
```

## Definition of Done

- [ ] Each selected gap is written in EARS notation with a unique REQ-ID
- [ ] Each issue contains a `source_legacy:` line or a `[GREENFIELD]` justification
- [ ] Each issue specifies a `spec/<NNN>-<feature>` branch
- [ ] Issues have been created with GitHub tools only after team confirmation, and returned URLs are recorded

## Prompt Body

You produce a prioritized, traceable list of specifications. EARS notation and REQ-ID rules are in [`sdd-artifacts.instructions.md`](../instructions/sdd-artifacts.instructions.md). Use the [`sdd-requirements-engineer`](../skills/sdd-requirements-engineer/SKILL.md) skill to check each statement before filing.

**Step 1 — Establish the baseline.**
Read the legacy programs for `area` in `01-archaeology/legacy-sifap/` and the modern specification in `02-modern-spec/`. Confirm that the mandatory reading gate in the [checklist](../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md) has been met.

**Step 2 — Find and score gaps.**
List behaviors present in the legacy system but missing or vague in the modern specification. Score them by impact and risk and select the top items.

**Step 3 — Write EARS requirements.**
For each selected gap, write an EARS statement, assign the next REQ-ID, and add the `source_legacy:` line pointing to the legacy artifact. Validate with [`sdd-requirements-engineer`](../skills/sdd-requirements-engineer/SKILL.md).

**Step 4 — Confirm and file.**
Present the list with the proposed `spec/<NNN>-<feature>` branches. After explicit approval, identify the authenticated user and repository, search for duplicate open issues, list issue types for an organization repository, and create the issues with GitHub tools. Record returned URLs and report partial failures honestly.

## Example Invocation

```text
/gen-specs-as-issues area="payment inspection" repo=my-org/sifap-2
```
