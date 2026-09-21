# Architecture guidance sources (for design direction decisions)

Source registry for using official Azure architecture guidance **only for design direction decisions**.

> **The URLs in this document indicate where to research.**
> Do not treat the content at these URLs as fixed facts.
> Do not use them to decide SKU, API version, region, model availability, or PE mappings. Those decisions use `azure-dynamic-sources.md` exclusively.

---

## Separation by purpose

| Purpose | Document | Items that can be decided |
|---------|----------------|-----------------|
| **Design direction decisions** | This document (architecture-guidance-sources) | Architecture patterns, best practices, service combination direction, and security boundary design |
| **Deployment specification verification** | `azure-dynamic-sources.md` | API version, SKU, region, model availability, PE `groupId`, and actual property values |

**What CANNOT be decided using this document:**

- API version
- SKU names/prices
- Regional availability
- Model names/versions/deployment types
- PE `groupId` / DNS Zone mappings
- Specific resource property values

---

## Primary sources

Targeted lookup destinations for design direction decisions.

| ID | Document | URL | Purpose |
|----|----------|-----|---------|
| A1 | Azure Architecture Center | https://learn.microsoft.com/en-us/azure/architecture/ | Entry hub for finding domain-specific documents |
| A2 | Well-Architected Framework | https://learn.microsoft.com/en-us/azure/architecture/framework/ | Security, reliability, performance, cost, and operations principles |
| A3 | Cloud Adoption Framework / Landing Zone | https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/ | Enterprise governance, network topology, and subscription structure |
| A4 | Azure AI/ML architecture | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/ | Reference architecture hub for AI/ML workloads |
| A5 | Basic Foundry chat reference architecture | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/basic-azure-ai-foundry-chat | Basic Foundry-based chat assistant structure |
| A6 | AI Foundry chat baseline reference architecture | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-openai-e2e-chat | Enterprise Foundry chat assistant baseline (includes network isolation) |
| A7 | RAG solution design guide | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide | RAG pattern design guide |
| A8 | Microsoft Fabric overview | https://learn.microsoft.com/en-us/fabric/get-started/microsoft-fabric-overview | Fabric platform overview and workload understanding |
| A9 | Fabric governance/adoption | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-governance | Fabric governance and adoption roadmap |

## Secondary sources (tracking only)

These are not direct lookup destinations. Use them only to track changes.

| Document | URL | Notes |
|----------|-----|-------|
| Azure Updates | https://azure.microsoft.com/en-us/updates/ | Service changes and new feature announcements. Not a targeted lookup destination |

---

## Lookup trigger: when to research

Architecture guidance documents **are not consulted for every request**. Perform targeted lookups only when the triggers below apply.

### Trigger conditions

0. **When the workload type is identified in Phase 1 (automatic)**
   - Consult the relevant reference architecture beforehand to adjust question depth.
   - The trigger is automatic, even without a mention of "best practice", etc.
   - Purpose: include decision points based on official architecture in the questions, beyond SKU/region specifications.
1. **When the user asks for a rationale for the design direction**
   - Keywords such as "best practice", "reference architecture", "recommended structure", "baseline", "well-architected", "landing zone", and "enterprise standard".
2. **When the architecture boundaries of a new service combination are ambiguous**
   - Service relationships that cannot be determined from reference files or service-gotchas.
3. **When enterprise security/governance design is needed**
   - Subscription structure, network topology, and landing zone patterns.

### When triggers do not apply

- Simple resource creation (questions about SKU, API version, or region) -> use only `azure-dynamic-sources.md`
- Service combinations already covered in domain packs -> prioritize reference files
- Bicep property value verification -> use `service-gotchas.md` or the Microsoft Docs Bicep reference

---

## Lookup limit

| Scenario | Maximum number of lookups |
|----------|----------------|
| Default (when triggered) | **Up to two** architecture guidance documents |
| Additional lookup allowed when | Documents conflict, a core design uncertainty remains, or the user requests deeper justification |
| Simple deployment specification questions | **0** (no architecture guidance lookup) |

---

## Decision rule by question type

| Question type | Documents to consult | Decision points to extract | Documents NOT to consult |
|--------------|-------------------|----------------------------------|----------------------|
| RAG / chat assistant / Foundry application | A5 or A6 + A7 | Network isolation level, authentication method (managed identity or key), indexing strategy (`push` or `pull`), and monitoring scope | Do not traverse the entire Architecture Center |
| Enterprise security / governance / landing zone | A2 + A3 | Subscription structure, `hub-spoke` network topology, identity/governance model, and security boundary | AI/ML domain documents are unnecessary |
| Fabric data platform | A8 + A9 | Capacity model (SKU selection criteria), governance level, and data boundary (workspace separation, etc.) | AI documents are unnecessary |
| Ambiguous service combination (uncertain pattern) | A1 (find the closest domain document in the hub) + that document | Key decision points identified in the document | Do not traverse all subdocuments |
| Simple resource creation values (SKU/API/region) | No lookup | - | All architecture guidance |
| General AI/ML architecture | A4 (hub) + closest reference architecture | Compute isolation, data boundary, and model serving approach | Do not traverse everything |

---

## URL fallback rule

1. Use `en-us` Learn URLs by default.
2. If a specific URL returns 404, redirects, or is obsolete -> use the parent hub page.
   - Example: if A5 fails -> search for "foundry chat" in A4 (AI/ML hub).
3. If not found in the parent hub either -> search title keywords in A1 (Architecture Center home page).
4. **Do not treat a URL's content as a fixed rule merely because the URL exists.**

---

## Full-crawl prohibition

- Do not broadly traverse Architecture Center subdocuments.
- Consult only one or two related documents specifically, according to the question-type rule.
- Even within consulted documents, use only relevant sections; do not read the entire document.
- Unlimited lookups, recursive link following, and subpage enumeration are prohibited.
