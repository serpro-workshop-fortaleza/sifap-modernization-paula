# Codebase structure

## Core sections (required)

### 1) Top-level map

List only relevant top-level directories and files.

| Path | Purpose | Evidence |
|------|---------|----------|
| [path/] | [purpose] | [source] |

### 2) Entry points

- Main runtime entry: [FILE]
- Secondary entry points (worker/CLI/jobs): [FILES or NONE]
- How the entry is selected (script/configuration): [NOTE]

### 3) Module boundaries

| Boundary | What belongs here | What must not be here |
|----------|-------------------|------------------------|
| [module/layer] | [responsibility] | [forbidden logic] |

### 4) Naming and organization rules

- File naming pattern: [kebab/camel/Pascal + examples]
- Directory organization pattern: [feature/layer/domain]
- Import alias or path conventions: [RULE]

### 5) Evidence

- [path/to/root-tree-source]
- [path/to/entry-config]
- [path/to/key-module]

## Extended sections (optional)

Add only when repository complexity requires it:

- Detailed subdirectory maps by feature/layer
- Middleware/startup order details
- Boundaries between generated structure and source code
- Monorepo workspace structure maps
