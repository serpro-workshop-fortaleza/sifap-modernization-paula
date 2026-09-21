---
name: "iac-review"
description: "Use when reviewing Terraform, Bicep, or CloudFormation, checking drift, or hardening infrastructure code. Triggers include \"review terraform\", \"review bicep\", \"IaC review\", \"drift detection\", and \"state file\"."
---
# IaC review

## When to Invoke

- "Review this Terraform module."
- "Why does our plan show drift?"
- "Is this Bicep production-ready?"

## Review checklist

### Structure

- [ ] Modules are **composable** and have a single responsibility (one module = a logical grouping, not a resource).
- [ ] **No hardcoded values**: parameterize everything with appropriate defaults.
- [ ] Documented inputs (`description`, `type`, and `validation` rules) and documented outputs.
- [ ] A **README** at the module root with a usage example.

### State and remote backends

- [ ] **Remote state** with locking (S3+DynamoDB, Azure Storage with blob leases, GCS).
- [ ] State is **never committed** to Git; `.gitignore` covers `*.tfstate*`.
- [ ] State is separated by environment, with no implicit cross-environment coupling.
- [ ] IAM controls state access, not shared credentials.

### Security

- [ ] No secrets in code or variable defaults. Use Key Vault / Secrets Manager / SOPS.
- [ ] IAM follows least privilege, with no `*:*` or `Resource: "*"` unless justified.
- [ ] Encryption at rest and in transit is enabled for all data stores.
- [ ] Public access is explicitly denied unless intentional. Document intentional access in the module README.
- [ ] `tfsec` / `checkov` / `PSRule` report no findings, or exceptions are documented.

### Change safety

- [ ] `terraform plan` is included in pull requests (PRs) as a comment (Atlantis / tfcmt / GitHub Actions).
- [ ] `prevent_destroy` is set on stateful resources (databases, KV, and storage accounts).
- [ ] Provider (`provider`) versions are **pinned** (`~>` with explicit major and minor versions).
- [ ] Module versions are pinned.
- [ ] Destructive changes require a second approval.

### Drift

- [ ] Scheduled drift detection (daily `terraform plan -detailed-exitcode` or Driftctl).
- [ ] Drift automatically creates a ticket and never stays silent.
- [ ] No manual console changes without subsequent codification.

## Common findings

- **`count` used on lists that can be reordered**: use `for_each` with stable keys.
- **`depends_on` everywhere**: usually indicates missing implicit dependencies; remove it unless truly needed.
- **Data sources used for values available at plan time**: unnecessary API calls and flaky continuous integration (CI).
- **Environment differences through string interpolation with `terraform.workspace`**: a fragile approach; use tfvars or separate stacks.

## Output Template

```markdown
## IaC review: <module or stack>

| Area | Finding | Severity | Recommendation |
|---|---|---|---|
| State | Local state, no locking | High | Move to a remote backend with locking |
| Security | Storage account allows public access | High | Set public_network_access_enabled = false |
| Change safety | Provider version not pinned | Medium | Pin with ~> major.minor |

**Blocking findings**: <count>
**Verdict**: approve / request changes
```

In the template, `major.minor` identifies the major and minor versions.

## Quality Gate

- [ ] `terraform fmt` and `terraform validate` pass, and the plan is attached to the pull request (PR).
- [ ] No secrets appear in code, variables, or state; secrets use Key Vault or Secrets Manager.
- [ ] Provider and module versions are pinned; stateful resources set `prevent_destroy`.
- [ ] `tfsec` or `checkov` reports no findings, or all exceptions are documented.
- [ ] All resources have `project`, `environment`, and `owner` tags (`tags`).

## References

- [Terraform style guide](https://developer.hashicorp.com/terraform/language/style)
- [Azure Verified Modules](https://azure.github.io/Azure-Verified-Modules/)
- [tfsec](https://aquasecurity.github.io/tfsec/), [checkov](https://www.checkov.io/)
