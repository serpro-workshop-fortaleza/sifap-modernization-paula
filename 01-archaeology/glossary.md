# SIFAP legacy glossary

> **Trail:** [Team kit](../README.md) > [Stage 1](README.md) > **Glossary**

**Source-backed vocabulary for discussing the corpus without assuming one business meaning.**

Date: 2026-09-10. Team: [To be filled by the team].
`CONFIRMED` below means a literal technical definition or field label exists in
the cited source, not that a business rule has been approved. `HYPOTHESIS`
means competing meanings or intent require human review. Proposed reviewers
are roles, not a record of a person's approval.

## Registration and calculation

| Term | Source-bound meaning / use | Evidence | Status / proposed reviewer |
|---|---|---|---|
| BENEFIC | Logical beneficiary view bound to DB 057/file 150 | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L31) | CONFIRMED |
| NUM-CPF | Eleven-character beneficiary identifier; unique descriptor in BENEFIC | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L40) | CONFIRMED |
| NUM-NIS | Eleven-digit NIS/PIS-PASEP field; validator receives an alpha representation | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L52); [PDAVALID.NSA](legacy-sifap/natural-programs/PDAVALID.NSA#L49) | CONFIRMED |
| SOCPROG | Social-program parameter view, file 151 | [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L20) | CONFIRMED |
| COD-PROGRAM | Four-character program key linking stored beneficiary context and program lookup | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L302) | CONFIRMED |
| GRP-DEPEND | Dependent occurrences embedded in the holder record | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L87) | CONFIRMED |
| QTY-DEPEND | DDM calls this active count; registration increments it without initializing all dependent-state fields | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L81); [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L191) | HYPOTHESIS / benefits owner |
| RELATION | Relationship code with different value sets in DDM and registration | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L91); [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L152) | HYPOTHESIS / benefits owner |
| AMT-FAMILY-INCOME | Declared family income used in calculation and eligibility | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L78); [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L92) | CONFIRMED |
| MAX-PERCAP-INCOME | DDM's per-person ceiling, compared with family income in VALELEG | [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L56); [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L174) | HYPOTHESIS / program owner |
| IND-DOCS-OK | S/N documentation indicator read by eligibility; writer not established in supplied validation flow | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L83); [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L96) | HYPOTHESIS / registration owner |
| COD-ELIGIBILITY | Five-character eligibility code; helper tests first `R` and second `D` positions | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L249) | HYPOTHESIS / program owner |
| COD-REGION | Region code whose DDM and calculation-table interpretations differ | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L66); [LDASIFAP.NSL](legacy-sifap/natural-programs/LDASIFAP.NSL#L34) | HYPOTHESIS / benefits owner |
| Region 99 | Value causing early eligibility success, with authorization still unknown | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L123) | HYPOTHESIS / benefits and control owners |
| AMT-BASE-INDIVIDUAL | Program's individual base amount | [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L41) | CONFIRMED |
| FACTOR-K | Stored field and separately computed local factor are not automatically the same business parameter | [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L47); [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L124) | HYPOTHESIS / program owner |
| FACTOR-ADJUST | Factor used in program registration and again in benefit calculation | [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L124); [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L262) | HYPOTHESIS / calculation owner |
| AMT-GROSS | Stored gross amount; definition of included December components is in the calculation body | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L43); [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L275) | CONFIRMED |
| AMT-DISC-TOTAL | Stored total deductions, distinct from repeated itemized deduction amounts | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L45) | CONFIRMED |
| AMT-NET | Calculated gross minus deductions, floored at zero in calculation | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L299) | CONFIRMED |
| AMT-BONUS | Stored bonus; December type-A path adds 15% of benefit | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L284) | CONFIRMED |
| Thirteenth payment | December component whose comment and executed formula disagree | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L271) | HYPOTHESIS / benefits owner |
| IPCA-YEAR | Hardcoded monthly index matrix; supplied assignments cover 2010-2012 | [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L86) | CONFIRMED |
| IND-CORR | S/N field used to skip already corrected payments | [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L186) | CONFIRMED |

## Payment and audit operations

| Term | Source-bound meaning / use | Evidence | Status / proposed reviewer |
|---|---|---|---|
| YEAR-MONTH-REF | Six-digit reference period YYYYMM | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L38) | CONFIRMED |
| NUM-BATCH / SEQ-BATCH | Remittance batch identifier and within-batch sequence | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L89) | CONFIRMED |
| SUPER-CPF-PERIOD | Composite CPF plus period descriptor used by generation's existence check | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L127); [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L294) | CONFIRMED |
| STAT-PAYMENT | Payment status code; labels conflict between DDM, bank writer and reports | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L60); [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L204) | HYPOTHESIS / payments owner |
| TYPE-PAYMENT | Payment type code; N/D/T program usage differs from N/R/A/C DDM remarks | [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L170); [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L79) | HYPOTHESIS / payments owner |
| CNAB 240 | Name used for the bank-return fixed-length record read by BATCHCON; full external contract not supplied | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L131) | HYPOTHESIS / bank integration owner |
| COD-BANK-RETURN | Two-character bank response used by reconciliation DECIDE | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L204) | CONFIRMED |
| COD-ACTION | Audit action whose CO/CN interpretation differs between writers and report | [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L39); [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L163) | HYPOTHESIS / audit owner |
| COD-PROFILE | Declared actor profile, not populated by the common audit copycode | [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L76); [CCAUDIT.NSC](legacy-sifap/natural-programs/CCAUDIT.NSC#L50) | CONFIRMED |
| ID-CORRELATION | Declared composite-operation identifier; no producer established in this corpus | [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L93) | CONFIRMED |
| CMSYNIN | In-stream Natural command input in the JCLs | [SIFAPJ01.jcl](legacy-sifap/natural-programs/SIFAPJ01.jcl#L65) | CONFIRMED |
| CMWKF01 / CMWKF02 | Job-bound work-file DD names; roles vary by job/program | [SIFAPJ01.jcl](legacy-sifap/natural-programs/SIFAPJ01.jcl#L53) | CONFIRMED |
| CMPRT01 | Logical printer/DD name used by the report programs | [SIFAPJ02.jcl](legacy-sifap/natural-programs/SIFAPJ02.jcl#L56) | CONFIRMED |
| RC | Return code used by Natural TERMINATE and JCL step conditions; zero-output and error are not interchangeable | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L558) | CONFIRMED |

## Natural and Adabas mechanisms

| Term | Source-bound meaning / use | Evidence | Status |
|---|---|---|---|
| PDA | Positional parameter data area imported by caller/callee | [PDACALC.NSA](legacy-sifap/natural-programs/PDACALC.NSA#L18) | CONFIRMED |
| LDA | Local declarations and initial values imported into a member | [LDASIFAP.NSL](legacy-sifap/natural-programs/LDASIFAP.NSL#L14) | CONFIRMED |
| DDM | Logical Natural view with long field names and access descriptors | [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L150) | CONFIRMED |
| FDT | Physical field definition table identified by short field names | [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L8) | CONFIRMED |
| DBID / FNR | Database and file numbers in the view binding | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L32) | CONFIRMED |
| ISN | Adabas internal record number; listed capacity/reuse values are historical, not a stable external business key | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L149); [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L115) | CONFIRMED |
| MU | Multiple-value field, such as additional phone numbers | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L101) | CONFIRMED |
| PE | Periodic group whose child fields repeat together, such as dependents | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L87) | CONFIRMED |
| NU | Physical null-suppression option; empty values may be absent from the index | [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L148) | CONFIRMED |
| UQ | Physical unique-descriptor option, distinct from format U | [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L97) | CONFIRMED |
| HYPEREXIT 03 | Named custom derived-descriptor mechanism without supplied implementation | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L152) | CONFIRMED |
| CALLNAT | External Natural subprogram invocation with positional parameters | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L369) | CONFIRMED |
| INCLUDE | Compilation-time copycode insertion, not an external runtime call | [SUBVALCP.NSN](legacy-sifap/natural-programs/SUBVALCP.NSN#L94) | CONFIRMED |
| PERFORM | Invocation of an internal or included subroutine | [SUBVALCP.NSN](legacy-sifap/natural-programs/SUBVALCP.NSN#L72) | CONFIRMED |
| AT BREAK / AT END OF DATA | Control-break and data-end reporting hooks | [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L128) | CONFIRMED |
| HISTOGRAM | Descriptor-value occurrence counts, used separately from detailed filtering | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L260) | CONFIRMED |
| END TRANSACTION | Explicit commit point in the source | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L320) | CONFIRMED |
| BACKOUT TRANSACTION | Backout of the current transaction; not reversal of earlier commits | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L578) | CONFIRMED |
| CENTURY-WINDOW | Pivot initialized to 50 for expanding historical two-digit years; consumers differ | [LDASIFAP.NSL](legacy-sifap/natural-programs/LDASIFAP.NSL#L88) | CONFIRMED |

## Review checklist

- [x] More than 30 terms are recorded with source references.
- [x] Literal definitions are distinguished from disputed business meanings.
- [ ] Human reviewers validate the hypothesis entries before choosing modern domain names.

Related: [Data map](data-map.md), [rule candidates](business-rules-catalog.md),
[open questions](mysteries-found.md), [discovery report](discovery-report.md).
