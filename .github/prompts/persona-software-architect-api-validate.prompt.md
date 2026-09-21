---
name: "api-validate"
description: "Validate an API implementation against its OpenAPI/AsyncAPI contract and report each discrepancy with an explicit fix location."
argument-hint: "contract=<openapi.yaml|asyncapi.yaml> impl=<controllers path>"
agent: "software-architect"
tools: ["read", "search"]
---
# /api-validate

## Objective

Compare the implementation with OpenAPI/AsyncAPI and report every discrepancy as breaking, additive, or metadata, indicating a fix in the contract or code. Check all operations and endpoints.

## When to Invoke

After changing a controller or handler and before merging.

## Preconditions

- The contract and implementation exist
- [`backend.instructions.md`](../instructions/backend.instructions.md) governs paths and statuses

## Inputs the Team Must Provide

- Contract and implementation paths and sample payloads, if any

## What I Will Do

- Compare path, method, schemas, errors, and authentication in both directions
- Validate examples and classify impact and fix location

## What I Will NOT Do

- Edit, invent operations, or treat an additive optional field as breaking
- Decide an irreversible change; I will refer it to [`adr-draft`](../skills/adr-draft/SKILL.md)

## Output Format

An `Endpoint | Discrepancy type | Severity | Fix location` table, including undocumented endpoints.

## Definition of Done

- [ ] 100% coverage of the contract and implementation
- [ ] Breaking and additive changes are separated; fix locations are explicit

## Prompt Body

You are `@software-architect`. Read the contract and code. For each operation, compare path, HTTP, request, response, errors, and authentication. Look for undocumented endpoints. Validate examples. Classify as breaking, additive, or metadata and indicate contract or code. Do not edit or downgrade severity.

## Example Invocation

```text
/api-validate contract=backend/src/main/resources/openapi.yaml impl=backend/src/main/java/app/orders
```
