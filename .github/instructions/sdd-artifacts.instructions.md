---
applyTo: "specs/**/*.md,specs/**/*.yaml,specs/**/*.json,02-modern-spec/scope-decisions.md,02-modern-spec/bounded-contexts.md,02-modern-spec/ADRs/*.md"
description: "Use when editing tracked SDD artifacts that require naming, EARS, traceability, evidence, or status conventions."
---

# Specification-Driven Development Artifacts

The [sdd-requirements-engineer skill](../skills/sdd-requirements-engineer/SKILL.md) owns lifecycle and generation procedures. These instructions own the shape of this kit's `specs/` artifacts and supporting Stage 2 decisions. Follow the [H2 contract](../../00-TEAM-FLOW.md#handoff-h2-da-spec-para-o-código-fim-do-estágio-2-1500); do not create a parallel `.specs/` tree.

## Artifact Contracts

Each approved feature uses `specs/<NNN>-<feature>/` with these files:

| Artifact | Responsibility |
|---|---|
| `spec.md` | EARS requirements, `source_legacy`, acceptance criteria, scope, assumptions, dependencies, source register, and approval status |
| `plan.md` | Design, decisions, risks, applicable contracts and diagrams, test strategy, and requirement-to-component traceability |
| `tasks.md` | Dependency-ordered implementation and test tasks, REQ-ID/AC-ID mapping, planned checks, dated execution evidence, and completion status |
| `02-modern-spec/scope-decisions.md` | Human-approved scope and deferred work |
| `02-modern-spec/bounded-contexts.md`, `02-modern-spec/ADRs/` | Supporting boundary decisions and ADRs, only when needed |

Preserve existing standalone specifications and their IDs, including the portal specification. Do not rename them as part of a new feature. A requirements-only request does not authorize creating a full package. Add contracts, evidence files, or supplementary analysis only when the selected scope needs them, and link them from the owning artifact.

Reuse `.specify/memory/constitution.md` if the team has created it with Spec-Kit. If it is absent, record that fact and use the repository instructions; do not invent a constitution or claim CLI initialization. Templates from another repository do not impose extra filenames, generated artifacts, or scripts here.

## Requirements and Evidence

- Use `REQ-NNN` for new SIFAP requirements and preserve existing identifiers. Classify the EARS pattern and write one observable response using `shall`.
- Put a `source_legacy:` line within 20 lines after each requirement declaration and before the next requirement. It must name an existing supported legacy file or contain `[GREENFIELD]` plus an explicit justification, as defined in [repository instructions](../copilot-instructions.md).
- Give new acceptance criteria stable `AC-REQ-NNN-NN` IDs and Given/When/Then scenarios. Preserve existing acceptance IDs.
- Supplement primary evidence with `SRC-###` IDs where useful; they do not replace `source_legacy:`.
- Keep draft, approval, implementation, and verification states separate. Record `PENDING`, `BLOCKED`, or `NOT APPLICABLE` with a reason instead of inventing execution or acceptance.

## Diagram and Task Presentation

- Apply the [SDD document and Mermaid standard](../skills/sdd-requirements-engineer/references/sdd-document-and-mermaid-standard.md) to requested diagrams. Include only views that clarify a material decision; do not create diagrams to satisfy a quota.
- In `plan.md`, map requirements to design components, tasks, dependencies, tests/evidence, and current-versus-target state.
- In `tasks.md`, use checkboxes with a stable task ID, dependency/parallelism metadata, requirement and acceptance trace, change surface, and planned or executed evidence. A checked task requires actual acceptance evidence in its dated execution ledger.
- Keep a task graph consistent with the task list when a graph is needed. A planned red-green-refactor cycle is not proof that tests ran.

## Executable Checks

Run the same [traceability CLI](../scripts/validate-spec-traceability.py) used by [spec-quality.yml](../workflows/spec-quality.yml), from the repository root:

```bash
python3 -B .github/scripts/validate-spec-traceability.py --mode legacy
python3 -B .github/scripts/validate-spec-traceability.py --mode tests
python3 -B -m unittest discover -s .github/scripts/tests -v
```

`legacy` blocks invalid or missing source declarations. `tests` only reports missing REQ-ID references; it does not run tests or prove coverage. Neither mode verifies EARS semantics, human approvals, Mermaid rendering, line-anchor accuracy, or behavioral equivalence. Review those explicitly and attach execution evidence for applicable runtime checks. With no execution tool, report commands as not executed.

## Conventions

- Preserve the kit's lowercase filenames and zero-padded feature directories.
- Preserve bidirectional traceability from primary evidence through requirements, design, tasks, tests, and results.
- Treat live-state claims as dated evidence, not plans or expected output.
- Redact credentials, personal data, and sensitive command output from evidence.

## Do / Don't

| Do | Don't |
|---|---|
| Keep `specs/<NNN>-<feature>/spec.md`, `plan.md`, and `tasks.md` | Generate a parallel uppercase portfolio or `.specs/` tree |
| Use the checked-in validation commands and disclose their limits | Require absent scripts or claim semantic/runtime validation from a text scan |
| Retain human decisions, dated evidence, or explicit blockers | Mark planned work complete or simulate approval |

## PR Checklist

- [ ] Requested artifacts use canonical paths and consistent IDs, sources, and acceptance criteria.
- [ ] Every active requirement maps to planned or executed checks, with gaps explicit.
- [ ] The legacy-source gate passes and the informational test report is reviewed.
- [ ] EARS meaning, scope approval, diagram rendering, and runtime evidence are reviewed separately where applicable.
- [ ] Artifact validation is not reported as implementation success.
