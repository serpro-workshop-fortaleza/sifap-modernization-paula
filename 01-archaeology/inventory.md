# Legacy inventory - [Team name]

> **Trail:** [Team kit](../README.md) > [Stage 1](README.md) > **Inventory**

**First Stage 1 artifact: structural orientation, not a program analysis.**

| Field | Value |
|---|---|
| Audience | Pair responsible for the initial inventory |
| Date | 2026-09-10 (UTC) |
| Responsible pair | [To be filled by the team] |
| Stage | Stage 1 - Archaeology, step 1 |
| Inspected directory | [01-archaeology/legacy-sifap/](legacy-sifap/) |
| Evidence | File and directory names, extensions, placement, and file sizes in bytes |
| Measurement status | Rechecked against filesystem metadata on 2026-09-10 (UTC) |
| Prerequisite | No individual-file reading before kickoff, assumed from the prompt; explicit team confirmation was not collected in this run |

> [!NOTE]
> This is the first analysis and will be revised during subsequent file reading.
> During this kickoff, no legacy file content was opened, including documentation,
> programs, DDMs, or JCL. No legacy files were modified. Evidence therefore cites paths and
> metadata, not source lines. Probable purposes and reading priorities are
> hypotheses, not confirmed behavior or dependencies.

## Directory structure

```text
01-archaeology/legacy-sifap/
|-- adabas-ddms/
|-- legacy-docs/
`-- natural-programs/
```

**Directory count: 4 including the root, or 3 subdirectories.**
There are no deeper directories or symbolic links in the inspected tree.

| Directory | Direct regular files |
|---|---:|
| [legacy-sifap/](legacy-sifap/) | 2 |
| [adabas-ddms/](legacy-sifap/adabas-ddms/) | 6 |
| [legacy-docs/](legacy-sifap/legacy-docs/) | 7 |
| [natural-programs/](legacy-sifap/natural-programs/) | 25 |
| **Total** | **40** |

All 40 entries counted below are regular files. Two are directly under the root;
38 have exactly one intervening directory. Depth does not distinguish a unique
outlier.

## File counts by type

Extension spelling and case are preserved. Probable purposes below reflect
general file-format conventions only; contents were not checked.

| Extension | Count | Probable purpose |
|---|---:|---|
| `.NSA` | 2 | Natural parameter data area (PDA) |
| `.NSC` | 2 | Natural copycode |
| `.NSL` | 1 | Natural local data area (LDA) |
| `.NSN` | 5 | Natural subprogram source |
| `.NSP` | 12 | Natural program source; extension alone does not distinguish batch from online |
| `.ddm` | 4 | Data Definition Module describing an Adabas view |
| `.docx` | 3 | Word-format documentation |
| `.jcl` | 2 | Job Control Language, commonly used for batch execution |
| `.md` | 8 | Markdown documentation |
| `.txt` | 1 | Plain-text file; its specific format is unverified |
| **Total** | **40** | **10 distinct extensions** |

No `.cpy`, `.map`, `.NSM`, or `.NSD` files were found. These zero counts describe
filenames only, not whether corresponding capabilities exist in the system.

The 25 files in `natural-programs/` comprise **22 Natural source/data/copycode
members, 2 JCL files, and 1 Markdown file**. Thus, the 24 non-documentation files
there should not all be described as Natural programs.

## Naming patterns

Grouping rule: for every regular file in the entire tree, take its basename,
remove its final extension, stop at the first `-`, `_`, or digit, and keep the
first three characters of the remaining leading segment. For example,
`BATCHCON.NSP` becomes `BAT` and `BUSINESS-RULES-2012.docx` becomes `BUS`.
No content is used and each file belongs to exactly one group.

The following are **all 12 groups with at least two files**:

| Prefix | Count | Hypothesis |
|---|---:|---|
| `BAT` | 3 | All names start with `BATCH`; candidate batch entry programs, not confirmed entry points |
| `BUS` | 2 | Same `BUSINESS-RULES-2012` basename in `.md` and `.docx`; equivalence and authority unverified |
| `CAD` | 3 | Unknown - investigate in the next stage |
| `CAL` | 3 | Unknown - investigate in the next stage |
| `ORI` | 2 | Same `ORIGINAL-ARCHITECTURE-1997` basename in `.md` and `.docx`; equivalence and authority unverified |
| `PDA` | 2 | Conventional parameter data area prefix, consistent with both `.NSA` extensions |
| `REA` | 4 | Repeated `README.md` names suggest documentation entry points at different directory levels |
| `REL` | 2 | Unknown - investigate in the next stage |
| `SIF` | 2 | Unknown - investigate in the next stage; both files have the `.jcl` extension |
| `SUB` | 2 | Conventional subprogram prefix, consistent with both `.NSN` extensions; callers are unknown |
| `TEC` | 2 | Same `TECHNICAL-MANUAL-SIFAP-2008` basename in `.md` and `.docx`; equivalence and authority unverified |
| `VAL` | 3 | Unknown - investigate in the next stage |

These groups account for 30 files. The ten singleton prefixes are `AUD`, `BEN`,
`CCA`, `CCV`, `CON`, `FDT`, `HOW`, `LDA`, `PAY`, and `SOC`, one file each.
This reconciles to 40 files without overlapping groups.

No names use the literal `BN-`, `PG-`, or `PS-` prefixes. Their absence does not
establish whether batch, online, or subprogram roles exist. Likewise, opaque
prefixes such as `CAD`, `CAL`, `REL`, and `VAL` must not be expanded into business
purposes without reading the files later.

## Unusual items (top three)

These are structural investigation candidates, not defects or confirmed
business mysteries. Selection uses the global maximum file size, the global
maximum filename length, and a unique extension in the data directory.

| # | File path, relative to the inspected root | Observed distinction | Suggested investigation, in a later reading session |
|---|---|---|---|
| 1 | [legacy-docs/ORIGINAL-ARCHITECTURE-1997.md](legacy-sifap/legacy-docs/ORIGINAL-ARCHITECTURE-1997.md) | Largest file in the entire tree: **30,041 bytes**. It has a same-basename `.docx` counterpart. | Check whether the two formats describe the same material and establish their provenance and authority; do not assume either is current. |
| 2 | [legacy-docs/TECHNICAL-MANUAL-SIFAP-2008.docx](legacy-sifap/legacy-docs/TECHNICAL-MANUAL-SIFAP-2008.docx) | Longest filename: **32 characters including extension**; **27,362 bytes**. | Investigate the dated naming/version convention and compare with the same-basename Markdown file. This is a document, so Natural member-name limits do not apply. |
| 3 | [adabas-ddms/FDT-150-BENEFICIARY.txt](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt) | The only `.txt` file: **6,961 bytes**, alongside four `.ddm` files. | Establish the actual text format and whether it relates to any DDM. `FDT` suggests a field-definition listing, but the number and name do not prove a file-number mapping. |

## Proposed reading order

This is a provisional order for **future** reading. No step below was performed
as part of this kickoff.

1. **Identify batch entry candidates.** Start with
   [SIFAPJ01.jcl](legacy-sifap/natural-programs/SIFAPJ01.jcl) and
   [SIFAPJ02.jcl](legacy-sifap/natural-programs/SIFAPJ02.jcl) to establish which
   members they actually reference. The names
   [BATCHCON.NSP](legacy-sifap/natural-programs/BATCHCON.NSP),
   [BATCHPGT.NSP](legacy-sifap/natural-programs/BATCHPGT.NSP), and
   [BATCHREL.NSP](legacy-sifap/natural-programs/BATCHREL.NSP) make them candidates,
   not proven targets of either job. Job numbering does not prove execution
   order. Defer detailed program logic until the data pass below.
2. **Read data definitions before detailed code.** Review all four DDM files:
   [AUDIT.ddm](legacy-sifap/adabas-ddms/AUDIT.ddm),
   [BENEFIC.ddm](legacy-sifap/adabas-ddms/BENEFIC.ddm),
   [PAYMENT.ddm](legacy-sifap/adabas-ddms/PAYMENT.ddm), and
   [SOCPROG.ddm](legacy-sifap/adabas-ddms/SOCPROG.ddm). This alphabetical listing
   is a neutral tie-breaker, not a dependency order. Include the unusual
   [text file](legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt) to determine its
   relationship, if any, to those definitions.
3. **Investigate possible shared members and name relationships.** The `.NSA`,
   `.NSL`, and `.NSC` extensions suggest supporting declarations or code.
   [PDACALC.NSA](legacy-sifap/natural-programs/PDACALC.NSA) shares `CALC` with
   the `CALC*` filenames; [PDAVALID.NSA](legacy-sifap/natural-programs/PDAVALID.NSA)
   shares `VAL` with the `VAL*` and `SUBVAL*` names. Treat these as navigation
   hints only. Read actual declarations and calls before recording an edge.
4. **Reorder programs using verified dependencies.** Continue through the
   confirmed batch members and the remaining `CAD*`, `CAL*`, `CONS*`, `REL*`,
   `SUB*`, and `VAL*` groups. Use
   [/map-dependencies](../.github/prompts/stage-archaeologist-map-dependencies.prompt.md)
   to trace actual references and then prioritize connected members.
   **The most connected program cannot be identified from filenames or sizes.**
   No filename match here establishes a `CALLNAT`, `INCLUDE`, or data-area
   dependency.
5. **Read documentation as context, not behavioral proof.** The root guides,
   directory READMEs, and paired documents under
   [legacy-docs/](legacy-sifap/legacy-docs/) can support subsequent reading.
   Reconcile any claims with observed source behavior. Use
   [/extract-business-rules](../.github/prompts/stage-archaeologist-extract-business-rules.prompt.md)
   for the later program-by-program investigation.

The team should revise this order once entry points and dependencies have been
traced. This inventory does not select modernization boundaries or conclude
Stage 1 discovery.

## Reproducing the measurements

Run these commands from the repository root with GNU `find`. They enumerate
metadata only; none opens legacy file contents.

```bash
# Directory tree and total, including the inspected root.
find 01-archaeology/legacy-sifap -type d -print | LC_ALL=C sort
find 01-archaeology/legacy-sifap -type d -printf '.\n' | wc -l

# Total regular files and case-sensitive extension counts.
find 01-archaeology/legacy-sifap -type f -printf '.\n' | wc -l
find 01-archaeology/legacy-sifap -type f -printf '%f\n' |
  awk '{n=split($0,a,"."); e=(n>1 ? "." a[n] : "[none]"); c[e]++}
       END {for(e in c) print e, c[e]}' | LC_ALL=C sort

# Direct file counts and depth relative to the inspected root.
find 01-archaeology/legacy-sifap -type f -printf '%h\n' |
  LC_ALL=C sort | uniq -c
find 01-archaeology/legacy-sifap -type f -printf '%P\n' |
  awk -F/ '{c[NF-1]++} END {for(d in c) print d, c[d]}' | sort -n

# All prefix groups, including singletons.
find 01-archaeology/legacy-sifap -type f -printf '%f\n' |
  awk '{sub(/\.[^.]*$/, ""); split($0,a,/[-_0-9]/);
        p=substr(a[1],1,3); c[p]++}
       END {for(p in c) print p, c[p]}' | LC_ALL=C sort

# File sizes and filename lengths, ranked independently.
find 01-archaeology/legacy-sifap -type f -printf '%s\t%P\n' |
  LC_ALL=C sort -k1,1nr
find 01-archaeology/legacy-sifap -type f -printf '%f\t%P\n' |
  awk -F '\t' '{print length($1), $2}' | LC_ALL=C sort -k1,1nr

# A blank result confirms that the inspected tree contains no symlinks.
find 01-archaeology/legacy-sifap -type l -print
```

## Kickoff completion checklist

- [x] All directories are shown, with root inclusion stated explicitly.
- [x] File and extension totals reconcile and can be reproduced with `find`.
- [x] At least three naming patterns are counted; 12 repeated groups are listed.
- [x] Exactly three unusual items have paths, measured evidence, and follow-up actions.
- [x] The proposed reading order is justified and explicitly provisional.
- [x] No legacy file contents were opened or modified during this kickoff.

### Continue reading

| Previous | Next |
|---|---|
| [Stage 1 guide](GUIDE.md)<br/><sub>Step-by-step schedule.</sub> | [Business rules catalog](business-rules-catalog.md)<br/><sub>Step 2 - extract rules after reading.</sub> |

<sub>[Back to the kit index](../README.md)</sub>
