# SDD document and Mermaid standard

Use this contract for canonical packages under `specs/<NNN>-<feature>/` and
supporting Stage 2 decisions. The [artifact instructions](../../../instructions/sdd-artifacts.instructions.md)
own filenames and validation boundaries. Include only sections and diagrams
that clarify the approved scope; do not generate a parallel artifact tree.

## Artifact responsibilities

| Artifact | Required responsibility |
| --- | --- |
| `spec.md` | Canonical EARS requirements, `source_legacy`, acceptance, source register, assumptions, scope, approval, and open decisions |
| `plan.md` | Design, applicable diagrams, decisions or ADR links, risks, test strategy, and requirement-to-component traceability |
| `tasks.md` | Dependency order, test mapping, checkboxes, completion gate, deterministic commands, and dated execution evidence |
| Supporting contracts and decisions | Separate files only when justified, linked from the owning artifact, with explicit applicability |

## Universal Mermaid theme

Begin every Mermaid block with this exact directive:

```text
%%{init: {"theme":"base","themeVariables":{"background":"#FFFFFF","primaryColor":"#FFFFFF","primaryTextColor":"#222222","primaryBorderColor":"#777777","lineColor":"#555555","secondaryColor":"#F2F2F2","tertiaryColor":"#E8E8E8"}}}%%
```

For `flowchart`, `graph`, and `classDiagram`, include these
definitions exactly once:

```text
classDef default fill:#FFFFFF,stroke:#777777,color:#222222
classDef zone fill:#F2F2F2,stroke:#999999,color:#222222
classDef external fill:#E8E8E8,stroke:#555555,color:#222222
```

Use `zone` for owned boundaries and logical groupings, and `external` for
actors, external systems, neighboring specifications, or evidence sources
outside the feature boundary. `stateDiagram`, `sequenceDiagram`, `erDiagram`,
and `gantt` inherit the universal theme and must not contain `classDef`.
Current `stateDiagram-v2` renderers treat `default` as a reserved token.

Keep diagrams reviewable:

- fewer than 40 nodes per block;
- short labels, with detail in adjacent tables;
- quoted edge labels;
- explicit subgraph IDs;
- no chromatic colors;
- separate current, partial, planned, blocked, and target states.

## Required design portfolio

When material to the feature, `plan.md` includes:

1. Architecture Overview
2. System Context
3. Component or Service Map
4. Deployment View
5. State Model
6. Critical Sequences
7. Data Flow or Data Lifecycle
8. Data Model
9. Interfaces and Contracts
10. Error, Security, Threat, and Observability design
11. Implementation Surface
12. Delivery and Traceability View
13. Risks and Trade-Offs
14. Phased Development

The delivery view maps real REQ/NFR IDs to design components, plan items and
tasks, dependency IDs or neighboring specs, tests/evidence, and
current-versus-target state. Do not invent an implementation or approval to
complete a diagram.

## Task contract

Use one checkbox entry per task:

```text
- [ ] **T001 [S] [Plan:P1.1] RED** Add a failing contract test. Traces REQ-001.
  - Files: `tests/test_contract.py`.
  - Acceptance: TST-C001 fails before implementation and passes afterward.
```

- `[S]` means sequential; `[P]` means dependency- and change-surface independent.
- The dependency DAG contains every task exactly once.
- The test map names the governing requirements and planned or executed tests.
- `[x]` is allowed only when the task appears in the dated
  `Marked complete by verification sweep:` ledger and its acceptance evidence
  exists.
- Existing partial code stays unchecked until the complete acceptance signal is
  demonstrated.

## Required validation

```bash
python3 -B .github/scripts/validate-spec-traceability.py --mode legacy
python3 -B .github/scripts/validate-spec-traceability.py --mode tests
python3 -B -m unittest discover -s .github/scripts/tests -v
```

The source gate blocks invalid declarations; the test report only warns about
missing references. Neither proves EARS correctness, source-line accuracy,
diagram syntax, approval, or passing product tests. Review those separately.
Render applicable diagrams using an available repository renderer and record
the result; if no renderer is available, report rendering as not executed.

Report a failing or blocked check as such. Never weaken a gate, add a baseline,
or create empty evidence merely to obtain a green result.
