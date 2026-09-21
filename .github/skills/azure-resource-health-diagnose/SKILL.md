---
name: "azure-resource-health-diagnose"
description: "Use when the user reports a deployed Azure resource is failing, degraded, throttled, or unavailable, or asks to investigate it. Diagnoses a specific resource through logs, metrics, and telemetry and produces a prioritized remediation plan. Requires the resource to be deployed and emitting telemetry. Triggers include \"unhealthy resource\", \"troubleshoot Azure\", \"why is this failing\", \"diagnose throttling\", and \"investigate a degraded resource\"."
---
# Azure resource health and issue diagnosis

This workflow analyzes a specific Azure resource to assess its health, diagnose issues through logs and telemetry, and develop a remediation plan.

> [!NOTE]
> This skill depends on the **Azure MCP server** (or the `az` CLI) and requires the target resource to be deployed and emitting telemetry. When both are available, prefer Azure MCP tools (`azmcp-*`) over the Azure CLI.

## When to Invoke

- "Our App Service is returning 500 errors. Diagnose it."
- "Investigate why this Cosmos DB is being throttled."
- "The storage account appears degraded. Find the root cause."
- "Troubleshoot this VM and provide a remediation plan."

## Prerequisites

- Azure MCP server configured and authenticated.
- Target Azure resource identified (name and, optionally, resource group/subscription).
- The resource must be deployed and running to generate logs and telemetry.

## Workflow steps

### Step 1: Get Azure best practices

Get diagnostic and troubleshooting best practices with the Azure best practices tool. Focus on health monitoring, log analysis, and problem-solving patterns. Use them to guide the diagnosis and remediation recommendations.

### Step 2: Resource discovery and identification

1. **Locate the resource**:
    - If only a name is provided, search subscriptions (`azmcp-subscription-list` or `az resource list --name <resource-name>`).
    - If there are multiple matches, ask the user to specify the subscription or resource group.
    - Collect resource type and status, location, tags, configuration, and dependencies.
2. **Detect the resource type** to choose appropriate diagnostics:

| Resource type | Primary diagnostics |
|---|---|
| Web Apps / Function Apps | Application logs, performance metrics, dependency tracing |
| Virtual Machines | System logs, performance counters, boot diagnostics |
| Cosmos DB | Request metrics, throttling, partition statistics |
| Storage Accounts | Access logs, performance metrics, availability |
| SQL Database | Query performance, connection logs, resource utilization |
| Application Insights | Application telemetry, exceptions, dependencies |
| Key Vault | Access logs, certificate status, secret usage |
| Service Bus | Message metrics, dead-letter queues, throughput |

### Step 3: Health status assessment

1. **Basic health check**: provisioning state and operational status, service availability, recent deployment or configuration changes, and current utilization (CPU, memory, and storage).
2. **Service-specific indicators**:

| Resource type | Health indicators |
|---|---|
| Web Apps | HTTP response codes, response times, uptime |
| Databases | Connection success rate, query performance, deadlocks |
| Storage | Availability percentage, request success rate, latency |
| VMs | Boot diagnostics, guest operating system metrics, network connectivity |
| Functions | Execution success rate, duration, and error frequency |

### Step 4: Log and telemetry analysis

1. **Find monitoring sources**: identify Log Analytics workspaces (`azmcp-monitor-workspace-list`), associated Application Insights instances, and relevant log tables (`azmcp-monitor-table-list`).
2. **Run diagnostic queries** with `azmcp-monitor-log-query` and choose KQL based on the resource type.

General error analysis:

```kql
union isfuzzy=true
    AzureDiagnostics,
    AppServiceHTTPLogs,
    AppServiceAppLogs,
    AzureActivity
| where TimeGenerated > ago(24h)
| where Level == "Error" or ResultType != "Success"
| summarize ErrorCount=count() by Resource, ResultType, bin(TimeGenerated, 1h)
| order by TimeGenerated desc
```

Performance analysis:

```kql
Perf
| where TimeGenerated > ago(7d)
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| summarize avg(CounterValue) by Computer, bin(TimeGenerated, 1h)
| where avg_CounterValue > 80
```

Application-specific queries:

```kql
requests
| where timestamp > ago(24h)
| where success == false
| summarize FailureCount=count() by resultCode, bin(timestamp, 1h)
| order by timestamp desc
```

3. **Recognize patterns**: recurring errors or anomalies, correlation with deployment/configuration changes, performance degradation trends, and failures in dependencies or external services.

### Step 5: Issue classification and root cause analysis

1. **Classify severity**:

| Severity | Meaning |
|---|---|
| Critical | Service unavailable, data loss, security breach |
| High | Performance degradation, intermittent failures, high error rate |
| Medium | Warnings, suboptimal configuration, minor performance issues |
| Low | Informational alerts, optimization opportunities |

2. **Determine the root cause category**: configuration issue, resource constraint (CPU/memory/disk/throttling), network issue, application issue (failure, memory leak, inefficient query), external dependency, or security issue (authentication failure, certificate expiration).
3. **Assess impact**: affected users and systems, implications for data integrity and security, and recovery time priorities.

### Step 6: Generate a remediation plan

1. **Immediate actions** (Critical): emergency fixes to restore availability, workarounds, and escalation procedures.
2. **Short-term fixes** (High/Medium): configuration adjustments, resource scaling, software fixes, and monitoring improvements.
3. **Long-term improvements**: architectural changes for resilience, preventive measures, and documentation.
4. **Implementation steps**: prioritized items with specific Azure CLI commands, testing/validation, rollback plans, and post-change monitoring.

### Step 7: User confirmation and report generation

Present a summary and gate remediation on user approval:

```text
Azure resource health assessment

Resource overview:
- Resource: [Name] ([Type])
- Status: [Healthy/Warning/Critical]
- Location: [Region]
- Last analysis: [Timestamp]

Issues identified:
- Critical: X issues requiring immediate attention
- High: Y issues affecting performance or reliability
- Medium: Z issues for optimization
- Low: N informational items

Key issues:
1. [Issue type]: [Description] - Impact: [High/Medium/Low]

Remediation plan:
- Immediate actions: X items
- Short-term fixes: Y items
- Long-term improvements: Z items
- Estimated resolution time: [Timeline]

Proceed with the detailed remediation plan? (y/n)
```

After approval, generate the detailed report using the output template below.

## Error handling

| Situation | Action |
|---|---|
| Resource not found | Request the exact name and location |
| Authentication issues | Provide guidance on Azure authentication setup |
| Insufficient permissions | List the required read-only RBAC roles |
| No logs available | Suggest enabling diagnostic settings and waiting for data |
| Query timeouts | Split the analysis into smaller time windows |
| Service-specific gaps | Provide a generic health assessment and record limitations |

## Output Template

The skill writes a health report. Below the H1 title (`Azure resource health report: <resource>`), it contains:

````markdown
## Executive summary

<overview of health status and key findings>

## Health metrics

- Availability: X% over the last 24 h
- Error rate: X% over the last 24 h
- Resource utilization: CPU/memory/storage percentages

## Issues identified

### Critical issues

- <Issue>: root cause, business impact, immediate action

### High-priority issues

- <Issue>: root cause, reliability impact, recommended fix

## Remediation plan

### Phase 1: Immediate actions (0 to 2 hours)

```bash
<Azure CLI commands to restore service, with explanations>
```

### Phase 2: Short-term fixes (2 to 24 hours)

```bash
<Azure CLI commands for reliability improvements>
```

### Phase 3: Long-term improvements (1 to 4 weeks)

```bash
<Azure CLI and configuration changes>
```

## Validation steps

- [ ] Verify issue resolution through logs
- [ ] Confirm performance improvements
- [ ] Test application functionality
- [ ] Update monitoring and alerts
````

## Quality Gate

- [ ] Resource health status was accurately assessed from logs, metrics, and telemetry.
- [ ] All significant issues were identified and classified by severity.
- [ ] Root cause analysis was completed for each Critical and High finding.
- [ ] The remediation plan provides specific Azure CLI steps, with validation and rollback.
- [ ] Issues are prioritized by business impact, with monitoring and prevention recommendations.
- [ ] Detailed remediation actions are executed only after explicit user confirmation.
