# Codebase concerns

## Core sections (required)

### 1) Top risks (prioritized)

| Severity | Concern | Evidence | Impact | Suggested action |
|----------|---------|----------|--------|------------------|
| [high/medium/low] | [issue] | [file or scan output] | [impact] | [next action] |

### 2) Technical debt

List only the most important debt items.

| Debt item | Why it exists | Where | Risk if ignored | Suggested fix |
|-----------|---------------|-------|-----------------|---------------|
| [item] | [reason] | [path] | [risk] | [fix] |

### 3) Security concerns

| Risk | OWASP category (if applicable) | Evidence | Current mitigation | Gap |
|------|--------------------------------|----------|--------------------|-----|
| [risk] | [A01/A03/etc. or N/A] | [path] | [what exists] | [what is missing] |

### 4) Performance and scaling concerns

| Concern | Evidence | Current symptom | Scaling risk | Suggested improvement |
|---------|----------|-----------------|-------------|-----------------------|
| [issue] | [path/metric] | [symptom] | [risk] | [action] |

### 5) Fragile or high-churn areas

| Area | Reason for fragility | Churn signal | Safe change strategy |
|------|-------------|-------------|----------------------|
| [path] | [reason] | [evidence of recent changes] | [approach] |

### 6) `[ASK USER]` questions

Add unresolved, intent-dependent questions as a numbered list.

1. [ASK USER] [question]

### 7) Evidence

- [scan output section reference]
- [path/to/code-file]
- [path/to/config-or-history-evidence]

## Extended sections (optional)

Add only when needed:

- Full bug inventory
- Remediation roadmap per component
- Cost/effort estimates per concern
- Dependency risk and ownership mapping
