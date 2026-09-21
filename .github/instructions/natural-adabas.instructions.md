---
description: "Use when reading Natural/Adabas legacy code, language patterns, FDT structure, naming conventions, and batch workflows."
applyTo: "01-archaeology/legacy-sifap/**,**/*.NSP,**/*.nsp,**/*.NSN,**/*.nsn,**/*.NSS,**/*.nss,**/*.NSA,**/*.nsa,**/*.NSL,**/*.nsl,**/*.NSC,**/*.nsc,**/*.NSM,**/*.nsm,**/*.NSD,**/*.nsd,**/*.NAT,**/*.nat,**/*.CPY,**/*.cpy,**/*.DDM,**/*.ddm,**/*.jcl,**/*.JCL"
---

# Natural/Adabas legacy code - Reading guide

This file activates when you open Natural programs, Adabas DDMs, JCL, copycodes, or any file in `01-archaeology/legacy-sifap/`. It teaches how to read SIFAP (Payment Oversight and Administration System) legacy code: Natural program structure, CALLNAT and INCLUDE dependencies, Adabas FDTs, legacy naming, batch patterns, packed decimals, and a first-reading strategy. It does **not** decide modern module boundaries or JPA mappings, which belong to [`modular-monolith.instructions.md`](modular-monolith.instructions.md), and does not write EARS requirements or traceability records, which belong to [`sdd-artifacts.instructions.md`](sdd-artifacts.instructions.md).

## Natural program structure

A Natural program follows this skeleton:

```text
DEFINE DATA
  LOCAL
    01 #MY-VARIABLE  (A20)    /* A = alphanumeric, 20 characters */
    01 #COUNTER      (N5)     /* N = numeric, 5 digits */
    01 #AMOUNT       (P9.2)   /* P = packed decimal, 9 integer + 2 decimal digits */
    01 #RATES        (N3.4/1:27)  /* array: 27 occurrences of N3.4 */
  END-DEFINE

  /* Main logic here */

END
```

> **In this lab, the decimal separator in a format specification is a dot.**
> Natural Community Edition 9.3.3 compiles `(P9.2)` and `(N3.4)`. It rejects `(P9,2)` with `NAT0165`.
> Natural installations may vary with the decimal-character configuration; this immersion follows the Community Edition image.
> This rule applies only to the *declaration*; **literals also use a dot**: `MOVE 1.3500 TO #FATOR`.
> In arrays, the range is part of the notation: `(A60/1:10)`, `(N3.4/1:27)`, `(N3.6/1:10,1:12)`.

Important blocks:

| Block | Purpose |
|-------|---------|
| `DEFINE DATA LOCAL` | Variable declarations scoped to this program |
| `DEFINE DATA PARAMETER` | Input/output variables received from a caller |
| `DEFINE DATA GLOBAL` | Shared across programs in a session (rare and fragile) |
| `INPUT` | Reads from the terminal (online) or a sequential file (batch) |
| `DISPLAY` / `WRITE` | Screen or report output |
| `MAP` | Screen layout definition (terminal UI) |

## CALLNAT and PERFORM

- **`CALLNAT 'SUBPROG' parm1 parm2`**: calls an external subprogram (separate source file). Parameters are passed by reference unless marked `(AD=O)` for output only.
- **`PERFORM subroutine-name`**: calls an internal subroutine defined with `DEFINE SUBROUTINE ... END-SUBROUTINE` in the same program.

When mapping call chains, `CALLNAT` is essential because it crosses file boundaries.

## INCLUDE copycodes

`INCLUDE copycode-name` inserts a shared code fragment at compile time, like `#include` in C. Copycodes commonly contain:

- Shared data area definitions (Natural's "struct")
- Common validation routines
- Standard error handling blocks

When you encounter `INCLUDE`, locate the corresponding copycode to understand the complete data layout.

### Member extensions

A Natural library is **flat**: there are no subdirectories, and each member resolves by name, not path. The extension indicates the type:

| Extension | Type | Called by |
|----------|------|-------------|
| `.NSN` | Program or subprogram | executed by JCL or `CALLNAT` |
| `.NSA` | Parameter Data Area (PDA) | `PARAMETER USING` |
| `.NSL` | Local Data Area (LDA) | `LOCAL USING` |
| `.NSC` | Copycode | `INCLUDE` |
| `.NSM` | Map (3270 screen layout) | `INPUT USING MAP` |
| `.jcl` | Job Control Language | batch scheduler |

`CALLNAT`, `INCLUDE`, `PARAMETER USING`, and `LOCAL USING` **MUST NOT be ignored**: each incorporates code or declarations from another file. Reading a program in isolation is incomplete.

Natural member names are limited to 8 characters. In this corpus, the DDM/Natural member names are `BENEFIC`, `SOCPROG`, `PAYMENT`, and `AUDIT`. The Adabas file may still be described conceptually as a Beneficiary or Social Program file, and DDM field names retain their long names.

## Adabas FDT (Field Definition Table)

Every Adabas file has an FDT defining its fields. Think of it as the schema:

| Column | Meaning |
|--------|---------|
| Level | Hierarchical depth (01 = top level, 02+ = children) |
| Name | Two-character short name (AA, AB, AC...) |
| Format | `A` = alphabetic, `N` = numeric, `P` = packed, `B` = binary, `D` = date, `T` = time |
| Length | Field length in bytes |
| Descriptor | `DE` = searchable index, `MU` = multiple values (array), `PE` = periodic (repeating) group |

### MU fields (multiple values)

A field marked `MU` can contain multiple values (like an array). In Natural, it is accessed by index: `FIELD(1)`, `FIELD(2)`, etc. The FDT defines the maximum number of occurrences.

**Modern mapping**: JPA `@ElementCollection` or a PostgreSQL JSONB column.

### PE (periodic groups)

A `PE` group is a repeating group of related fields, like a row in an embedded table. For example, an address history where each occurrence has a street, city, and date.

**Modern mapping**: `@OneToMany` relationship with an embedded entity or a JSONB array.

### Superdescriptors

A superdescriptor combines multiple fields into a single searchable key (composite index). A notation such as `SU = AA + AB(1-4)` means "concatenate field AA with the first 4 bytes of AB".

**Modern mapping**: JPA `@Index(columnList = "col_a, col_b")`.

## 1990s naming conventions

Legacy Natural codebases use prefix-based names. Common patterns:

| Prefix pattern | Typical meaning |
|---|---|
| `BN-` or `BATCH-` | Batch program or batch-related variable |
| `PG-` or `PROG-` | Main program |
| `PS-` or `SUB-` | Subprogram (called by CALLNAT) |
| `AU-` or `AUT-` | Authorization- or audit-related |
| `#` prefix on variables | Local working variable (Natural convention) |
| `+` prefix on variables | Parameter variable passed by the caller |

These are conventions, not rules; verify in the code instead of assuming.

## Batch job patterns

Batch Natural programs commonly follow this structure:

```text
READ WORK FILE 1 record
  /* process each record */
  AT END OF DATA
    /* final totals / cleanup */
  END-ENDDATA
END-WORK
```

Control-break reports use:

```text
READ logical-file BY descriptor
  AT BREAK OF descriptor
    /* subtotal when the descriptor value changes */
  BEFORE BREAK PROCESSING
    /* detail line for each record */
  END-BREAK
END-READ
```

## Packed decimal handling

Packed decimal (format `P`) stores digits efficiently: each byte contains two digits, and the final nibble is the sign (C=positive, D=negative). It is common in financial calculations.

When mapping to Java, ALWAYS use `BigDecimal`, NEVER `double` or `float`. Packed fields in `P9.2` format mean 9 integer digits plus 2 decimal places → `BigDecimal` with `scale(2)`.

**On the mainframe, monetary values are packed (`P`), not `N`.** When reading the corpus, a monetary value declared as `N` is a warning: it may be an original author oversight or a deliberate mismatch between the program and the DDM. ALWAYS compare the program's format with that of the same field in the `.ddm`: type and length mismatches are a classic source of silent truncation and overflow.

## Reading strategy

When approaching a legacy program for the first time:

1. **Start with DEFINE DATA**: understand the variables and their types
2. **Find the main READ or FIND**: it reveals which data the program processes
3. **Trace CALLNAT calls**: these are the dependencies
4. **Look for INCLUDE copycodes**: they extend the data definitions
5. **Check AT BREAK / AT END OF DATA**: they reveal report or processing logic
6. **Record every ESCAPE or ON ERROR**: these are error handling paths
7. **Check `IF NO RECORDS FOUND`**: the `FIND ... IF NO RECORDS FOUND ... END-NOREC` block defines what happens when the search returns nothing; silent defaults hide here. View fields have values only **inside** the `FIND`/`READ` block.
8. **Compare `FIND ... WITH` against the DDM**: searches are possible only on fields marked as descriptors (`D`, `S`, or `H`) in the DDM listing. A search on a non-descriptor field does not compile.

## Conventions

| Rule | Rationale |
|---|---|
| In this lab, Natural declarations use dot decimal notation, such as `(P9.2)` | Comma notation, such as `(P9,2)`, fails with `NAT0165` in Natural CE 9.3.3 |
| Trace `CALLNAT`, `INCLUDE`, `PARAMETER USING`, and `LOCAL USING` | A Natural member read in isolation is incomplete |
| Compare program field formats against the corresponding DDM | Type and length mismatches can cause silent truncation or overflow |
| Map packed monetary fields to `BigDecimal` | `double` and `float` lose financial precision |
| Check descriptors before interpreting `FIND ... WITH` | Searches compile only on descriptor fields in the DDM |
| Treat prefixes as clues, not proof | Legacy conventions vary and must be checked in the code |

## Do / Don't

| Do | Don't |
|---|---|
| Start with `DEFINE DATA` to understand variables and types | Interpret business rules before knowing the data layout |
| Find the main `READ` or `FIND` to identify processed data | Assume the main file solely from the program name |
| Trace every `CALLNAT` dependency and `INCLUDE` copycode | Ignore external subprograms, PDAs, LDAs, copycodes, or maps |
| Check `AT BREAK`, `AT END OF DATA`, `ESCAPE`, and `ON ERROR` paths | Read only the program's happy path |
| Check `IF NO RECORDS FOUND` and view field scope in `FIND`/`READ` blocks | Assume missing records and view fields behave like normal variables |
| Compare `FIND ... WITH` against DDM descriptors | Assume a non-descriptor field is searchable |

## PR Checklist

- [ ] Relevant `DEFINE DATA` variables, arrays, parameters, and formats were recorded before summarizing behavior
- [ ] The main `READ`, `FIND`, work file, report, and control-break paths were identified
- [ ] Every `CALLNAT`, `INCLUDE`, `PARAMETER USING`, `LOCAL USING`, map, and JCL dependency was traced or recorded as open
- [ ] Program field formats were compared against the DDM for type, length, descriptor, MU, PE, and superdescriptor
- [ ] Packed decimal and monetary values were mapped or documented as `BigDecimal` candidates, never floating point
- [ ] Error, escape, no-records, end-of-data, and silent-default paths were included in extracted business rules
