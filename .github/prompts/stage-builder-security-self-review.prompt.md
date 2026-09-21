---
name: "security-self-review"
description: "Security self-review checklist for OWASP Top 10 issues in a newly built feature."
argument-hint: "context=<context> files=<Controller>.java,<Service>.java,<Entity>.java"
agent: "builder"
tools: ["read", "search", "edit"]
---
# /security-self-review

## Objective

Examine a feature against the OWASP Top 10 and produce a prioritized report. Do not fix automatically; the team decides.

## When to Invoke

After implementing entities, services, controllers, and tests, before Stage 4.

## Preconditions

- The code exists and compiles
- The team identifies the classes

## Inputs the Team Must Provide

- Controllers, services, and entities
- Bounded context name

## What I Will Do

- Check for secrets, SQL injection, authorization, validation, sensitive data in logs or errors, and missing rate limits
- Identify areas that require an actual scanner

## What I Will NOT Do

- Run a scanner, fix automatically, invent severity, or guarantee completeness

## Output Format

```markdown
# Security self-review - [Bounded context]
## Summary
Findings: N total | High: N | Medium: N | Low: N
## Findings
| No. | Severity | Category | File:line | Description | Remediation |
## Areas requiring external scanning
## Approval
```

Save to `03-implementation/security-review-[context].md`.

## Definition of Done

- [ ] Authentication for all endpoints, injection in all queries, and input validation have been checked
- [ ] Secrets are absent or flagged
- [ ] Severity levels are justified
- [ ] There is a section for external scanning

## Prompt Body

You are `@builder`, performing a quick self-review, not a formal audit.

**Step 1 - Secrets.** Search for "password", "secret", "key", "token", "api_key", Base64 tokens, literal values instead of `${ENV_VAR}`, and tracked `.env` files. Report the file, line, redacted pattern, and High severity.

**Step 2 - SQL injection.** Look for concatenation, interpolation in `@Query`, `nativeQuery = true` for review, and concatenated `JdbcTemplate` queries. Recommend named parameters or derived queries.

**Step 3 - Authorization.** At each endpoint, check `@PreAuthorize`, `@Secured`, method security, and filters. An unjustified public endpoint is High if it writes and Medium if it only reads.

**Step 4 - Validation.** Check `@Valid`, Bean Validation, and `@Size` or `@Pattern` constraints on strings.

**Step 5 - Exposure.** Look for passwords, tokens, or personal data in logs, stack traces, and DTOs with `password`, `token`, or `ssn`.

**Step 6 - Rate limit.** Flag POST, PUT, and DELETE without rate limiting and record this as a production concern.

**Step 7 - Report.** Sort by severity and include areas for SAST/DAST. The report is informational; the team decides what to fix or defer.

## Example Invocation

```text
/security-self-review context=<context> files=<Controller>.java,<Service>.java,<Entity>.java
```
