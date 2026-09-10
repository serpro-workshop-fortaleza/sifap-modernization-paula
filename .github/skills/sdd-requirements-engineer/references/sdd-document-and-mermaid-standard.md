# SDD document and Mermaid standard

Use this contract for every canonical package under `.specs/`. The repository
instructions and executable validators remain authoritative when this reference
and the checked-in tree differ.

## Artifact responsibilities

| Artifact | Required responsibility |
| --- | --- |
| `SPECIFICATION.md` | Canonical REQ/NFR statements, acceptance, assumptions, dependencies, open decisions, and evidence-based implementation status |
| `ANALYSIS.md` | Gate summary, bidirectional traceability, dated evidence, findings, approval conditions, and sign-off |
| `DESIGN.md` | Architecture, context, components, deployment, state, sequences, data, interfaces, failures, security, observability, implementation surface, delivery traceability, and phased state |
| `TASKS.md` | Pre-gate, execution rules, dependency DAG, test mapping, phased checkboxes, completion gate, and execution ledger |
| `TESTING.md` | Named tests, deterministic commands, failure injection, evidence contract, exit criteria, and dated verification state |
| `DECISIONS.md` | Stable decisions, status, context, alternatives, consequences, traces, evidence, and revisit triggers |
| `checkpoints/` | Machine-readable requirement-to-plan-to-task-to-test closure |
| `contracts/` | Versioned API/state contracts or a reviewed non-applicability manifest |

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

When material to the feature, `DESIGN.md` includes:

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
python3 scripts/format-sdd-mermaid.py --check
python3 scripts/validate-design-diagrams.py
python3 scripts/validate-sdd-documents.py
python3 scripts/validate-specs.py --spec-root .specs --strict
python3 scripts/validate-spec-status.py .specs
python3 scripts/validate-task-graph.py --all
python3 scripts/validate-testing-evidence.py
```

Report a failing or blocked check as such. Never weaken a gate, add a baseline,
or create empty evidence merely to obtain a green result.
