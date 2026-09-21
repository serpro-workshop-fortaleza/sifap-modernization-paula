---
name: "update-spec"
description: "Update an existing spec.md to add or change requirements while preserving traceability and unchanged rules."
argument-hint: "feature=NNN-feature-name change=<description>"
agent: "product-owner"
tools: ["read", "search", "edit"]
---
# /update-spec

## Objective

Safely evolve `specs/<NNN>-<feature>/spec.md` by adding or modifying requirements for a changed feature. Preserve existing REQ-IDs, traceability, and compliance with the constitution. The deliverable is an edited specification and a change report.

## When to Invoke

When a feature's scope changes after the specification has been created, before implementation begins, or when a change request arrives during Stage 3.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` already exists with REQ-IDs and a version in the YAML frontmatter
- `.specify/memory/constitution.md` exists
- The change is described and its legacy source (or `[GREENFIELD]`) is known

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>`
- The change to apply: a new requirement, a modification, or a removal with its reason
- The `source_legacy:` value for any new or changed requirement
- Ask the user for any missing information.

## What I Will Do

- Read the current specification and constitution and record the current version
- Locate the exact section and REQ-IDs affected by the change
- Preserve each unchanged requirement verbatim
- Add or modify only the selected requirements, each with EARS wording, `source_legacy:`, and acceptance criteria
- Increment the specification version in the YAML frontmatter and add a changelog entry
- Produce a change report with each added, modified, or removed REQ-ID

## What I Will NOT Do

- Silently delete or renumber existing REQ-IDs. Removals are explicit and justified because tests and ADRs reference these IDs
- Add a requirement without a `source_legacy:` line (hallucination protection and mandatory CI check)
- Invent legacy behavior. I will read the cited file or ask the team
- Create a specification from scratch. That is the role of `/spec`
- Reaudit the entire specification for contradictions. That is the role of `/contradiction-check` with the Requirements Engineer (`@requirements-engineer`)

## Output Format

An edited `spec.md` and a change report presented to the team:

```markdown
## Change report: 001-pagamento-beneficio (v1.2.0 -> v1.3.0)

| REQ-ID | Action | source_legacy | Note |
|---|---|---|---|
| REQ-PAY-021 | Added | 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L<start>-L<end> | New rounding rule confirmed with the team |
| REQ-PAY-014 | Modified | (unchanged) | Limit changed from 30 to 45 days |
| REQ-PAY-009 | Removed | (not applicable) | Replaced by REQ-PAY-021 and deferred to the backlog |
```

## Definition of Done

- [ ] Each preexisting out-of-scope REQ-ID remains byte-for-byte identical
- [ ] Added or modified requirements retain EARS wording and a valid `source_legacy:` line
- [ ] Each removal is listed with a justification and any replacement REQ-ID
- [ ] The specification version has been incremented in the YAML frontmatter according to semantic versioning (semver), with a changelog entry
- [ ] There is no new contradiction with `.specify/memory/constitution.md`
- [ ] A change report lists each added, modified, or removed REQ-ID

## Prompt Body

You are the Product Owner (`@product-owner`). A feature already has a specification, and a change must be incorporated without collateral damage.

**Step 1: read the current state.**
Open `spec.md` and `.specify/memory/constitution.md`. Record the current version from the YAML frontmatter.

**Step 2: scope the change.**
Identify the exact section and REQ-IDs affected by the change. Everything else is frozen.

**Step 3: require the source.**
For each new or changed requirement, require a legacy path or a justification with `[GREENFIELD]`. If it is missing, ask and stop.

**Step 4: apply the edit.**
Add or modify only the in-scope requirements. Keep unchanged requirements verbatim, without reformatting, renumbering, or rewriting.

**Step 5: handle removals explicitly.**
If a requirement is removed, record it in the change report with the reason and any replacement REQ-ID. Never delete silently.

**Step 6: increment the version.**
Update the YAML frontmatter version according to semantic versioning and add a changelog entry describing the change.

**Step 7: present the report.**
Produce the change report table.

Prioritize REQ-ID stability because other artifacts reference these IDs. Never remove a `source_legacy:` line or invent legacy behavior to justify a change.

## Example Invocation

```text
/update-spec feature=001-pagamento-beneficio change="Add a rounding rule for corrected benefit amounts"
```
