# External integrations

## Core sections (required)

### 1) Integration inventory

| System | Type (API/DB/queue/etc.) | Purpose | Authentication model | Criticality | Evidence |
|--------|---------------------------|---------|------------|-------------|----------|
| [name] | [type] | [purpose] | [authentication] | [high/medium/low] | [file] |

### 2) Data stores

| Store | Role | Access layer | Main risk | Evidence |
|-------|------|--------------|----------|----------|
| [db/cache/etc.] | [role] | [module] | [risk] | [file] |

### 3) Secret and credential handling

- Credential sources: [environment/secret manager/configuration]
- Hardcoded value checks: [result]
- Rotation or lifecycle notes: [known/unknown]

### 4) Reliability and failure behavior

- Retry/backoff behavior: [implemented/none/partial]
- Timeout policy: [where configured]
- Circuit breaker or fallback behavior: [if any]

### 5) Integration observability

- Logging around external calls: [yes/no + where]
- Metrics/tracing coverage: [yes/no + where]
- Visibility gaps: [list]

### 6) Evidence

- [path/to/integration-wrapper]
- [path/to/config-or-env-template]
- [path/to/monitoring-or-logging-config]

## Extended sections (optional)

Add only when needed:

- Per-endpoint catalog
- Authentication flow sequence diagrams
- SLA/SLO per integration
- Region/failover topology notes
