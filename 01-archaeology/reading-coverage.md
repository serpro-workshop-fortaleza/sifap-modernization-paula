# Reading coverage - complete supplied corpus

> **Trail:** [Team kit](../README.md) > [Stage 1](README.md) > **Reading coverage**

**An auditable ledger of source reading, not a claim of runtime or human acceptance coverage.**

| Field | Value |
|---|---|
| Date / branch / acceptance | 2026-09-10 / develop / acceptance reported by the requesting user |
| Requested scope | Every supplied library member and Adabas artifact |
| Library read | 24/24: 12 NSP, 5 NSN, 2 NSC, 2 NSA, 1 NSL, 2 JCL |
| Adabas read | 5/5: 4 DDMs and 1 physical FDT listing |
| Static control points | 219 IF, including IF NO RECORDS FOUND; 15 DECIDE; 8 report hooks |
| Source dependency points | 9 CALLNAT, 9 INCLUDE, 23 USING; 3 JCL program invocations separately |
| DDM inventory | 199 value-bearing declarations including MU, 7 groups, 14 derived descriptors |

Comments were read for provenance but excluded from executable-control counts.
No legacy file was edited. The requesting user reported completion of the
human acceptance on 2026-09-10; the agent did not independently collect each
pair's signature or witness its reading. The [H1 record](discovery-report.md)
releases the isolated CPF/NIS scope, not all unresolved business interpretations.

## Program catalogue and reading ledger

The intervals include every line from the file header to final END. Author and
last-change date are copied from source headers, not inferred from README tables,
Git modification time or names mentioned in historical narrative. The purpose
column is a reading hypothesis grounded in the body, not business approval.

| Member / full read interval | DEFINE DATA interval | Header author / last change | Body-grounded purpose hypothesis | Catalogue entries |
|---|---|---|---|---|
| [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L1), 1-596 | 27-156 | Carlos Roberto da Silva / 2016-03-18 | Filter beneficiaries, invoke validators/calculation, calculate locally, store and export payments | BP-01..20 |
| [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L1), 1-280 | 22-78 | Patricia Gomes de Souza / 2014-06-05 | Aggregate period payments by region/status and print/archive totals | BL-01..07 |
| [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L1), 1-347 | 20-103 | Marcos Antonio Ribeiro / 2017-05-11 | Compare bank-return records with payments, update status and audit | BC-01..08 |
| [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L1), 1-430 | 13-104 | Carlos Roberto da Silva / 2012-09-12 | Insert/update beneficiary fields with mixed blocking and warning validation | CA-01..10 |
| [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L1), 1-247 | 12-82 | Ana Lucia Pereira / 2012-09-12 | Append dependent occurrences to a holder record | DP-01..08 |
| [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L1), 1-188 | 12-72 | Marcos Antonio Ribeiro / 2012-11-18 | Add/query program parameters and compute adjusted base | PR-01..05 |
| [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L1), 1-378 | 16-93 | Carlos Roberto da Silva / 2016-06-14 | Compute amounts, store a payment and return values to the caller | CB-01..09 |
| [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L1), 1-255 | 12-82 | Patricia Gomes de Souza / 2016-06-14 | Apply the selected local index to payment gross and record positive corrections | CR-01..06 |
| [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L1), 1-217 | 12-57 | Roberto Mendes Junior / 2016-06-14 | Recalculate a payment's deduction total from contribution and PE items | DS-01..07 |
| [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L1), 1-333 | 15-71 | Marcia Helena Oliveira / 2011-08-18 | Return CPF/date/name/UF/status validation results | VB-01..07 |
| [VALDOCS.NSP](legacy-sifap/natural-programs/VALDOCS.NSP#L1), 1-243 | 14-52 | Ana Lucia Pereira / 2011-08-18 | Validate input CPF/RG/NIS with a special-prefix result-reset path | VD-01..06 |
| [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L1), 1-269 | 15-66 | Jose Ferreira dos Santos / 2013-04-05 | Check stored beneficiary/program eligibility and return a first reason | VE-01..10 |
| [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L1), 1-316 | 18-104 | Marcia Helena Oliveira / 2018-05-30 | Query beneficiary/history and write an access audit | CQ-01..07 |
| [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L1), 1-273 | 17-72 | Ana Lucia Pereira / 2018-05-30 | Print period payment details, program-change subtotals and totals | RP-01..06 |
| [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L1), 1-305 | 18-66 | Roberto Mendes Junior / 2018-05-30 | Filter audit details and optionally print date occurrence counts | RA-01..08 |
| [SUBVALCP.NSN](legacy-sifap/natural-programs/SUBVALCP.NSN#L1), 1-96 | 28-42 | Marcia Helena Oliveira / 2011-06-07 | Validate CPF through the shared copycode and return PDA codes | SC-01..03 |
| [SUBVALNI.NSN](legacy-sifap/natural-programs/SUBVALNI.NSN#L1), 1-152 | 38-50 | Roberto Mendes Junior / 2015-09-30 | Validate NIS digits and return PDA codes | SN-01..03 |

The [business-rule catalogue](business-rules-catalog.md) describes conditions and
actions by block. The [declaration dictionary](program-data-dictionary.md) lists
all local/parameter fields, imported areas and declared view subsets.

## Supporting members

| Member / full read interval | Header author / last change | Recorded content | Location |
|---|---|---|---|
| [CCAUDIT.NSC](legacy-sifap/natural-programs/CCAUDIT.NSC#L1), 1-100 | Adilson Batista / 2015-07-10 | Required fields, seed branch, timestamp, batch branch and STORE without commit | AU-01..03; declaration dictionary |
| [CCVALCPF.NSC](legacy-sifap/natural-programs/CCVALCPF.NSC#L1), 1-130 | Carlos Roberto da Silva / 2011-06-07 | Required fields, mask/equal-digit checks, both check digits | CV-01..02; declaration dictionary |
| [PDACALC.NSA](legacy-sifap/natural-programs/PDACALC.NSA#L1), 1-79 | Carlos Roberto da Silva / 2015-09-30 | All 16 positional fields and declared return contract | Catalogue shared declarations; dictionary |
| [PDAVALID.NSA](legacy-sifap/natural-programs/PDAVALID.NSA#L1), 1-57 | Marcia Helena Oliveira / 2011-06-07 | All 6 positional fields and declared return contract | Catalogue shared declarations; dictionary |
| [LDASIFAP.NSL](legacy-sifap/natural-programs/LDASIFAP.NSL#L1), 1-107 | Carlos Roberto da Silva / 2015-09-30 | All 24 fields, arrays, initial values and century pivot | Catalogue shared declarations; dictionary |
| [SIFAPJ01.jcl](legacy-sifap/natural-programs/SIFAPJ01.jcl#L1), 1-101 | Carlos Roberto da Silva / 2015-07-10 | DDs, input period, copy/notice conditions and scheduler/restart comments | J1-01..03; dependency map |
| [SIFAPJ02.jcl](legacy-sifap/natural-programs/SIFAPJ02.jcl#L1), 1-108 | Patricia Gomes de Souza / 2013-02-14 | Both program steps, DDs, periods/filter and scheduler/restart comments | J2-01..03; dependency map |

Data areas have no executable IF/DECIDE bodies. Copycode conditions are counted
once in their own source, not multiplied by the number of includers. JCL
conditions are recorded separately, not counted as Natural IF statements.

## Control-block intervals

Numbers are physical lines in the linked member. Nested IF intervals are listed
individually; `IF NO RECORDS FOUND` ends at `END-NOREC`. The catalogue may group
nested guards into one candidate, so candidate counts must not be equated with
control-point counts. ELSE/NONE actions and commented alternatives were read.

| Member | IF intervals | DECIDE intervals | Report hooks / error handler |
|---|---|---|---|
| [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L171) | 171-173; 256-259; 263-266; 279-288; 295-298; 303-313; 319-321; 322-325; 339-347; 341-345; 376-379; 390-394; 397-409; 400-408; 403-407; 415-427; 418-426; 421-425; 442-454; 448-453; 458-462; 466-468; 513-516; 558-561; 562-565; 587-590 | None | ON ERROR 572-582 |
| [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L145) | 145-147; 172-176; 179-185; 189-191; 193-235; 290-293 | 204-232 | ON ERROR 299-308 |
| [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L119) | 119-122; 136-138; 147-163; 150-162; 153-161; 156-160; 203-206 | 177-190 | AT BREAK 128-130; AT END 132-134; ON ERROR 258-266 |
| [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L139) | 139-143; 145-149; 164-168; 170-174; 176-180; 182-186; 199-201; 207-209; 213-217; 219-223; 245-247; 250-252; 254-256; 266-268; 337-339; 385-389; 391-394; 404-408; 410-412 | 271-331; 350-374 | ON ERROR 423-428 |
| [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L97) | 97-99; 105-108; 110-113; 117-120; 147-150; 152-156; 158-160; 169-171; 177-182; 186-188; 216-218 | None | ON ERROR 240-245 |
| [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L84) | 84-87; 89-92; 112-114; 118-121; 168-170 | None | ON ERROR 181-186 |
| [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L158) | 158-162; 167-171; 180-185; 189-193; 200-204; 207-219; 210-218; 213-217; 240-252; 243-251; 246-250; 275-293; 284-292; 300-302; 349-352; 361-365 | None | ON ERROR 370-376 |
| [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L151) | 151-154; 163-167; 175-177; 179-181; 182-184; 186-188; 204-219; 234-237 | None | ON ERROR 247-253 |
| [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L80) | 80-84; 87-90; 96-99; 117-120; 121-123; 130-135; 140-145; 158-163; 170-174; 171-173; 199-203 | 127-167 | ON ERROR 209-215 |
| [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L85) | 85-89; 101-105; 114-118; 123-128; 133-151; 134-150; 139-149; 144-148; 156-162; 157-161; 163-169; 164-168; 174-180; 175-179; 188-195; 189-194; 196-200; 203-207; 210-214; 224-226; 231-237; 251-258; 253-257; 259-266; 261-265 | 185-219 | ON ERROR 240-246 |
| [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L127) | 127-131; 137-141; 147-151; 156-169; 159-162; 164-168; 174-179; 232-235; 237-245; 239-242; 255-259; 260-263; 273-277; 278-280; 302-305; 306-309; 310-312; 318-321; 325-327; 328-330 | 202-226 | ON ERROR 186-193 |
| [VALDOCS.NSP](legacy-sifap/natural-programs/VALDOCS.NSP#L79) | 79-83; 89-93; 112-116; 123-125; 139-142; 179-183; 184-187; 196-200; 201-203; 209-212; 215-219; 220-222; 233-239 | 145-169 | ON ERROR 128-134 |
| [SUBVALCP.NSN](legacy-sifap/natural-programs/SUBVALCP.NSN#L50) | 50-54; 56-60; 62-66; 74-78 | None | ON ERROR 85-91 |
| [SUBVALNI.NSN](legacy-sifap/natural-programs/SUBVALNI.NSN#L58) | 58-62; 64-68; 70-74; 82-86; 144-148 | 108-131 | ON ERROR 93-99 |
| [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L119) | 119-121; 123-125; 132-144; 139-142; 150-153; 158-161; 272-274; 276-278; 286-288; 299-310 | 147-166; 228-241 | ON ERROR 188-193 |
| [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L131) | 131-133; 135-138; 142-148; 155-157; 198-200; 226-228 | 170-179; 182-195 | AT TOP 115-120; AT START 126-129; AT END 225-230; ON ERROR 237-243 |
| [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L99) | 99-101; 103-105; 106-108; 118-120; 121-123; 130-133; 136-141; 137-140; 144-149; 145-148; 152-157; 153-156; 190-192; 195-210; 216-220; 226-229; 256-266; 281-301 | 163-182 | AT START 114-116; AT BREAK 215-222; AT END 225-230; ON ERROR 271-276 |
| [CCVALCPF.NSC](legacy-sifap/natural-programs/CCVALCPF.NSC#L45) | 45-48; 82-85; 87-90; 101-105; 106-109; 121-125; 126-128 | 52-76 | Uses caller error handler |
| [CCAUDIT.NSC](legacy-sifap/natural-programs/CCAUDIT.NSC#L65) | 65-70; 93-96 | None | Uses caller error handler |

The complete bodies, not only these markers, were read: initialization, loops,
assignments, calls, numeric intermediates, READ/FIND blocks, work output and
transaction order are included in the catalogue/dictionary/dependency map.

## Adabas and document coverage

| Artifact | Read coverage | Recorded result |
|---|---|---|
| [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L1) | Full, 1-179 | 69 fields, 2 groups, 5 derived; types, remarks, identities and historical notes |
| [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L1) | Full, 1-165 | 57 fields, 1 PE, 4 derived; status/type and deduction-code comparisons |
| [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L1) | Full, 1-126 | 41 fields, 2 PE, 1 derived; factors, eligibility and unused parameter surfaces |
| [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L1) | Full, 1-147 | 32 fields, 2 groups, 4 derived; MU arrays, action meanings and partition note |
| [FDT-150-BENEFICIARY.txt](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L1) | Full, 1-156 | Physical names/options, derived definitions, PE/MU bounds and missing JA/JB comparison |
| [BUSINESS-RULES-2012.md](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L1) | Full Markdown reading | RN-001..023 compared, including incompleteness/approval disclaimers |
| [TECHNICAL-MANUAL-SIFAP-2008.md](legacy-sifap/legacy-docs/TECHNICAL-MANUAL-SIFAP-2008.md#L230) | Targeted sections 3.2-3.5, 230-388; headings searched | Registration, calculation and batch comparison; not full-document review |
| [ORIGINAL-ARCHITECTURE-1997.md](legacy-sifap/legacy-docs/ORIGINAL-ARCHITECTURE-1997.md#L310) | Targeted sections 5-6, 310-389; headings searched | Proposed integration/audit versus source; not current architecture approval |

DOCX counterparts were not converted or checked for equivalence. Technical
source coverage is 29/29; that denominator does not include every README,
historical document format or a live system. The original metadata-only kickoff
is retained in [inventory.md](inventory.md) as a separate earlier activity.

## Open-question navigation

Local Q numbers below refer to `BONUS-Qnn` in the [question register](mysteries-found.md),
not canonical IDs. The mapping is for review navigation only.

| Reading group | Local questions requiring review |
|---|---|
| Registration and shared CPF | Q01-Q07, Q31-Q32, Q36-Q37 |
| Eligibility and dates | Q08-Q12, Q30-Q32, Q34 |
| Calculation, discounts and corrections | Q07-Q08, Q13-Q21, Q33, Q35, Q41 |
| Batch and bank interface | Q13-Q15, Q22-Q24, Q33-Q35, Q39 |
| Queries and reports | Q24-Q29, Q33-Q35, Q38 |
| Data/physical definitions | Q04-Q07, Q11-Q12, Q18, Q34-Q38, Q40-Q41 |

## Reproducing static checks

The closure uses the existing [evidence validator](scripts/validate-evidence.mjs)
and its [tests](scripts/validate-evidence.test.mjs). Run from the repository root:

```bash
node --test --experimental-test-coverage --test-coverage-include='**/validate-evidence.mjs' --test-coverage-lines=80 --test-coverage-branches=70 --test-reporter=spec --test-reporter=tap --test-reporter-destination=stdout --test-reporter-destination=01-archaeology/validation/validator-tests.tap 01-archaeology/scripts/validate-evidence.test.mjs
node 01-archaeology/scripts/validate-evidence.mjs --write-report
npx markdownlint-cli2 01-archaeology/{inventory,business-rules-catalog,dependency-map,data-map,program-data-dictionary,reading-coverage,mysteries-found,glossary,discovery-report,LEGACY-EXPLORATION-CHECKLIST}.md
```

The generated [evidence report](validation/evidence.json) contains execution
time, baseline commit, static totals, SHA-256 for all 29 technical sources,
fingerprints for all ten documents (including the closure checklist), and the
validator/test-source fingerprints. `source_commit` identifies the repository
baseline; it does not assert that closure edits have been committed. The hashes
capture the working-tree snapshot, which becomes stale after a later edit until
regenerated. No commit or push is performed by these commands.

The closure suite passed **17/17 tests**, including six H1-specific checks;
validator coverage was **94.84% of lines and 98.43% of branches**, above the
configured 80%/70% gates. The [TAP execution record](validation/validator-tests.tap)
retains that result. The validator also enforces exactly one disposition per
question, role ownership, reopening gates and preservation of the original
unresolved statuses. Markdown lint (CLI 0.23.2) passed for all ten documents.

These checks do not hash the evidence report itself or certify human acceptance,
Natural runtime equivalence, physical precision, every prose interpretation or
historical DOCX equivalence. Test coverage here measures the documentary validator,
not coverage of the SIFAP business logic.

The following optional searches reproduce the initial inventory of markers.
They exclude Natural comment lines and count source text, not executed branches.

```bash
rg -n '^\s*IF\b' 01-archaeology/legacy-sifap/natural-programs -g '*.NSP' -g '*.NSN' -g '*.NSC'
rg -n '^\s*DECIDE\b' 01-archaeology/legacy-sifap/natural-programs -g '*.NSP' -g '*.NSN' -g '*.NSC'
rg -n '^\s*AT (BREAK|END OF DATA|START OF DATA|TOP OF PAGE)' 01-archaeology/legacy-sifap/natural-programs -g '*.NSP'
rg -n '^\s*(CALLNAT|INCLUDE|LOCAL USING|PARAMETER USING|FETCH)\b' 01-archaeology/legacy-sifap/natural-programs
rg -n '^\s*(M\s+)?[12]\s+[A-Z][A-Z0-9]\s+\S+\s+[ANP]\s+' 01-archaeology/legacy-sifap/adabas-ddms -g '*.ddm'
```

## H1 closure and later gates

- [x] Every supplied technical artifact has a complete reading record.
- [x] Source conditions and declarations are traced to the written artifacts.
- [x] DDM/code and historical-document differences remain explicit.
- [x] Record the requesting user's report of team reading/review and H1 acceptance, without invented individual signatures.
- [x] Select isolated CPF/NIS validation and assign all 41 question dispositions and reopening gates.
- [x] Release the source-linked selected scope to Stage 2; broader domains remain excluded.
- [ ] Pair 1 reconciles canonical IDs with the facilitator before a canonical completion score is claimed.
- [ ] Compile/run or document unavailable runtime evidence before claiming behavioral equivalence at implementation acceptance.
