---
name: "pipeline-hardening"
description: "Use when hardening a CI/CD pipeline, migrating to OIDC, signing artifacts, or meeting SLSA requirements. Triggers include \"SLSA\", \"supply chain\", \"OIDC\", \"sigstore\", \"cosign\", \"CI/CD pipeline security\", and \"GHA hardening\"."
---
# CI/CD pipeline hardening

## When to Invoke

- "Harden our GitHub Actions / Azure DevOps / GitLab CI/CD pipeline."
- "Migrate from long-lived secrets to OIDC."
- "Achieve SLSA Level 2/3."
- "Sign our container images."

## Threat model (shortlist)

1. **Secrets stolen** from CI/CD pipeline logs or a compromised runner.
2. **Malicious dependency** published upstream or through typosquatting.
3. **Compromised third-party GitHub Action or shared step**.
4. **Tampered artifact** between build and deployment.
5. **Privilege escalation** caused by overly broad CI/CD pipeline permissions.

## Controls (ordered by return on investment, ROI)

### Level 1: do first

- [ ] **OIDC for cloud access**: do not store long-lived cloud credentials as secrets. Use federated identity with short-lived tokens.
- [ ] **Pin third-party actions by SHA**, not tag (`actions/checkout@<sha>` with a comment showing the version).
- [ ] Include a **`permissions:` block** in every workflow, with `contents: read` as the default and elevation only when needed.
- [ ] **Branch protection**: required reviews and status checks, no force pushes, and signed commits on `main`.
- [ ] Enable **secret scanning and push protection** across the organization.
- [ ] Use **Dependabot / Renovate** for dependencies and actions.

### Level 2: supply chain integrity

- [ ] **Software bill of materials (SBOM)** generated for every build (Syft / CycloneDX).
- [ ] **Artifact signing** with Cosign (preferably keyless through OIDC).
- [ ] **Provenance** (SLSA v1.0 attestation) published with the artifact.
- [ ] **Signature verification during deployment**: the deployment job rejects unsigned artifacts.
- [ ] **Vulnerability scanning** (Trivy / Grype) on the image; fails on Critical/High findings unless exceptions are justified.

### Level 3: mature

- [ ] **Hermetic, reproducible builds** where feasible.
- [ ] **Two-person review** for release workflows.
- [ ] **Runner hardening**: ephemeral, with restricted network egress and no shared mutable state.

## Anti-patterns

- Storing `AWS_ACCESS_KEY_ID` / `AZURE_CLIENT_SECRET` as repository secrets when OIDC is available.
- `permissions: write-all`.
- Floating `@main` or `@v3` tags on third-party actions.
- Deploying an artifact built in another CI/CD pipeline without verifying its signature.
- Printing secrets in logs through unquoted shell expansion.

## Output Template

```markdown
## CI/CD pipeline hardening report - <workflow or repository>

| Control | Status | Evidence / gap |
|---|---|---|
| OIDC for cloud authentication | done / missing | <URL or note> |
| SHA-pinned actions | done / missing | <count of floating tags> |
| Least-privilege permissions | done / missing | <workflows without the block> |
| SBOM + artifact signing | done / missing | <tool> |
| Provenance (SLSA) | Level 0/1/2/3 | <attestation URL> |

**Target SLSA level**: <N>
**Blocking gaps**: <count>
```

## Quality Gate

- [ ] No long-lived cloud secrets remain; cloud authentication uses OIDC federation.
- [ ] Every third-party action is pinned by commit SHA, not a floating tag.
- [ ] Every workflow declares a least-privilege `permissions:` block (`contents: read` by default).
- [ ] Release artifacts are signed, and signatures are verified during deployment.
- [ ] Secret scanning, push protection, and dependency updates are enabled.

## References

- [SLSA v1.0](https://slsa.dev/spec/v1.0/)
- [GitHub - Security hardening for GHA](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Sigstore / Cosign](https://docs.sigstore.dev/)
- [OpenSSF Scorecard](https://scorecard.dev/)
