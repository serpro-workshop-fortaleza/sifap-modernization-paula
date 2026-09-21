# Work items, area paths, and iterations

## Contents

- [Work items (Boards)](#work-items-boards)
- [Area paths](#area-paths)
- [Iterations](#iterations)

---

## Work items (Boards)

### Query work items

```bash
# WIQL query
az boards query \
  --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] = 'Active'"

# Query with output format
az boards query --wiql "SELECT * FROM WorkItems" --output table
```

### Show work item

```bash
az boards work-item show --id {work-item-id}
az boards work-item show --id {work-item-id} --open
```

### Create work item

```bash
# Basic work item
az boards work-item create \
  --title "Fix sign-in failure" \
  --type Bug \
  --assigned-to user@example.com \
  --description "Users cannot sign in with SSO"

# With area and iteration
az boards work-item create \
  --title "New feature" \
  --type "User Story" \
  --area "Project\\Area1" \
  --iteration "Project\\Sprint 1"

# With custom fields
az boards work-item create \
  --title "Task" \
  --type Task \
  --fields "Priority=1" "Severity=2"

# With discussion comment
az boards work-item create \
  --title "Issue" \
  --type Bug \
  --discussion "Initial investigation completed"

# For a long --discussion body on Windows, see references/long-comments-on-windows.md.
# Summary: use azps.ps1 in PowerShell or fall back to 'az devops invoke'
# with --in-file when no native --file-path option exists.

# Open in the browser after creation
az boards work-item create --title "Bug" --type Bug --open
```

### Update work item

```bash
# Update state, title, and assignee
az boards work-item update \
  --id {work-item-id} \
  --state "Active" \
  --title "Updated title" \
  --assigned-to user@example.com

# Move to another area
az boards work-item update \
  --id {work-item-id} \
  --area "{ProjectName}\\{Team}\\{Area}"

# Change iteration
az boards work-item update \
  --id {work-item-id} \
  --iteration "{ProjectName}\\Sprint 5"

# Add comment/discussion
az boards work-item update \
  --id {work-item-id} \
  --discussion "Work in progress"

# Long comment on Windows: read the body into a PowerShell variable and call
# azps.ps1 instead of az.cmd or fall back to 'az devops invoke' with --in-file.
# Full guidance in references/long-comments-on-windows.md.
#
# PowerShell example:
#   $body = Get-Content -Raw .\comment.md
#   azps.ps1 boards work-item update --id 1234 --discussion $body

# Update with custom fields
az boards work-item update \
  --id {work-item-id} \
  --fields "Priority=1" "StoryPoints=5"
```

### Delete work item

```bash
# Soft delete (can be restored)
az boards work-item delete --id {work-item-id} --yes

# Permanent deletion
az boards work-item delete --id {work-item-id} --destroy --yes
```

### Work item relations

```bash
# List relations
az boards work-item relation list --id {work-item-id}

# List supported relation types
az boards work-item relation list-type

# Add relation
az boards work-item relation add --id {work-item-id} --relation-type parent --target-id {parent-id}

# Remove relation
az boards work-item relation remove --id {work-item-id} --relation-id {relation-id}
```

## Area paths

### List project areas

```bash
az boards area project list --project {project}
az boards area project show --path "Project\\Area1" --project {project}
```

### Create area

```bash
az boards area project create --path "Project\\NewArea" --project {project}
```

### Update area

```bash
az boards area project update \
  --path "Project\\OldArea" \
  --new-path "Project\\UpdatedArea" \
  --project {project}
```

### Delete area

```bash
az boards area project delete --path "Project\\AreaToDelete" --project {project} --yes
```

### Team area management

```bash
# List team areas
az boards area team list --team {team-name} --project {project}

# Add area to team
az boards area team add \
  --team {team-name} \
  --path "Project\\NewArea" \
  --project {project}

# Remove area from team
az boards area team remove \
  --team {team-name} \
  --path "Project\\AreaToRemove" \
  --project {project}

# Update team area
az boards area team update \
  --team {team-name} \
  --path "Project\\Area" \
  --project {project} \
  --include-sub-areas true
```

## Iterations

### List project iterations

```bash
az boards iteration project list --project {project}
az boards iteration project show --path "Project\\Sprint 1" --project {project}
```

### Create iteration

```bash
az boards iteration project create --path "Project\\Sprint 1" --project {project}
```

### Update iteration

```bash
az boards iteration project update \
  --path "Project\\OldSprint" \
  --new-path "Project\\NewSprint" \
  --project {project}
```

### Delete iteration

```bash
az boards iteration project delete --path "Project\\OldSprint" --project {project} --yes
```

### Team iterations

```bash
# List team iterations
az boards iteration team list --team {team-name} --project {project}

# Add iteration to team
az boards iteration team add \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}

# Remove iteration from team
az boards iteration team remove \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}

# List iteration work items
az boards iteration team list-work-items \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}
```

### Default and backlog iterations

```bash
# Set the team's default iteration
az boards iteration team set-default-iteration \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}

# Show default iteration
az boards iteration team show-default-iteration \
  --team {team-name} \
  --project {project}

# Set the team's backlog iteration
az boards iteration team set-backlog-iteration \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}

# Show backlog iteration
az boards iteration team show-backlog-iteration \
  --team {team-name} \
  --project {project}

# Show current iteration
az boards iteration team show --team {team-name} --project {project} --timeframe current
```
