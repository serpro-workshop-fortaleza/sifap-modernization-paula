---
name: "azure-devops-cli"
description: "Use when managing Azure DevOps resources through the CLI: projects, repositories, pipelines, builds, pull requests, work items, artifacts, and service endpoints. Applies only when a team integrates with an existing Azure DevOps organization. Triggers include \"az devops\", \"az pipelines\", \"az boards\", \"az repos\", and \"Azure DevOps automation\"."
---
# Azure DevOps CLI

Manage Azure DevOps resources with the Azure CLI and the `azure-devops` extension.

> [!NOTE]
> This kit's source of truth for work, code, and continuous integration (CI) is **GitHub** (GitHub Issues, GitHub Pull Requests, GitHub Actions, and GitHub Projects). Use this skill only when a team also needs to operate an existing Azure DevOps organization. Do not migrate the kit's workflow to Azure DevOps.

## When to Invoke

- "Create a pull request in our Azure DevOps repository through the CLI."
- "Queue a pipeline run and track its status without opening the portal."
- "Bulk-update work items with a script."
- "List the branch policies for our Azure DevOps repository."

## Prerequisites

Install the Azure CLI and the Azure DevOps extension:

```bash
brew install azure-cli                                     # macOS
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash     # Linux
az extension add --name azure-devops
```

## Authentication

Authenticate with a Personal Access Token (PAT) and set defaults to avoid repeating `--org`/`--project`:

```bash
export AZURE_DEVOPS_EXT_PAT="<your-pat>"
az devops login --organization https://dev.azure.com/{org}
az devops configure --defaults organization=https://dev.azure.com/{org} project={project}
az devops configure --list
```

> [!WARNING]
> Never hardcode a PAT in a script, repository commit, or command that will be logged. Supply it through the `AZURE_DEVOPS_EXT_PAT` environment variable (or a secret vault) and restrict it to the minimum required permissions.

> [!NOTE]
> Replace the legacy URL `https://{org}.visualstudio.com` with `https://dev.azure.com/{org}`.

## CLI Structure

```text
az devops          Core DevOps commands
├── admin          Administration (banner)
├── extension      Extension management
├── project        Team projects
├── security       Security operations (group, permission)
├── service-endpoint   Service connections
├── team           Teams
├── user           Users
├── wiki           Wikis
├── configure      Set defaults
├── invoke         Invoke the REST API
├── login / logout Authenticate / clear credentials

az pipelines       Azure Pipelines
├── agent / pool / queue   Agents, pools, and queues
├── build          Builds
├── folder         Pipeline folders
├── release        Releases
├── runs           Pipeline runs
└── variable / variable-group   Variables and groups

az boards          Azure Boards
├── area           Area paths
├── iteration      Iterations
└── work-item      Work items

az repos           Azure Repos
├── import         Git imports
├── policy         Branch policies
├── pr             Pull requests
└── ref            Git references

az artifacts       Azure Artifacts
└── universal      Universal packages
```

## Reference Files

Read the reference file relevant to the task. Each file contains complete command syntax and examples for its domain.

| File | When to read | Covers |
|---|---|---|
| [references/repos-and-prs.md](references/repos-and-prs.md) | Repositories, branches, pull requests, and branch policies | Repositories, import, pull requests (create/list/vote/reviewers/policies), Git references, and branch policies |
| [references/pipelines-and-builds.md](references/pipelines-and-builds.md) | Pipelines, builds, releases, and artifacts | Pipeline create, read, update, and delete (CRUD), runs, builds, releases, artifact download and upload |
| [references/boards-and-iterations.md](references/boards-and-iterations.md) | Work items, sprints, and area paths | Work items (WIQL/create/update/relations), area paths, and team iterations |
| [references/variables-and-agents.md](references/variables-and-agents.md) | Pipeline variables and agent pools | Pipeline variables, variable groups, pipeline folders, and agent pools/queues |
| [references/org-and-security.md](references/org-and-security.md) | Projects, teams, users, permissions, and wikis | Projects, extensions, teams, users, security groups/permissions, service endpoints, wikis, and administration |
| [references/advanced-usage.md](references/advanced-usage.md) | Output formatting and JMESPath queries | Output formats, JMESPath queries, global arguments, common parameters, and Git aliases |
| [references/workflows-and-patterns.md](references/workflows-and-patterns.md) | Automation scripts, best practices, error handling | Common workflows, best practices, error handling, scripting patterns, real-world examples |
| [references/long-comments-on-windows.md](references/long-comments-on-windows.md) | Windows failures with long `--discussion`, `--description`, or `--content` values | The 8,191-character `cmd.exe` limit in `az.cmd`, shell detection, and three verified workarounds (`azps.ps1`, native `--file-path`, `az devops invoke --in-file`) |

## Output Template

Provide an executable command sequence and the returned identifiers:

```bash
az repos pr create \
  --repository sifap \
  --source-branch feature/import-report \
  --target-branch main \
  --title "Add import report" \
  --description "Implements REQ-042" \
  --output table
az pipelines run --name sifap-ci --branch feature/import-report --output table
```

Summarize the result:

```text
Pull request: !128 sifap feature/import-report -> main (active)
Pipeline: sifap-ci run #345 queued on feature/import-report
```

## Quality Gate

- [ ] `az devops configure --list` shows the intended default organization and project.
- [ ] The PAT is supplied through `AZURE_DEVOPS_EXT_PAT` or a secret vault, never hardcoded or logged.
- [ ] Commands explicitly specify `--output table`/`--output json` so results can be processed.
- [ ] Long `--description`/`--discussion` values on Windows use one of the documented workarounds.
- [ ] The action has been verified (pull request, run, or work item ID returned), rather than assumed successful without evidence.
