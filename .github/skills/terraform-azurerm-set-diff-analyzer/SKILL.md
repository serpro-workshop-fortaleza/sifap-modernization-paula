---
name: "terraform-azurerm-set-diff-analyzer"
description: "Use when a Terraform plan for AzureRM resources shows many changes even though only one element was added or removed, to separate false-positive Set ordering diffs from real changes. Covers Application Gateway, Load Balancer, Firewall, Front Door, and NSG. Triggers include \"terraform plan noise\", \"Set type diff\", \"all elements changed\", \"spurious diff\", and \"filter false positives in CI\"."
---
# Terraform AzureRM set diff analyzer

Identify **false-positive diffs** in Terraform plans caused by Set-type attributes in the AzureRM provider and distinguish them from real changes. This kit's IaC uses Terraform (`azurerm ~> 3.x`), so this skill applies directly to the `infra/` tree created by the team in Stage 3.

## When to Invoke

- "`terraform plan` shows dozens of changes, but I only added one NSG rule."
- "My Application Gateway plan says all routing rules changed. Is that real?"
- "How do I prevent Set ordering noise from blocking plan review in CI?"
- "Which of these Load Balancer diffs will actually modify the resource?"

## Background

Terraform's Set type compares elements by position, not by a stable key. As a result, adding or removing an element can make all of them appear "changed". This general Terraform behavior is especially visible in AzureRM resources that rely heavily on Set-type attributes: Application Gateway, Load Balancer, Firewall, Front Door, and NSG. These false-positive diffs do not change the deployed resource, but obscure real changes and make plan review error-prone.

## Prerequisites

- Python 3.8+ (standard library only; no third-party packages).

If Python is unavailable, install it through the package manager (`brew install python3`, `apt install python3`) or [python.org](https://www.python.org/downloads/).

## Basic usage

```bash
terraform plan -out=plan.tfplan                 # 1. capture the plan
terraform show -json plan.tfplan > plan.json    # 2. export it as JSON
python scripts/analyze_plan.py plan.json        # 3. classify the diffs
```

The analyzer reads the JSON plan, inspects Set-type attributes in supported AzureRM resources, and reports which resources show only ordering changes (false positives) and which have real additions, removals, or modifications.

## Interpreting results

| Signal | Meaning | Action |
|---|---|---|
| Ordering-only change in a Set attribute | False positive, no real change | Safe to ignore; document in the pull request |
| Element added or removed | Real change | Review before running `terraform apply` |
| Attribute value modified | Real change | Review before running `terraform apply` |
| Resource absent from the support list | Not analyzed | Inspect manually |

Supported resources and their Set-type attributes are in [references/azurerm_set_attributes.md](references/azurerm_set_attributes.md). Full command-line interface (CLI) options, output formats, exit codes, and CI/CD examples are in [scripts/README.md](scripts/README.md).

## Troubleshooting

| Problem | Solution |
|---|---|
| `python: command not found` | Use `python3` or install Python 3.8+ |
| `ModuleNotFoundError` | The script uses only the standard library; confirm that Python 3.8+ is active |
| A resource was not classified | Confirm that it appears in `references/azurerm_set_attributes.md`; otherwise, review it manually |

## Output Template

Report the classification in a table and add a one-line verdict:

```markdown
## Set diff analysis — plan.json

| Resource | Set attribute | Verdict | Real changes |
|---|---|---|---|
| azurerm_application_gateway.main | request_routing_rule | False positive (ordering only) | 0 |
| azurerm_network_security_group.web | security_rule | Real change | +1 / -0 |

Total: 2 resources analyzed, 1 false positive and 1 with real changes.
Verdict: review the NSG rule change before applying the plan; the gateway diff can safely be ignored.
```

## Quality Gate

- [ ] A JSON plan was produced with `terraform show -json` before analysis.
- [ ] `scripts/analyze_plan.py` was run on the JSON plan with Python 3.8+.
- [ ] Every flagged resource is classified as a false positive (ordering only) or a real change.
- [ ] Real changes are reviewed before `terraform apply`; false positives are documented as safe to ignore.
- [ ] All resources outside the support list were reviewed manually.
