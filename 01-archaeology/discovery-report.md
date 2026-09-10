# Discovery report - Stage 1

> **Trail:** [Team kit](../README.md) > [Stage 1](README.md) > **Discovery report**

**Complete static reading of the supplied corpus, with human decisions still open.**

| Field | Value |
|---|---|
| Date / edition | 2026-09-10 / English documentation on develop |
| Team / participants | [To be filled by the team] |
| Scope | All 24 library files, four DDMs and the FDT listing |
| H1 status | Not approved; no team sign-off or feature-selection decision recorded |

## 1. Executive summary

All 24 supplied library members and five Adabas artifacts were read from header
to end, covering registration, validation, calculation, batch, consultation and
reporting paths in the SIFAP corpus. The resulting catalogue preserves source
conditions and side effects rather than assuming program names or historical
descriptions are accurate. The data map records every DDM field and contrasts
logical definitions with the physical FDT and consuming code. Historical
documents corroborate some statements but also contain explicit gaps and
contradictions, so no unresolved hypothesis has been promoted to an approved
rule. Legacy code, the shared lab and deployed infrastructure were not modified.

## 2. Evidence coverage

| Surface | Measured coverage | Evidence artifact |
|---|---|---|
| Library | 24/24 files; 17 program/subprogram bodies, 5 source/data helpers, 2 JCLs | [reading-coverage.md](reading-coverage.md) |
| Control flow | 219 IF, 15 DECIDE, 8 report hooks; comments excluded | [reading-coverage.md](reading-coverage.md) |
| Data | 4/4 DDMs + 1/1 FDT; 199 value-bearing fields, 7 groups, 14 derived descriptors | [data-map.md](data-map.md) |
| Dependencies | 9 CALLNAT, 9 INCLUDE, 23 USING, plus 3 JCL invocations | [dependency-map.md](dependency-map.md) |
| Declarations | Local variables, interfaces, imported arrays, view subsets and copycode-required fields | [program-data-dictionary.md](program-data-dictionary.md) |

The catalogue's EARS column contains pattern candidates only. Formal requirements,
REQ-IDs, acceptance criteria and modern architecture belong to Stage 2 after H1.

## 3. Questions for the handoff

Full evidence, unconfirmed hypotheses, proposed owners and open statuses are
in [mysteries-found.md](mysteries-found.md). The following are discussion priorities,
not resolved findings or an implementation plan.

| Decision needed | Local question references | Potential impact |
|---|---|---|
| Calculation/storage ownership and restart behavior | Q13-Q21 | Payment identifiers, duplicate writes, transmitted output and audit consistency |
| Intended registration/document/eligibility rules | Q01-Q12, Q30-Q32 | Acceptance differences, status changes, exceptions and data loss |
| Bank, payment and audit vocabularies | Q22-Q24, Q35, Q39 | Incorrect lifecycle interpretation and operational outcomes |
| Ordering, masks and report populations | Q25-Q29, Q33-Q34 | Misleading totals/history or inconsistent data disclosure |
| Complete physical/data ownership model | Q36-Q38, Q40-Q41 | Unmapped fields/partitions, derived behavior and numeric representation |

The canonical checklist supplies pair-level ID ranges, not an individual mapping.
Local BONUS-Q keys do not replace the 20 canonical mysteries or certify a score.
No named owner has yet approved a business interpretation.

## 4. Scope conversation

Full-source reading is not a commitment to modernize the entire system at once.
The PO has not selected a feature or confirmed deferred scope. Three existing
paths are available for the team's H1 discussion, without defining bounded contexts:

1. Document validation: compare shared CPF/NIS contracts and caller blocking/warning behavior.
2. Beneficiary consultation: validate lookup, history order, masking and the audit side effect together.
3. Payment calculation: first resolve callee/caller persistence, rounding and period assumptions.

These are investigation options, not approved requirements. The architect should
receive the selected path and open questions before any Stage 2 design begins.

## 5. Deliverables

| Artifact | Status |
|---|---|
| [inventory.md](inventory.md) | Original metadata-only kickoff retained; linked to subsequent source reading |
| [reading-coverage.md](reading-coverage.md) | Full technical-source ledger and individual control-block intervals |
| [business-rules-catalog.md](business-rules-catalog.md) | All members represented; documentation comparison; business validation pending |
| [program-data-dictionary.md](program-data-dictionary.md) | Complete declaration reading aid; no compiler compatibility claim |
| [data-map.md](data-map.md) | All DDM fields, descriptors, relationships and FDT comparisons |
| [dependency-map.md](dependency-map.md) | Executable calls/imports/accesses, work files and transaction ordering |
| [mysteries-found.md](mysteries-found.md) | Questions only, all awaiting human validation |
| [glossary.md](glossary.md) | More than 30 source-backed terms; disputed meanings distinguished |

## 6. Verification and approval

Anchored workspace searches checked control-flow marker counts, dependencies, file
end markers and DDM field counts. Markdown diagnostics were checked in the editor.
No terminal lint command, Natural compilation, runtime execution, equivalence
tests or live database inspection was performed in this read/search/edit session.
The 2012 Markdown document was read fully; the 2008 and 1997 documents were
consulted in relevant sections. DOCX equivalence was not checked.

- [x] Technical reading covers all supplied programs, helpers, jobs and Adabas definitions.
- [x] Evidence and unresolved interpretations are preserved separately.
- [ ] Each pair confirms its reading and discusses the evidence.
- [ ] Assign named reviewers and validate canonical question IDs and business intent.
- [ ] PO confirms one small feature and deferred scope.
- [ ] Conduct the live H1 conversation and record the receiving team's approval.

### Continue reading

| Previous | Next, after H1 approval |
|---|---|
| [Stage 1 guide](GUIDE.md) | [Stage 2 guide](../02-modern-spec/GUIDE.md) |
