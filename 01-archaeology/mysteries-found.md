# Open questions - Stage 1

> **Trail:** [Team kit](../README.md) > [Stage 1](README.md) > **Open questions**

**Source questions preserved with approved H1 dispositions, owners and reopening gates.**

Reading and H1 closure date: 2026-09-10. The requesting user authorized the
remaining decisions and reported acceptance of everything in the Copilot
conversation. The [H1 dispositions](#h1-dispositions) record how every question
is handled for the isolated CPF/NIS scope; they do not confirm the hypotheses.
The original question status and proposed domain reviewers below are retained
as the reading snapshot. Accountability is assigned to repository roles, not
invented individuals; the requesting user is the escalation contact until the
team identifies the person occupying a role.

## Canonical-ID boundary

The [canonical checklist](mysteries-checklist.md) provides four-ID ranges per
pair, but does not enumerate the individual question-to-ID mapping. The local
`BONUS-Qnn` keys below therefore do not claim a canonical assignment, replace
the denominator of 20, or report any mystery as solved. The facilitator/team
must validate the mapping to `SIFAP-M-01` through `SIFAP-M-20` explicitly.

H1 accepts the source-linked local register for the selected feature. Pair 1
(Requirements Engineer) owns canonical reconciliation with the facilitator
before reporting a canonical score. No canonical completion claim is made,
and no prerequisite or score is silently marked complete by this disposition.

## Question register

| Local key | Open question | Evidence (path and physical line) | Impact | Unconfirmed hypothesis | Proposed validation owner | Status |
|---|---|---|---|---|---|---|
| BONUS-Q01 | Which CPF implementation governs conflicting check-digit and all-zero results? | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L152), 152-168, 344-413; [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L237), 237-245; [SUBVALCP.NSN](legacy-sifap/natural-programs/SUBVALCP.NSN#L56), 56-78 | Registration/query acceptance may diverge | Unconfirmed: legacy copies may preserve different exception policies | Registration owner + QA | Awaiting human validation |
| BONUS-Q02 | What authorizes suspension above 75, and which status should updates at 75 or below preserve? | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L241), 241-252, 306-318 | Existing eligibility/status could change | Unconfirmed: a historical review policy may be incomplete in the update path | Benefits owner | Awaiting human validation |
| BONUS-Q03 | Which address length is intended across input, storage and display? | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L58), 58; [assignment](legacy-sifap/natural-programs/CADBENEF.NSP#L276), 276-281; [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L58), 58-62 | Loss or inconsistent display of address text | Unconfirmed: the screen may have retained a wider legacy field | Registration owner + DBA | Awaiting human validation |
| BONUS-Q04 | Is the dependent limit three, five, six, or the ten declared slots? | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L117), 117-120, 191-194; [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L87); [2012 RN-004](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L78), 78-82 | Different accepted family sizes | Unconfirmed: a business limit may differ from storage capacity and boundary implementation | Benefits owner + DBA | Awaiting human validation |
| BONUS-Q05 | Which relationship-code vocabulary is valid? | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L152), 152-156; [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L91), 91-92 | Incorrect interpretation of existing dependents | Unconfirmed: code and DDM may represent different revisions | Benefits owner | Awaiting human validation |
| BONUS-Q06 | Which dependent attributes should be persisted and initialized, including document, sex, status and disability? | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L122), 122-129, 191-203; [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L87), 87-94 | Captured data and active counts may disagree | Unconfirmed: some screen fields or state initialization may belong to a missing process | Registration owner + DBA | Awaiting human validation |
| BONUS-Q07 | What is the provenance of .347215 and the relation between local K, DDM FACTOR-K and later adjustment? | [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L124), 124-139; [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L262); [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L47), 47-52 | Monetary equivalence and parameter ownership | Unconfirmed: the identifiers may describe different historical factors | Program/benefits owner | Awaiting human validation |
| BONUS-Q08 | Which reference date and century convention should eligibility and payment reprocessing use? | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L339), 339-348; [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L68), 68-97; [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L225), 225-252 | Age-based decisions differ by execution path | Unconfirmed: historical YY dates and current-year recalculation may require explicit separate rules | Benefits owner + QA | Awaiting human validation |
| BONUS-Q09 | What calendar checks are intended for non-leap February and future dates within the current year? | [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L104); [date helper](legacy-sifap/natural-programs/VALBENEF.NSN#L302), 302-313 | Birth-date acceptance | Unconfirmed: the fixed month table may not express the intended calendar policy | Registration owner + QA | Awaiting human validation |
| BONUS-Q10 | What authorizes the region-99 early-success path and which checks may it bypass? | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L114), 114-128; [2012 section 4.2](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L199), 199-205 | Eligibility and control exceptions | Unconfirmed: a special business case or historical test path may exist | Benefits owner + control owner | Awaiting human validation |
| BONUS-Q11 | Is the income ceiling per household or per person? | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L174), 174-180; [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L56); [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L78), 78-80 | Eligibility thresholds | Unconfirmed: source may use a different income measure from the field label | Program owner | Awaiting human validation |
| BONUS-Q12 | What is the complete eligibility-code grammar and how should its NIS lookup obtain a valid record context? | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L224), 224-267; [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L65) | Optional eligibility checks and runtime compatibility | Unconfirmed: only part of the intended grammar may be implemented | Program owner + Natural specialist | Awaiting human validation |
| BONUS-Q13 | Which component owns payment calculation, identifiers and storage when callee and caller both write? | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L309), 309-328; [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L381), 381-489; [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L34) | Duplicate writes, zero/unassigned identifiers and return-code handling | Unconfirmed: conversion to a subprogram may have left persistence and local calculation active | Payments owner + DBA | Awaiting human validation |
| BONUS-Q14 | How are committed payments reconciled with work-file failure and same-period restart? | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L488), 488-502, 572-582; [SIFAPJ01.jcl](legacy-sifap/natural-programs/SIFAPJ01.jcl#L24), 24-33 | Missing/duplicated bank transmission on restart | Unconfirmed: operational recovery may rely on an external reconciliation step | Operations + payments owner | Awaiting human validation |
| BONUS-Q15 | What factor applies above the final income ceiling when no branch assigns one? | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L585), 585-592; [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L347), 347-354 | High-income calculation and state dependence | Unconfirmed: an upstream domain bound or explicit fallback may be missing | Benefits owner + QA | Awaiting human validation |
| BONUS-Q16 | Should the thirteenth payment use age factor, active-month proportion or another rule? | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L271), 271-293; [2012 section 2.1](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L129), 129-136 | December monetary equivalence | Unconfirmed: the formula comment may be historical rather than current | Benefits owner | Awaiting human validation |
| BONUS-Q17 | Should a later non-court deduction cap earlier court amounts, and should net be recomputed after deduction updates? | [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L127), 127-188; [2012 RN-021/023](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L156), 156-174 | Order-sensitive deductions and inconsistent stored totals | Unconfirmed: the intended exemption/priority may not match a running-total cap | Payments/legal owner + QA | Awaiting human validation |
| BONUS-Q18 | How do three-character DDM deduction codes map to one-character local processing? | [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L125), 125-167; [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L51); [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L78) | Misclassified or ignored deduction types | Unconfirmed: a mapping layer or legacy encoding may be absent | Payments owner + DBA | Awaiting human validation |
| BONUS-Q19 | Should correction accumulate multiple months, and what indices cover years outside 2010-2012? | [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L86), 86-128, 229-239; [2008 section 3.3.2](legacy-sifap/legacy-docs/TECHNICAL-MANUAL-SIFAP-2008.md#L309), 309-322 | Incorrect correction scope or missing indices | Unconfirmed: a historical table/update process may be incomplete | Calculation owner | Awaiting human validation |
| BONUS-Q20 | Does CPF ordering justify ending correction at the first period above the requested end? | [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L174), 174-188; [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L35), 35-38, 127-128 | Eligible records may depend on within-CPF order | Unconfirmed: chronological order may have been assumed without the composite descriptor | DBA + QA | Awaiting human validation |
| BONUS-Q21 | What commits the final correction audit and keeps it consistent with the already committed payment? | [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L204), 204-226; [CCAUDIT.NSC](legacy-sifap/natural-programs/CCAUDIT.NSC#L57), 57-58, 98 | Audit durability and transaction consistency | Unconfirmed: a caller/session commit may have been assumed | DBA + audit owner | Awaiting human validation |
| BONUS-Q22 | Why is parsed bank identity not used in the successful reconciliation update? | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L140), 140-147, 204-212; [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L72) | Bank attribution and alpha formatting | Unconfirmed: only one bank may have been supported operationally | Bank integration owner | Awaiting human validation |
| BONUS-Q23 | Should unknown return codes count as reconciled and allow a successful job return? | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L201), 201-235, 290-294 | Unhandled bank outcomes can be hidden by counters | Unconfirmed: unknown codes may need a separate exception category | Bank integration owner + operations | Awaiting human validation |
| BONUS-Q24 | Which audit action meanings and query-recording policy govern CO, CN and DV across writers and reports? | [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L168), 168-179; [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L311), 311-343; [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L163), 163-182; [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L39), 39-49, 134-140 | Audit interpretation and completeness | Unconfirmed: multiple generations of action codes may coexist | Audit/control owner | Awaiting human validation |
| BONUS-Q25 | What makes consultation history the latest twelve payments rather than the first twelve in CPF order? | [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L264), 264-288; [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L35), 35-38, 127-128 | Misleading history ordering | Unconfirmed: within-CPF chronological order may have been assumed | Query owner + DBA | Awaiting human validation |
| BONUS-Q26 | Which CPF mask should apply consistently to leading-zero identifiers, screens and reports? | [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L298), 298-311; [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L163), 163-167 | Inconsistent personal-data disclosure | Unconfirmed: differing historical display policies may need one approved rule | Privacy/audit owner | Awaiting human validation |
| BONUS-Q27 | Are program subtotals complete when records are read in period order? | [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L123), 123-149; [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L129), 129-130 | Split or misleading totals | Unconfirmed: the report may assume contiguous program groups not guaranteed by the selected descriptor | Reporting owner + DBA | Awaiting human validation |
| BONUS-Q28 | Who authorizes unconditional exclusion of deletion events, including explicit EX searches? | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L130), 130-141; [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L138), 138-140 | Audit report completeness | Unconfirmed: a historical control policy or workaround may exist | Audit/control owner | Awaiting human validation |
| BONUS-Q29 | Should the date histogram use all events or the filtered report population? | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L136), 136-157, 256-266 | Totals from different populations may be compared incorrectly | Unconfirmed: histogram and detail may intentionally answer different questions | Reporting/audit owner | Awaiting human validation |
| BONUS-Q30 | Which special prefixes may erase prior CPF/RG errors, and why does NIS validation still follow? | [VALDOCS.NSP](legacy-sifap/natural-programs/VALDOCS.NSP#L58), 58-65, 98-116, 228-241 | Validation exemptions | Unconfirmed: exemptions may be document-specific rather than universal | Document/benefits owner | Awaiting human validation |
| BONUS-Q31 | What validates CTPS/voter ID and persists IND-DOCS-OK for eligibility? | [VALDOCS.NSP](legacy-sifap/natural-programs/VALDOCS.NSP#L67), 67-125; [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L83); [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L196) | Validation result may not reach stored eligibility input | Unconfirmed: a manual or external approval flow may exist | Registration/document owner | Awaiting human validation |
| BONUS-Q32 | Does fixed-width padding satisfy the first/last-name test for a single-word name? | [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L18); [helper](legacy-sifap/natural-programs/VALBENEF.NSN#L316), 316-331 | Name validation and user acceptance | Unconfirmed: the original check may rely on string semantics not yet characterized | Registration owner + QA | Awaiting human validation |
| BONUS-Q33 | Which rounding/truncation semantics govern calculation versus region, status and grand totals? | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L264), 264-266; [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L165), 165-198; [2012 RN-014](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L127) | Financial reconciliation | Unconfirmed: integer and packed assignments may change the effect of the rounding expression | Finance owner + Natural specialist | Awaiting human validation |
| BONUS-Q34 | Which region vocabulary governs calculations and where should unknown/missing/special regions appear in reports? | [LDASIFAP.NSL](legacy-sifap/natural-programs/LDASIFAP.NSL#L34), 34-46; [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L141), 141-163; [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L84), 84-91 | Wrong regional factors or classification | Unconfirmed: state-index and macroregion schemes may have been conflated | Benefits/reporting owner | Awaiting human validation |
| BONUS-Q35 | Which payment status and type vocabularies apply to stored data and displayed labels? | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L204), 204-227; [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L170), 170-195; [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L60), 60-80 | Incorrect lifecycle or payment-category translation | Unconfirmed: historical data revisions may require explicit mappings | Payments owner + DBA | Awaiting human validation |
| BONUS-Q36 | Which extract is authoritative for legal-representative fields present in DDM but absent in the supplied FDT? | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L139), 139-140; [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L81), 81-95 | Schema coverage and extraction fidelity | Unconfirmed: one listing may omit later physical changes | DBA | Awaiting human validation |
| BONUS-Q37 | Which processes populate the remaining control, biometric, death/block, correlation and audit-profile fields? | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L103), 103-140; [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L74), 74-94; [CCAUDIT.NSC](legacy-sifap/natural-programs/CCAUDIT.NSC#L82), 82-98 | Unmapped data ownership and missing controls | Unconfirmed: the supplied corpus may exclude external writers or operational procedures | DBA + control/integration owners | Awaiting human validation |
| BONUS-Q38 | Do the documented historical audit partitions exist and belong in requested reports? | [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L142), 142-145; [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L111), 111-123 | Historical audit completeness | Unconfirmed: FNR 153 alone may represent only part of the intended history | DBA + audit owner | Awaiting human validation |
| BONUS-Q39 | What sends job-failure notifications, parameterizes the period and reconciles RC 4/8 with the documented successor condition? | [SIFAPJ01.jcl](legacy-sifap/natural-programs/SIFAPJ01.jcl#L13), 13-33, 69-93; [SIFAPJ02.jcl](legacy-sifap/natural-programs/SIFAPJ02.jcl#L13), 13-21 | Scheduling and operational recovery | Unconfirmed: scheduler or operations tooling outside the supplied JCL may supply these functions | Operations owner | Awaiting human validation |
| BONUS-Q40 | What implements hyperexit 03 and the phonetic/derived-key semantics needed outside the supplied source? | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L144), 144-153; [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L89), 89-95 | Derived-query equivalence | Unconfirmed: database-level extensions may require a separately supplied implementation | Adabas DBA | Awaiting human validation |
| BONUS-Q41 | How should DDM decimal lengths, Natural formats and physical packed-byte lengths be reconciled? | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L78), 78-80; [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L44), 44-46; [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L60), 60-68 | Precision, range and overflow behavior | Unconfirmed: notation conventions or reconstructed listings may differ | Natural specialist + DBA | Awaiting human validation |

## H1 dispositions

Decision authority: the requesting user's authorization and acceptance reported
on 2026-09-10; scope and provenance are recorded in the
[discovery report](discovery-report.md). `Scoped decision` settles only which
source behavior is selected for the first feature. `Deferred` accepts postponement
because the affected behavior is excluded, not because its risk is resolved.
One scoped decision and 40 deferrals cover all 41 local questions exactly once.

Owners use the existing [team roles](../00-TEAM-FLOW.md): Pair 1 owns business
interpretation, Pair 3 technical translation, Pair 4 data/quality, and Pair 5
operational controls. Pair 2 receives this record for architecture. The accountable
role gathers the domain review identified above before any expansion of scope.

| Question | H1 disposition | Approved action for the first feature | Accountable role | Reopen gate |
|---|---|---|---|---|
| BONUS-Q01 | Scoped decision | Use SUBVALCP with CCVALCPF and SUBVALNI via PDAVALID only. Preserve their error precedence; do not replace or unify CADBENEF, VALBENEF or VALDOCS. Historic authority remains open outside this boundary. | Pair 1 / Requirements Engineer | Before integrating a caller, review differing outcomes with the business owner and require source-linked tests. |
| BONUS-Q02 | Deferred | Exclude beneficiary status changes and age-based suspension. | Pair 1 / Product Owner | Before registration updates, approve a status-transition table and age boundary examples. |
| BONUS-Q03 | Deferred | Exclude address capture, storage and display. | Pair 4 / DBA | Before address migration, approve length/overflow handling with registration and sample data. |
| BONUS-Q04 | Deferred | Exclude dependent registration and counts; do not choose a new limit. | Pair 1 / Product Owner | Before dependent scope, approve the business maximum separately from storage capacity. |
| BONUS-Q05 | Deferred | Do not translate relationship codes. | Pair 1 / Requirements Engineer | Before dependent scope, approve a code-mapping table against domain and stored-data evidence. |
| BONUS-Q06 | Deferred | Exclude dependent attributes and active-state initialization. | Pair 4 / DBA | Before dependent writes, identify mandatory attributes, defaults and the responsible producer. |
| BONUS-Q07 | Deferred | Exclude all K factors and monetary adjustment. | Pair 1 / Product Owner | Before calculation scope, obtain factor provenance and approved numerical examples. |
| BONUS-Q08 | Deferred | Exclude age, birth-date and period computations. | Pair 1 / Requirements Engineer | Before eligibility/reprocessing, approve the reference date and century policy. |
| BONUS-Q09 | Deferred | Exclude calendar validation from the document-number feature. | Pair 4 / QA Engineer | Before date validation, approve leap-year and future-date cases with the domain owner. |
| BONUS-Q10 | Deferred | Do not introduce a region-99 bypass into CPF/NIS validation. | Pair 1 / Product Owner | Before eligibility scope, require explicit exception authority and affected-check boundaries. |
| BONUS-Q11 | Deferred | Exclude income and eligibility thresholds. | Pair 1 / Requirements Engineer | Before eligibility scope, confirm the income unit and household divisor with examples. |
| BONUS-Q12 | Deferred | Validate NIS digits only; exclude eligibility-code interpretation and database lookups. | Pair 1 / Requirements Engineer | Before eligibility integration, approve the grammar and obtain valid record-context behavior. |
| BONUS-Q13 | Deferred | No payment calculation, identifier allocation or persistence in the first feature. | Pair 3 / Technical Lead | Before payment design, settle write ownership and test duplicate/concurrent creation paths. |
| BONUS-Q14 | Deferred | No remittance generation or batch restart in the first feature. | Pair 5 / DevOps Engineer | Before batch implementation, approve a restart/reconciliation procedure with failure injection evidence. |
| BONUS-Q15 | Deferred | No income-band calculation or invented fallback factor. | Pair 1 / Product Owner | Before calculation scope, approve the no-matching-band result and boundary examples. |
| BONUS-Q16 | Deferred | Exclude December/thirteenth-payment calculation. | Pair 1 / Product Owner | Before December scope, approve the formula, proration basis and numerical examples. |
| BONUS-Q17 | Deferred | No deductions, court exemptions, cap ordering or net updates. | Pair 1 / Product Owner | Before deduction scope, obtain finance/legal approval and order-sensitive examples. |
| BONUS-Q18 | Deferred | No deduction-code translation. | Pair 4 / DBA | Before deduction scope, reconcile every stored code with an approved mapping. |
| BONUS-Q19 | Deferred | No index tables or retroactive monetary correction. | Pair 1 / Product Owner | Before correction scope, identify the index authority, covered periods and accumulation rule. |
| BONUS-Q20 | Deferred | No payment scans or dependence on within-CPF ordering. | Pair 4 / DBA | Before correction queries, demonstrate descriptor order and inclusive interval behavior. |
| BONUS-Q21 | Deferred | No correction persistence or legacy audit transaction. | Pair 4 / DBA | Before correction writes, verify atomicity and final-audit durability with failure cases. |
| BONUS-Q22 | Deferred | No bank identity assignment or bank-return parsing. | Pair 5 / DevOps Engineer | Before bank integration, obtain the actual bank/layout contract and approved code mapping. |
| BONUS-Q23 | Deferred | No reconciliation status or job-return mapping. | Pair 5 / DevOps Engineer | Before reconciliation scope, approve unknown-return handling and operational escalation. |
| BONUS-Q24 | Deferred | No reuse or normalization of CO/CN/DV actions; no legacy audit writes. | Pair 1 / Requirements Engineer | Before audit integration, approve the versioned vocabulary and query-recording policy. |
| BONUS-Q25 | Deferred | No beneficiary/payment history query. | Pair 4 / DBA | Before consultation scope, define deterministic latest-first order and ties. |
| BONUS-Q26 | Deferred | No legacy screen/report masks are adopted. The first feature must not log raw CPF/NIS or echo them in diagnostics. | Pair 5 / DevOps Engineer | Before identifier display or logging changes, obtain the privacy policy and disclosure tests. |
| BONUS-Q27 | Deferred | No program subtotal reporting. | Pair 4 / QA Engineer | Before report scope, verify complete grouping across noncontiguous records. |
| BONUS-Q28 | Deferred | No audit report or deletion-event filter. | Pair 1 / Product Owner | Before audit-report scope, obtain control-owner approval of included events. |
| BONUS-Q29 | Deferred | No histogram or filtered-report totals. | Pair 4 / QA Engineer | Before reporting scope, approve populations and reconciliation expectations. |
| BONUS-Q30 | Deferred | No VALDOCS prefix exemptions or clearing of prior errors. Preserve only the selected helpers' behavior. | Pair 1 / Product Owner | Before special-document support, require an approved exception list and error precedence. |
| BONUS-Q31 | Deferred | Exclude CTPS, voter ID and stored documentation approval; valid digits do not establish registration or eligibility. | Pair 1 / Requirements Engineer | Before document-approval scope, identify validators, producer and persistence responsibility. |
| BONUS-Q32 | Deferred | Exclude personal-name validation and string-padding policy for names. | Pair 4 / QA Engineer | Before name validation, approve trimmed/padded and single-word examples. |
| BONUS-Q33 | Deferred | Use the selected integer check-digit logic only; no money or rounding is involved. | Pair 4 / QA Engineer | Before monetary scope, obtain runtime numeric characterization and finance-approved totals. |
| BONUS-Q34 | Deferred | No regional classification, lookup or factor table. | Pair 1 / Requirements Engineer | Before regional scope, reconcile macroregion/state codes and missing/special values. |
| BONUS-Q35 | Deferred | No payment lifecycle or payment-type translation. | Pair 1 / Requirements Engineer | Before payments, approve code meanings, transitions and historical mappings. |
| BONUS-Q36 | Deferred | No database migration or choice between the DDM and FDT extract. | Pair 4 / DBA | Before data extraction, obtain authoritative physical definitions including JA/JB. |
| BONUS-Q37 | Deferred | No new writes to control, biometric, death/block, correlation or profile fields. | Pair 4 / DBA | Before dependent integration, document each field's producer and ownership. |
| BONUS-Q38 | Deferred | No audit partition query or historical completeness claim. | Pair 4 / DBA | Before audit-history scope, inventory authorized partition definitions and retention coverage. |
| BONUS-Q39 | Deferred | No scheduler, job parameterization, alerts or production operations. | Pair 5 / DevOps Engineer | Before batch deployment, verify live scheduling, notifications and RC handling in an authorized environment. |
| BONUS-Q40 | Deferred | No phonetic/hyperdescriptor emulation; the selected helpers do not access DDMs. | Pair 4 / DBA | Before derived searches, obtain implementation and fixtures for hyperexit 03 and phonetic rules. |
| BONUS-Q41 | Deferred | No packed-decimal or physical-byte translation. Keep document identifiers as text and check-digit calculations as bounded integers. | Pair 4 / DBA | Before Adabas/numeric migration, validate actual precision, scale, byte layout and overflow behavior. |

## H1 release rule

All 41 questions have an accepted disposition; zero is marked resolved as a
historical business question. None blocks specification of the isolated
CPF/NIS feature under the selected contract. This is not permission to implement
the deferred behavior: its reopening gate becomes blocking before that behavior
enters a specification or implementation. Pair 1 approves a changed scope and
Pair 2 records the architectural impact before the disposition is revised.

The selected behavior still needs source-linked examples and tests during
specification/implementation. In particular, document length/normalization,
error precedence, leading zeros, wrong check digits, repeated digits, repeated
calls and the difference between invalid input and execution error must be made
explicit. No runtime equivalence has been certified at H1.

## Validation record requirements

- [x] Record all 41 dispositions, accountable roles and reopening gates.
- [x] Record the requesting user's acceptance date and provenance separately from source observations.
- [x] Keep unanswered hypotheses out of approved factual claims and implementation assumptions.
- [ ] Pair 1 reconciles canonical IDs with the facilitator before claiming a canonical score.
- [ ] Role holders add their names and decisions when reopening a deferred item; no signature is fabricated here.

Related: [Rule candidates](business-rules-catalog.md), [data map](data-map.md),
[dependency map](dependency-map.md), [discovery report](discovery-report.md).
