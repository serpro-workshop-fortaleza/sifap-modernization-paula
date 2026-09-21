# Posting long comments and bodies on Windows

On Windows, the `az` command resolves to `az.cmd`, a batch wrapper invoked by `cmd.exe`. The full command line has a limit of about 8,191 characters. Therefore, a long `--discussion`, `--description`, or `--content` value can be silently truncated or fail. Detect the shell before composing a long argument and choose the appropriate approach. Ignoring this is the most common reason an agent spends 3 to 5 interactions falling back to direct token retrieval and REST calls.

## Detect the shell first

| Environment | Signal | Action |
|---|---|---|
| PowerShell on Windows | `$IsWindows -eq $true` and `$PSVersionTable.PSVersion` defined | Use `azps.ps1` (see below) |
| PowerShell on macOS/Linux | `$IsWindows -eq $false` | Regular `az` works, without the cmd.exe wrapper |
| bash/zsh/sh | `$BASH_VERSION` or `$ZSH_VERSION` defined, or `uname` works | Regular `az` works, without the cmd.exe wrapper |
| Windows `cmd.exe` | `%ComSpec%` ends in `cmd.exe`, no `$PSVersionTable` | Use `azps.ps1` if PowerShell is installed. Otherwise, see the `az devops invoke` fallback below |

## Option 1: `azps.ps1` (PowerShell on Windows)

`azps.ps1` ships with the Azure CLI installer and invokes the Python entry point directly. There is no `cmd.exe` length limit.

```powershell
# Read the long body into a variable and pass it directly. No quoting issues.
$body = Get-Content -Raw .\comment.md
azps.ps1 boards work-item update --id 1234 --discussion $body
```

## Option 2: dedicated `--file-path` option when offered by the Azure CLI

Some commands have a native file option. Prefer it over any inline body:

- `az devops wiki page create` and `az devops wiki page update` accept `--file-path` (with optional `--encoding`).
- Use it in any shell, including on Windows.

```bash
az devops wiki page create --path 'My page' --wiki myproject --file-path ./page.md --encoding utf-8
```

## Option 3: `az devops invoke` fallback

When there is no `--file-path` (work item `--discussion`, pull request `--description`) and you are not in PowerShell, post the body through the underlying REST API. `az devops invoke` runs in the Python entry point, so it is also not subject to the `cmd.exe` limit, and reads the request body from a file with `--in-file`:

```bash
# Post a long discussion comment on work item 1234.
# REST: POST /{project}/_apis/wit/workItems/{id}/comments?api-version=7.0-preview.3
az devops invoke \
  --area wit --resource comments \
  --route-parameters project={project} workItemId=1234 \
  --api-version 7.0-preview.3 \
  --http-method POST \
  --in-file ./comment.json
```

In this case, `comment.json` is `{ "text": "<long markdown body>" }`. This is the universal workaround when neither `azps.ps1` nor `--file-path` is available. `az devops invoke` itself supports `--in-file` natively.

## Do not rely on `@<file>` for plain text arguments

The Azure CLI's `@<file>` convention is documented for JSON parameters (see the [official quoting guide](https://learn.microsoft.com/en-us/cli/azure/use-azure-cli-successfully-quoting)). It is not guaranteed to expand plain text arguments such as `--discussion` or `--description`. Therefore, do not use it as a substitute for the three options above.
