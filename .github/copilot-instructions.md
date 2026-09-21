# GitHub Copilot instructions - Legacy modernization immersion

> These instructions tell Copilot what your team is building, which stack to use,
> which conventions to follow, and what NOT to do. They apply to the team's
> entire repository.

## Approved tools - use only these

This immersion uses a **fixed toolchain**: VS Code, GitHub Copilot (Ask + Plan + Agent modes), GitHub Spec-Kit, GitHub, Docker / Docker Compose, and Terraform. Other AI assistants, IDEs, web chat interfaces, and SDD frameworks are not allowed because mixing tools breaks traceability between specifications, code, and tests. Full table: [`README.md`](../README.md).

## Project context

Modernize the 29-year-old Natural/Adabas legacy system **SIFAP** (Payment Oversight and Administration System) to Java 21 + Next.js 15. Legacy code lives in [`01-archaeology/legacy-sifap/`](../01-archaeology/legacy-sifap/): 24 Natural members, 4 `.ddm` DDMs, and 1 FDT listing. The [`natural-programs/`](../01-archaeology/legacy-sifap/natural-programs/README.md) README documents the split between 15 assigned members and 9 supporting members.

The kit uses **two agent layers** (one persona kit per person + one stage agent per team). See [`06-stage-agents/README.md`](../06-stage-agents/README.md) for details.

Use the skills in [`.github/skills/`](skills/) for specialized workflows. Copilot selects the relevant skill by its description; do not duplicate specialized workflows in these global instructions.

## Repository languages

- Keep documentation and all Copilot primitive prose (agents, prompts, instructions, skills, and hooks) in English on `main` and `develop`; publish Brazilian Portuguese on `portugues-br` and Spanish on `espanol`.
- Follow the target branch's language, not the conversation's language. Never merge the translated documentation tree into `main`.
- Preserve technical paths, identifiers, and legacy sources. Keep the [language selector](../README.md#idiomas-do-repositório) linked to the existing branches and their instructions.
- The documentation portal in `site/` uses Astro + React, separately from the SIFAP application. Its translated UI dictionaries are allowed on `main`; documentation remains in English. See [ADR-0002](../docs/adr/0002-trilingual-documentation-portal.md).

## Target stack

- **Backend:** Java 21 + Spring Boot 3.3 + JPA/Hibernate + PostgreSQL 16
- **Frontend:** Next.js 15 (App Router) + TypeScript 5 (strict) + Tailwind CSS + shadcn/ui
- **Containers:** Docker + Docker Compose created by the team in Stages 3/4 as needed
- **IaC:** Terraform (Azure provider ~> 3.x)
- **CI/CD:** GitHub Actions
- **Tests:** JUnit 5 + Testcontainers (backend); Vitest + Testing Library (frontend)

## Cross-cutting implementation rules

Detailed Java, TypeScript, database, security, infrastructure, and testing rules live in [`.github/instructions/`](instructions/) and load automatically for matching paths.

- Use English class names and Brazilian Portuguese comments.
- Define REST API paths as `/api/v1/{resource}`.
- Validate input at every system boundary.
- Never hardcode secrets, API keys, or credentials.
- Never expose sensitive data (CPF, benefit amounts) in logs; mask it.
- Configure CORS explicitly; do not use the `*` wildcard in production.
- Use Managed Identity for service-to-service authentication in Azure.
- Write tests during implementation, not afterward.

## Specification-driven development (Spec-Kit)

- Every requirement uses **EARS notation** (Easy Approach to Requirements Syntax).
- Every requirement has a unique **REQ-ID** in the `REQ-NNN` format.
- **Every requirement includes a `source_legacy:` line** pointing to legacy files or containing `[GREENFIELD] + justification.`
  Use `01-archaeology/legacy-sifap/natural-programs/*.{NSP,NSN,NSS,NSA,NSL,NSC,NSM,jcl}` or `01-archaeology/legacy-sifap/adabas-ddms/*.{NSD,ddm,txt}` for legacy-backed requirements.
  The `legacy-traceability` CI job rejects PRs that violate this rule. See [`01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`](../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md).
- Tests trace to REQ-IDs through inline comments.
- Branch strategy: one prefix per persona/stage, always branched from `develop` (never from `spec/*`) and merged back through `develop` -> `main`; there is no `stage` branch.
  - `spec/<NNN>-<feature>` - Requirements Engineer + Software Architect, Stage 2
  - `impl/<NNN>-<feature>` - Developer + DBA + QA Engineer, Stage 3
  - `infra/<component>` - DevOps Engineer, Stage 4
  - `docs/<topic>` - Technical Writer
  - `agent/<issue-NN>` - Copilot Agent
  - Do not turn `impl/`, or any other prefix, into `spec/`.
  - Full persona table: [`00-GIT-WORKFLOW.md`](../00-GIT-WORKFLOW.md)
- Before writing EARS requirements in Stage 2, the pair MUST have read its assigned Natural programs (HARD GATE; see the checklist above).

## Strict rules - do not do this

- Do not assume an existing application prototype, inherited containerization, or immersion infrastructure. `backend/`, `frontend/`, and `infra/` do not exist yet; the team creates only what the selected scope needs in Stages 3 and 4. The shared Natural/Adabas viewer is external and read-only; never provision or administer it from this repository.
- Do not write an EARS requirement without `source_legacy:`; CI will reject the PR.
- Do not add dependencies without an ADR justification.
- Do not write tests afterward; write them during implementation.
- Do not expose secrets in commit messages, logs, or PR descriptions.
- Do not merge into `main` without at least one peer review.
- Do not skip guided handoff discussions between stages (see [`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md)).
- Do not create root-level `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`. This file is the single source of truth for repository-wide agent instructions; every Copilot surface that reads `AGENTS.md` also reads this file, which takes precedence. A second file only increases drift risk. See [`docs/adr/0001-agent-instructions-single-source-of-truth.md`](../docs/adr/0001-agent-instructions-single-source-of-truth.md).
- Do not add or edit a Copilot primitive (agent, prompt, instruction, skill, or hook) that violates [`PRIMITIVE-STANDARD.md`](PRIMITIVE-STANDARD.md); the `copilot-primitives` CI job enforces its structure.

## References

- Schedule + pairs: [`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md)
- Git workflow: [`00-GIT-WORKFLOW.md`](../00-GIT-WORKFLOW.md)
- Three Copilot modes (Ask, Plan, Agent): [`09-cheat-sheets/copilot-3-modes.md`](../09-cheat-sheets/copilot-3-modes.md)
- Persona kits (read 2 per person; active artifacts are already consolidated in `.github/`): [`05-personas/`](../05-personas/)
- Stage agents: [`06-stage-agents/`](../06-stage-agents/)
- SIFAP legacy system: [`01-archaeology/legacy-sifap/`](../01-archaeology/legacy-sifap/)
- Legacy system viewer: [`docs/legacy-system-access.md`](../docs/legacy-system-access.md)
- SDD with Spec-Kit: <https://github.com/github/spec-kit>
