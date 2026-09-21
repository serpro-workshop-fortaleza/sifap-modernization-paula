---
name: "pipeline"
description: "Create a robust GitHub Actions CI/CD pipeline for SIFAP 2.0, with build, test, security, and environment-promotion gates."
argument-hint: "target=backend|frontend|infra component=<name>"
agent: "devops-engineer"
tools: ["read", "search", "edit"]
---
# /pipeline

## Objective

Create or refactor a **GitHub Actions** workflow for SIFAP 2.0 that builds, tests, scans, and promotes artifacts from `develop` to `main` (production) with explicit continuous integration and delivery (CI/CD) gates. The workflow follows the existing pattern in `.github/workflows/ci.yml`: actions pinned to full commit SHAs with a trailing `# vN` comment, a least-privilege `permissions:` block, a `concurrency` group, and `timeout-minutes` on every job. The artifact is delivered in `.github/workflows/`.

## When to Invoke

Use when a bounded context reaches Stages 3 or 4 and needs automated build, test, and deployment, or when an existing workflow needs hardening (OIDC, SHA pinning, or signing).

## Preconditions

- The target component exists (`backend/`, `frontend/`, or `infra/`) or is being created in this pull request
- GitHub environments (`dev`, `prod`) are configured with required reviewers
- Azure federated credentials (OIDC) and the container registry are available to the repository

## Inputs the Team Must Provide

- The pipeline target: Java backend service, Next.js frontend application, IaC module, or end-to-end orchestration
- The branching model (feature branches created from `develop`, with promotion from `develop` to `main`; see `00-GIT-WORKFLOW.md`)
- GitHub environments and their required reviewers
- The container registry, for example, Azure Container Registry, and any compliance needs (SBOM or signed images)

Ask the user for any missing item.

## What I Will Do

- Read the [`pipeline-hardening`](../skills/pipeline-hardening/SKILL.md) skill and apply its level 1 to 3 gates
- Choose triggers and organize jobs by stage (build, quality, security, packaging, and deployment)
- Authenticate to Azure with OIDC, without a long-lived service principal secret
- Pin every action by SHA with a `# vN` comment and set a least-privilege `permissions:` block, a `concurrency` group, and `timeout-minutes`, as in `.github/workflows/ci.yml`
- Emit deployment traceability (merge SHA and related `REQ-ID`s)

## What I Will NOT Do

- Invent action SHAs, secret names, or registry addresses. Unknown SHAs will be obtained from the action's published release, and secrets will be referenced by name, never inlined
- Write application code (`@builder`), create Terraform modules (`/iac-module`), or change requirements (`@requirements-engineer`)
- Store an Azure secret in GitHub when OIDC works or grant `permissions: write-all`
- Pin an action to a floating tag (`@v3`, `@main`) instead of a SHA
- Deploy to production without an approval gate or inline a secret in YAML

## Output Format

The main artifact is the workflow YAML. Example for a backend service:

```yaml
name: backend-ci
on:
  pull_request:
    paths: ["backend/**"]
  push:
    branches: [develop, main]
    paths: ["backend/**"]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    name: Build, test, and scan
    runs-on: ubuntu-latest
    timeout-minutes: 20
    defaults:
      run:
        shell: bash
        working-directory: backend
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: "21"
          cache: maven
      - name: Build and test
        run: ./mvnw -B verify
      - name: Scan filesystem (fail on critical/high severity)
        uses: aquasecurity/trivy-action@ed142fd0673e97e23eac54620cfb913e5ce36c25 # v0.36.0
        with:
          scan-type: fs
          severity: CRITICAL,HIGH
          exit-code: "1"

  deploy-prod:
    name: Deploy to production
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 20
    environment: prod # required reviewers enforce two approvals
    permissions:
      contents: read
      id-token: write # OIDC federated authentication; no Azure secret stored
    steps:
      - name: Log in to Azure (OIDC)
        uses: azure/login@7184910d9eb2b1c5e48f7073824a90609bb9b6d6 # v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - name: Install cosign and sign the image by digest
        uses: sigstore/cosign-installer@398d4b0eeef1380460a10c8013a76f728fb906ac # v3
```

Accompany the YAML with all required secrets and variables (by name and purpose), branch protection settings (required checks `build`, `quality`, and `security`), and a one-line promotion flow: pull request → `build+scan` → `develop` → `deploy-dev` → `main` → two approvals → `deploy-prod`.

## Definition of Done

- [ ] Authentication uses OIDC and no Azure secret is stored in GitHub
- [ ] Every action is pinned to a commit SHA with a `# vN` comment
- [ ] `build`, `quality`, and `security` are required pull request checks
- [ ] Top-level `permissions:` is `contents: read` and is elevated only when a job needs it
- [ ] A `concurrency` group prevents two simultaneous deployments to the same environment
- [ ] `timeout-minutes` is set on every job
- [ ] Production deployments require approvals and record the merge SHA and related `REQ-ID`s

## Prompt Body

You are `@devops-engineer`. The team needs a workflow that exactly matches the repository's existing CI conventions.

**Step 1: load the hardening gates.**
Read the [`pipeline-hardening`](../skills/pipeline-hardening/SKILL.md) skill and open `.github/workflows/ci.yml` to copy the repository pattern (SHA pinning with `# vN`, `permissions:`, `concurrency`, and `timeout-minutes`).

**Step 2: choose triggers.**
Use `pull_request` for build and tests, `push` on protected branches for deployment, and `workflow_dispatch` for manual rollback. Avoid `pull_request_target` unless forks truly need secrets.

**Step 3: organize jobs by stage.**
Use `build` (build and unit tests: `./mvnw -B verify` or `pnpm install --frozen-lockfile && pnpm build && pnpm test`), `quality` (static analysis, type checking, and coverage upload), `security` (Trivy, dependency scanning, and secret scanning of diffs), `package` (image build, push by digest, SBOM generation with syft, and signing with cosign), `deploy-dev` (automatic on `develop`), and `deploy-prod` (on `main`, with required approvals).

**Step 4: authenticate with OIDC.**
Use `azure/login` with federated credentials and scope `id-token: write` to the deployment job only. Never store a service principal secret.

**Step 5: pin, cache, and bound each job.**
Pin every action by SHA with a `# vN` comment. Cache Maven by the `pom.xml` hash and use the pnpm cache. Set `timeout-minutes` per job and a workflow-level `concurrency` group.

**Step 6: enforce gates and traceability.**
Make `build`, `quality`, and `security` required checks through branch protection. Tag the deployed image with the merge commit SHA and related `REQ-ID`s from the pull request description. Expose this information in the deployment description.

Top-level `permissions:` defaults to `contents: read` and is elevated only where needed. Use OIDC only, with no long-lived Azure secrets and no secrets inlined in YAML. All actions are pinned by SHA with a `# vN` comment, and production deployments are protected by an approval gate.

## Example Invocation

```text
/pipeline target=backend component=<service>
```
