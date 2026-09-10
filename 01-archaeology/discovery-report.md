# Discovery report - Stage 1

> **Trail:** [Team kit](../README.md) > [Stage 1](README.md) > **Discovery report**

**Accepted H1 evidence package for the isolated CPF/NIS validation feature.**

| Field | Value |
|---|---|
| Date / edition | 2026-09-10 / English documentation on develop |
| Acceptance source | Requesting user in this Copilot conversation; no individual attendee names supplied |
| Reading scope | All 24 library files, four DDMs and the FDT listing |
| Selected feature | Isolated CPF/NIS validation using the existing shared-validator contract |
| Baseline commit | 5801b1cb712f3c2a909a63060cfa3d55bbea72c3 |
| H1 status | Accepted for Stage 2 specification of the selected feature; acceptance reported by the requesting user on 2026-09-10 |

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

Full evidence, unconfirmed hypotheses and original question statuses are in
[mysteries-found.md](mysteries-found.md). Its H1 disposition table covers all
41 questions: one bounded source-selection decision and 40 accepted deferrals,
each with an accountable role and a reopening gate. None is falsely closed as
a historical business question. These domains remain outside the first feature:

| Decision needed | Local question references | Potential impact |
|---|---|---|
| Calculation/storage ownership and restart behavior | Q13-Q21 | Payment identifiers, duplicate writes, transmitted output and audit consistency |
| Intended registration/document/eligibility rules | Q01-Q12, Q30-Q32 | Acceptance differences, status changes, exceptions and data loss |
| Bank, payment and audit vocabularies | Q22-Q24, Q35, Q39 | Incorrect lifecycle interpretation and operational outcomes |
| Ordering, masks and report populations | Q25-Q29, Q33-Q34 | Misleading totals/history or inconsistent data disclosure |
| Complete physical/data ownership model | Q36-Q38, Q40-Q41 | Unmapped fields/partitions, derived behavior and numeric representation |

The canonical checklist supplies pair-level ID ranges, not an individual mapping.
Local BONUS-Q keys do not replace the 20 canonical mysteries or certify a score.
Pair 1 owns reconciliation with the facilitator before any canonical score is
reported. This administrative mapping is not substituted for source traceability.

## 4. Approved scope

The requesting user delegated the remaining scope decisions and reported their
acceptance. The first feature is **isolated CPF/NIS validation**, not complete
registration, eligibility or payment modernization. It has a small, source-linked
contract and no database or external registry dependency.

| Decision | Accepted boundary | Evidence / follow-through |
|---|---|---|
| H1-D01 | Select SUBVALCP, CCVALCPF, SUBVALNI and PDAVALID as the behavior baseline for this feature only. | [SUBVALCP.NSN](legacy-sifap/natural-programs/SUBVALCP.NSN#L28), [CCVALCPF.NSC](legacy-sifap/natural-programs/CCVALCPF.NSC#L39), [SUBVALNI.NSN](legacy-sifap/natural-programs/SUBVALNI.NSN#L38), [PDAVALID.NSA](legacy-sifap/natural-programs/PDAVALID.NSA#L43). Catalogue SC, CV and SN entries. |
| H1-D02 | Preserve selected error precedence, leading-zero identifiers, success code 0 and special indicator N. For CPF, a shared-validator failure returns 1001, not the unused header code 1003. Do not add CPF's equal-digit rule to NIS. | [CPF branches](legacy-sifap/natural-programs/SUBVALCP.NSN#L44), [NIS branches](legacy-sifap/natural-programs/SUBVALNI.NSN#L52). Wrong type, absent value, nonnumeric content and check-digit failure remain distinct. |
| H1-D03 | Keep identifiers as text and retain the A11 parameter contract. No silent trimming, padding, punctuation removal or lossy numeric conversion is approved for a new interface. | [PDAVALID.NSA](legacy-sifap/natural-programs/PDAVALID.NSA#L47). Stage 2 must make boundary/length handling explicit and justify any adapter behavior not present in the selected source. |
| H1-D04 | Do not replace existing callers or normalize conflicting CADBENEF, VALBENEF and VALDOCS behavior. Valid check digits do not establish identity, active NIS registration, document approval or eligibility. | BONUS-Q01, Q10, Q12, Q30 and Q31 in the [disposition register](mysteries-found.md#h1-dispositions). |
| H1-D05 | Exclude Adabas writes/migration, money, dates, dependent registration, bank files, audit persistence, dashboards, deployment and live-lab operations. Do not log raw CPF/NIS or echo them in diagnostics. | All deferred items remain blocked before scope expansion; the fixed repository privacy rules still apply. No new production integration is authorized by H1. |
| H1-D06 | Require source-linked tests of error order, both CPF digits, NIS weights/remainders, repeated digits, leading zeros, wrong length/type, repeated calls and execution-error separation before implementation acceptance. | Pair 4 / QA owns examples; Pair 3 owns implementation. Static checks below are not a Natural execution baseline. Any intended behavior change returns to Pair 1 for approval. |

Pair 2 / Architect can now specify this feature using the repository's current
Spec-Kit workflow. Pair 1 owns the scope and requirement interpretation, Pair 4
the characterization evidence, and Pair 5 the documentation/operational boundary.
These decisions are not formal EARS, an architecture selection or H2 approval.

## 5. Deliverables

| Artifact | Status |
|---|---|
| [inventory.md](inventory.md) | Original metadata-only kickoff retained; linked to subsequent source reading |
| [reading-coverage.md](reading-coverage.md) | Full technical-source ledger and individual control-block intervals |
| [business-rules-catalog.md](business-rules-catalog.md) | Accepted source-reading package; selected baseline identified; unresolved interpretations preserved |
| [program-data-dictionary.md](program-data-dictionary.md) | Complete declaration reading aid; no compiler compatibility claim |
| [data-map.md](data-map.md) | All DDM fields, descriptors, relationships and FDT comparisons |
| [dependency-map.md](dependency-map.md) | Executable calls/imports/accesses, work files and transaction ordering |
| [mysteries-found.md](mysteries-found.md) | All 41 H1 dispositions accepted; original hypotheses remain open with reopening gates |
| [glossary.md](glossary.md) | More than 30 source-backed terms; disputed meanings distinguished |
| [validation/evidence.json](validation/evidence.json) | Reproducible static-check results and SHA-256 fingerprints, not a business approval certificate |
| [validation/validator-tests.tap](validation/validator-tests.tap) | Test execution and coverage evidence for the documentary validator |

## 6. Verification and approval

On 2026-09-10 the requesting user authorized the remaining closure decisions
and reported: "foi feito o aceute de tudo". This records user-reported acceptance;
it does not invent individual signatures, meeting attendance, runtime results or
answers to unresolved legacy questions. Team reading/review and receiving-side
acceptance are recorded through that report, not independently collected
signatures. The required human transition is not described as an agent-run meeting.
Responsibility follows the existing team roles; no personal names were supplied.

The closure run executes the existing validator and its negative tests. It checks
control intervals, declared variable formats, DDM field names/formats and local
links, plus all 41 H1 dispositions, owners and reopening gates. **17/17 tests pass**,
with **94.84% line coverage and 98.43% branch coverage of the validator**; Markdown
lint reports no issues in the ten documents. Source fingerprints identify all 29
technical inputs; artifact fingerprints identify the working-tree documentary
snapshot based on the recorded commit, not a claim that closure edits are committed.
No commit/push was performed. Commands and their limitations are in
[reading-coverage.md](reading-coverage.md#reproducing-static-checks).

No Natural compilation, runtime equivalence test or live database inspection has
been performed. The 2012 Markdown was read fully; the 2008 and 1997 documents were
consulted in relevant sections. DOCX equivalence, deployed settings and legal
validity of historic rules are not certified by this acceptance.

- [x] Technical reading and reproducible documentary validation are recorded.
- [x] Requesting user's report of team/receiving acceptance is recorded with date and provenance.
- [x] The selected CPF/NIS feature and all deferred scope have an approved disposition.
- [x] Every question has an accountable role and a reopening gate; none is fabricated as solved.
- [x] Release the selected feature to the architect for Stage 2 specification.
- [ ] Before implementation acceptance, produce source-linked characterization tests and identify any unavailable legacy runtime evidence.

### Continue reading

| Previous | Next, within the accepted scope |
|---|---|
| [Stage 1 guide](GUIDE.md) | [Stage 2 guide](../02-modern-spec/GUIDE.md) |
