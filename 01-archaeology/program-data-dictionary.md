# Natural declaration dictionary

> **Trail:** [Team kit](../README.md) > [Stage 1](README.md) > **Declarations**

**Variable names, formats, sizes and declaration context for every supplied Natural member.**

Date: 2026-09-10. This is a reading aid, not replacement source or a proposed
schema. Each format includes its declared size/scale; `/1:n` denotes an array.
`L` is logical. Original comments and view nesting remain authoritative in the
linked `DEFINE DATA` intervals. Where there is no specific comment, the field
is retained as a work field rather than assigned an invented business meaning.

## Repeated declaration sets

These sets shorten this document only: they do not add code abstractions or
imply shared runtime storage. Each member's local section names the sets it declares.

### Audit work fields

Declared in BATCHPGT, BATCHCON, CADBENEF, CADDEPEN, CADPROG, CALCCORR and
CONSBENF. Required/commented contract:
[CCAUDIT.NSC](legacy-sifap/natural-programs/CCAUDIT.NSC#L36), 36-43.

| Variable | Format | Declared role |
|---|---|---|
| #AUD-ACTION | A2 | Input action |
| #AUD-ENTITY | A4 | Input entity type |
| #AUD-ID | A15 | Input entity key |
| #AUD-CPF | A11 | Affected CPF or blank |
| #AUD-DESCR | A80 | Input description |
| #AUD-SEQ | N15 | Sequence work field |
| #AUD-TIMN | N7 | Time work field |

### Shared CPF work fields

Declared in CADDEPEN and SUBVALCP, used by the included CCVALCPF body.
Required/commented contract: [CCVALCPF.NSC](legacy-sifap/natural-programs/CCVALCPF.NSC#L19), 19-30.

```text
A11: #CPF-STR
L: #CPF-OK, #CPF-EQUAL
N1/1:11: #CPF-DIG
N5: #CPF-SUM, #CPF-QUOT
N2: #CPF-REMAIN, #CPF-WEIGHT, #CPF-IDX
N1: #CPF-DV1, #CPF-DV2
```

The comments identify input, output and algorithm work fields; no DDM is accessed.

### Inline CPF arithmetic fields

The following declarations occur separately in CADBENEF, VALBENEF and VALDOCS.
Their algorithms are not assumed equivalent to CCVALCPF.

```text
N1/1:11: #DIG
N5: #SUM
N3: #REMAIN
N1: #DV1, #DV2
N2: #WEIGHT, #I
```

## Imported data areas

### PDAVALID.NSA

Source: [PDAVALID.NSA](legacy-sifap/natural-programs/PDAVALID.NSA#L43), 43-57.
Order is part of the parameter contract.

| Variable | Format | Comment / direction |
|---|---|---|
| #PV-TYPE-DOC | A1 | IN, C=CPF, N=NIS/PIS/PASEP |
| #PV-CPF | A11 | IN, unmasked/left-padded CPF |
| #PV-NIS | A11 | IN, unmasked NIS |
| #PV-COD-RETURN | N4 | OUT, zero means valid |
| #PV-MSG | A60 | OUT, blank when valid |
| #PV-IND-SPECIAL | A1 | OUT, S=special, N=common |

### PDACALC.NSA

Source: [PDACALC.NSA](legacy-sifap/natural-programs/PDACALC.NSA#L49), 49-79.
The header lists more possible returns than every callee actually implements.

| Variable | Format | Comment / direction |
|---|---|---|
| #PC-CPF | A11 | IN, unmasked CPF |
| #PC-COD-PROGRAM | A4 | IN, program code |
| #PC-PERIOD | N6 | IN, YYYYMM |
| #PC-COD-REGION | A2 | IN, region |
| #PC-FAMILY-INCOME | P9.2 | IN, declared income |
| #PC-QTY-DEPEND | N2 | IN, active dependent count |
| #PC-AGE | N3 | IN, completed years per comment; consumers may recompute |
| #PC-STAT-BENEF | A1 | IN, A/S/C/I/D |
| #PC-AMT-BASE | P9.2 | IN, base amount |
| #PC-AMT-GROSS | P9.2 | OUT, gross |
| #PC-AMT-DISC | P9.2 | OUT, deductions |
| #PC-AMT-BONUS | P9.2 | OUT, bonus |
| #PC-AMT-NET | P9.2 | OUT; header formula needs comparison with actual calculation |
| #PC-TYPE-PAYMENT | A1 | OUT, N/D/T per comment |
| #PC-COD-RETURN | N4 | OUT, zero means OK |
| #PC-MSG | A60 | OUT, blank when OK |

### LDASIFAP.NSL

Source: [LDASIFAP.NSL](legacy-sifap/natural-programs/LDASIFAP.NSL#L32), 32-107.
All 24 declared fields are retained, including work variables and unused imports.

| Variables | Format | Comment / initialized value |
|---|---|---|
| #L-TAB-REGION-FACTOR | N3.4/1:27 | Region factors, 27 initial values |
| #L-TAB-REGION-UF | A2/1:27 | Region-to-UF labels including reserved ZZ |
| #L-INCOME-BAND | P9.2/1:5 | 300, 600, 1000, 1500, 9999.99 |
| #L-BAND-FACTOR | N3.4/1:5 | 1, .85, .70, .55, .40 |
| #L-CONTRIB-BAND | P9.2/1:4 | 500, 1000, 2000, 9999.99 |
| #L-CONTRIB-RATE | N3.2/1:4 | .03, .05, .07, .09 |
| #L-VALID-UF | A2/1:27 | 27 state/DF codes |
| #L-DAYS-MONTH | N2/1:12 | Month lengths; February=29 |
| #L-DT-TODAY | N8 | YYYYMMDD work value |
| #L-YEAR, #L-PERIOD-YEAR | N4 | Date/period work values |
| #L-MONTH, #L-DAY, #L-PERIOD-MONTH | N2 | Date/period work values |
| #L-PERIOD | N6 | YYYYMM |
| #L-AA-SHORT | N2 | Historical short year |
| #L-CENTURY-WINDOW | N2 | INIT 50 |
| #L-EXPANDED-YEAR | N4 | Expanded-year work field |
| #L-AMT-TEMP | P13.2 | Monetary intermediate per comment |
| #L-MSG | A78 | Standard message |
| #L-COD-RETURN | N4 | Return work field |
| #L-I, #L-J, #L-K | N2 | General work indices |

## Local and explicit parameter declarations

Every `#` variable in the linked declaration interval is listed directly or in
a named repeated/imported set above. View fields are enumerated separately below.

### BATCHPGT.NSP

Source: [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L27), 27-156.
Imports all three data areas locally and declares the audit work set.
Comments group counters, monetary accumulators, calculation fields, regional/income
tables, batch control and work records.

```text
N8: #QTY-PROCESSED, #QTY-ERRS, #QTY-IGNORED, #QTY-GENERATED, #QTY-REJECT, #DT-TODAY, #NUM-BATCH
P13.2: #AMT-TOT-GROSS, #AMT-TOT-DISC, #AMT-TOT-NET, #AMT-TOT-BONUS
N6: #PERIOD, #SEQ-BATCH
A6: #PERIOD-A
N2: #MONTH, #NUM-DEPEND, #COD-REGION, #J
N4: #YEAR, #YEAR-BIRTH, #QTY-REMAIN
P9.2: #AMT-BASE, #AMT-BENF, #AMT-GROSS, #AMT-DISC, #AMT-NET, #AMT-BONUS, #AMT-13, #INCOME
N11: #AMT-TEMP
N3.4: #FACTOR-REGION, #FACTOR-FAMILY, #FACTOR-INCOME, #FACTOR-AGE, #FACTOR-ADJUST
N3: #AGE
A1: #TYPE-PROG, #TYPE-PAYMENT, #STAT-PROG
L: #ERR-CALC
N15: #SEQ-PAYMENT
A120: #MSG-LOG, #LOG-ERR
A11: #CPF-PREV
A17: #KEY-CPF-PERIOD
A15: #SEQ-PAYMENT-A
A9: #AMT-NET-A
N9: #QTY-QUOT
N3.4/1:27: #TAB-REGION
P9.2/1:5: #INCOME-BAND
N3.4/1:5: #BAND-FACTOR
A240: #REC-EXTRACT
```

### BATCHCON.NSP

Source: [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L20), 20-103.
Imports LDASIFAP, declares audit work fields. CNAB fields are slices of one
240-character record; the file-name input is a label rather than a binding.

```text
A240: #REC-CNAB
A3: #CNAB-BANK
A4: #CNAB-BATCH
A1: #CNAB-TYPE-REC
A11: #CNAB-CPF
A15: #CNAB-AMT, #AMT-STR
A8: #CNAB-DT-PAYMENT
A2: #CNAB-COD-RETURN, #COD-RETURN
A10: #CNAB-NUM-DOC
N6: #PERIOD, #HR-CURRENT
A6: #PERIOD-A
N8: #DT-TODAY, #QTY-READ, #QTY-RECONCILED, #QTY-DIVERGENT, #QTY-NOT-FOUND, #QTY-AUDIT, #DT-PAYMENT-WK
N7: #TIMN-AUX
A60: #FILE-RETURN, #AMT-PREV-STR, #AMT-NEW-STR
N11: #CPF-NUM
P9.2: #AMT-RETURN, #AMT-PAYMENT-SIFAP, #DIFF
N15: #AMT-CENT, #NUM-PAYMENT, #SEQ-AUDIT
L: #FOUND
A80: #MSG
N2: #I
```

### BATCHREL.NSP

Source: [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP#L22), 22-78.
Imports LDASIFAP. Five-slot arrays are region/status totals; local pagination
fields coexist with printer formatting. Rounding intermediates differ in scale.

```text
N6: #PERIOD
N8: #DT-TODAY, #QTY-OVERALL
P13.2/1:5: #TOT-REGION-GROSS, #TOT-REGION-DISC, #TOT-REGION-NET, #TOT-STS-GROSS
N8/1:5: #QTY-REGION, #QTY-STS
A15/1:5: #NAME-REGION, #NAME-STS
P15.2: #TOT-OVERALL-GROSS, #TOT-OVERALL-DISC, #TOT-OVERALL-NET
N2: #IDX-REGION, #COD-REGION, #IDX-STS, #I, #LINE, #MAX-LINES
A1: #STATUS
L: #FOUND
A132: #LINE-REPORT
N4: #PAGE
P13.2: #AMT-ROUND
N15: #AMT-TEMP
```

### CADBENEF.NSP

Source: [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L13), 13-104.
Imports PDAVALID; declares audit work and inline CPF arithmetic fields.
The screen fields are not identical to the set saved during updates.

```text
N11: #CPF, #NIS
A60: #NAME, #MSG
N8: #DT-BIRTH, #CEP, #DT-TODAY
A1: #SEX, #STATUS, #OPER, #RESULT
A80: #ADDRESS
A40: #CITY
A2: #UF
A15: #PHONE, #RG
N4: #COD-PROG, #YEAR-CURRENT, #YEAR-BIRTH
P9.2: #FAMILY-INCOME
N2: #NUM-DEPEND, #COD-REGION, #QTY-ERRS
N3: #AGE
L: #ERR, #CPF-VALID, #FOUND
A60/1:10: #MSG-ERR
A11: #CPF-STR
```

### CADDEPEN.NSP

Source: [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L12), 12-82.
Imports LDASIFAP and declares audit/shared CPF work sets. Document and sex
inputs are retained even though the persistence block does not save them.

```text
N11: #CPF-HOLDER, #CPF-DEPEND
A11: #CPF-HOLDER-STR, #CPF-DEPEND-STR
A60: #NAME-DEPEND, #MSG
N8: #DT-BIRTH-DEPEND
A2: #RELATION
A15: #DOC-DEPEND
A1: #SEX-DEPEND, #STAT-BENEF, #COUNT
N2: #NUM-DEPEND, #IDX
L: #FOUND, #ERR
```

### CADPROG.NSP

Source: [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L12), 12-72.
Imports LDASIFAP and declares audit work. Local monetary fields are wider than
the corresponding `P7.2` view fields; local K is distinct from DDM FACTOR-K.

```text
N4: #COD-PROG
A4: #COD-PROG-A
A60: #NAME-PROG, #MSG
A1: #TYPE, #STATUS, #OPER
P9.2: #AMT-BASE, #MAX-INCOME, #AMT-CALC
A5: #COD-ELIG
N8: #DT-START, #DT-END
N3: #AGE-MIN, #AGE-MAX
N3.4: #FACTOR-ADJUST
N5.6: #FACTOR-K
L: #FOUND
```

### CALCBENF.NSN

Source: [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L16), 16-93.
Imports PDACALC as parameters and LDASIFAP locally. Local variables include
separate calculation amounts, numeric CPF conversion and two factor tables.

```text
N11: #CPF, #AMT-TEMP
A11: #CPF-STR
N6: #PERIOD
N2: #MONTH, #NUM-DEP, #COD-REGION, #J
N4: #YEAR, #YEAR-BIRTH
N3: #AGE
P9.2: #AMT-BASE, #AMT-BENF, #AMT-GROSS, #AMT-DISC, #AMT-NET, #AMT-BONUS, #AMT-13, #AMT-TOTAL, #INCOME
N3.4: #FACTOR-REGION, #FACTOR-FAMILY, #FACTOR-INCOME, #FACTOR-AGE, #FACTOR-ADJUST
A4: #COD-PROG
A1: #TYPE-PROG, #STATUS-BENEF, #TYPE-PAYMENT
A78: #MSG
L: #ERR
N8: #DT-TODAY, #DT-BIRTH
N3.4/1:27: #TAB-REGION
P9.2/1:5: #INCOME-BAND
N3.4/1:5: #BAND-FACTOR
```

### CALCCORR.NSP

Source: [CALCCORR.NSP](legacy-sifap/natural-programs/CALCCORR.NSP#L12), 12-82.
Imports PDAVALID/LDASIFAP and declares audit work. The two-dimensional year/month
table is separate from the declared one-dimensional IPCA table.

```text
N11: #CPF, #AMT-TEMP
A11: #CPF-STR
N6: #PERIOD-START, #PERIOD-END, #PERIOD-CURRENT
N8: #DT-TODAY
P9.2: #AMT-ORIG, #AMT-CORR, #AMT-DIFF
P11.2: #AMT-TOTAL-CORRECTION
N5.6: #INDEX-ACCUM
N3.6: #INDEX-MONTH
N2: #MONTH-REF, #K, #MONTH-C
N4: #YEAR-REF, #YEAR-C
N5: #QTY-REC
A60: #MSG
N3.6/1:12: #IPCA-TAB
N4/1:10: #YEAR-TAB
N3.6/1:10,1:12: #IPCA-YEAR
```

### CALCDSCT.NSP

Source: [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L12), 12-57.
Imports LDASIFAP. Local `#TYPE-DISC (A1)` receives the wider view `TYPE-DISC (A3)`.

```text
N11: #CPF, #AMT-TEMP
A11: #CPF-STR
N15: #NUM-PAYMENT
P9.2: #AMT-GROSS, #AMT-TOTAL-DISC, #AMT-DISC-ITEM, #AMT-MAX-DISC
P3.2: #PCT-DISC
A1: #TYPE-DISC
N2: #NUM-DISC, #INDEX, #K
N8: #DT-TODAY
L: #FOUND
N6: #PERIOD
A60: #MSG
P9.2/1:4: #BAND-CONTRIB
N3.2/1:4: #RATE-CONTRIB
```

### VALELEG.NSN

Source: [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L15), 15-66.
Imports PDACALC as parameters and LDASIFAP locally. Reasons are an array;
the returned message takes only the first reason on rejection.

```text
A11: #CPF-STR
A4: #COD-PROG
L: #ELIGIBLE, #ELIG-OK
A60/1:10: #REASON
N2: #QTY-REASON, #NUM-DEP, #COD-REGION, #I
N3: #AGE, #AGE-MIN, #AGE-MAX
N4: #YEAR-BIRTH, #YEAR-CURRENT
P9.2: #INCOME
A5: #COD-ELIG
A1: #TYPE-PROG, #STATUS-BENEF, #DOCS-OK, #STAT-PROG
P7.2: #MAX-INCOME
A78: #MSG
```

### VALBENEF.NSN

Source: [VALBENEF.NSN](legacy-sifap/natural-programs/VALBENEF.NSN#L15), 15-71.
Imports LDASIFAP and declares inline CPF arithmetic fields. Explicit parameters,
in order, are listed separately from locals.

| Parameter | Format | Direction / comment |
|---|---|---|
| #CPF-STR | A11 | IN |
| #NAME | A60 | IN |
| #DT-BIRTH | N8 | IN |
| #SEX | A1 | IN |
| #UF | A2 | IN |
| #CEP | N8 | IN; no body validation found |
| #STATUS | A1 | IN |
| #RESULT | A1 | OUT V/I |
| #QTY-ERRS | N2 | OUT |
| #MSG-ERR | A60/1:10 | OUT |

```text
A11: #CPF
L: #UF-OK, #CPF-VALID, #DT-VALID, #NAME-VALID, #ALL-EQUAL, #HAS-SPACE
N4: #YEAR, #YEAR-CURRENT
N2: #MONTH, #DAY, #POS
N2/1:12: #DAYS-MONTH
A60: #NAME-TEMP
A1: #CHAR
A2/1:27: #UF-TAB
```

### VALDOCS.NSP

Source: [VALDOCS.NSP](legacy-sifap/natural-programs/VALDOCS.NSP#L14), 14-52.
Imports PDAVALID, declares inline CPF arithmetic fields. CTPS and voter ID
are inputs without checks in the supplied body.

```text
N11: #CPF, #NIS
A15: #RG, #CTPS
A12: #TITLE
A1: #RESULT
A60/1:5: #MSG
N2: #QTY-ERRS, #RG-LEN
L: #CPF-OK, #RG-OK, #DOC-SPECIAL-OK
A3: #PREFIX-CPF
A11: #CPF-STR
A3/1:8: #PREFIX-SPECIAL
```

### SUBVALCP.NSN and SUBVALNI.NSN

SUBVALCP imports PDAVALID as parameters and declares exactly the shared CPF
work set: [SUBVALCP.NSN](legacy-sifap/natural-programs/SUBVALCP.NSN#L28), 28-42.

SUBVALNI also imports PDAVALID; all locals follow:
[SUBVALNI.NSN](legacy-sifap/natural-programs/SUBVALNI.NSN#L38), 38-50.

```text
A11: #NIS-STR
N1/1:11: #NIS-DIG
N1/1:10: #NIS-WEIGHT  (INIT 3,2,9,8,7,6,5,4,3,2)
N5: #NIS-SUM, #NIS-QUOT
N2: #NIS-REMAIN, #NIS-IDX
N1: #NIS-DV
```

### CONSBENF.NSP

Source: [CONSBENF.NSP](legacy-sifap/natural-programs/CONSBENF.NSP#L18), 18-104.
Imports PDAVALID/LDASIFAP and declares audit work. The source marks MAX-HIST
obsolete; the history arrays are still retained in this declaration inventory.

```text
N11: #CPF-SEARCH, #NIS-SEARCH, #CPF-NUM
A1: #TYPE-SEARCH
A11: #CPF-A11, #CPF-STR
A14: #CPF-MASK
A80: #ADDRESS
A60: #MSG
A15: #STATUS-DESCR
N3: #I, #MAX-HIST, #QTY-HIST
N6/1:12: #HIST-PERIOD
P9.2/1:12: #HIST-GROSS, #HIST-NET
A1/1:12: #HIST-STS, #HIST-TYPE
A3: #CPF-P1, #CPF-P2, #CPF-P3
A2: #CPF-P4
```

### RELPGT.NSP

Source: [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L17), 17-72.
Imports LDASIFAP. Comments separate filters, pagination, totals and print separators.

```text
N6: #PERIOD-START, #PERIOD-END
N4: #COD-PROG-FILTER, #PAGE
A4: #COD-PROG-A4, #PROG-PREV
N8: #DT-TODAY, #QTY-REC, #QTY-SUB
N2: #LINE, #MAX-LINES
P13.2: #TOT-GROSS, #TOT-DISC, #TOT-NET, #TOT-BONUS, #SUB-GROSS, #SUB-NET
A30: #NAME-BENEF
A2: #UF-BENEF
A14: #CPF-MASK
A11: #CPF-STR
A8: #TYPE-DESCR, #STATUS-DESCR
A100: #SEP-100
A80: #SEP-DASH80, #SEP-EQUAL80
```

### RELAUDIT.NSP

Source: [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L18), 18-66.
Imports LDASIFAP. Output is T=screen/I=printer by comment; counters include
separate query and reconciliation labels whose business meaning is disputed.

```text
N8: #DT-START, #DT-END, #DT-TODAY, #QTY-TOTAL, #QTY-DISPLAYED, #QTY-FILTERED, #QTY-DAY, #QTY-INSERT, #QTY-UPDATE, #QTY-QUERY, #QTY-RECONCIL, #QTY-DIVERG, #QTY-OTHERS
A2: #ACTION-FILTER
A8: #USER-FILTER, #HR-FORMAT
A4: #TABLE-FILTER
A1: #TYPE-OUTPUT
N4: #PAGE
N2: #LINE, #MAX-LINES, #I
A20: #ACTION-DESCR
A6: #HR-STR
A100: #SEP-100
A120: #SEP-120
```

## Declared views

The [Adabas data map](data-map.md) supplies each listed field's exact DDM format,
size, storage marker and comment. The source intervals below identify the
program's declared subset and nesting; these are declarations, not access edges.
Normalized field formats agree with those listed DDM fields; local input/work
formats may differ, as retained above. This comparison is not compilation proof.

### BENEFICIARY-V, VIEW OF BENEFIC

| Members / declaration evidence | Declared field subset | Group context |
|---|---|---|
| [BATCHPGT](legacy-sifap/natural-programs/BATCHPGT.NSP#L32), 32-42; [CALCBENF](legacy-sifap/natural-programs/CALCBENF.NSN#L20), 20-30 | NUM-CPF, FULL-NAME, DT-BIRTH, STAT-BENEFICIARY, COD-PROGRAM, AMT-FAMILY-INCOME, QTY-DEPEND, COD-REGION, UF, NUM-NIS | Flat view declarations |
| [CADBENEF](legacy-sifap/natural-programs/CADBENEF.NSP#L16), 16-36 | NUM-CPF, FULL-NAME, DT-BIRTH, SEX, STREET-ADDRESS, DISTRICT, CITY, UF, CEP, PHONE-MOBILE, RG-NUMBER, STAT-BENEFICIARY, COD-PROGRAM, AMT-FAMILY-INCOME, QTY-DEPEND, DT-REGISTRATION, DT-LAST-UPDATE, COD-REGION, NUM-NIS | GRP-ADDRESS contains street/district/city/UF/CEP |
| [CADDEPEN](legacy-sifap/natural-programs/CADDEPEN.NSP#L15), 15-26 | NUM-CPF, FULL-NAME, STAT-BENEFICIARY, QTY-DEPEND, NAME-DEPEND, DT-BIRTH-DEPEND, RELATION, CPF-DEPEND, STAT-DEPEND, IND-DISABILITY | GRP-DEPEND 1:10 contains last six fields |
| [BATCHREL](legacy-sifap/natural-programs/BATCHREL.NSP#L37), 37-40 | NUM-CPF, COD-REGION, UF | Flat view |
| [CALCDSCT](legacy-sifap/natural-programs/CALCDSCT.NSP#L30), 30-34 | NUM-CPF, FULL-NAME, STAT-BENEFICIARY, UF | Flat view |
| [VALELEG](legacy-sifap/natural-programs/VALELEG.NSN#L19), 19-31 | NUM-CPF, FULL-NAME, DT-BIRTH, STAT-BENEFICIARY, COD-PROGRAM, AMT-FAMILY-INCOME, QTY-DEPEND, UF, COD-REGION, NUM-NIS, IND-DOCS-OK | GRP-ADDRESS contains UF/COD-REGION |
| [VALBENEF](legacy-sifap/natural-programs/VALBENEF.NSN#L30), 30-38 | NUM-CPF, FULL-NAME, DT-BIRTH, SEX, UF, CEP, STAT-BENEFICIARY | GRP-ADDRESS contains UF/CEP; no body access |
| [VALDOCS](legacy-sifap/natural-programs/VALDOCS.NSP#L18), 18-24 | NUM-CPF, FULL-NAME, RG-NUMBER, UF, IND-DOCS-OK | GRP-ADDRESS contains UF; no body access |
| [CONSBENF](legacy-sifap/natural-programs/CONSBENF.NSP#L22), 22-40 | NUM-CPF, FULL-NAME, DT-BIRTH, SEX, STREET-ADDRESS, NUMBER, DISTRICT, CITY, UF, CEP, COD-REGION, STAT-BENEFICIARY, COD-PROGRAM, AMT-FAMILY-INCOME, QTY-DEPEND, NUM-NIS, DT-REGISTRATION | GRP-ADDRESS contains street through region |
| [RELPGT](legacy-sifap/natural-programs/RELPGT.NSP#L33), 33-37 | NUM-CPF, FULL-NAME, UF | GRP-ADDRESS contains UF |

### PROGRAM-V, VIEW OF SOCPROG

| Members / declaration evidence | Declared field subset |
|---|---|
| [BATCHPGT](legacy-sifap/natural-programs/BATCHPGT.NSP#L59), 59-65 | COD-PROGRAM, TYPE-PROGRAM, AMT-BASE-INDIVIDUAL, FACTOR-ADJUST, STAT-PROGRAM, MAX-PERCAP-INCOME |
| [CALCBENF](legacy-sifap/natural-programs/CALCBENF.NSN#L45), 45-50 | COD-PROGRAM, TYPE-PROGRAM, AMT-BASE-INDIVIDUAL, FACTOR-ADJUST, STAT-PROGRAM |
| [VALELEG](legacy-sifap/natural-programs/VALELEG.NSN#L33), 33-42 | COD-PROGRAM, NAME-PROGRAM, TYPE-PROGRAM, AMT-BASE-INDIVIDUAL, COD-ELIGIBILITY, STAT-PROGRAM, MAX-PERCAP-INCOME, AGE-MIN, AGE-MAX |
| [CADPROG](legacy-sifap/natural-programs/CADPROG.NSP#L15), 15-27 | COD-PROGRAM, NAME-PROGRAM, TYPE-PROGRAM, AMT-BASE-INDIVIDUAL, COD-ELIGIBILITY, DT-CREATION, DT-CLOSURE, STAT-PROGRAM, MAX-PERCAP-INCOME, AGE-MIN, AGE-MAX, FACTOR-ADJUST |

### PAYMENT-V, VIEW OF PAYMENT

| Members / declaration evidence | Declared field subset | Group context |
|---|---|---|
| [BATCHPGT](legacy-sifap/natural-programs/BATCHPGT.NSP#L44), 44-57 | NUM-PAYMENT, NUM-CPF, COD-PROGRAM, YEAR-MONTH-REF, AMT-GROSS, AMT-DISC-TOTAL, AMT-NET, DT-GENERATION, STAT-PAYMENT, TYPE-PAYMENT, AMT-BONUS, NUM-BATCH, SEQ-BATCH | Flat view |
| [CALCBENF](legacy-sifap/natural-programs/CALCBENF.NSN#L32), 32-43; [RELPGT](legacy-sifap/natural-programs/RELPGT.NSP#L20), 20-31 | NUM-PAYMENT, NUM-CPF, COD-PROGRAM, YEAR-MONTH-REF, AMT-GROSS, AMT-DISC-TOTAL, AMT-NET, DT-GENERATION, STAT-PAYMENT, TYPE-PAYMENT, AMT-BONUS | Same field set, source order differs |
| [BATCHREL](legacy-sifap/natural-programs/BATCHREL.NSP#L25), 25-35 | NUM-PAYMENT, NUM-CPF, COD-PROGRAM, YEAR-MONTH-REF, AMT-GROSS, AMT-DISC-TOTAL, AMT-NET, STAT-PAYMENT, TYPE-PAYMENT, AMT-BONUS | No generation-date field |
| [BATCHCON](legacy-sifap/natural-programs/BATCHCON.NSP#L23), 23-34 | NUM-PAYMENT, NUM-CPF, COD-PROGRAM, YEAR-MONTH-REF, AMT-GROSS, AMT-NET, STAT-PAYMENT, DT-GENERATION, DT-CREDIT, COD-BANK, COD-BANK-RETURN | Flat view |
| [CALCCORR](legacy-sifap/natural-programs/CALCCORR.NSP#L16), 16-27 | NUM-PAYMENT, NUM-CPF, YEAR-MONTH-REF, AMT-GROSS, AMT-DISC-TOTAL, AMT-NET, DT-GENERATION, STAT-PAYMENT, AMT-CORR, DT-CORR, IND-CORR | Flat view |
| [CALCDSCT](legacy-sifap/natural-programs/CALCDSCT.NSP#L15), 15-28 | NUM-PAYMENT, NUM-CPF, AMT-GROSS, AMT-DISC-TOTAL, YEAR-MONTH-REF, TYPE-DISC, AMT-DISC, PCT-DISC, DT-START-DISC, DT-END-DISC, NUM-CASE | GRP-DISC 1:8 contains last six fields |
| [CONSBENF](legacy-sifap/natural-programs/CONSBENF.NSP#L42), 42-51 | NUM-PAYMENT, NUM-CPF, YEAR-MONTH-REF, AMT-GROSS, AMT-DISC-TOTAL, AMT-NET, STAT-PAYMENT, TYPE-PAYMENT, DT-GENERATION | Flat view |

### AUDIT-V, VIEW OF AUDIT

The seven audit-copycode callers declare this common typed set:

```text
N15: NUM-AUDIT
N8: DT-EVENT
N6: HR-EVENT
N14: TS-EVENT
A2: COD-ACTION
A8: COD-MODULE, USR-EVENT
A80: DESCR-ACTION
A4: TYPE-ENTITY
A15: ID-ENTITY
A11: NUM-CPF-AFFECTED
A16: NAME-JOB-BATCH
A1: STAT-BATCH
```

Evidence: [BATCHPGT](legacy-sifap/natural-programs/BATCHPGT.NSP#L68), 68-81;
[BATCHCON](legacy-sifap/natural-programs/BATCHCON.NSP#L36), 36-51;
[CADBENEF](legacy-sifap/natural-programs/CADBENEF.NSP#L39), 39-52;
[CADDEPEN](legacy-sifap/natural-programs/CADDEPEN.NSP#L29), 29-42;
[CADPROG](legacy-sifap/natural-programs/CADPROG.NSP#L30), 30-43;
[CALCCORR](legacy-sifap/natural-programs/CALCCORR.NSP#L30), 30-43;
[CONSBENF](legacy-sifap/natural-programs/CONSBENF.NSP#L54), 54-67.
BATCHCON additionally declares `AMT-PREV` and `AMT-NEW`, both `A60`.

RELAUDIT has a different subset: `NUM-AUDIT N15`, `DT-EVENT N8`, `HR-EVENT N6`,
`USR-EVENT A8`, `COD-ACTION A2`, `TYPE-ENTITY A4`, `ID-ENTITY A15`,
`AMT-PREV A60`, `AMT-NEW A60`, `DESCR-ACTION A80`:
[RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L21), 21-31.

## Members without DEFINE DATA

CCAUDIT and CCVALCPF use the including member's declarations; their commented
required-field examples are not independent compiled data areas. Both bodies
were read and their conditions are covered in the catalogue.

The two JCLs have DD allocations, job parameters and in-stream Natural inputs,
not Natural variables. `&SYSUID` appears in JOB notification configuration:
[SIFAPJ01.jcl](legacy-sifap/natural-programs/SIFAPJ01.jcl#L35), 35-37;
[SIFAPJ02.jcl](legacy-sifap/natural-programs/SIFAPJ02.jcl#L38), 38-40.
Their record sizes and inputs are documented in the [dependency map](dependency-map.md).

## Review checks

- [x] Parameter, local, imported, view and copycode-required declarations are distinguished.
- [x] Names, formats and dimensions are retained, including apparently unused fields.
- [x] All 24 library members have declaration context or an explicit not-applicable explanation.
- [ ] Validate Natural compilation and physical numeric representation before translation.
