---
name: "code-modernization"
description: "Use when modernizing a legacy system with a disciplined, behavior-preserving workflow. Triggers include \"modernize\", \"legacy code\", \"COBOL\", \"business rule extraction\", and \"behavior-preserving rewrite\"."
---
# Code modernization

Use this skill to guide behavior-preserving modernization of legacy systems. The workflow is divided into stages so the team understands the system before transforming it.

## When to Invoke

- "Plan the modernization of this legacy module."
- "Assess this codebase before we rewrite anything."
- "Extract the business rules hidden in this program."
- "Transform this module while preserving its behavior."

## Workflow

1. **Brief**: define what will be modernized, why now, constraints, exclusions, and success criteria.
2. **Assess**: inventory languages, modules, integrations, builds, test coverage, complexity, and risks.
3. **Extract rules**: turn hidden procedural logic into business rule cards with source code evidence.
4. **Map**: relate legacy modules to target domains, packages, and services and to the migration sequence.
5. **Reimagine**: design the target API, data model, runtime, and operational model.
6. **Transform**: rewrite module by module in `backend/` and `frontend/`, with tests that pin legacy behavior.
7. **Harden**: review security, tests, error handling, observability, and deployment readiness.

## GitHub Copilot primitives

| Need | Primitive |
| --- | --- |
| In-depth legacy discovery | [`@archaeologist`](../../agents/archaeologist.agent.md) agent (Stage 1) |
| Business rule extraction | [`/extract-business-rules`](../../prompts/stage-archaeologist-extract-business-rules.prompt.md) prompt |
| Target design and ADRs | [`@architect`](../../agents/architect.agent.md) agent (Stage 2) |
| Module translation and tests | [`@builder`](../../agents/builder.agent.md) agent (Stage 3) |
| Security and delivery hardening | [`@evolution`](../../agents/evolution.agent.md) agent (Stage 4) |
| Safe legacy code reading | [`natural-adabas`](../../instructions/natural-adabas.instructions.md) instructions |

## Folder contract

- `01-archaeology/legacy-sifap/**`: legacy source code and behavior evidence. Read-only.
- `01-archaeology/**` and `specs/<NNN>-<feature>/`: briefs, assessments, maps, rule catalogs, EARS specifications, and reports.
- `backend/**` and `frontend/**`: transformed or replacement implementation and tests.

## Rules

- Do not transform code before assessment and business rule extraction.
- Cite source files in findings. If line numbers are unavailable, cite the file and explain why.
- Distinguish observed behavior from inferred intent.
- Prefer several focused artifacts to an excessively large report.
- Use characterization tests to preserve legacy behavior before intentional changes.
- Do not invent complexity, cost, runtime, or risk metrics. Use measured values or state assumptions.

## Validation

- Run available inventory tools such as `scc`, `cloc`, or language-specific analyzers.
- Run available test suites before and after transformation.
- For transformed modules, provide evidence that tests compare or pin legacy behavior.
- During hardening, report findings by severity with concrete fixes.

## Output Template

Record each modernized module as an assessment note in `01-archaeology/`, linked to its target in `backend/` or `frontend/`:

```markdown
## Modernization record - <legacy module>

| Field | Value |
|---|---|
| Legacy source code | 01-archaeology/legacy-sifap/natural-programs/<FILE>.NSN |
| Target module | backend/src/main/java/<package>/ |
| Stage reached | Brief / Assess / Extract / Map / Reimagine / Transform / Harden |
| Behavior evidence | <characterization test path> |
| Traces to | REQ-NNN |

### Observed behavior
- <fact drawn from the legacy code, with path:line evidence>

### Open questions
- <mystery that needs human validation>
```

## Quality Gate

- [ ] Assessment and business rule extraction were completed before any transformation.
- [ ] Every finding cites a legacy source file, with line numbers when available.
- [ ] Observed behavior is separate from inferred intent.
- [ ] Characterization tests pin legacy behavior before intentional changes.
- [ ] No complexity, cost, runtime, or risk metrics are invented. Values are measured or identified as assumptions.
