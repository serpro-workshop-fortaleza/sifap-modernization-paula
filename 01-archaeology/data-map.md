# Adabas data map - source evidence

> **Trail:** [Team kit](../README.md) > [Stage 1](README.md) > **Data map**

**Field-level reading of all four DDMs and the supplied physical FDT.**

| Field | Value |
|---|---|
| Date / team | 2026-09-10 / [To be filled by the team] |
| Scope | 4 DDMs, 1 FDT; no live database inspection |
| Coverage | 199 value-bearing field declarations, including MU fields; 7 group declarations; 14 derived descriptors |
| Evidence | DDM field rows and physical source lines; historical comments are not current production facts |
| Decision boundary | No PostgreSQL schema, migration, constraint or business-domain decision is approved here |

## Reading conventions

`A` is alpha, `N` is Natural numeric, `P` is packed numeric. DDM decimal lengths
such as `9,2` are transcribed below as `9.2` for comparison with source notation,
not as an independently verified SQL precision or physical byte allocation.
Storage `N` means null suppression, `F` fixed storage, `-` no marker.
Descriptor `U` means unique, `D` ordinary, `S` superdescriptor, `H` hyperdescriptor,
`P` phonetic. These letters belong to different columns and are not interchangeable.
An `M` declaration is a multiple-value field; a `P` group is a periodic group.
Bounds are the supplied view's declarations, not a universal Adabas limit.

## Files and keys

| DDM | DBID / FNR | Unique descriptors | Fields / groups / derived | Source |
|---|---|---|---|---|
| BENEFIC | 057 / 150 | AA registration, AB CPF, AM NIS, AN benefit number | 69 / 2 / 5 | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L31), 31-166 |
| SOCPROG | 057 / 151 | AA program code | 41 / 2 / 1 | [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L20), 20-116 |
| PAYMENT | 057 / 152 | AA payment number | 57 / 1 / 4 | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L26), 26-145 |
| AUDIT | 057 / 153 | AA audit number | 32 / 2 / 4 | [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L23), 23-118 |

All four specify default sequence `AA`. Other file numbers in program comments
do not override these bindings. Unique descriptor declarations are not proof
that a program assigns a valid identifier or enforces cross-file relationships.

## BENEFIC fields

Source: [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L39), 39-140.
Each row below preserves the short field name, logical name, format and markers.

| DB | Logical name | Format / group | Storage / descriptor | Source remark or grouping |
|---|---|---|---|---|
| AA | NUM-REGISTRATION | N11 | - / U | Alternate registration key |
| AB | NUM-CPF | A11 | - / U | Unformatted CPF |
| AC | FULL-NAME | A60 | N / - | Official name |
| AD | MOTHER-NAME | A60 | N / - | Remark says required, storage is suppressed |
| AE | FATHER-NAME | A60 | N / - | Optional |
| AF | DT-BIRTH | N8 | - / D | YYYYMMDD |
| AG | SEX | A1 | F / - | M/F/I |
| AH | MARITAL-STAT | A1 | F / - | S/C/D/V/U |
| AI | RG-NUMBER | A15 | N / - | Identity document |
| AJ | RG-AGENCY | A10 | N / - | Issuing authority |
| AK | RG-UF | A2 | N / - | Issuing state |
| AL | RG-DT-ISSUE | N8 | N / - | YYYYMMDD |
| AM | NUM-NIS | N11 | N / U | NIS/PIS-PASEP |
| AN | NUM-BENEFIT | N13 | N / U | Grant number |
| BA | GRP-ADDRESS | G, level 1 | - / - | BB-BJ are level 2 |
| BB | STREET-ADDRESS | A60 | N / - | Street |
| BC | NUMBER | A10 | N / - | Alphanumeric address number |
| BD | ADDRESS-COMPL | A30 | N / - | Complement |
| BE | DISTRICT | A40 | N / - | Address group |
| BF | CITY | A40 | N / - | Address group |
| BG | UF | A2 | - / D | State |
| BH | CEP | N8 | N / - | Postal code |
| BI | COD-IBGE | N7 | N / - | Municipality |
| BJ | COD-REGION | A2 | - / D | Remark says 01-05 or 99 |
| CA | COD-PROGRAM | A4 | - / D | Program reference |
| CB | DT-REGISTRATION | N8 | - / D | YYYYMMDD |
| CC | DT-START-BENEF | N8 | - / - | YYYYMMDD |
| CD | DT-END-BENEF | N8 | - / - | Zero means no end |
| CE | STAT-BENEFICIARY | A1 | F / D | A/S/C/I/D |
| CF | REASON-STAT | A3 | N / - | External/internal code table not supplied |
| CG | DT-LAST-STAT | N8 | N / - | YYYYMMDD |
| CH | AMT-FAMILY-INCOME | P9.2 | N / - | Declared family income |
| CI | QTY-FAMILY-MEMBERS | N2 | - / - | Household count |
| CJ | IND-PERCAP-INCOME | P7.2 | N / - | Calculated per-person income |
| CK | QTY-DEPEND | N2 | N / - | Remark says active count |
| CL | IND-DOCS-OK | A1 | F / - | S/N |
| DA | GRP-DEPEND | PE 1:10 | - / - | DB-DG are repeated together |
| DB | CPF-DEPEND | A11 | N / - | CPF or all-zero value |
| DC | NAME-DEPEND | A60 | N / - | Dependent group |
| DD | DT-BIRTH-DEPEND | N8 | N / - | YYYYMMDD |
| DE | RELATION | A2 | F / - | FI/CJ/NT/TU |
| DF | STAT-DEPEND | A1 | F / - | A/I/D |
| DG | IND-DISABILITY | A1 | F / - | S/N |
| EA | PHONE-LANDLINE | A14 | N / - | Formatted phone |
| EB | PHONE-MOBILE | A15 | N / - | Formatted mobile |
| EC | EMAIL | A80 | N / - | Notification email |
| ED | NUM-PHONE | A15, MU 1:5 | N / - | Additional phones |
| FA | IND-BIOMETRICS | A1 | F / - | S/N/P |
| FB | DT-COLLECT-BIO | N8 | N / - | YYYYMMDD |
| FC | COD-STATION-BIO | A6 | N / - | Collection station |
| FD | DIGITAL-HASH | A64 | N / - | Remark says not implemented |
| GA | DT-INSERT | N8 | - / D | YYYYMMDD |
| GB | HR-INSERT | N6 | - / - | HHMMSS |
| GC | USR-INSERT | A8 | N / - | Natural login |
| GD | DT-LAST-UPDATE | N8 | N / - | YYYYMMDD |
| GE | HR-LAST-UPDATE | N6 | N / - | HHMMSS |
| GF | USR-LAST-UPDATE | A8 | N / - | Natural login |
| GG | NUM-VERSION | N5 | - / - | Remark says concurrency control |
| HA | COD-BANK | A3 | N / D | FEBRABAN code |
| HB | COD-BRANCH | A6 | N / - | Branch |
| HC | NUM-ACCOUNT | A13 | N / - | Account with check digit |
| HD | TYPE-ACCOUNT | A1 | F / - | C/P/S |
| HE | IND-PORTABILITY | A1 | F / - | S/N |
| IA | IND-DEATH | A1 | F / D | S/N, SISOBI remark |
| IB | DT-DEATH | N8 | N / - | Zero means not provided |
| IC | COD-REASON-BLOCK | A2 | N / D | Code table not supplied |
| ID | IND-JUDICIAL | A1 | F / - | S/N |
| IE | NUM-CASE | A20 | N / - | Court case |
| IG | COD-PAYER-AGENCY | N5 | N / D | Paying agency; no IF field declared |
| JA | IND-LEGAL-REPRESENTATIVE | A1 | F / - | S/N |
| JB | CPF-REPRESENTATIVE | A11 | N / D | Representative CPF |

## PAYMENT fields

Source: [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L34), 34-121.

| DB | Logical name | Format / group | Storage / descriptor | Source remark or grouping |
|---|---|---|---|---|
| AA | NUM-PAYMENT | N15 | - / U | Unique sequence |
| AB | NUM-CPF | A11 | - / D | Beneficiary CPF |
| AC | NUM-REGISTRATION | N11 | N / - | Beneficiary registration |
| AD | COD-PROGRAM | A4 | - / D | Program |
| AE | YEAR-MONTH-REF | N6 | - / D | YYYYMM |
| AF | NUM-CYCLE | N6 | - / D | Processing cycle |
| BA | AMT-GROSS | P9.2 | - / - | Gross |
| BB | AMT-NET | P9.2 | - / - | Gross minus discount |
| BC | AMT-DISC-TOTAL | P7.2 | N / - | Discount total |
| BD | AMT-BONUS | P9.2 | N / - | Allowance |
| CA | GRP-DISC | PE 1:8 | - / - | CB-CG repeat together |
| CB | TYPE-DISC | A3 | N / - | IR/JD/CS/PA/EM/TX/OU/EX |
| CC | AMT-DISC | P7.2 | N / - | Fixed amount |
| CD | PCT-DISC | P3.2 | N / - | Percentage |
| CE | NUM-CASE | A20 | N / - | If JD |
| CF | DT-START-DISC | N8 | N / - | YYYYMMDD |
| CG | DT-END-DISC | N8 | N / - | Zero means undefined |
| DA | STAT-PAYMENT | A1 | F / D | P pending, G generated, E issued, C confirmed, D returned, X canceled, R reprocessed |
| DB | DT-GENERATION | N8 | - / D | Generation date |
| DC | HR-GENERATION | N6 | - / - | HHMMSS |
| DD | DT-ISSUE | N8 | N / - | Sent to bank |
| DE | DT-CONFIRMATION | N8 | N / - | Bank response |
| DF | DT-CANCELLATION | N8 | N / - | If applicable |
| DG | REASON-CANCELLATION | A3 | N / - | Code table not supplied |
| EA | COD-BANK | A3 | N / D | FEBRABAN |
| EB | COD-BRANCH | A6 | N / - | Branch |
| EC | NUM-ACCOUNT | A13 | N / - | Account |
| ED | TYPE-ACCOUNT | A1 | F / - | C/P |
| EE | COD-OPERATION | A3 | N / - | Caixa operation |
| EF | DT-CREDIT | N8 | N / D | Account credit date |
| EG | TYPE-PAYMENT | A1 | F / D | N normal, R retroactive, A allowance, C correction |
| FA | NUM-OB-SIAFI | A12 | N / - | Bank order |
| FB | NUM-NE-SIAFI | A12 | N / - | Commitment note |
| FC | COD-UG-ISSUER | A6 | N / - | Management unit |
| FD | COD-MANAGEMENT | A5 | N / - | Management code |
| FE | STAT-INTEG-SIAFI | A1 | F / - | I/P/E |
| FF | NUM-BATCH | N8 | - / D | Remittance batch |
| FG | SEQ-BATCH | N6 | - / - | Batch sequence |
| GA | DT-RECONCIL | N8 | N / - | Reconciliation date |
| GB | STAT-RECONCIL | A1 | F / - | C/D/P/N |
| GC | AMT-RECONCILED | P9.2 | N / - | Bank-confirmed amount |
| GD | COD-BANK-RETURN | A2 | N / D | Return code |
| GE | DESCR-BANK-RETURN | A40 | N / - | Return description |
| GF | DT-RETURN | N8 | N / - | Return date |
| GG | IND-REVERSAL | A1 | F / - | S/N |
| GH | NUM-PAYMENT-ORIGIN | N15 | N / D | Original payment reference |
| GI | AMT-CORR | P9.2 | N / - | Correction amount |
| GJ | DT-CORR | N8 | N / - | Correction date |
| GK | IND-CORR | A1 | F / - | S/N |
| HA | HASH-REMITTANCE-FILE | A64 | N / - | SHA-256 text |
| HB | HASH-RETURN-FILE | A64 | N / - | SHA-256 text |
| HC | COD-OCCURRENCE | A3, MU 1:10 | N / - | Bank occurrences |
| IA | DT-INSERT | N8 | - / - | YYYYMMDD |
| IB | HR-INSERT | N6 | - / - | HHMMSS |
| IC | USR-INSERT | A8 | N / - | Login |
| ID | DT-LAST-UPDATE | N8 | N / - | YYYYMMDD |
| IE | HR-LAST-UPDATE | N6 | N / - | HHMMSS |
| IF | USR-LAST-UPDATE | A8 | N / - | Control field |

## SOCPROG fields

Source: [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L28), 28-98.

| DB | Logical name | Format / group | Storage / descriptor | Source remark or grouping |
|---|---|---|---|---|
| AA | COD-PROGRAM | A4 | - / U | Program key |
| AB | NAME-PROGRAM | A60 | - / - | Official name |
| AC | ACRONYM-PROGRAM | A10 | N / - | Acronym |
| AD | TYPE-PROGRAM | A1 | F / D | A/T/P |
| AE | RESPONSIBLE-AGENCY | A10 | N / - | Agency |
| AF | CREATION-LAW | A20 | N / - | Law/decree reference |
| AG | DT-CREATION | N8 | - / - | YYYYMMDD |
| AH | DT-CLOSURE | N8 | - / - | Zero means active |
| AI | STAT-PROGRAM | A1 | F / D | A/I/E |
| BA | AMT-BASE-INDIVIDUAL | P7.2 | - / - | Per-person base |
| BB | AMT-BASE-FAMILY | P7.2 | - / - | Per-family base |
| BC | AMT-CEILING-BENEF | P9.2 | - / - | Maximum benefit |
| BD | AMT-FLOOR-BENEF | P7.2 | - / - | Minimum benefit |
| BE | PCT-ANNUAL-ADJUST | P3.2 | N / - | Annual percentage |
| BF | DT-LAST-ADJUST | N8 | N / - | YYYYMMDD |
| BG | FACTOR-K | P5.4 | N / - | Explicitly undocumented in remarks |
| BH | FACTOR-ADJUST | P3.4 | N / - | Base adjustment |
| CA | MAX-PERCAP-INCOME | P7.2 | - / - | Per-person ceiling |
| CB | AGE-MIN | N3 | - / - | Zero means no bound |
| CC | AGE-MAX | N3 | - / - | Zero means no bound |
| CD | IND-REQUIRES-CHILDREN | A1 | F / - | S/N |
| CE | QTY-MIN-CHILDREN | N2 | - / - | Conditional on CD |
| CF | IND-REQUIRES-SCHOOL | A1 | F / - | S/N |
| CG | IND-REQUIRES-VACCINE | A1 | F / - | S/N |
| CH | IND-REQUIRES-PRENATAL | A1 | F / - | S/N |
| CI | IND-REQUIRES-BIOMETRICS | A1 | F / - | S/N |
| CJ | COD-ELIGIBILITY | A5 | N / D | Ticket reference, not a complete grammar |
| DA | GRP-CALC-BAND | PE 1:5 | - / - | DB-DF repeat together |
| DB | INCOME-START | P7.2 | N / - | Band start |
| DC | INCOME-END | P7.2 | N / - | Band end |
| DD | FACTOR-MULTIPLIER | P3.4 | N / - | Multiplier |
| DE | AMT-ADDITIONAL | P7.2 | N / - | Fixed supplement |
| DF | IND-ACCUM | A1 | F / - | S accumulates prior band |
| EA | TYPE-DISC-APPLIC | A3, MU 1:8 | N / - | IR/JD/CS/PA/EM/TX/OU/EX |
| FA | GRP-REGIONAL-PARAM | PE 1:6 | - / - | Five regions plus special |
| FB | COD-REGION | A2 | N / - | 01-05 or 99 |
| FC | FACTOR-REGIONAL | P3.4 | N / - | Multiplier |
| FD | AMT-REG-COMPLEMENT | P7.2 | N / - | Fixed supplement |
| FE | IND-ACTIVE-REGION | A1 | F / - | S/N |
| GA | DT-INSERT | N8 | - / - | YYYYMMDD |
| GB | USR-INSERT | A8 | N / - | Control field |
| GC | DT-LAST-UPDATE | N8 | N / - | YYYYMMDD |
| GD | USR-LAST-UPDATE | A8 | N / - | Control field |

## AUDIT fields

Source: [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L31), 31-94.
Before/after groups contain independent MU arrays, not a single periodic group.
Their positional pairing and count consistency are not guaranteed by this listing.

| DB | Logical name | Format / group | Storage / descriptor | Source remark or grouping |
|---|---|---|---|---|
| AA | NUM-AUDIT | N15 | - / U | Unique sequence |
| AB | DT-EVENT | N8 | - / D | YYYYMMDD |
| AC | HR-EVENT | N6 | - / - | HHMMSS |
| AD | TS-EVENT | N14 | N / - | YYYYMMDDHHMMSS |
| AE | NUM-TRANSACTION | A8 | N / D | CICS transaction |
| BA | COD-ACTION | A2 | F / D | IN/AL/EX/CO/LG/LO/BT/ER/AU/RE |
| BB | COD-MODULE | A8 | N / - | Natural member name |
| BC | DESCR-ACTION | A80 | N / - | Description |
| CA | TYPE-ENTITY | A4 | - / D | BENF/PGTO/PROG/ADMN/SIST |
| CB | ID-ENTITY | A15 | - / D | Entity identifier |
| CC | NUM-CPF-AFFECTED | A11 | N / D | CPF if applicable |
| DA | GRP-BEFORE | G, level 1 | - / - | DB/DC at level 2 |
| DB | FIELD-UPDATED-PREV | A30, MU 1:20 | N / - | Field names |
| DC | VALUE-PREV | A80, MU 1:20 | N / - | Prior values |
| DD | GRP-AFTER | G, level 1 | - / - | DE/DF at level 2 |
| DE | FIELD-UPDATED-AFTER | A30, MU 1:20 | N / - | Field names |
| DF | VALUE-AFTER | A80, MU 1:20 | N / - | New values |
| DG | AMT-PREV | A60 | N / - | Scalar, coexists with DC |
| DH | AMT-NEW | A60 | N / - | Scalar, coexists with DF |
| EA | USR-EVENT | A8 | - / D | Natural login |
| EB | NAME-USER | A40 | N / - | Full name |
| EC | COD-PROFILE | A3 | N / - | ADM/OPR/CON/AUD/SUP |
| ED | COD-ASSIGNMENT | A10 | N / - | Organizational unit |
| EE | IP-ORIGIN | A15 | N / - | Origin address text |
| EF | ID-SESSION | A20 | N / - | Session identifier |
| EG | COD-TERMINAL | A8 | N / D | Terminal |
| EH | COD-LU | A8 | N / - | VTAM LU |
| FA | NUM-CYCLE-BATCH | N6 | N / - | Cycle |
| FB | NUM-SEQ-BATCH | N10 | N / - | Cycle sequence |
| FC | NAME-JOB-BATCH | A16 | N / - | Job name |
| FD | STAT-BATCH | A1 | F / - | S/E/W |
| FE | DESCR-ERR-BATCH | A120 | N / - | Error message |
| GA | ID-CORRELATION | A36 | N / - | Composite-operation UUID |
| GB | NUM-SEQ-CORRELATION | N3 | N / - | Sequence within operation |

## Derived descriptors

| File / DB | Name | Format / kind | Composition as listed | Evidence |
|---|---|---|---|---|
| BENEFIC PN | PHON-NAME | A20 / phonetic | AC | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L144), 144-145 |
| BENEFIC SA | YEAR-BIRTH | N4 / subdescriptor | AF(1-4) | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L146), 146-147 |
| BENEFIC S2 | SUPER-UF-STAT | A3 / super | BG(1-2), CE(1-1) | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L148), 148-149 |
| BENEFIC S3 | SUPER-PROG-STAT | A5 / super | CA(1-4), CE(1-1) | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L150), 150-151 |
| BENEFIC H1 | HYPER-BAND-ELIG | A6 / hyperexit 03 | AF, CJ | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L152), 152-153 |
| PAYMENT SA | YEAR-REF | N4 / subdescriptor | AE(1-4) | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L125), 125-126 |
| PAYMENT S1 | SUPER-CPF-PERIOD | A17 / super | AB(1-11), AE(1-6) | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L127), 127-128 |
| PAYMENT S2 | SUPER-PROG-PERIOD-STAT | A11 / super | AD(1-4), AE(1-6), DA(1-1) | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L129), 129-130 |
| PAYMENT S3 | SUPER-CYCLE-STAT | A7 / super | AF(1-6), DA(1-1) | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L131), 131-132 |
| SOCPROG S2 | SUPER-TYPE-STAT | A2 / super | AD(1-1), AI(1-1) | [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L102), 102-103 |
| AUDIT SA | YEAR-MONTH-EVENT | N6 / subdescriptor | AB(1-6) | [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L98), 98-99 |
| AUDIT S1 | SUPER-DATE-ACTION | A10 / super | AB(1-8), BA(1-2) | [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L100), 100-101 |
| AUDIT S2 | SUPER-ENTITY-DATE | A27 / super | CA(1-4), CB(1-15), AB(1-8) | [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L102), 102-103 |
| AUDIT S3 | SUPER-USR-DATE | A16 / super | EA(1-8), AB(1-8) | [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L104), 104-105 |

No supplied member implements hyperexit 03. A descriptor name alone does not
establish its executable rule. S1 on PAYMENT is not marked unique; the batch's
existence check is distinct from a uniqueness guarantee for concurrent writers.

## Physical FDT cross-check

The entire [FDT listing](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L1),
1-156, was read. Its timestamp is 2018-03-14, not a measurement of today's system.

| Surface | Observation | Evidence / question |
|---|---|---|
| File identity | DB 057, FNR 150; physical names AA..IG rather than long logical names | [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L4), 4-6, 13-87 |
| Formats | Physical `U` denotes unpacked numeric; `DE,UQ` denotes a unique descriptor. `NU` and `FI` are storage options. | [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L97), 97-107 |
| Packed lengths | CH is 5 physical bytes with remark `9,2`; CJ is 4 with remark `7,2` | [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L44), 44-46; confirm precision/scale against the target Natural runtime before translating |
| Groups | BA is GR; DA is PE; ED is MU. Listed maxima are DA=10 and ED=5; a separate historical hard-limit line says 191. | [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L27), 27-36; [groups](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L55), 55-65; [limits](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L119), 119-121 |
| Derived definitions | PN, SA, S2, S3, H1 match the listed DDM compositions | [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L89), 89-95 |
| Missing physical rows | DDM JA/JB legal-representative fields have no corresponding row in the supplied FDT | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L139), 139-140 versus [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L81), 81-95; which extract is authoritative? |
| Storage semantics | Warning says suppressed empty values are not in the index; populated mandatory business fields cannot be inferred from suppression flags | [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L144), 144-154 |
| Historical statistics | Counts, ISN capacity, compression, encryption and extraction estimates are statements in the archived listing | [FDT](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt#L113), 113-146; no live verification or current sizing conclusion |

## Relationships observed

| Relationship | Evidence | What is not established |
|---|---|---|
| BENEFIC.COD-PROGRAM to SOCPROG.COD-PROGRAM | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L302), 302-318 | No database foreign-key enforcement or create-time program validation inferred |
| PAYMENT.NUM-CPF to BENEFIC.NUM-CPF | [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L154), 154-161 | Orphans are possible from this reader's perspective; data population not inspected |
| PAYMENT.COD-PROGRAM from BENEFIC | [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP#L476), 476-478 | It does not prove historical program ownership or referential enforcement |
| BENEFIC.GRP-DEPEND embedded in holder | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L191), 191-203 | No separate dependent file or unique dependent constraint inferred |
| AUDIT entity/type and affected CPF | [CCAUDIT.NSC](legacy-sifap/natural-programs/CCAUDIT.NSC#L82), 82-90 | Polymorphic reference, not a verified FK; correlation fields are not populated here |
| PAYMENT.NUM-PAYMENT-ORIGIN to payment | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L102), 102 | Declared meaning only; no supplied writer proves reversal linkage |

## Cross-source questions

Every row is an open question; neither side is silently chosen as correct.

| ID | Question and observed difference | Code evidence | Data evidence |
|---|---|---|---|
| DM-01 | Which domain owns dependent relationship codes: code FI/CO/IR/OU or DDM FI/CJ/NT/TU? | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L152), 152-156 | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L91), 91-92 |
| DM-02 | How should ten stored dependent slots, the `>5` addition guard and the active-count label be reconciled? | [CADDEPEN.NSP](legacy-sifap/natural-programs/CADDEPEN.NSP#L117), 117-120, 191-203 | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L81), 81-94 |
| DM-03 | Is undefined sex `I` valid, or should entry/validation permit only M/F? | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L182), 182-186 | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L45), 45 |
| DM-04 | Do region codes identify five macroregions or the 27 table positions used by calculations? | [LDASIFAP.NSL](legacy-sifap/natural-programs/LDASIFAP.NSL#L34), 34-46 | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L66), 66; [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L84), 84-91 |
| DM-05 | Is the income ceiling per family or per person; should household count/per-capita fields participate? | [VALELEG.NSN](legacy-sifap/natural-programs/VALELEG.NSN#L174), 174-180 | [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L56), 56; [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L78), 78-80 |
| DM-06 | What connects local K `.347215`, stored `FACTOR-K`, stored adjustment, regional PE and calculation bands? | [CADPROG.NSP](legacy-sifap/natural-programs/CADPROG.NSP#L124), 124-139; [CALCBENF.NSN](legacy-sifap/natural-programs/CALCBENF.NSN#L258), 258-266 | [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L47), 47-52, 67-91 |
| DM-07 | Which payment status meanings apply: bank code sets P as paid and E as reversed, while DDM labels differ? | [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP#L204), 204-227 | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L60), 60-62 |
| DM-08 | Are payment types N/D/T or N/R/A/C? | [RELPGT.NSP](legacy-sifap/natural-programs/RELPGT.NSP#L170), 170-179 | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L79), 79-80 |
| DM-09 | How do three-character deduction codes map to local single-character J/P/I/S/A processing? | [CALCDSCT.NSP](legacy-sifap/natural-programs/CALCDSCT.NSP#L125), 125-174 | [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm#L51), 51-56; [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm#L78), 78-82 |
| DM-10 | What writes documentation approval, mother name, household count, biometrics, death/block fields, version and audit profile when these excerpts do not? | [CADBENEF.NSP](legacy-sifap/natural-programs/CADBENEF.NSP#L271), 271-328; [CCAUDIT.NSC](legacy-sifap/natural-programs/CCAUDIT.NSC#L82), 82-98 | [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm#L39), 39-140; [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L74), 74-81 |
| DM-11 | What resolves audit CO/CN/DV meanings and the exclusion of EX? | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L130), 130-182 | [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L39), 39-49, 134-145 |
| DM-12 | Do historical audit partitions 154-156 exist and belong in requested reports? Only FNR 153 has a supplied DDM. | [RELAUDIT.NSP](legacy-sifap/natural-programs/RELAUDIT.NSP#L111), 111-123 | [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm#L142), 142-145 |

## Verification and review

- [x] Read each DDM and the FDT to its end, including legends and historical notes.
- [x] Reconcile the field inventory with 199 source declarations, 7 groups and 14 derived descriptors.
- [x] Keep ordinary groups, PE groups and MU arrays distinct.
- [x] Record every source-side descriptor and the actual query relationships.
- [ ] Human owners validate each cross-source question and physical precision interpretation.
- [ ] Obtain runtime/compiler evidence before asserting compatibility of all views and assignments.

Related: [Business rule candidates](business-rules-catalog.md),
[dependency map](dependency-map.md), [open questions](mysteries-found.md).