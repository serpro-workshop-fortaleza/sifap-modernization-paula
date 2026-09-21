---
name: "spec"
description: "Draft EARS requirements in spec.md from user stories, each with a mandatory legacy traceability line."
argument-hint: "feature=NNN-feature-name stories=<path-or-inline>"
agent: "product-owner"
tools: ["read", "search", "edit"]
---
# /spec

## Objective

Turn confirmed user stories into formal EARS requirements in `specs/<NNN>-<feature>/spec.md`. Each requirement contains a unique REQ-ID, a Given/When/Then acceptance criterion, and a valid `source_legacy:` line. This allows the `legacy-traceability` continuous integration (CI) job to pass on the first submission.

## When to Invoke

At the start of Stage 2, after the pair has read its assigned Natural programs (the HARD GATE in `01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`) and the team has agreed on a narrow feature.

## Preconditions

- `specs/<NNN>-<feature>/` exists (created by the Specify command-line interface, the Specify CLI)
- `.specify/memory/constitution.md` exists
- `01-archaeology/business-rules-catalog.md` contains confirmed rules and source line ranges
- The pair has read the legacy files it intends to cite

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>`: the folder in `specs/`
- The confirmed user stories or business rules to formalize (a path or inline text)
- For each story, the legacy source: a `01-archaeology/legacy-sifap/natural-programs/*.{NSP,NSN,NSS,NSA,NSL,NSC,NSM,jcl}` or `01-archaeology/legacy-sifap/adabas-ddms/*.{NSD,ddm,txt}` path, or an explicit justification with `[GREENFIELD]`
- Ask the user for any missing information.

## What I Will Do

- Read `.specify/memory/constitution.md` and list the constraints related to the feature
- Read each cited legacy file before drafting any requirement
- Refine raw stories with the [`user-story-refine`](../skills/user-story-refine/SKILL.md) skill (INVEST and vertical slices)
- Classify each requirement by EARS pattern with the [`sdd-requirements-engineer`](../skills/sdd-requirements-engineer/SKILL.md) skill
- Assign unique REQ-IDs in the `REQ-<DOMAIN>-NNN` format
- Append a `source_legacy:` line to each requirement
- Write Given/When/Then acceptance criteria and mark out-of-scope items

## What I Will NOT Do

- Write an EARS requirement without a `source_legacy:` line. I will request the source or a `[GREENFIELD]` marker and stop
- Invent the contents of a Natural program or DDM field. I will read the file or ask the team, without relying on memory
- Point `source_legacy:` to `legacy-docs/*.md`. The mandatory check accepts only paths in `natural-programs` and `adabas-ddms`, or `[GREENFIELD]`
- Turn an unvalidated hypothesis or open question into a requirement
- Scan the entire specification for contradictions between requirements. That is the role of `/contradiction-check` with the Requirements Engineer (`@requirements-engineer`)

## Output Format

Append EARS blocks to `specs/<NNN>-<feature>/spec.md`. The mandatory CI check parses the `REQ-ID:` key and the `source_legacy:` line located within the next 20 lines.

```yaml
REQ-PAY-014:
  pattern: unwanted
  text: "IF a payment row references an inactive beneficiary, THEN the system SHALL reject the row and record the rejection reason."
  source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L<start>-L<end>
  acceptance:
    - "Given an inactive beneficiary, when the batch processes the row, then the row is rejected with reason INACTIVE_BENEFICIARY."
  priority: P0

REQ-AUTH-001:
  pattern: unwanted
  text: "IF a user submits invalid credentials three consecutive times, THEN the system SHALL lock the account for 15 minutes."
  source_legacy: "[GREENFIELD] Authentication and lockout have no equivalent in the batch-oriented legacy system."
  acceptance:
    - "Given three consecutive failed authentication attempts, when a fourth attempt occurs, then the system responds with 423 Locked (account locked)."
  priority: P1
```

> [!NOTE]
> The wording above is illustrative. The `<PROGRAM>` and `<start>`/`<end>` tokens must be replaced with the actual file and line range the team has read. The model never fills them in from memory.

## Definition of Done

- [ ] Each story is expressed as an EARS requirement with exactly one pattern
- [ ] Each requirement has a unique REQ-ID in the `REQ-<DOMAIN>-NNN` format (or `REQ-NNN`)
- [ ] Each requirement has a valid `source_legacy:` line within 20 lines after the REQ-ID (an actual path in `natural-programs`/`adabas-ddms`, or `[GREENFIELD]` with justification)
- [ ] Each requirement has at least one Given/When/Then acceptance criterion
- [ ] No requirement contradicts `.specify/memory/constitution.md`
- [ ] Assumptions and out-of-scope items are stated explicitly
- [ ] Open questions remain questions, not requirements

## Prompt Body

You are the Product Owner (`@product-owner`). The team has agreed on a narrow feature and is presenting user stories to formalize.

**Step 1: confirm the feature and read the constraints.**
Open `specs/<NNN>-<feature>/spec.md` (if it exists) and `.specify/memory/constitution.md`. List the constitutional rules that constrain the feature.

**Step 2: require a legacy source for each story.**
For each story or rule, require a path in `natural-programs` or `adabas-ddms` (preferably with `#L<start>-L<end>`) or an explicit justification with `[GREENFIELD]`. If the story has neither, stop and ask. Do not draft it.

**Step 3: read the cited legacy files.**
Open each cited `.NSP`, `.NSN`, `.ddm`, or `.txt` file and confirm the behavior before drafting the requirement. Never infer a rule from the filename.

**Step 4: refine the stories.**
Apply the [`user-story-refine`](../skills/user-story-refine/SKILL.md) skill: INVEST, one outcome per story, and vertical slices.

**Step 5: formalize in EARS.**
Use the patterns from the [`sdd-requirements-engineer`](../skills/sdd-requirements-engineer/SKILL.md) skill. Use exactly one pattern per requirement. Split any hidden "and" into separate requirements.

**Step 6: assign REQ-IDs and traceability.**
Assign each requirement a unique `REQ-<DOMAIN>-NNN`. Place the `source_legacy:` line directly below the REQ-ID and add Given/When/Then acceptance criteria.

**Step 7: flag and defer.**
Record ambiguities, contradictions with the constitution, and out-of-scope items. Route a full contradiction analysis to `/contradiction-check`.

No requirement is delivered without a `source_legacy:` line. Otherwise, the `legacy-traceability` CI job rejects the pull request (PR), and `legacy-docs/*.md` is not an accepted source. Never invent legacy behavior. If you have not read the file, say so and request the source.

## Example Invocation

```text
/spec feature=001-pagamento-beneficio stories=02-modern-spec/user-stories.md
```
