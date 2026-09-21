---
description: "Use when creating or reviewing GitHub Actions, CI/CD workflows, YAML pipeline gates, build checks, and deployment automation."
applyTo: ".github/workflows/**,.github/actions/**,**/action.yml,**/action.yaml"
---

# CI/CD conventions - GitHub Actions gates

This file activates when you edit workflows in `.github/workflows/`, composite actions in `.github/actions/`, or any `action.yml`/`action.yaml`. It teaches pipeline structure, action pinning, permission scoping, and reliable gates. The two active workflows, [`ci.yml`](../workflows/ci.yml) and [`spec-quality.yml`](../workflows/spec-quality.yml), are the reference; read them before changing a gate.

## Active gates

| Workflow · Job | What it enforces | Blocking? |
|---|---|---|
| `ci.yml` · `detect-changes` | `dorny/paths-filter` sets `backend`/`frontend`/`infra` outputs so downstream jobs run only for relevant changes | n/a |
| `ci.yml` · `natural-format` | Fails when Natural code uses comma decimal format declarations, such as `(P9,2)`, instead of Natural CE's dot format `(P9.2)` | Yes |
| `ci.yml` · `backend` | JDK 21 (temurin) + `./mvnw -B verify`; uploads the Jacoco report | Yes |
| `ci.yml` · `frontend` | pnpm 9 + Node 20; `pnpm lint`, `pnpm typecheck`, `pnpm test --run --coverage` | Yes |
| `ci.yml` · `infra` | `terraform fmt -check -recursive`, then `init -backend=false` + `validate` per module | Yes |
| `spec-quality.yml` · `markdown-lint` | `markdownlint-cli2` on `**/*.md` | Yes |
| `spec-quality.yml` · `spec-traceability` | Reports REQ-IDs in `specs/` not yet referenced by a test (emits `::warning::`) | No |
| `spec-quality.yml` · `legacy-traceability` | Every REQ-ID in `specs/` must have a valid `source_legacy:` line | Yes |
| `pages.yml` · `build` | Resolves the three language snapshots, runs portal unit and browser tests, and rejects incomplete files, links, anchors, or original downloads | Yes |
| `pages.yml` · `deploy` | Rechecks Pages visibility; a private repository cannot publish with public or unknown access | Yes |

> [!IMPORTANT]
> `legacy-traceability` fails the build; `spec-traceability` only warns. See [`copilot-instructions.md`](../copilot-instructions.md) for the `source_legacy:` rule and [`sdd-artifacts.instructions.md`](sdd-artifacts.instructions.md) for SDD artifact conventions.

## Pin every action by commit SHA

Reference actions by the full 40-character commit SHA, with the readable tag in a trailing comment. Tags are mutable; SHAs are not.

```yaml
# Correct - immutable reference
- uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
# Wrong - a tag can be moved to malicious code
- uses: actions/checkout@v6
```

## Least-privilege permissions

Declare `permissions` at the top of every workflow with the narrowest scope and expand per job only when needed.

```yaml
permissions:
  contents: read # workflow-wide default

jobs:
  detect-changes:
    permissions:
      contents: read
      pull-requests: read # only this job needs it
```

## Path-filtered conditional jobs

Put heavy jobs behind `detect-changes` so a documentation-only PR runs neither Maven nor Terraform.

```yaml
backend:
  needs: detect-changes
  if: needs.detect-changes.outputs.backend == 'true'
```

## Concurrency and timeouts

Every workflow cancels superseded runs, and every job sets `timeout-minutes` to prevent a stuck step from consuming the runner.

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## OIDC deployment (future planning)

No deployment job exists yet. When adding it, authenticate to Azure with OIDC federation, never a stored client secret, and request `id-token: write` only in that job.

```yaml
permissions:
  id-token: write # requests the short-lived OIDC token
  contents: read
steps:
  - uses: azure/login@<full-sha> # pin it
    with:
      client-id: ${{ vars.AZURE_CLIENT_ID }}
      tenant-id: ${{ vars.AZURE_TENANT_ID }}
      subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

Deployed workloads use Managed Identity for service-to-service authentication (see [`infrastructure.instructions.md`](infrastructure.instructions.md)); hardening checklists live in the [`pipeline-hardening`](../skills/pipeline-hardening/SKILL.md) skill.

## Conventions

| Rule | Rationale |
|---|---|
| Pin actions by full commit SHA | Prevents supply-chain tag hijacking |
| `permissions:` block in every workflow, with `contents: read` by default | Least privilege by construction |
| `concurrency` + `cancel-in-progress` | No wasted or concurrent runs on the same ref |
| `timeout-minutes` on every job | A stuck step fails fast |
| OIDC federation, never a stored cloud secret | No long-lived credentials in the repository |

## Do / Don't

| Do | Don't |
|---|---|
| Reference `@<sha> # vN` | Reference `@v4`, `@main`, or a branch |
| Grant `id-token: write` per deployment job | Grant `write-all` at workflow level |
| Read the workflow before editing a gate | Guess what a gate checks |
| Let `detect-changes` skip irrelevant jobs | Run every job on every PR |

## PR Checklist

- [ ] Every `uses:` is pinned to a full commit SHA with a version comment
- [ ] The workflow declares a top-level least-privilege `permissions:` block
- [ ] Each job sets `timeout-minutes`, and the workflow sets `concurrency`
- [ ] New gates are accurately described in the relevant instruction file
- [ ] Every cloud step uses OIDC, not a stored secret, and requests `id-token: write` narrowly
- [ ] `markdownlint-cli2` and existing CI jobs pass locally when reproducible
