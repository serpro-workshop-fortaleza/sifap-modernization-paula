---
applyTo: ".specs/**/*.md,.specs/**/*.yaml,.specs/**/*.json"
description: "Use when editing tracked SDD artifacts that require naming, EARS, traceability, evidence, or status conventions."
---

# Specification-Driven Development Artifacts

The `sdd-requirements-engineer` skill owns lifecycle and generation procedures. These instructions own only the durable shape of files under `.specs/`.

## Artifact Contracts

Every canonical feature package contains the same ten feature artifacts:

- `SPECIFICATION.md`
- `ANALYSIS.md`
- `DESIGN.md`
- `TASKS.md`
- `TESTING.md`
- `DECISIONS.md`
- `CHECKLIST.md`
- `CROSS_ANALYSIS.md`
- `VERIFICATION.md`
- `SOURCE_TRACEABILITY.md`

Every package also carries two subdirectories, both required by
`scripts/validate-specs.py`:

- `checkpoints/` holding `spec-to-plan.yaml`, `plan-to-tasks.yaml` and
  `test-coverage.yaml`.
- `contracts/` holding `manifest.yaml`, which declares which canonical
  contracts the package provides, alongside the contract files themselves.

Four of the ten markdown artifacts -- `CHECKLIST.md`, `CROSS_ANALYSIS.md`,
`VERIFICATION.md` and `SOURCE_TRACEABILITY.md` -- are generated from the other
six by `scripts/generate-sdd-support-artifacts.py`. Author the six and run the
generator; hand-authoring the four invites the two sides to disagree.

Reuse the repository-level `.specs/CONSTITUTION.md`. Do not create a
feature-local constitution as a substitute for missing feature artifacts.
Optional `IMPLEMENTATION_PLAN.md`, `TEST_PLAN.md`, or machine-readable test
manifests may supplement the portfolio but never replace an artifact above.
Historical packages follow the same content-quality and traceability standard;
their status may be historical or superseded, but their artifacts must remain
substantive and internally consistent.

- `SPECIFICATION.md` owns canonical REQ/NFR statements, acceptance scenarios,
  assumptions, dependencies, open decisions, and `implementation_status`.
- `ANALYSIS.md` owns the gate summary, cross-artifact traceability, dated
  validation evidence, current findings, approval conditions, and sign-off.
- `DESIGN.md` owns architecture, system context, components, deployment, state,
  critical sequences, data flow and lifecycle, interfaces, errors, security,
  observability, implementation surface, phased development, and the delivery
  trace from requirements through evidence.
- `TASKS.md` owns the dependency DAG, test mapping, phased checklist, completion
  gate, and dated execution ledger. A checked task must appear in the
  verification-sweep ledger; code presence without complete acceptance evidence
  stays unchecked and is reported as partial.
- `TESTING.md` owns the named test catalog, deterministic commands, evidence
  contract, exit criteria, and dated verification status.
- `DECISIONS.md` owns stable decision IDs, alternatives, consequences,
  evidence, requirement traces, and revisit triggers.

## Diagram and Task Presentation

- Use the same light neutral Mermaid palette in every graph-like SDD diagram:
  white feature-owned nodes, light-gray zones/groupings, and darker-gray
  external systems or neighboring specifications.
- Begin every Mermaid block, including sequence, ER, class, state, and gantt,
  with the canonical `theme: base` directive defining white background and
  primary nodes, dark-gray text and lines, light-gray secondary surfaces, and
  darker-gray tertiary surfaces.
- Give every `flowchart`, `graph`, and `classDiagram` the canonical `default`,
  `zone`, and `external` class definitions. Do not put `classDef` in
  `stateDiagram`, `sequenceDiagram`, `erDiagram`, or `gantt`; those types
  inherit the same colors from the universal theme directive. In particular,
  `stateDiagram-v2` treats `default` as a reserved token in current renderers.
- Make architecture, component, deployment, state, sequence, and data-flow or
  lifecycle views reviewable. Keep labels concise and move detail to tables.
- In `DESIGN.md`, map REQ/NFR IDs to design components, tasks or plan items,
  dependencies, tests/evidence, and current-versus-target state.
- In `TASKS.md`, use `- [ ]` or `- [x]` task entries with stable task ID, `[S]`
  or `[P]`, `[Plan:...]`, requirement trace, change surface, and acceptance
  evidence. The Mermaid dependency graph and execution ledger must cover the
  same task IDs.

## Conventions

- Name feature directories with a zero-padded numeric prefix and kebab-case slug, matching the `feature_id` in artifact frontmatter.
- Use the established uppercase artifact names such as `SPECIFICATION.md`, `DESIGN.md`, `TASKS.md`, `SOURCE_TRACEABILITY.md`, `VERIFICATION.md`, and `DECISIONS.md`.
- Give every normative requirement a unique stable ID and one observable EARS response using `SHALL`; do not reuse retired IDs for different behavior.
- Give acceptance criteria stable IDs tied to their parent requirement.
- Preserve bidirectional traceability from source and decision through requirement, design, task, test, verification, and evidence.
- Distinguish requested, brownfield, official, repository-constraint, and greenfield claims; greenfield behavior requires an explicit decision.
- Treat live-state claims as dated evidence with source, scope, result, and freshness limits. Plans and expected output are not proof of execution.
- Keep status, implementation state, blockers, and verification results truthful; use `PENDING` or `BLOCKED` when evidence is absent.
- Redact credentials, personal data, private tenant details, and sensitive command output from evidence.

## Do / Don't

| Do | Don't |
|---|---|
| Preserve the canonical artifact names, IDs and traceability defined above | Substitute optional plans for required artifacts |
| Retain dated execution evidence or an explicit blocker | Present artifact validation as implementation success |
| Reuse the repository constitution and the owning skill's workflow | Invent a parallel lifecycle in these file-shape instructions |

## PR Checklist

- [ ] Required artifacts, metadata, IDs, and cross-references are internally consistent.
- [ ] Every active requirement maps to acceptance, implementation, and verification evidence or an explicit blocker.
- [ ] Artifact-only validation is not reported as implementation success.
- [ ] `python3 scripts/validate-sdd-documents.py` passes for the canonical package.
- [ ] `python3 scripts/validate-design-diagrams.py` reports every SDD Mermaid block
  themed and free of chromatic colors.
