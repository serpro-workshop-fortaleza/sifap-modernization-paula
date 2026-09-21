# Code conventions

## Core sections (required)

### 1) Naming rules

| Item | Rule | Example | Evidence |
|------|------|---------|----------|
| Files | [RULE] | [EXAMPLE] | [FILE] |
| Functions/methods | [RULE] | [EXAMPLE] | [FILE] |
| Types/interfaces | [RULE] | [EXAMPLE] | [FILE] |
| Constants/environment variables | [RULE] | [EXAMPLE] | [FILE] |

### 2) Formatting and linting

- Formatter: [TOOL + CONFIGURATION FILE]
- Linter: [TOOL + CONFIGURATION FILE]
- Most relevant enforced rules: [RULE_1], [RULE_2], [RULE_3]
- Run commands: [COMMANDS]

### 3) Import and module conventions

- Import grouping/order: [RULE]
- Alias versus relative import policy: [RULE]
- Public/barrel export policy: [RULE]

### 4) Error and logging conventions

- Error strategy per layer: [BRIEF SUMMARY]
- Logging style and required context fields: [SUMMARY]
- Sensitive data masking rules: [SUMMARY]

### 5) Testing conventions

- Test file naming/location rule: [RULE]
- Default mocking strategy: [RULE]
- Coverage expectation: [RULE or TODO]

### 6) Evidence

- [path/to/lint-config]
- [path/to/format-config]
- [path/to/representative-source-file]

## Extended sections (optional)

Add only for large or inconsistent codebases:

- Layer-specific error handling matrix
- Language-specific strictness options
- Repository-specific commit and branch conventions
- Known convention violations requiring correction
