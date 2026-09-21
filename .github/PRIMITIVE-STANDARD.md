# Copilot primitive standard

`.github/` contains this kit's Copilot **primitives**: agents, prompts, instructions, skills, and hooks. This file is the authoritative standard for their structure. It lets new primitives match the existing set without reverse engineering. The team's reference implementation is the archaeologist agent ([`archaeologist.agent.md`](agents/archaeologist.agent.md)); the patterns below derive from it and its peers.

> [!IMPORTANT]
> The documentation style guide ([`../docs/DOC-STYLE-GUIDE.md`](../docs/DOC-STYLE-GUIDE.md), rule R4) deliberately governs **only** `docs/` and the numbered stage folders, never `.github/`. Copilot primitives follow *this* standard. A documentation review must not restructure a primitive as prose.

## The harness model

A primitive is part of the repository's agent harness. The kit uses this model:

```text
Harness = Instructions + Constraints + Feedback + Memory + Evaluation + Governance
```

| Layer | Owning primitive |
|---|---|
| Instructions | `copilot-instructions.md`, `instructions/*.instructions.md` |
| Constraints | `hooks/*.json` that block tool calls; instruction `applyTo` scopes |
| Feedback | Prompts and agents that run checks and report results |
| Memory | Team-maintained ADRs, specifications, tests, and Git history |
| Evaluation | `workflows/spec-quality.yml` and `scripts/validate-copilot-primitives.py` |
| Governance | This standard, enforced by the `copilot-primitives` CI job |

Prefer updating an existing primitive over adding a near-duplicate.

The branch's [language metadata](language.json) identifies its edition. The validator recognizes equivalent structural headings in Spanish on `espanol`; translating prose never changes frontmatter schemas or technical identifiers.

## Rules for all primitives

### Markdown and style

- [ ] Use English on `main` and `develop`, Brazilian Portuguese on `portugues-br`, and Spanish on `espanol`, including primitive prose. Follow the [language policy](../README.md#idiomas-do-repositório), preserving paths, identifiers, schemas, and official technical names. Do not use emojis; convey NOTE, TIP, IMPORTANT, WARNING, and CAUTION with GFM alerts such as `> [!NOTE]`.
- [ ] Use exactly one H1 (`#`) per file: the document title below the frontmatter. The primitive validator enforces this rule; markdownlint's MD025 (multiple top-level headings) is disabled.
- [ ] The blank line between the closing `---` and H1 is optional; both forms pass lint. Agents, prompts, and skills omit it, while instruction files retain it. MD022 does not trigger at the frontmatter boundary and is not overridden. Follow neighboring files in the same directory instead of creating a formatting-only diff.
- [ ] Never skip a heading level; use `#`, then `##`, then `###`.
- [ ] Every fenced code block declares a language, such as `java`, `json`, `text`, or `bash`. Review enforces this convention because markdownlint's MD040 is disabled.
- [ ] Use real GFM tables (with a `|---|` separator row) for two or more dimensions, and `- [ ]` checklists for items readers must verify.
- [ ] End with exactly one newline. Do not use trailing spaces, hard tabs, or consecutive blank lines.
- [ ] Never disable a markdownlint rule inline with an HTML-comment pragma (failure no. 2). The root [`../.markdownlint-cli2.jsonc`](../.markdownlint-cli2.jsonc) is the only lint configuration. Inline pragmas duplicate it and consume context-window tokens without instructional value. The pragmas removed from 158 files disabled the same rules already disabled by that configuration: redundant text that changed nothing and consumed tokens.

### Content and accuracy

- [ ] **Cite each convention's authoritative source** instead of repeating the summary in `copilot-instructions.md`. Branch names come from [`../00-GIT-WORKFLOW.md`](../00-GIT-WORKFLOW.md); legacy reading rules from [`instructions/natural-adabas.instructions.md`](instructions/natural-adabas.instructions.md); EARS from [`skills/sdd-requirements-engineer/SKILL.md`](skills/sdd-requirements-engineer/SKILL.md); and `source_legacy` from [`copilot-instructions.md`](copilot-instructions.md).
- [ ] **Branch prefixes** (authoritative table in [`../00-GIT-WORKFLOW.md`](../00-GIT-WORKFLOW.md)): `spec/<NNN>-<feature>`, `impl/<NNN>-<feature>`, `infra/<component>`, `docs/<topic>`, and `agent/<issue-NN>`, all branched from `develop`. Never turn `impl/` into `spec/` (failure no. 1).
- [ ] **Never invent SIFAP facts.** A primitive teaches *how to discover* legacy behavior; it never declares a business rule. The corpus in `01-archaeology/legacy-sifap/` contains 24 Natural members (12 `.NSP`, 5 `.NSN`, 2 `.NSC`, 2 `.NSA`, 1 `.NSL`, 2 `.jcl`), 4 `.ddm` DDMs, and 1 `.txt` FDT listing. No `.NSD` file exists.
- [ ] **Approved toolchain only.** Never recommend, install, or migrate to Cursor, Windsurf, Codex, Cline, Continue, Aider, Codeium, Tabnine, IntelliJ, Eclipse, or Neovim; VS Code with GitHub Copilot is the only approved editor and assistant.
- [ ] Call the event an immersion, never a `workshop` or `hackathon`.
- [ ] Use only the current English paths; the validator's stale-path check rejects retired Portuguese directory names (failure no. 5). `backend/`, `frontend/`, and `infra/` **do not exist yet**; the team creates them in Stages 3 and 4 as needed for the selected scope.

## Frontmatter by primitive type

Each primitive type has a closed frontmatter schema: an unknown, retired, or invalid key **fails the `copilot-primitives` gate**. Platform-specific keys are silently ignored on other surfaces and may be retained. Quote the string values of `name` and `description`, following the kit's convention for agents, prompts, instructions, and skills.

### Agent frontmatter

File: `agents/<id>.agent.md`.

| Key | Notes |
|---|---|
| `name` | Agent ID, present by convention. Renaming an agent silently breaks every prompt linked to it through `agent:`. |
| `description` | The only key strictly required by the gate. |
| `tools` | For example, `[read, search, edit]`; add `execute` or `"github/*"` only when needed. |
| `model` | Optional. |
| `handoffs` | Stage agents only, and only in VS Code. Persona agents never use it. |
| `target`, `user-invocable`, `disable-model-invocation`, `metadata`, `agents` | Optional. |
| `mcp-servers` | GitHub.com and CLI only. |
| `argument-hint` | VS Code only. |

The `infer:` key is retired; remove it.

> [!NOTE]
> Only sequential **stage** agents have `handoffs`, and only when a next stage exists. `archaeologist -> architect -> builder` pass work onward, while the final Stage 4 agent (`evolution`) has no transition. No persona agent has `handoffs`.

### Prompt frontmatter

File: `prompts/<name>.prompt.md`. The slash-command name comes from the filename unless `name:` overrides it. Valid keys: `name`, `description`, `agent`, `model`, `tools`, `argument-hint`.

- `agent:` must resolve to a built-in agent (`ask`, `agent`, or `plan`) or a file in `agents/`.
- `mode:` is obsolete (old chat-mode syntax, replaced by `agent:`); remove it.
- `tested_with:` is an invented key with no effect; remove it.

### Instruction frontmatter

File: `instructions/<name>.instructions.md`. Valid keys: `applyTo`, `name`, `description`, `excludeAgent`.

- Limit `applyTo` to concrete globs. `applyTo: "**"` injects the file into every request and **fails the gate**; overlapping files targeting paths such as `**/*.tf` caused failure no. 6.

### Repository-wide instructions (`copilot-instructions.md`)

This file has **no frontmatter** and is injected into every Chat, agent, and code-review request on every surface. Each line therefore incurs a recurring token cost. Keep it to **100 lines or fewer**.

- Include only **broadly applicable** content: project context, target stack, cross-cutting rules, and strict prohibitions. GitHub's guidance is to use "short, self-contained statements".
- **Do not repeat language- or path-specific rules.** Path-scoped files exist to avoid overloading repository-wide instructions. Java, TypeScript, Terraform, database, and security details belong in `instructions/*.instructions.md`, loaded automatically for matching paths.
- Keep the **stack declaration** here even though scoped files repeat it. Whether `applyTo` matches a nonexistent directory is undocumented, and `backend/` and `frontend/` are created only in Stage 3.
- Avoid the documented anti-patterns: instructions to read another document, routing by tool or extension, tone mandates, and response-length limits.

### Skill frontmatter

File: `skills/<dir>/SKILL.md`. Only `name` and `description` are valid.

- `name` **must exactly match the parent directory name** (lowercase letters, digits, and hyphens; at most 64 characters), or the skill silently fails to load (failure no. 4).
- `description` must explain **when to use** the skill because it controls semantic loading, and it is limited to 1,024 characters.
- `license`, `allowed-tools`, `compatibility`, and `metadata` are **not** part of the schema; remove them.

### Hook configuration

A hook is a flat JSON file at `hooks/<name>.json`. A nested `<name>/hooks.json` is **never discovered** or executed (failure no. 3). The handler script lives in `hooks/<name>/` and must be executable.

- `version` must be `1`; `hooks` maps each event to a list of handlers.
- Events include `sessionStart`, `sessionEnd`, `userPromptSubmitted`, `preToolUse`, and `postToolUse`. A handler's `type` is `command`, `http`, or `prompt`.

A `preToolUse` hook blocks a tool call by writing this object to stdout:

```json
{"permissionDecision":"deny","permissionDecisionReason":"..."}
```

## Required body sections

The section structure is checked by `scripts/validate-copilot-primitives.py`. Use these headings in the order shown.

The validator accepts the English agent and prompt headings below alongside the existing Portuguese headings. These aliases do not make any required section optional. English skills use `When to Use` or `When to Invoke`, `Output Template`, and `Quality Gate`. English scoped instructions use `Conventions`, `Do / Don't`, and `PR Checklist`.

| Primitive | Required `##` sections, in order |
|---|---|
| Agent | `Mission`, `Leading Personas`, `Operating Principles`, `What This Agent Knows`, `What This Agent Does NOT Know`, `Available Prompts`, `Definition of Done` or `Stage N Definition of Done`, `Anti-Patterns This Agent Rejects` |
| Prompt | `Objective`, `When to Invoke` or `When to Use`, `Preconditions`, `Inputs the Team Must Provide`, `What I Will Do`, `What I Will NOT Do`, `Output Format`, optional `Rules for <file>`, `Definition of Done`, `Prompt Body`, `Example Invocation` |
| Instruction | Concrete topic sections, followed by `Conventions`, `Do / Don't`, `PR Checklist` |
| Skill | `When to Invoke`, a substantive procedure section, `Output Template`, `Quality Gate` |

Agents also have a recommended `SDD Workflow` section describing skills, artifact ownership, and handoff gates independently of tooling. The validator accepts the existing `Integração com o Spec-Kit` heading as a compatibility alias; it does not require adopting that tool. Describe optional tool setup and operation separately from the agent's responsibilities.

## Templates

Copy a template, retain its frontmatter and section order, and replace every angle-bracket placeholder.

### Agent template

````markdown
---
name: "<agent-id>"
description: "<Stage N or Persona> assistant: one-line description"
tools: [read, search, edit]
# handoffs:                 # Stage agents only, when a next stage exists
#   - label: "Start Stage <N+1>"
#     agent: <next-agent-id>
#     prompt: "<what the next agent does with this stage's artifacts>"
#     send: false
---
# @<agent-id>-agent

## Mission

<What the agent helps the team do and the boundary it will not cross.>

## Leading Personas

| Role | Involvement |
|------|-----------|
| **<Persona>** | LEAD: <responsibility> |

## Operating Principles

- **<Principle>.** <One or two sentences about judgment or routing.>

## What This Agent Knows

<General, transferable patterns, never system-specific answers.>

## What This Agent Does NOT Know

<Everything that must emerge from the team's own investigation.>

## Available Prompts

| Command | Purpose |
|---------|---------|
| [`/<command>`](../prompts/<file>.prompt.md) | <purpose> |

## Definition of Done

- [ ] <verifiable outcome>

## Anti-Patterns This Agent Rejects

1. **<Anti-pattern>.** <Why it is rejected and how to proceed instead.>

## SDD Workflow

<Required skills, artifact ownership, validation, and handoff. Identify any optional tooling and who operates it without making it a prerequisite.>
````

A stage agent may prefix the third-to-last heading with its stage, for example, `## Stage 1 Definition of Done`.

### Prompt template

`## Prompt Body` is plain Markdown addressed to the agent in the second person, never a code block. Start with a role line such as `You are @<agent-id>.` Guide the work with bold step headings, such as `**Step 1 - ...**` and `**Step 2 - ...**`, each followed by items.

````markdown
---
name: "<slash-command>"
description: "<one line>"
argument-hint: "<arg=... arg=...>"
agent: "<agent-id>"
tools: ["read", "search", "edit"]
---
# /<slash-command>

## Objective

<The single outcome this prompt produces.>

## When to Invoke

## Preconditions

## Inputs the Team Must Provide

## What I Will Do

## What I Will NOT Do

## Output Format

```markdown
<the exact format the prompt appends or returns>
```

## Definition of Done

- [ ] <verifiable outcome>

## Prompt Body

You are `@<agent-id>`. <One-line task framing.>

**Step 1 - <action>**

- <instruction>

**Step 2 - <action>**

- <instruction>

## Example Invocation

```text
/<slash-command> arg=<value>
```
````

When a prompt depends on an instruction or skill, add an optional `## Rules for <file>` section with the applicable rules immediately before `## Definition of Done`.

### Instruction template

````markdown
---
description: "Use when <situation covered by this file>."
applyTo: "<glob>,<glob>"
---

# <Topic> guide

<One paragraph: what activates this file, what it covers, and which neighboring instruction owns the rest.>

## <Concrete topic>

<Guidance with examples.>

## Conventions

| Rule | Rationale |
|---|---|
| <rule> | <reason> |

## Do / Don't

| Do | Don't |
|---|---|
| <do> | <do not> |

## PR Checklist

- [ ] <verifiable item>
````

### Skill template

`name` must match the directory name in `skills/<dir>/`.

````markdown
---
name: "<dir>"
description: "Use when <trigger>. Triggers include \"<keyword>\", \"<keyword>\"."
---
# <Skill title>

## When to Invoke

- "<paraphrase of a request that should load this skill>"

## <Substantive procedure>

<A checklist, table, or numbered steps: the operational procedure.>

## Output Template

```markdown
<the format produced by the skill>
```

## Quality Gate

- [ ] <objective pass/fail check>
````

### Hook template

A flat `hooks/<name>.json` file, with the referenced script in `hooks/<name>/` marked executable.

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "type": "command",
        "bash": ".github/hooks/<name>/<script>.sh",
        "cwd": ".",
        "env": { "MODE": "block" },
        "timeoutSec": 10
      }
    ]
  }
}
```

## Enforcement

- The **`copilot-primitives`** job in [`workflows/spec-quality.yml`](workflows/spec-quality.yml) runs [`scripts/validate-copilot-primitives.py`](scripts/validate-copilot-primitives.py). It checks frontmatter schemas, `prompt -> agent` and `handoff -> agent` integrity, one H1, exactly one final newline, relative links in `.github/`, forbidden pragmas and tools, stale paths, and the required sections above.
- The **`markdown-lint`** job uses the root [`../.markdownlint-cli2.jsonc`](../.markdownlint-cli2.jsonc); **`spec-traceability`** and **`legacy-traceability`** enforce REQ-ID and `source_legacy` coverage.
- This configuration disables `MD025` and `MD040`, among other rules. Do not confuse the two gates: "exactly one H1" is enforced by the primitive validator, not markdownlint. "Every fenced block declares a language" is a review convention, not a lint failure.
- Every recurring error gets a named guard in code or CI and, when it changes a durable decision, an ADR. Facilitator postmortems and answer materials remain outside this public repository.

Reference implementations: [`agents/archaeologist.agent.md`](agents/archaeologist.agent.md), [`prompts/stage-archaeologist-extract-business-rules.prompt.md`](prompts/stage-archaeologist-extract-business-rules.prompt.md), [`skills/sdd-requirements-engineer/SKILL.md`](skills/sdd-requirements-engineer/SKILL.md), and [`instructions/modular-monolith.instructions.md`](instructions/modular-monolith.instructions.md).

## Authoring checklist

- [ ] The primitive is in the correct folder with the correct suffix (`.agent.md`, `.prompt.md`, `.instructions.md`, `SKILL.md`, or a flat `hooks/<name>.json`).
- [ ] Frontmatter uses only valid keys, with no retired (`infer`, `mode`) or invented (`tested_with`) keys, and the skill's `name` matches its directory.
- [ ] Every required section is present and in order.
- [ ] There is exactly one H1, no skipped heading level, a language on every fenced block, one final newline, and no markdownlint pragma.
- [ ] Every convention cites its authoritative document; there are no invented SIFAP facts or forbidden tools. Content follows the branch language policy and contains no emojis.
- [ ] Every relative link resolves to a file on disk.
- [ ] `python3 .github/scripts/validate-copilot-primitives.py` and `npx markdownlint-cli2 "<file>"` report zero issues.
