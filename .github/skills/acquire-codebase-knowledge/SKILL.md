---
name: "acquire-codebase-knowledge"
description: "Use this skill when someone explicitly asks to map or document an existing codebase, or to guide onboarding to it. Trigger for requests such as \"map this codebase\", \"document this architecture\", \"help me get started in this repository\", or \"create codebase documentation\". Do not trigger for routine feature implementation, bug fixes, or targeted edits unless repository-level discovery is requested."
---
# Acquire codebase knowledge

Produces seven completed documents in `docs/codebase/` with everything needed to work effectively on the project. Document only what can be verified in files or terminal output. Never infer or assume.

## When to Invoke

- "Map this codebase and document its architecture."
- "Help me get started in this repository. Where do I begin?"
- "Create codebase documentation so a new engineer can be productive in the first week."
- "Document this project's stack, structure, and integrations."

> [!NOTE]
> In this immersion, the modern application does not exist until Stage 3. Therefore, target this skill at an existing project or the kit itself. Treat everything in `01-archaeology/legacy-sifap/` as read-only evidence and never assert the contents of a legacy program or field. Record how to discover this information and follow the reading criterion in [`01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`](../../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md) and [`01-archaeology/legacy-sifap/HOW-TO-READ-NATURAL.md`](../../../01-archaeology/legacy-sifap/HOW-TO-READ-NATURAL.md).

## Workflow

Copy and track this checklist:

```text
- [ ] Phase 1: run the scan and read intent documents
- [ ] Phase 2: investigate each documentation area
- [ ] Phase 3: complete the seven documents in docs/codebase/
- [ ] Phase 4: validate the documents, present findings, and resolve all [ASK USER] items
```

## Focus area mode

If the person provides a focus area (for example, "architecture only" or "testing and concerns"):

1. Always run all of Phase 1.
2. Fully complete the focus area documents first.
3. In out-of-focus documents not yet analyzed, retain required sections and mark unknowns as `[TODO]`.
4. Before the final output, still run the Phase 4 validation loop on all seven documents.

### Phase 1: scan and read intent

1. Run the scan script from the target project root:

   ```bash
   python3 "$SKILL_ROOT/scripts/scan.py" --output docs/codebase/.codebase-scan.txt
   ```

   Where `$SKILL_ROOT` is the absolute path to the skill folder. Works on Windows, macOS, and Linux.

   **Quick start:** if you have the path inline:

   ```bash
   python3 /absolute/path/to/skills/acquire-codebase-knowledge/scripts/scan.py --output docs/codebase/.codebase-scan.txt
   ```

2. Find and read `PRD`, `TRD`, `README`, `ROADMAP`, `SPEC`, and `DESIGN` files.
3. Summarize the project's stated intent before reading any source code.

### Phase 2: investigate

Use the scan output to answer the questions in each of the seven templates. Load [`references/inquiry-checkpoints.md`](references/inquiry-checkpoints.md) for the full question list for each template.

If the stack is ambiguous (multiple manifest files, unfamiliar file types, or no `package.json`), load [`references/stack-detection.md`](references/stack-detection.md).

### Phase 3: fill in templates

Copy each template from `assets/templates/` to `docs/codebase/`. Fill them in this order:

1. [STACK.md](assets/templates/STACK.md): language, runtime, frameworks, and all dependencies
2. [STRUCTURE.md](assets/templates/STRUCTURE.md): directory structure, entry points, and key files
3. [ARCHITECTURE.md](assets/templates/ARCHITECTURE.md): layers, patterns, and data flow
4. [CONVENTIONS.md](assets/templates/CONVENTIONS.md): naming, formatting, error handling, and imports
5. [INTEGRATIONS.md](assets/templates/INTEGRATIONS.md): external APIs, databases, authentication, and monitoring
6. [TESTING.md](assets/templates/TESTING.md): frameworks, file organization, and mocking strategy
7. [CONCERNS.md](assets/templates/CONCERNS.md): technical debt, bugs, security risks, and performance bottlenecks

Use `[TODO]` for anything that cannot be determined from code. Use `[ASK USER]` when the correct answer depends on team intent.

### Phase 4: validate, fix, and verify

Run this mandatory validation loop before finalizing:

1. Validate each document against `references/inquiry-checkpoints.md`.
2. For each nontrivial claim, confirm at least one evidence reference exists.
3. If any required section is missing or unsupported:

- Fix the document.
- Run validation again.

4. Repeat until all seven documents pass.

Then present a summary of the seven documents, list every `[ASK USER]` item as a numbered question, and highlight any intent-versus-reality mismatch identified in Phase 1.

Validation pass criteria:

- No unsupported claims.
- No empty required sections.
- Unknowns use `[TODO]` instead of assumptions.
- Gaps in team intent are explicitly marked `[ASK USER]`.

---

## Pitfalls

**Monorepos:** the root `package.json` may not contain source code. Check `workspaces` and the `packages/` or `apps/` directories. Each workspace may have its own dependencies and conventions. Map each subpackage separately.

**Outdated README:** the README often describes the intended architecture, not the current one. Compare it with the actual file structure before treating any README claim as fact.

**TypeScript path aliases:** the `paths` setting in `tsconfig.json` means imports like `@/foo` do not map directly to the file system. Map aliases to actual paths before documenting the structure.

**Generated or compiled output:** never document patterns from `dist/`, `build/`, `generated/`, `.next/`, `out/`, or `__pycache__/`. These directories contain artifacts. Document only source code conventions.

**`.env.example` reveals required configuration:** secrets are never versioned. Read `.env.example`, `.env.template`, or `.env.sample` to discover required environment variables.

**`devDependencies` is not the production stack:** only `dependencies` (or the equivalent, for example, `[tool.poetry.dependencies]`) runs in production. Document linters, formatters, and test frameworks separately as development tools.

**Test TODOs are not production debt:** TODOs in `test/`, `tests/`, `__tests__/`, or `spec/` are coverage gaps, not production technical debt. Separate them in `CONCERNS.md`.

**High-churn files = fragile areas:** files appearing most often in recent git history have a higher modification rate and likely hide complexity. Always record them in `CONCERNS.md`.

---

## Anti-patterns

| Anti-pattern | Instead |
|---------|--------------|
| "Uses Clean Architecture with Domain/Data layers." (when those directories do not exist) | State only what the directory structure actually shows. |
| "This is a Next.js project." (without checking `package.json`) | Check `dependencies` first. State what actually exists. |
| Inferring the database from a variable name like `dbUrl` | Check the manifest for `pg`, `mysql2`, `mongoose`, `prisma`, etc. |
| Documenting naming patterns from `dist/` or `build/` as conventions | Use only source files. |

---

## Expanded scan output sections

The `scan.py` script now produces the following sections in addition to the original output:

- **CODE METRICS**: total files, lines of code per language, and largest files (complexity signals)
- **CI/CD PIPELINES**: detected GitHub Actions, GitLab CI, Jenkins, CircleCI, etc.
- **CONTAINERS AND ORCHESTRATION**: Docker, Docker Compose, Kubernetes, and Vagrant configurations
- **SECURITY AND COMPLIANCE**: Snyk, Dependabot, SECURITY.md, SBOM, and security policies
- **PERFORMANCE AND TESTING**: benchmarking configurations, profiling markers, and load-testing tools

Use these sections during Phase 2 to guide investigation questions and identify tool-specific patterns.

---

## Bundled resources

| Resource | When to load |
|-------|-------------|
| [`scripts/scan.py`](scripts/scan.py) | Phase 1: run first, before reading any code (requires Python 3.8+) |
| [`references/inquiry-checkpoints.md`](references/inquiry-checkpoints.md) | Phase 2: load for each template's investigation questions |
| [`references/stack-detection.md`](references/stack-detection.md) | Phase 2: only if the stack is ambiguous |
| [`assets/templates/STACK.md`](assets/templates/STACK.md) | Phase 3, step 1 |
| [`assets/templates/STRUCTURE.md`](assets/templates/STRUCTURE.md) | Phase 3, step 2 |
| [`assets/templates/ARCHITECTURE.md`](assets/templates/ARCHITECTURE.md) | Phase 3, step 3 |
| [`assets/templates/CONVENTIONS.md`](assets/templates/CONVENTIONS.md) | Phase 3, step 4 |
| [`assets/templates/INTEGRATIONS.md`](assets/templates/INTEGRATIONS.md) | Phase 3, step 5 |
| [`assets/templates/TESTING.md`](assets/templates/TESTING.md) | Phase 3, step 6 |
| [`assets/templates/CONCERNS.md`](assets/templates/CONCERNS.md) | Phase 3, step 7 |

Template usage mode:

- Default mode: fill only the "Core sections (required)" of each template.
- Extended mode: add optional sections only when repository complexity justifies them.

## Output Template

Each of the seven files in `docs/codebase/` presents claims first, then supporting evidence. For example, `STACK.md`:

```markdown
## Technology stack

| Layer | Technology | Version | Evidence |
|---|---|---|---|
| Language | Java | 21 | backend/pom.xml |
| Framework | Spring Boot | 3.3.x | backend/pom.xml |
| Database | PostgreSQL | 16 | compose.yml, application.yml |

### Unknowns
- [TODO] No caching layer found in the manifests
- [ASK USER] Is Redis planned, or is in-memory caching intended?

### Evidence
- backend/pom.xml
- compose.yml
```

## Quality Gate

- [ ] Exactly seven files exist in `docs/codebase/`, each with its required sections.
- [ ] Every nontrivial claim is traceable to a file, configuration, or terminal output.
- [ ] Unknowns use `[TODO]`; intent-dependent decisions use `[ASK USER]`.
- [ ] Each document contains a concrete evidence list with real paths.
- [ ] Generated outputs (`dist/`, `build/`, `.next/`) are excluded from convention claims.
- [ ] The final response presents numbered `[ASK USER]` questions and every intent-versus-reality mismatch.
