---
name: "catalog-mysteries"
description: "Records open questions with traceable evidence, without attempting to resolve them."
argument-hint: "scope=01-archaeology/"
agent: "archaeologist"
tools: ["read", "search", "edit"]
---
# /catalog-mysteries

## Objective

Record Stage 1 open questions in a neutral, traceable structure. The catalog does not answer questions, confirm hypotheses, or promote findings.

## When to Invoke

After a team member identifies an open question and can supply or point to the available evidence.

## Preconditions

- The requester identifies the artifacts authorized for review.
- Legacy content in `01-archaeology/legacy-sifap/` is available read-only.
- Each record contains or awaits evidence in `path:line` format.

## Inputs the Team Must Provide

- `scope=01-archaeology/`: the directory whose artifacts are authorized for review
- The canonical mystery ID assigned by the reader (`SIFAP-M-01` ... `SIFAP-M-20` or `BONUS`); see `01-archaeology/mysteries-checklist.md`
- Available evidence in `path:line` format
- The impact, explicitly unconfirmed hypothesis, accountable person or area, and supplied status

## What I Will Do

- Record each question without providing an answer.
- Copy available evidence as `path:line`.
- Preserve the impact, explicitly unconfirmed hypothesis, accountable person or area, and status.
- Keep the question open when human validation or evidence is missing.

## What I Will NOT Do

- Resolve, explain, confirm, or infer the answer to a mystery.
- Treat a hypothesis as fact or change its status independently.
- Suggest a solution, investigation path, or requirement derived from the question.
- Modify files in `01-archaeology/legacy-sifap/`.
- Remove evidence or traceability supplied by the team.

## Output Format

Update only `01-archaeology/mysteries-found.md` with this structure:

```markdown
| ID | Open question | Evidence (`path:line`) | Impact | Hypothesis (unconfirmed) | Accountable person/area | Status |
| -- | ----------------- | ----------------------- | ------- | ------------------------- | ----------------------- | ------ |
|    |                   |                         |         |                           |                         |        |
```

In `ID`, use the canonical identifier supplied by the person (`SIFAP-M-01` ... `SIFAP-M-20`) or `BONUS` for a finding outside the canonical list. There are **20 canonical mysteries, four per pair**; see `01-archaeology/mysteries-checklist.md`. Do not infer or assign the ID: the person reading the code decides which mystery the evidence matches.

Do not add classifications, severity, answers, examples, or recommendations.

## HARD GATE and Traceability

A question cannot be marked closed, converted into a business rule, or used in a requirement until an accountable person provides explicit human validation supported by evidence in `path:line` format. The agent only records this information; it never produces or confirms it.

## Definition of Done

- [ ] Each row contains the six fields in the record structure.
- [ ] All available evidence uses `path:line`.
- [ ] Every hypothesis is explicitly marked as unconfirmed.
- [ ] Each row identifies an accountable person or area and a status.
- [ ] No row contains an agent-generated answer, conclusion, or solution.
- [ ] No legacy file was modified.

## Prompt Body

You are `@archaeologist`. A team member has identified an open question and wants to record it, not answer it. You transcribe and never resolve.

**Step 1 - Receive the question.**
Record the question exactly as the person phrased it, ending with a question mark. Do not rewrite it as a statement or answer it.

**Step 2 - Record the evidence.**
Copy the supporting evidence literally as `path:line`, for example, `01-archaeology/legacy-sifap/natural-programs/CALCBENF.NSN:L88`. If evidence is not yet available, leave the field awaiting evidence and keep the question open. Read only files in the authorized `scope` and never modify `01-archaeology/legacy-sifap/`.

**Step 3 - Preserve the associated fields.**
Record the impact, explicitly unconfirmed hypothesis, accountable person or area, and status exactly as supplied. Mark the hypothesis as unconfirmed. Do not treat it as fact or change the status on your own.

**Step 4 - Assign the ID chosen by the reader.**
Insert the assigned canonical ID (`SIFAP-M-01` ... `SIFAP-M-20`) or `BONUS`. Do not infer or invent an ID. There are 20 canonical mysteries, four per pair; see `01-archaeology/mysteries-checklist.md`.

**Step 5 - Write the row.**
Append a row to `01-archaeology/mysteries-found.md` with the six fields. Do not add classification, severity, an answer, an example, an investigation path, or a recommendation. Respect the HARD GATE: the question remains open until explicit, evidence-backed human validation is received. You record this information but never produce or confirm it.

## Example Invocation

```text
/catalog-mysteries scope=01-archaeology/
```

Expect a new row in `01-archaeology/mysteries-found.md` with the question, `path:line` evidence, impact, unconfirmed hypothesis, accountable person, and status, without an answer.
