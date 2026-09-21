# Instruction index

This directory contains the immersion's file-specific GitHub Copilot instructions.

> Important: Copilot discovers `*.instructions.md` files in `.github/instructions/` and its subdirectories. This immersion keeps them directly in this directory to make the index and scopes easy to review.

## Instruction files

| File | Description | `applyTo` scope |
| --- | --- | --- |
| `agent-skills.instructions.md` | Use when creating, reviewing, or debugging GitHub Copilot Agent Skills: SKILL.md frontmatter, name-to-directory equality, description tuning, and progressive disclosure. | `.github/skills/**/SKILL.md` |
| `backend.instructions.md` | Use when implementing backend APIs, services, controllers, request validation, error handling, and business service boundaries. | `backend/src/main/java/**,backend/src/test/java/**` |
| `cicd.instructions.md` | Use when creating or reviewing GitHub Actions, CI/CD workflows, YAML pipeline gates, build checks, and deployment automation. | `.github/workflows/**,.github/actions/**,**/action.yml,**/action.yaml` |
| `database.instructions.md` | Use when writing database repositories, migrations, schema changes, SQL queries, indexes, and rollback-safe data changes. | `backend/src/main/java/**/infrastructure/**,backend/src/main/resources/db/migration/**` |
| `draw-io.instructions.md` | Use when creating, editing, or reviewing draw.io diagrams and mxGraph XML in .drawio, .drawio.svg, or .drawio.png files. | `**/*.drawio,**/*.drawio.svg,**/*.drawio.png` |
| `frontend-spec.instructions.md` | Use when implementing or reviewing Next.js 15 App Router, TypeScript, Tailwind CSS, shadcn/ui, and server components in frontend/. | `frontend/app/**,frontend/components/**,frontend/src/app/**,frontend/src/components/**,frontend/**/*.ts,frontend/**/*.tsx` |
| `frontend.instructions.md` | Use when creating frontend UI components, pages, client interactions, component state, accessibility, and user-facing workflows. | `frontend/app/**,frontend/components/**,frontend/src/app/**,frontend/src/components/**` |
| `infrastructure.instructions.md` | Use when creating or reviewing infrastructure as code, Terraform, Bicep, Azure resource definitions, and environment configuration. | `infra/**,**/*.tf,**/*.bicep,compose*.yml,compose*.yaml,docker-compose*.yml,docker-compose*.yaml` |
| `java-junit5-assertions.instructions.md` | Use when writing or reviewing JUnit 5 (Jupiter) assertions in backend Java tests: expected-value ordering, lazy messages, assertAll, assertThrows/assertThrowsExactly, timeouts, and assertInstanceOf. | `**/*Test.java,**/*IT.java,**/*Steps.java,**/*StepDefs.java` |
| `modular-monolith.instructions.md` | Use when designing or reviewing Modular Monolith architecture, package-by-feature boundaries, JPA mapping, and Strangler Fig migration. | `backend/src/main/java/**,backend/pom.xml,backend/build.gradle*` |
| `natural-adabas.instructions.md` | Use when reading Natural/Adabas legacy code, language patterns, FDT structure, naming conventions, and batch workflows. | `01-archaeology/legacy-sifap/**,**/*.NSP,**/*.nsp,**/*.NSN,**/*.nsn,**/*.NSS,**/*.nss,**/*.NSA,**/*.nsa,**/*.NSL,**/*.nsl,**/*.NSC,**/*.nsc,**/*.NSM,**/*.nsm,**/*.NSD,**/*.nsd,**/*.NAT,**/*.nat,**/*.CPY,**/*.cpy,**/*.DDM,**/*.ddm,**/*.jcl,**/*.JCL` |
| `sdd-artifacts.instructions.md` | Use when editing SDD requirements, plans, tasks, scope decisions, bounded contexts, and supporting ADRs. | `specs/**/*.md,specs/**/*.yaml,specs/**/*.json,02-modern-spec/scope-decisions.md,02-modern-spec/bounded-contexts.md,02-modern-spec/ADRs/*.md` |
| `security.instructions.md` | Use when implementing or reviewing authentication, authorization, cryptography, secure configuration, secret handling, and security-sensitive code. | `backend/src/main/java/**/auth/**,backend/src/main/java/**/security/**,backend/src/main/java/**/config/**,backend/src/main/resources/**,frontend/**/auth/**,frontend/**/middleware.ts` |
| `terraform.instructions.md` | Use for general Terraform hygiene (file layout, variables, outputs, formatting, validation, tests, and state); the kit's Azure rules live in infrastructure.instructions.md. | `**/*.tf` |
| `tests.instructions.md` | Use when creating or reviewing automated tests, test strategy, specs, coverage gaps, regression tests, and quality gates. | `**/*.test.*,**/*.spec.*,**/tests/**` |

## Maintenance rule

- Every file MUST retain valid YAML frontmatter with exactly the required `description` and `applyTo` fields.
- `applyTo` is a single quoted string; multiple globs are comma-separated without spaces.
- Avoid `applyTo: "**"`; prefer specific globs matching the files actually governed by the instruction.
- Keep the internal pattern consistent: introductory paragraph -> topical sections -> `## Conventions` -> `## Do / Don't` -> `## PR Checklist`.
- When creating a new area, add a flat `*.instructions.md` file in this directory and update this index.
