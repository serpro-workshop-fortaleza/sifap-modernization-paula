---
description: "Use when creating, reviewing, or debugging a GitHub Copilot Agent Skill in .github/skills/: SKILL.md frontmatter, name-to-directory matching, description tuning for automatic loading, progressive disclosure, and bundled resources."
applyTo: ".github/skills/**/SKILL.md"
---

# Agent Skills - Authoring guide

This file activates when creating or editing a `SKILL.md` in `.github/skills/`. It teaches how to create a reliably loaded, clearly scoped skill: a two-key frontmatter schema, equality between `name` and directory, using `description` for automatic loading, progressive disclosure, and bundling scripts and references. It teaches how to structure and package a skill, but does not decide which skills the immersion needs or what domain procedure each should contain. That belongs to each skill's `SKILL.md` and [`.github/copilot-instructions.md`](../copilot-instructions.md).

## What a skill is

A skill is a self-contained folder with a `SKILL.md` and optional resources (scripts, references, templates, and assets) that teaches Copilot a specialized, repeatable capability.

| Primitive | Purpose | Loading |
|---|---|---|
| Instruction file (`*.instructions.md`) | Standing rules for files matching `applyTo` | Whenever a matching file is in context |
| Skill (`SKILL.md`) | On-demand workflow or capability | Only when the request matches `description` |

Skills are portable across VS Code, Copilot CLI, and Copilot coding agent. The body and resources remain outside context until needed.

## Where skills live

| Location | Scope |
|---|---|
| `.github/skills/<skill-name>/` | This repository; location of all immersion skills |
| `~/.copilot/skills/<skill-name>/` | Personal; all your repositories |

Each skill has its own directory and at least one `SKILL.md`. This file governs `.github/skills/**/SKILL.md`.

## Frontmatter - Only two keys

`SKILL.md` frontmatter accepts exactly `name` and `description`.

```yaml
---
name: "draw-io-diagram-generator"
description: "Use when creating, editing, or generating draw.io diagrams (.drawio, .drawio.svg, .drawio.png), flowcharts, sequence diagrams, or ER diagrams."
---
```

| Field | Required | Constraint |
|---|---|---|
| `name` | Yes | Lowercase letters, digits, and hyphens only; at most 64 characters; must exactly match the parent directory |
| `description` | Yes | States when to use the skill; emphasizes keywords; at most 1,024 characters |

> [!IMPORTANT]
> `name` must be identical to the folder name. `.github/skills/draw-io-diagram-generator/SKILL.md` must declare `name: "draw-io-diagram-generator"`. Any difference silently prevents the skill from loading.

> [!WARNING]
> Only `name` and `description` belong to the schema. `license`, `allowed-tools`, `compatibility`, and `metadata` are not recognized. Do not add them or assume that `LICENSE.txt` is connected through `license:`.

## The description controls automatic loading

Copilot reads only `name` and `description` during discovery. Include:

1. What the skill does.
2. When to use it, with concrete triggers, file types, or phrases.
3. Keywords the user is likely to type.

```yaml
# Good: specific
description: "Use when creating or generating draw.io files, flowcharts, sequence diagrams, or ER diagrams."

# Bad: vague
description: "Diagram helpers"
```

Quote the value. Use single quotes when triggers contain double quotes.

## Required body format

After the frontmatter, use a sentence-case `#` title and these sections, in order:

- `## When to Invoke`: three or four realistic requests in quotes.
- One or more procedure sections with tables, checklists, or steps.
- `## Output Template`: a fenced block with the exact artifact.
- `## Quality Gate`: a `- [ ]` checklist.

Sections such as `## Pitfalls`, `## Troubleshooting`, and `## References` are optional when they add information.

## Progressive disclosure

| Level | Loaded content | When |
|---|---|---|
| Discovery | Only `name` and `description` | Always |
| Instructions | Full `SKILL.md` body | When the request matches the description |
| Resources | Scripts, references, and templates | When the body links them and Copilot follows the link |

Keep the body focused. After about 200 lines, move details into `references/` and link them. Treat 500 lines as the hard limit.

## Bundling resources

| Folder | Content | Read into context? |
|---|---|---|
| `scripts/` | Executable automation (`.py`, `.sh`, `.ts`) | Only when executed |
| `references/` | Documentation Copilot uses to make decisions | Yes, when linked |
| `templates/` | Structures Copilot modifies | Yes, when linked |
| `assets/` | Static files emitted unchanged | No |

Use `templates/` when Copilot edits the file and `assets/` when it emits it unchanged. Reference files through relative paths, such as [the validator](../skills/draw-io-diagram-generator/scripts/validate-drawio.py).

Prefer scripts over regenerated inline code when logic repeats, requires determinism, or deserves tests. Scripts must provide `--help`, fail with clear messages, store no secrets, and use relative paths.

## Writing high-impact skills

- Teach only what Copilot is likely to get wrong: internal conventions, non-obvious patterns, version quirks, and domain workflows.
- Keep descriptions short and keyword-focused, since all compete for the same discovery window.
- Record pitfalls as "never do X because Y" when Copilot produces an incorrect result.
- Prefer flexible guidance for open-ended work and reserve numbered steps for mandatory sequences, such as builds, deployment, and setup.

## Conventions

| Rule | Rationale |
|---|---|
| Frontmatter contains only `name` and `description` | Other keys are ignored and hide false assumptions |
| `name` exactly matches the skill directory | A mismatch silently prevents loading |
| `description` states when to use the skill in at most 1,024 characters | It is the only text read during discovery |
| Body follows invocation, procedure, output template, and quality gate | Matches the immersion standard |
| Deep details move to `references/` after about 200 lines | Reduces context cost |
| Scripts provide `--help`, handle errors, and store no secrets | Bundled automation must be safe and self-explanatory |

## Do / Don't

| Do | Don't |
|---|---|
| Use the same name for the folder and `name` | Rename only one of them |
| Write a trigger-rich `description` | Use a vague description such as "helpers" |
| Keep only two keys in the frontmatter | Add keys outside the schema |
| Link bundled files through relative paths | Hardcode absolute or machine-specific paths |
| Split large skills into `references/` | Let a `SKILL.md` exceed about 500 lines |
| Include all four required sections | Omit invocation, output template, or quality gate |

## PR Checklist

- [ ] Frontmatter contains only `name` and `description`, both quoted
- [ ] `name` uses lowercase letters and hyphens, has at most 64 characters, and is identical to the parent directory
- [ ] `description` states what the skill does and when to use it, in at most 1,024 characters
- [ ] The body has invocation, at least one procedure, an output template, and a quality gate
- [ ] Content teaches non-obvious knowledge, not basic syntax
- [ ] Scripts, references, templates, and assets use relative paths
- [ ] The body remains focused, without emojis or inline lint pragmas
