# Architecture

## Core sections (required)

### 1) Architectural style

- Primary style: [layered/feature-based/event-driven/other]
- Classification rationale: [brief evidence-based justification]
- Key constraints: [two or three constraints shaping the design]

### 2) System flow

```text
[input] -> [processing] -> [domain logic] -> [data/integration] -> [response/output]
```

Describe the flow in four to six steps using file-based evidence.

### 3) Layer and module responsibilities

| Layer or module | Responsible for | Must not contain | Evidence |
|-----------------|------|--------------|----------|
| [name] | [responsibility] | [non-responsibility] | [file] |

### 4) Reused patterns

| Pattern | Where found | Why it exists |
|---------|-------------|---------------|
| [singleton/repository/adapter/etc.] | [path] | [reason] |

### 5) Known architectural risks

- [Risk 1 + impact]
- [Risk 2 + impact]

### 6) Evidence

- [path/to/entrypoint]
- [path/to/main-layer-files]
- [path/to/data-or-integration-layer]

## Extended sections (optional)

Add only when needed:

- Startup order details
- Async or event topology diagrams
- Anti-pattern catalog with refactoring paths
- Failure mode analysis and resilience posture
