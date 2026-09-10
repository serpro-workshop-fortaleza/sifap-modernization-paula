# Business rule candidates - SIFAP legacy

> **Trail:** [Team kit](../README.md) > [Stage 1](README.md) > **Business rule candidates**

**A source-reading record for team review, not an approved specification.**

| Field | Value |
|---|---|
| Team | [To be filled by the team] |
| Date | 2026-09-10 |
| Scope | All 24 library files and all 4 DDMs plus the FDT listing |
| Progress | All 24 library files and all 5 Adabas artifacts read; human validation pending |
| Method | Read declarations and executable bodies; distinguish code, comments, documentation and human decisions |

> [!IMPORTANT]
> `Inferred` means the behavior is observed in source, but its intended business
> meaning is not approved. `Mystery` means a question remains open. Documentation
> corroboration does not close a mystery or substitute for human validation.
> EARS entries below are pattern candidates only: no formal EARS requirements,
> REQ-IDs, acceptance criteria or Stage 2 approval are created here.
> Evidence uses physical source line numbers. Each linked starting line is
> followed by the full reviewed interval. Sources remain unchanged.

Complete declaration inventory: [program-data-dictionary.md](program-data-dictionary.md).
Per-file and per-block coverage: [reading-coverage.md](reading-coverage.md).
Questions and proposed human owners: [mysteries-found.md](mysteries-found.md).

## BATCHPGT.NSP

Read from declaration through final `END`. Declarations are at
[BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L27), lines 27-156.
The input is `#PERIOD (N6)`; output records are `#REC-EXTRACT (A240)` and
`#LOG-ERR (A120)`. Views are `BENEFIC`, `PAYMENT`, `SOCPROG` and `AUDIT`.
Amounts use packed decimals except the `#AMT-TEMP (N11)` intermediate;
factor tables use `N3.4`. Imported areas are `PDAVALID`, `PDACALC`, `LDASIFAP`.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| BP-01 | When the entered period is zero, use the current year/month; otherwise split the supplied period into year and month. No month-range check occurs here. | Event-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L158), 158-176 | Inferred |
| BP-02 | Read beneficiaries in CPF order. Skip repeated adjacent CPFs and any status other than `A`; the previous CPF is assigned before the status check. | State-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L249), 249-266 | Inferred; not proof of database uniqueness |
| BP-03 | Call `SUBVALCP`; a nonzero return writes a rejection, increments error/reject counters and skips the beneficiary. | Unwanted behavior | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L273), 273-288 | Inferred |
| BP-04 | If any payment matches the CPF-period superdescriptor, skip generation, without filtering existing payment status. | Unwanted behavior | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L292), 292-298 | Inferred |
| BP-05 | Missing program data creates a rejection and marker `X`; that marker skips the record. A program status other than `A` increments ignored and skips. | Unwanted behavior | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L301), 301-325 | Inferred |
| BP-06 | A birth year below 100 is expanded using `#L-CENTURY-WINDOW`: below the window adds 2000, otherwise 1900. Age is period year minus birth year, not birthday-aware. | State-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L328), 328-348 | Inferred; imported constant requires cross-check |
| BP-07 | A nonzero `VALELEG` return skips the record. `CALCBENF` is then called, but following calculations use local amount variables; its return code is not checked here. | Event-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L356), 356-435 | Mystery <!-- mystery: Which calculation path is intended to control generated amounts? --> |
| BP-08 | Regions 1-25 select the local factor table; all other values select 1.0000, although the table has 27 entries. | State-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L192), 192-219; [branch](legacy-sifap/natural-programs/BATCHPGT.NSP#L390), 390-394 | Inferred |
| BP-09 | Family factor is 1 for zero dependents; through 2 it is `1 + count * .05`; through 4, `1.10 + (count-2)*.03`; otherwise `1.16 + (count-4)*.02`. | State-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L397), 397-409 | Inferred |
| BP-10 | The first income ceiling matched selects factors 1/.85/.70/.55/.40 at 300/600/1000/1500/9999.99. The helper has no assignment when every ceiling is exceeded. | State-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L222), 222-231; [helper](legacy-sifap/natural-programs/BATCHPGT.NSP#L585), 585-592 | Mystery <!-- mystery: What factor is intended when no income band matches? --> |
| BP-11 | Age factors are 1.15 from 65; 1.10 from 60; 1.05 below 18; otherwise 1. | State-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L415), 415-427 | Inferred |
| BP-12 | Multiply base, region, family, income and age factors, then `1 + adjustment`; pass amounts through the integer intermediate at the shown steps. | Ubiquitous | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L430), 430-439 | Inferred; exact numeric assignment behavior needs runtime characterization |
| BP-13 | In December, set type `D`, add the product of base, region factor and age factor; for program type `A`, also add a 15% bonus of the calculated benefit. Other months retain type `N` and zero bonus. | Event-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L437), 437-454 | Inferred |
| BP-14 | Deduct 3% only when gross is strictly above 500. No `CALCDSCT` call appears in this body. | State-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L457), 457-462 | Inferred; a header reference is not a call edge |
| BP-15 | Net is gross minus deductions; negative net is replaced with zero before the integer-intermediate step. | Unwanted behavior | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L465), 465-470 | Inferred |
| BP-16 | Increment the maximum existing payment number and batch sequence; store status `G` and commit each payment before writing the 240-character bank work record. | Event-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L240), 240-242; [storage](legacy-sifap/natural-programs/BATCHPGT.NSP#L472), 472-502 | Mystery <!-- mystery: How are committed payments reconciled with a failed subsequent work-file write? --> |
| BP-17 | Every 1000 generated records, write progress including the last CPF. Rejection and error paths also print CPF values. | Event-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L509), 509-516; [rejection](legacy-sifap/natural-programs/BATCHPGT.NSP#L279), 279-288 | Inferred; sensitive-output review needed, no values reproduced here |
| BP-18 | After the loop, request a `BT` audit for `PGTO` and commit, then close both work files. | Event-driven | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L539), 539-549 | Inferred; audit body supplied by `CCAUDIT` |
| BP-19 | Return 8 if no payment was generated; otherwise return 4 if any rejection occurred, else 0. The zero-generated check precedes the rejection check. | Unwanted behavior | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L558), 558-566 | Inferred; RC 8 alone does not prove prior successful processing |
| BP-20 | On a Natural error, log context, back out the current transaction, close work files and return 12. Earlier committed payments are outside that current transaction. | Unwanted behavior | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L572), 572-582 | Inferred; runtime behavior not executed |

## VALELEG.NSN

Declarations: [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L15),
15-66. The 16-field `PDACALC` area is the interface; `BENEFIC` and `SOCPROG`
are read. The local reasons array is `A60/1:10`; only its first reason is returned.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| VE-01 | Missing beneficiary returns 2001; missing program returns 2003; inactive program returns 2004, all with early return. | Unwanted behavior | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L84), 84-118 | Inferred |
| VE-02 | Beneficiary lookup overwrites supplied age, income, dependents, region and status. Age uses the current calendar year, unlike the period-based batch calculation. | Event-driven | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L68), 68-97 | Mystery <!-- mystery: Which reference date and century convention should eligibility use during reprocessing? --> |
| VE-03 | Region 99 returns success after the program-status check but before beneficiary-status, age, income and documentation checks. | State-driven | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L114), 114-128 | Mystery <!-- mystery: What authorizes the region-99 early-success path, and for which checks? --> |
| VE-04 | Status `S`, `C`/`D`, or `I` adds a rejection reason. The outer non-`A` branch has no final rejection for an unrecognized status. | Unwanted behavior | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L133), 133-151 | Inferred; unknown status needs a boundary example |
| VE-05 | Positive minimum/maximum ages activate strict below/above rejection; zero disables that respective bound. | State-driven | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L156), 156-169 | Inferred |
| VE-06 | A positive `MAX-PERCAP-INCOME` is compared directly with family income; exceeding it adds a rejection reason. No per-person division occurs here. | State-driven | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L174), 174-180 | Mystery <!-- mystery: Is the configured ceiling per family or per person? --> |
| VE-07 | Type `A` rejects income above 600 with no dependent, and independently rejects documentation other than `S`; `P` rejects age below 60; `T` rejects ages outside 16-65; other types reject. | State-driven | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L185), 185-219 | Inferred |
| VE-08 | A nonblank eligibility code invokes a helper: first character `R` requires nonzero NIS; second character `D` requires at least one dependent. It does not call document validation. | Optional | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L224), 224-226; [helper](legacy-sifap/natural-programs/VALELEG.NSN#L249), 249-267 | Mystery <!-- mystery: What is the supported eligibility-code grammar, and is the view-field reference outside FIND valid in the intended runtime? --> |
| VE-09 | Eligible returns 0 and blank message; otherwise returns 2010 and the first accumulated reason, not the full reason list. | Event-driven | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L231), 231-237 | Inferred |
| VE-10 | Natural errors set 9999 with error/line/program context and return to the caller. | Unwanted behavior | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L240), 240-246 | Inferred |

## CALCBENF.NSN

Declarations: [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L16),
16-93. `PDACALC` supplies the interface; local CPF is numeric `N11`, converted
back to `A11` for lookup. Factors are `N3.4`, money `P9.2`, intermediate `N11`.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| CB-01 | Reset returned amounts/code/message; invalid month returns 2020. Missing beneficiary/program returns 2001/2003, and beneficiary status other than `A` returns 2002. | Unwanted behavior | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L148), 148-197 | Inferred; the program's status field is declared but not checked here |
| CB-02 | The stored beneficiary supplies program, birth date, dependents, region and income, rather than relying on all supplied context fields. | Event-driven | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L165), 165-197 | Inferred |
| CB-03 | Regions 1-25 use the local table; other values use 1. Family-factor branches match BP-09, including an uncapped final dependent-count branch. | State-driven | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L99), 99-125; [branches](legacy-sifap/natural-programs/CALCBENF.NSN#L200), 200-219 | Inferred |
| CB-04 | Select the first income ceiling 300/600/1000/1500/9999.99 with factors 1/.85/.70/.55/.40. No-match has no explicit fallback assignment. | State-driven | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L128), 128-137; [helper](legacy-sifap/natural-programs/CALCBENF.NSN#L347), 347-354 | Mystery <!-- mystery: Which result is intended above the final income ceiling? --> |
| CB-05 | Age is period year minus the stored birth year; factors are 1.15 from 65, 1.10 from 60, 1.05 below 18, else 1. The century-window example immediately above is commented out. | State-driven | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L225), 225-252 | Inferred; do not treat commented IF statements as executed |
| CB-06 | Multiply base by region/family/income/age and `1 + adjustment`, then use the `N11` intermediate. In December add the product of base, region factor and age factor, plus 15% of benefit for type `A`; other types set bonus to zero. | Event-driven | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L258), 258-293 | Mystery <!-- mystery: The thirteenth-payment comment mentions active months, but the executable formula uses age factor; which intent is valid? --> |
| CB-07 | Internal `CALC-DISC` deducts 3% only above 500, not the full standalone deduction algorithm. Net is floored at zero. | State-driven | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L296), 296-306; [helper](legacy-sifap/natural-programs/CALCBENF.NSN#L358), 358-366 | Inferred; `PERFORM CALC-DISC` is not `CALLNAT CALCDSCT` |
| CB-08 | Store and commit a `PAYMENT` record before returning calculated values. The shown assignment block does not assign `NUM-PAYMENT`, although it exists in the view. | Event-driven | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L309), 309-328 | Mystery <!-- mystery: How are identifiers, duplicate writes and transaction ownership handled when BATCHPGT also stores a payment? --> |
| CB-09 | On Natural error, print error context, back out the current transaction and terminate 12 rather than returning a PDA error. | Unwanted behavior | [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L370), 370-376 | Inferred; compare with VE-10 before assuming a common error contract |

## CALCDSCT.NSP

Declarations: [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L12),
12-57. This is an interactive program, not a `PDACALC` callee. The payment
view includes `GRP-DISC (1:8)`; a three-character type is moved into local `A1`.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| DS-01 | Input CPF and payment number; accept a found payment only if its CPF matches. Missing/mismatching payment or absent beneficiary ends the routine. | Unwanted behavior | [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L71), 71-99 | Inferred |
| DS-02 | Initial contribution uses the first gross ceiling 500/1000/2000/9999.99 with rates .03/.05/.07/.09. No matching ceiling contributes nothing through this helper. | State-driven | [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L61), 61-69; [helper](legacy-sifap/natural-programs/CALCDSCT.NSP#L197), 197-205 | Inferred |
| DS-03 | Traverse existing deduction occurrences. Skip if a nonzero end date is before today or start date is after today; endpoints are inclusive. | State-driven | [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L113), 113-125 | Inferred; uses today, not payment period |
| DS-04 | Types `J`, `P`, `A` use a positive fixed amount, otherwise gross * percentage / 100. Type `I` always uses percentage; `S` uses 1%; `NONE` adds nothing. | State-driven | [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L127), 127-167 | Inferred; all DECIDE branches retained |
| DS-05 | After each non-`J` occurrence, cap the accumulated total at 30% of gross if it exceeds that amount. `J` bypasses this check only for its own iteration. | State-driven | [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L106), 106-110; [cap](legacy-sifap/natural-programs/CALCDSCT.NSP#L169), 169-174 | Mystery <!-- mystery: Should later non-court deductions cap earlier court amounts, making the result order-dependent? --> |
| DS-06 | Convert total through the integer intermediate, update only `AMT-DISC-TOTAL`, and commit. This block does not recompute net or write audit. | Event-driven | [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L179), 179-194 | Inferred; reconciliation of totals needs review |
| DS-07 | Natural error prints context, backs out the current transaction and terminates 12. | Unwanted behavior | [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L209), 209-215 | Inferred |

## CALCCORR.NSP

Declarations: [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L12),
12-82. Inputs are CPF `N11` and start/end periods `N6`; the index table has
10 year slots by 12 months (`N3.6`), with an accumulator `N5.6`.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| CR-01 | Reject start period greater than end; validate CPF through `SUBVALCP` and stop on a nonzero return. No separate month-range validation occurs. | Unwanted behavior | [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L145), 145-168 | Inferred |
| CR-02 | Read by CPF, stop when CPF changes, skip periods below start, stop above end and skip already corrected (`S`) records. | State-driven | [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L174), 174-188 | Mystery <!-- mystery: Does ordering by CPF justify stopping at the first period above the requested end? --> |
| CR-03 | Load indices for 2010-2012. For each payment, start at factor 1 and apply the index for that payment's year/month once; there is no loop advancing through the requested end period. | Event-driven | [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L86), 86-128; [helper](legacy-sifap/natural-programs/CALCCORR.NSP#L229), 229-239 | Mystery <!-- mystery: Is a single-month factor intended, and what covers years absent from the table? --> |
| CR-04 | Only a positive corrected-minus-original amount triggers update of correction amount/date/indicator; gross and net are not changed. Nonpositive differences leave the record unmarked. | State-driven | [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L190), 190-219 | Inferred |
| CR-05 | Commit payment changes before calling `WRITE-AUDIT`; no explicit commit follows that audit call in the same loop iteration or after the loop. | Event-driven | [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L204), 204-226 | Mystery <!-- mystery: What commits the final audit record and guarantees atomicity with the correction? --> |
| CR-06 | Historical currency-adjustment IF blocks are comments only. Natural error backs out the current transaction and terminates 12. | Unwanted behavior | [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L130), 130-143; [error](legacy-sifap/natural-programs/CALCCORR.NSP#L247), 247-253 | Inferred; commented formulas are not active rules |

## BATCHCON.NSP

Declarations: [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L20),
20-103. Input is a 240-character work record; document number is read as `A10`
and converted to `N15`. Returned cents use `N15`, amounts/difference `P9.2`.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| BC-01 | Input period/file label; read work file 1 and process only record type `3`. Extract CPF at 44/11, amount at 120/15, date at 140/8, return at 231/2 and document at 74/10; convert amount from cents. | Event-driven | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L120), 120-166 | Inferred; the file label is printed, not used to bind the work file |
| BC-02 | Find by payment number, then require both CPF and period equality; otherwise count not-found, log and skip. | Unwanted behavior | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L169), 169-185 | Inferred |
| BC-03 | Make the amount difference absolute. Values strictly greater than .01 are discrepancies and receive a divergence audit; differences up to .01 follow the reconciled path. | State-driven | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L188), 188-203 | Inferred |
| BC-04 | Return `00` sets status `P`, credit date, bank literal 1 and bank return; `01` sets `D`; `02` sets `E`. Each recognized branch updates and commits. | Event-driven | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L204), 204-227 | Mystery <!-- mystery: Why is parsed bank identity ignored in favor of a fixed bank value? --> |
| BC-05 | An unknown bank code only logs, after the reconciled counter was incremented; reconciliation audit still follows. | Unwanted behavior | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L201), 201-235 | Mystery <!-- mystery: Should unknown return codes count as reconciled and allow RC 0? --> |
| BC-06 | Reconciliation audit stores action `CO`; divergence audit stores `DV` and before/after amounts. Both use direct view assignments and commit independently of payment updates. | Event-driven | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L311), 311-343 | Mystery <!-- mystery: How do direct audit records align with CCAUDIT fields and the meaning of action CO? --> |
| BC-07 | A final `BT` audit inherits the direct-audit sequence, then commits. Return 4 only if discrepancies or not-found records exist, otherwise 0. | Event-driven | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L275), 275-294 | Inferred |
| BC-08 | Natural error logs context, backs out the current transaction, closes work file 1 and terminates 12. The Banco Real alternative is commented out. | Unwanted behavior | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L239), 239-257; [error](legacy-sifap/natural-programs/BATCHCON.NSP#L299), 299-308 | Inferred; no active second-bank path established |

## BATCHREL.NSP

Declarations: [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L22),
22-78. Region/status arrays have five slots; gross totals use `P13.2` and
`P15.2`, the rounding intermediate uses `N15`, archival rows `A132`.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| BL-01 | Zero period terminates 12. Read by period starting at the requested value and stop when it changes. | Unwanted behavior | [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L118), 118-138 | Inferred |
| BL-02 | `AT BREAK OF` period and `AT END OF DATA` emit running-count messages; they are reporting hooks, not additional selection predicates. | Event-driven | [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L128), 128-134 | Inferred |
| BL-03 | Resolve beneficiary region, defaulting to zero before lookup. Codes 1-5/6-10/11-15/16-20 map to groups 1/2/3/4; every other value maps to group 5. | State-driven | [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L141), 141-163 | Mystery <!-- mystery: Should absent beneficiaries and region 99 be included in Central-West totals? --> |
| BL-04 | Region/grand gross totals use an intermediate assigned `gross + .005`, then integer conversion; status totals use stored gross directly. Deductions/net are summed directly. | Ubiquitous | [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L165), 165-198 | Mystery <!-- mystery: What totals reconcile after the two-decimal intermediate assignment, and what rounding is intended? --> |
| BL-05 | Status `G/P/C/D/E` maps to the five report groups; `NONE` maps to generated. | State-driven | [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L177), 177-192 | Inferred; unknown values are not a separate group |
| BL-06 | No selected payment returns 4. Otherwise print region/status/grand summaries, write `REG`, `STS`, `TOT` work records, close the file and return 0. | Event-driven | [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L203), 203-253 | Inferred; header prints once through the explicit helper call |
| BL-07 | Natural error logs, backs out the current transaction, closes the output file and returns 12. The program contains no database mutation. | Unwanted behavior | [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L258), 258-280 | Inferred |

## CADBENEF.NSP

Declarations: [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L13),
13-104. The screen accepts numeric CPF/program/region, then formats alpha keys.
Address is local `A80` but view street is `A60`; validation messages are `A60/1:10`.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| CA-01 | Accept only operations `I` and `A`; reject zero CPF, blank name, zero birth date and sex other than `M/F`. Failures set an error and leave the outer loop; the message is printed afterward. | Unwanted behavior | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L139), 139-186; [exit](legacy-sifap/natural-programs/CADBENEF.NSP#L337), 337-339 | Inferred; no delete operation appears in the executable DECIDE |
| CA-02 | Run internal CPF validation and `SUBVALCP`, but gate saving on internal `#CPF-VALID`, not the corporate return code. | Unwanted behavior | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L152), 152-168 | Mystery <!-- mystery: Which CPF implementation is authoritative when their results differ? --> |
| CA-03 | Nonzero `SUBVALNI` return produces a warning without setting the save-blocking flag. | Unwanted behavior | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L193), 193-201 | Inferred |
| CA-04 | Look up formatted CPF; adding an existing beneficiary or updating an absent one sets error and exits. | Unwanted behavior | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L205), 205-223 | Inferred |
| CA-05 | Calculate age by subtracting birth year from current year. For insertion initialize status `A`; for age strictly greater than 75 assign `S`. The century-window text is commented out. | State-driven | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L225), 225-256 | Mystery <!-- mystery: What validates automatic suspension and the status written on updates at age 75 or below? --> |
| CA-06 | Call `VALBENEF`; result `I` only writes a warning. It does not block storage. | Unwanted behavior | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L263), 263-268 | Inferred |
| CA-07 | Insert identity, contact, program, income, dependent count, dates, region and NIS; copy the wider local address into the street field; add an `IN` audit and commit together. | Event-driven | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L271), 271-304 | Mystery <!-- mystery: What address information may be lost at the A80-to-A60 boundary? --> |
| CA-08 | Update name, street/city/UF/CEP, phone, RG, status, income, dependent count and update date. Birth date, sex, program, region and NIS supplied on screen are not assigned in this update branch. Add `AL` audit and commit. | Event-driven | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L305), 305-331 | Inferred; DECIDE default prints invalid operation |
| CA-09 | Internal CPF routine maps characters `0`-`9`, rejects `NONE`, calculates two check digits with weighted sums and an arithmetic remainder expression; mismatches set invalid. There is no equal-digit rejection in this body. | Unwanted behavior | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L344), 344-413 | Mystery <!-- mystery: Are the arithmetic remainder and numeric-to-alpha MOVE equivalent to the shared validator on boundary inputs? --> |
| CA-10 | Natural error prints context, backs out the current transaction and terminates 12. | Unwanted behavior | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L423), 423-428 | Inferred |

## CADDEPEN.NSP

Declarations: [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L12),
12-82. The beneficiary view has ten dependent occurrences, while the addition
guard uses a different limit. The screen also accepts document and sex fields.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| DP-01 | Missing holder stops; holder status `C` or `D` stops additions. Other statuses are not blocked by this guard. | Unwanted behavior | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L95), 95-113 | Inferred |
| DP-02 | Before each addition, stop when current count is greater than 5; increment later before choosing the target occurrence. A current count of 5 passes that guard. | State-driven | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L117), 117-120; [increment](legacy-sifap/natural-programs/CADDEPEN.NSP#L191), 191-194 | Mystery <!-- mystery: Is the intended business limit five, six, or the declared ten occurrences? --> |
| DP-03 | Blank name or relationship outside `FI/CO/IR/OU` sets error and repeats input. No executable validation of birth date or sex appears here. | Unwanted behavior | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L145), 145-160 | Inferred |
| DP-04 | Shared CPF failure assigns a message only; it neither sets `#ERR` nor prints that message at this point. | Unwanted behavior | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L167), 167-171 | Inferred; comment says warning mode, executable effect is recorded separately |
| DP-05 | A matching nonzero dependent CPF among the stored count sets error and repeats input; zero CPF bypasses this duplicate predicate. | Unwanted behavior | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L174), 174-188 | Inferred |
| DP-06 | Write name, birth date, relationship, CPF and count; no assignments to dependent document/sex/status/disability occur in the active store block. Add `AL` audit and commit. | Event-driven | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L191), 191-213 | Mystery <!-- mystery: Which captured or declared dependent attributes are expected to persist and initialize? --> |
| DP-07 | Continue only when the response is exactly `S`; any other value exits. | Event-driven | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L215), 215-225 | Inferred |
| DP-08 | Include `CCVALCPF` and `CCAUDIT`; on error back out current transaction and terminate 12. | Unwanted behavior | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L230), 230-247 | Inferred |

## CADPROG.NSP

Declarations: [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L12),
12-72. Numeric `N4` program input is formatted as `A4`; local base/maximum
income are `P9.2`, stored view fields `P7.2`; factor K is `N5.6`.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| PR-01 | Accept `I` or `C`; reject other operations. `C` calls the query helper and exits before the addition input. | Event-driven | [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L79), 79-92 | Inferred |
| PR-02 | Insertion looks up formatted program code and rejects an existing record; the no-record block clears the found flag. | Unwanted behavior | [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L110), 110-121 | Inferred |
| PR-03 | Compute K as `1 + adjustment * .347215`, store base multiplied by K, retain the adjustment factor and assign status `A`. No further type/date/age/income guards appear before storing. | Ubiquitous | [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L124), 124-139 | Mystery <!-- mystery: What is the provenance of .347215 and its relationship to the later calculation adjustment? --> |
| PR-04 | Add `IN` audit for the program with blank affected CPF and commit it with registration. Query displays fields or prints not-found from `*NUMBER`. | Event-driven | [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L140), 140-171 | Inferred |
| PR-05 | Natural error backs out the current transaction and terminates 12. | Unwanted behavior | [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L181), 181-186 | Inferred |

## CCVALCPF.NSC

The caller declares the eleven required work fields; the commented field list is
at [CCVALCPF.NSC](legacy-sifap/natural-programs/CCVALCPF.NSC#L19), 19-30.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| CV-01 | Reject a CPF failing the eleven-digit mask or the digit DECIDE default; reject all-equal digits after the comparison loop. | Unwanted behavior | [CCVALCPF.NSC](legacy-sifap/natural-programs/CCVALCPF.NSC#L39), 39-90 | Inferred; all digit values and NONE were read |
| CV-02 | Compute first/second digits using weights 10..2 and 11..2 with `DIVIDE ... REMAINDER`; remainder below 2 maps to zero, otherwise 11 minus remainder. Either mismatch invalidates. | Unwanted behavior | [CCVALCPF.NSC](legacy-sifap/natural-programs/CCVALCPF.NSC#L92), 92-130 | Inferred; no DDM access or transaction |

## VALBENEF.NSN

Declarations: [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L15),
15-71. Ten explicit parameters include a ten-message output array. A `BENEFIC`
view is declared but never accessed; CEP is accepted but not validated in the body.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| VB-01 | Initialize result `V` and error count zero; each failed CPF/date/name helper adds its message and sets result `I`. | Unwanted behavior | [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L116), 116-151 | Inferred |
| VB-02 | Validate UF against the 27-entry table only when nonblank. Accept status only in `A/S/C/I/D`; otherwise append an error. | Unwanted behavior | [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L156), 156-179 | Inferred; blank UF is permitted by this guard |
| VB-03 | CPF digit DECIDE accepts `0`-`9` and rejects `NONE`. Equal digits reject except the nested zero-prefix branch, which returns success for the all-zero case before check-digit calculation. | Unwanted behavior | [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L196), 196-245 | Mystery <!-- mystery: Is the all-zero exception still authorized, given SUBVALCP rejects zero as missing? --> |
| VB-04 | Two weighted sums use arithmetic remainder expressions; remainder below 2 yields zero, otherwise 11 minus remainder; either check-digit mismatch invalidates. | Unwanted behavior | [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L247), 247-281 | Inferred; compare numeric semantics with CCVALCPF using characterization |
| VB-05 | Reject year outside 1900..current year, month outside 1..12 and day outside the fixed month table. February is always 29; there is no leap-year or full future-date comparison. | Unwanted behavior | [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L102), 102-114; [date helper](legacy-sifap/natural-programs/VALBENEF.NSN#L284), 284-313 | Mystery <!-- mystery: Which date validity rules are intended for non-leap February and future dates within the current year? --> |
| VB-06 | Reject blank name; otherwise consider it valid when the first space has position greater than 1. The fixed-width field is not trimmed before this test. | Unwanted behavior | [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L316), 316-331 | Mystery <!-- mystery: Does padding allow a single-word name to satisfy the first/last-name test? --> |
| VB-07 | On Natural error append error context, set result `I` and return through parameters; no database write occurs. | Unwanted behavior | [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L186), 186-193 | Inferred |

## VALDOCS.NSP

Declarations: [VALDOCS.NSP](legacy-sifap/natural-programs/VALDOCS.NSP#L14),
14-52. Numeric CPF/NIS inputs are `N11`; RG/CTPS `A15`, voter ID `A12`,
messages `A60/1:5`, special prefixes `A3/1:8`. The declared view is not accessed.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| VD-01 | CPF and RG failures append errors and mark invalid; then run the special-document helper before NIS validation. | Unwanted behavior | [VALDOCS.NSP](legacy-sifap/natural-programs/VALDOCS.NSP#L78), 78-98 | Inferred |
| VD-02 | Internal CPF rejects zero, invalid digit characters and either mismatching check digit. Remainder below 2 maps to zero; the alternative maps to 11 minus remainder. | Unwanted behavior | [VALDOCS.NSP](legacy-sifap/natural-programs/VALDOCS.NSP#L137), 137-204 | Inferred; no equal-digit exclusion in this helper |
| VD-03 | Reject blank RG; length is the position before the first space, or 15 if no space exists; reject length below 5. No issuing-state/check-digit validation appears. | Unwanted behavior | [VALDOCS.NSP](legacy-sifap/natural-programs/VALDOCS.NSP#L207), 207-223 | Inferred |
| VD-04 | Prefixes `000/001/002/010/011/099/100/999` mark special, set CPF valid/result `V` and reset the error count, including preceding RG errors. | Optional | [VALDOCS.NSP](legacy-sifap/natural-programs/VALDOCS.NSP#L58), 58-65; [helper](legacy-sifap/natural-programs/VALDOCS.NSP#L228), 228-241 | Mystery <!-- mystery: Which exemptions may reset earlier document errors, and who owns the prefix list? --> |
| VD-05 | `SUBVALNI` failure adds a new error after the reset and sets invalid. Output prints the final error count and optionally a special-document notice. | Unwanted behavior | [VALDOCS.NSP](legacy-sifap/natural-programs/VALDOCS.NSP#L106), 106-125 | Inferred; special-prefix handling does not bypass this later NIS check |
| VD-06 | Voter ID/CTPS are input but not checked; no assignment persists `IND-DOCS-OK`. Natural error marks invalid and terminates 12. | Event-driven | [VALDOCS.NSP](legacy-sifap/natural-programs/VALDOCS.NSP#L67), 67-134 | Mystery <!-- mystery: What process persists documentation approval and validates the supplementary identifiers? --> |

## SUBVALCP.NSN

Declarations: [SUBVALCP.NSN](legacy-sifap/natural-programs/SUBVALCP.NSN#L28),
28-42, plus `PDAVALID`. The unused NIS parameter still belongs to the positional contract.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
| SC-01 | Reset outputs and special flag `N`; reject non-`C` type with 1004, blank/all-zero CPF with 1002, and nonnumeric CPF with 1005, in that order. | Unwanted behavior | [SUBVALCP.NSN](legacy-sifap/natural-programs/SUBVALCP.NSN#L44), 44-66 | Inferred |
| SC-02 | Shared `CCVALCPF` failure returns 1001; success returns 0/blank message. No branch returns the PDA header's separate 1003 code. | Unwanted behavior | [SUBVALCP.NSN](legacy-sifap/natural-programs/SUBVALCP.NSN#L71), 71-82; [include](legacy-sifap/natural-programs/SUBVALCP.NSN#L94), 94 | Inferred; header and implementation must be distinguished |
| SC-03 | Natural error returns 9999 and context in the message without input, screen output or database access. | Unwanted behavior | [SUBVALCP.NSN](legacy-sifap/natural-programs/SUBVALCP.NSN#L85), 85-91 | Inferred |

## SUBVALNI.NSN

Declarations: [SUBVALNI.NSN](legacy-sifap/natural-programs/SUBVALNI.NSN#L38),
38-50, plus `PDAVALID`. Digits are `N1/1:11`; ten weights are `N1`;
sum/quotient are `N5`, remainder/index `N2`, check digit `N1`.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| SN-01 | Reset outputs/special flag; reject non-`N` type with 1004, blank/all-zero NIS with 1010, nonnumeric input with 1012. | Unwanted behavior | [SUBVALNI.NSN](legacy-sifap/natural-programs/SUBVALNI.NSN#L52), 52-74 | Inferred |
| SN-02 | Extract digits through DECIDE `0`-`9` (`NONE` assigns zero after the earlier mask guard). Use weights 3,2,9,8,7,6,5,4,3,2; remainder below 2 gives zero, otherwise 11 minus remainder. | Ubiquitous | [SUBVALNI.NSN](legacy-sifap/natural-programs/SUBVALNI.NSN#L102), 102-150 | Inferred |
| SN-03 | A mismatching eleventh digit returns 1011; otherwise return 0 with blank message. Natural error returns 9999/context. | Unwanted behavior | [SUBVALNI.NSN](legacy-sifap/natural-programs/SUBVALNI.NSN#L79), 79-99 | Inferred; no database access or screen interaction |

## CONSBENF.NSP

Declarations: [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L18),
18-104. Search values are `N11`, stored CPF `A11`, mask `A14`; twelve-slot
history arrays are declared, but the history loop prints directly from the view.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| CQ-01 | PF3 exits; blank search type defaults to `C`. CPF search calls `SUBVALCP` and uses REINPUT on failure. | Event-driven | [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L113), 113-144 | Inferred |
| CQ-02 | DECIDE `C/N` finds by CPF/NIS respectively, REINPUT on absence; other search types REINPUT as invalid. NIS search does not call `SUBVALNI`. | Unwanted behavior | [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L147), 147-166 | Inferred |
| CQ-03 | Display occurs inside the beneficiary FIND, builds an address, and maps `A/S/C/I/D` to status labels, otherwise `UNKNOWN`. | State-driven | [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L199), 199-262 | Inferred; no MAP member is referenced by the executable input |
| CQ-04 | Read payments by CPF; stop on changed CPF or count above 12. No descending period order is specified. Zero history prints a no-payments message. | State-driven | [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L264), 264-290 | Mystery <!-- mystery: What establishes that these are the latest twelve payments rather than the first twelve returned by CPF order? --> |
| CQ-05 | Numeric CPF below 10000000000 exposes the first three positions and masks the rest; otherwise positions 7-11 remain visible. | State-driven | [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L298), 298-311 | Mystery <!-- mystery: Which CPF masking policy is authorized across queries and reports? --> |
| CQ-06 | After a successful search, write a `CO`/`BENF` audit and commit using the CPF assigned by the display helper. This consultation path is not database-read-only. | Event-driven | [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L168), 168-181; [include](legacy-sifap/natural-programs/CONSBENF.NSP#L314), 314 | Mystery <!-- mystery: How does this query audit reconcile with the CCAUDIT comment excluding CO? --> |
| CQ-07 | Natural error writes context and executes `ESCAPE ROUTINE`, with no explicit backout or termination in this handler. | Unwanted behavior | [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L188), 188-193 | Inferred; recovery semantics require runtime validation |

## RELPGT.NSP

Declarations: [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L17),
17-72. Periods are `N6`; zero numeric program filter means all; totals `P13.2`;
display name `A30` receives part of stored `A60`; printer uses 66 lines by 132 columns.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| RP-01 | Read the start/end period interval; stop above the end. Nonzero program filter excludes nonmatching formatted `A4` codes; zero does not filter. | State-driven | [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L96), 96-138 | Inferred; no input interval-validity guard appears |
| RP-02 | When program changes and previous program is nonblank, print/reset a subtotal. The outer READ orders by period, not program. | Event-driven | [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L123), 123-149 | Mystery <!-- mystery: Are per-program subtotals complete when the same program occurs in noncontiguous period-ordered records? --> |
| RP-03 | Missing beneficiary leaves display name/UF blank. Present name is limited to 30 characters; CPF masking hides only the first three digits. | Event-driven | [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L152), 152-167 | Inferred; compare disclosure with CQ-05 |
| RP-04 | Map types `N/D/T` to normal/thirteenth/third, else other; statuses `G/P/C/D/E` to their labels, else other. | State-driven | [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L170), 170-195 | Inferred |
| RP-05 | At line 61 or later, issue a new page; page-top hook prints columns. Start-of-data resets totals; end-of-data prints a nonblank last subtotal and grand totals. | Event-driven | [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L115), 115-129; [pagination](legacy-sifap/natural-programs/RELPGT.NSP#L198), 198-230; [helpers](legacy-sifap/natural-programs/RELPGT.NSP#L246), 246-271 | Inferred; subtotal adds 3 to the manual line counter |
| RP-06 | Natural error prints to logical printer 1, backs out current transaction and terminates 12. The body has no database mutation. | Unwanted behavior | [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L237), 237-243 | Inferred |

## RELAUDIT.NSP

Declarations: [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L18),
18-66. Date limits are `N8`; optional filters are action `A2`, user `A8`,
entity `A4`; output type `A1`, time text `A8`, counters `N8`.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| RA-01 | Blank output defaults to `T`; zero start date defaults to 19970101, zero end to today. Date-ordered READ also skips below start and stops above end. | State-driven | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L90), 90-123 | Inferred; unrecognized output is not rejected |
| RA-02 | Always exclude action `EX` before optional filters, incrementing the filtered counter even if the requested action itself is `EX`. | Unwanted behavior | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L125), 125-141 | Mystery <!-- mystery: Who authorized deletion events to be omitted from the audit report? --> |
| RA-03 | Nonblank action, user and entity filters require exact equality; each mismatch increments filtered and skips. | Optional | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L136), 136-157 | Inferred |
| RA-04 | Count/display `IN` insertion, `AL` change, `CO` reconciliation, `CN` query, `DV` discrepancy, else other. | State-driven | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L160), 160-182 | Mystery <!-- mystery: Why do the query writer and report use different action meanings for CO/CN? --> |
| RA-05 | At line 61 or later print a header. `T` writes screen detail without description; all other output values use the printer with description. | State-driven | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L184), 184-211; [header](legacy-sifap/natural-programs/RELAUDIT.NSP#L279), 279-303 | Inferred |
| RA-06 | Start-of-data resets selection/day counts. Day break resets day count and prints a subtotal only for non-`T`; end-of-data prints selected total only for non-`T`. | Event-driven | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L114), 114-116; [hooks](legacy-sifap/natural-programs/RELAUDIT.NSP#L213), 213-230 | Inferred |
| RA-07 | Non-`T` output additionally runs a date-range HISTOGRAM without action/user/entity filters or the deletion exclusion. | Optional | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L256), 256-266 | Mystery <!-- mystery: Should histogram counts represent all stored events or the filtered report population? --> |
| RA-08 | Natural error prints context and terminates 12. This report performs no database mutation. | Unwanted behavior | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L271), 271-276 | Inferred |

## SIFAPJ01.jcl and SIFAPJ02.jcl

JCLs have no Natural `DEFINE DATA`. Their inputs/outputs are DD allocations,
in-stream commands and step conditions. Scheduler statements below are comments,
not evidence of a live Control-M configuration.

| ID | Operational behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| J1-01 | STEP010 runs `NATBATCH` with DBID 57/FNR 150; in-stream commands log on to `SIFAPPRD`, invoke `BATCHPGT` and provide literal period 202601. Work outputs have lengths 240 and 120. | Event-driven | [SIFAPJ01.jcl](legacy-sifap/natural-programs/SIFAPJ01.jcl#L46), 46-74 | Inferred; not proof of deployed database/file binding |
| J1-02 | STEP020 has `COND=(4,LT,STEP010)`, skipping the copy when 4 is less than the prior normal return code. STEP030 uses `COND=(5,GT,STEP010)` and `IEFBR14`. | Unwanted behavior | [SIFAPJ01.jcl](legacy-sifap/natural-programs/SIFAPJ01.jcl#L76), 76-93 | Mystery <!-- mystery: What actually sends a failure notice, and how should RC 8 be handled by the operational flow? --> |
| J1-03 | Comments describe a first-business-day 22:00 run, a four-hour window, successor only at RC 0 and same-period restart. | Event-driven | [SIFAPJ01.jcl](legacy-sifap/natural-programs/SIFAPJ01.jcl#L13), 13-33 | Inferred from comments only; restart safety remains open given CB-08/BP-16 |
| J2-01 | STEP010 invokes `BATCHREL` with 202601; STEP020 invokes `RELPGT` with start/end 202601 and filter 0000, using the same RC comparison as the copy step. | Event-driven | [SIFAPJ02.jcl](legacy-sifap/natural-programs/SIFAPJ02.jcl#L49), 49-101 | Inferred; literals are not an implemented scheduler substitution |
| J2-02 | Allocate printer records at 133 characters and archival work rows at 132. A second printer DD is allocated for the detail step, but the read RELPGT body uses printer 1 only. | Event-driven | [SIFAPJ02.jcl](legacy-sifap/natural-programs/SIFAPJ02.jcl#L56), 56-64; [detail DDs](legacy-sifap/natural-programs/SIFAPJ02.jcl#L84), 84-90 | Inferred; no separate printer-2 report inferred |
| J2-03 | Comments describe second-business-day 06:00 execution after `SIFAPJ01` RC 0 and read-only rerun. The two program bodies corroborate absence of database writes, not absence of repeated output files. | Event-driven | [SIFAPJ02.jcl](legacy-sifap/natural-programs/SIFAPJ02.jcl#L13), 13-36 | Inferred from comments and source; runtime scheduling not inspected |

## Shared declarations reviewed

| Member | Observed declaration | Evidence | Boundary |
|---|---|---|---|
| PDACALC.NSA | Positional area with 16 fields: CPF, program, period, region, income, dependents, age, status, base, gross, deductions, bonus, net, payment type, return code and message. Keys are alpha except period; amount fields are `P9.2`. | [PDACALC.NSA](legacy-sifap/natural-programs/PDACALC.NSA#L49), 49-79 | Header return-code descriptions are a declared contract, not evidence that every callee implements every code. |
| PDAVALID.NSA | Six fields in order: type `A1`, CPF `A11`, NIS `A11`, return `N4`, message `A60`, special indicator `A1`. | [PDAVALID.NSA](legacy-sifap/natural-programs/PDAVALID.NSA#L43), 43-57 | `USING` imports declarations; a caller still needs to pass all fields in the same order. |
| LDASIFAP.NSL | Regional factors/UFs, income and contribution tables, valid UFs, month days, date/work fields and a century pivot initialized to 50. | [LDASIFAP.NSL](legacy-sifap/natural-programs/LDASIFAP.NSL#L32), 32-107 | No executable branches. February is initialized to 29; importing this area does not prove that a consumer uses its tables. |

## CCAUDIT.NSC

This copycode declares no independent `DEFINE DATA`: required fields are supplied
by each including module. Header examples at lines 20-43 are not executable declarations.

| ID | Conditional behavior observed | EARS pattern candidate | Origin and interval | Classification / review note |
|---|---|---|---|---|
| AU-01 | If the audit seed is zero, read the greatest audit number; increment it for the new record. Reset the view and populate date, time, composed timestamp, action, module, entity and user. | Event-driven | [CCAUDIT.NSC](legacy-sifap/natural-programs/CCAUDIT.NSC#L60), 60-90 | Inferred; a max-plus-one seed is not evidence of concurrency control |
| AU-02 | Only action `BT` adds `*INIT-USER` as batch name and status `S`. Store the audit record; no commit or error handler is included. | Event-driven | [CCAUDIT.NSC](legacy-sifap/natural-programs/CCAUDIT.NSC#L92), 92-100 | Inferred; caller owns transaction/error handling |
| AU-03 | The body does not filter `CO` or populate `COD-PROFILE`; the header describes both omissions. | Optional | [CCAUDIT.NSC](legacy-sifap/natural-programs/CCAUDIT.NSC#L45), 45-58; [body](legacy-sifap/natural-programs/CCAUDIT.NSC#L60), 60-100 | Mystery <!-- mystery: Which callers enforce audit exclusions and provide the missing actor-profile context? --> |

## Historical documentation cross-check

The 2012 document explicitly labels itself incomplete and technically unvalidated:
[BUSINESS-RULES-2012.md](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L26),
26-64. Therefore, the matches below are corroboration of a statement or intent,
not automatic promotion of a candidate to an approved business rule.
All rule candidates retain `Inferred` or `Mystery` status in this pass.
The Markdown counterparts were used; equivalence with the three DOCX files was
not checked. Historical RN numbers are not modern REQ-IDs.

| Source section / rule | Comparison with the read corpus | Candidate references |
|---|---|---|
| 2012 section 1.1, RN-001 | CPF validation exists, but NIS failure in registration only warns; the historical routine names are not the supplied members. | CA-02/03, SC-01/02, SN-01/03; [document](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L72), 72 |
| 2012 section 1.1, RN-002 | Document limits duplication rejection to active records; registration source rejects any existing CPF. | CA-04; [document](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L74), 74 |
| 2012 section 1.1, RN-003/006/007 | Active-program linkage, minimum registration age 16 and mandatory bank data are not all enforced by the supplied registration body. Absence here does not prove absence from every external process. | CA-01/05/07; [document](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L76), 76-93 |
| 2012 RN-004; 2008 section 3.2.2 | Documents say three dependents and acknowledge possible change; code tests current count `>5`, DDM has ten slots. No limit is chosen as authoritative. | DP-02, DM-02 in [data map](data-map.md); [2012](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L78), 78-82; [2008](legacy-sifap/legacy-docs/TECHNICAL-MANUAL-SIFAP-2008.md#L254), 254-270 |
| 2012 RN-005 | A 01-27 table and special 99 are corroborated in LDASIFAP, but conflict with macroregion descriptions in DDMs. | BP-08, CB-03, BL-03, VE-03; [document](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L84), 84-89 |
| 2012 section 1.2, RN-010 | Registration emits audit, but not through the named historical routine or with complete field-level before/after data. | CA-07/08, AU-01/03; [document](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L101), 101 |
| 2012 section 1.3; 2008 section 3.2.1 | Historical deletion and CPF-change workflows are not present in the supplied CADBENEF DECIDE. They must not be invented from documentation alone. | CA-01/08; [2012](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L99), 99-107; [2008](legacy-sifap/legacy-docs/TECHNICAL-MANUAL-SIFAP-2008.md#L230), 230-248 |
| 2012 section 2.1, RN-013/014 | The additive formula differs from the source's multiplicative factors. Truncation intent is corroborated, but exact packed/numeric assignment behavior and report rounding are still unexecuted. | BP-12, CB-06, BL-04; [document](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L115), 115-136 |
| 2012 section 2.2, RN-017/018 | First matching upper ceiling is corroborated; ten configured bands and per-person input are not: code uses five hardcoded bands and family income. | BP-10, CB-04, VE-06; [document](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L140), 140-142 |
| 2012 section 2.3; 2008 section 3.3.2 | Annual January/CALCIDX description does not match the interactive correction member with local 2010-2012 indices. | CR-01/03; [2012](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L146), 146-148; [2008](legacy-sifap/legacy-docs/TECHNICAL-MANUAL-SIFAP-2008.md#L309), 309-322 |
| 2012 section 3, RN-021/022/023 | The 30% concept is corroborated, not the described reject-all behavior, numeric type codes or sorted priority. Source caps the running total after non-J occurrences in stored order. | DS-02/05, DM-09; [document](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L152), 152-174 |
| 2012 section 4.2 | Active status is one observed check, but region 99 returns earlier. Banking, multi-program, 24-month recency and blocking-audit checks described here do not occur in the supplied VALELEG body. | VE-03/08; [document](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L186), 186-205 |
| 2012 section 5.1; 2008 section 3.5.1 | CALCBENF call and first-business-day schedule comments match; name ordering, CALCDSCT call and stored status P do not match the body (CPF order, no such call, G). | BP-02/07/14/16, J1-03; [2012](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L208), 208-228; [2008](legacy-sifap/legacy-docs/TECHNICAL-MANUAL-SIFAP-2008.md#L330), 330-365 |
| 2012 section 5.2 | Error counters/work output exist, but no MAX-ERROS=100/ABEND U4038 condition appears in BATCHPGT; return and termination paths differ by callee. | BP-19/20, CB-09, VE-10; [document](legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md#L230), 230-237 |
| 2008 section 3.5.2 | The 132-column report description matches BATCHREL printer/work-file declarations. Detailed rounding and status mappings are not supplied by that section. | BL-04/06, J2-02; [document](legacy-sifap/legacy-docs/TECHNICAL-MANUAL-SIFAP-2008.md#L367), 367-375 |
| 1997 sections 5.1/5.2 | The proposed SIAFI layout differs from BATCHCON's bank-return offsets; the document itself says that layout was not implemented as proposed. | BC-01; [document](legacy-sifap/legacy-docs/ORIGINAL-ARCHITECTURE-1997.md#L310), 310-353 |
| 1997 section 6.2 | Historical intent for before/after audit differs from partial scalar/copycode writers; the note describes a later separate audit file. | AU-01/03, BC-06; [document](legacy-sifap/legacy-docs/ORIGINAL-ARCHITECTURE-1997.md#L371), 371-389 |

The [data map](data-map.md) contains the complete DDM/FDT comparison, including
12 cross-source questions. The [dependency map](dependency-map.md) preserves all
executable call/import/access evidence. Human review is required before writing
formal EARS in Stage 2.

## Completion criteria

- [x] All 24 library files and 5 Adabas artifacts have a recorded reading.
- [x] All source conditionals have a candidate or an explicit technical-only note.
- [x] Imported declarations, call contracts and DDM differences are statically cross-checked.
- [x] Open questions are linked to the human-validation register.
- [ ] The team has reviewed the candidates; no approval is inferred from tool execution.

### Continue reading

| Previous | Next |
|---|---|
| [Inventory](inventory.md) | [Dependency map](dependency-map.md) |

<sub>[Back to the kit index](../README.md)</sub>
