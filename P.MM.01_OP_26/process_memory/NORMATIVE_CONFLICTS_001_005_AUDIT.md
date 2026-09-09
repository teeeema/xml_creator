# Local normative audit: NORMATIVE_CONFLICT-001 through -005

Audit date: 2026-08-25. Scope is restricted to the five named conflicts.
Only files already present in this workspace were used. In particular, no web
search or external normative source was used.

| Conflict | Affected area | Type | Local evidence sufficient | Can resolve | Production blocker |
|---|---|---|---|---|---|
| `001` | TRN.002 / MSG.002 / R.HC.MM.01.001 / rule R22 | `REAL_NORMATIVE_CONFLICT` | YES, to establish the conflict; NO, to choose a correction | NO | YES |
| `002` | TRN.016 / MSG.023 / R.HC.MM.01.002 / rule R4 | `REAL_NORMATIVE_CONFLICT` | YES, to establish the conflict; NO, to choose a correction | NO | YES |
| `003` | TRN.016 / MSG.023 / R.HC.MM.01.002 / rule R5 | `REAL_NORMATIVE_CONFLICT` | YES, to establish the conflict; NO, to choose a correction | NO | YES |
| `004` | TRN.015 / MSG.024 / R.HC.MM.01.002 / rule R6 | `REAL_NORMATIVE_CONFLICT` | YES, to establish the conflict; NO, to choose a correction | NO | YES |
| `005` | TRN.015 / MSG.024 / R.HC.MM.01.002 / rule R7 | `REAL_NORMATIVE_CONFLICT` | YES, to establish the conflict; NO, to choose a correction | NO | YES |

`YES` in the evidence column means that the supplied local material proves
that the two claims coexist and conflict. It does **not** mean that it proves
which text, field, or version must replace the other claim. The latter evidence
is `NOT_ENOUGH_LOCAL_EVIDENCE` for every case.

## Local source chain and runtime impact

The only primary process document available locally is
`normative_sources/err_22042022_68_doc.pdf`: Decision of the Collegium of the
EEC dated 19 April 2022 No. 68, amending Decision No. 122. Its locally recorded
SHA-256 is `a15cc6c946b35145e58304b7e3621ea76241f510e2202bbaf8912b4f8b0715e6`.
`DECISION_68_ANALYSIS.md` records 465 pages and states that the rule pages and
the complete requisite tables were visually audited from that local PDF.

All five rule records name `SRC-PMM01-068`, section IX, version context
`P.MM.01 1.1.0`. The active profile independently selects `1.1.0` for both
`R.HC.MM.01.001` and `R.HC.MM.01.002`. Thus this audit found no local evidence
of competing document editions or of a version-profile mismatch.

Runtime chain, verified from local code and tests:

`err_22042022_68_doc.pdf` -> SourceReference in MessageRule/StructureDefinition
-> `INTERNAL_NORMATIVE_CONFLICT` -> Body validation error
`NORMATIVE_CONFLICT` -> facade/process issue -> generation block.

`eaeu_xml/src/eaeu_xml/process_packages/body.py` converts each such rule to an
error. `test_catalog.py` verifies the exact five IDs and that only MSG.002,
MSG.023 and MSG.024 are blocked. The all-transactions matrix records the same
impact: TRN.002, TRN.015 and TRN.016 initiating branches are blocked. This is
not merely documentation; it prevents Body/XML generation for the affected
messages. It is independent of R.006/R.007 unresolved versions, classifier
datasets, `P.MM.01.MSG.014.R2`, and physical XSD availability.

## Conflict cards

### NORMATIVE_CONFLICT-001

**Affected**

- process: `P.MM.01`; transaction: `P.MM.01.TRN.002`; procedure: `P.MM.01.PRC.002`
- message: `P.MM.01.MSG.002`; structure: `R.HC.MM.01.001`, active version `1.1.0`
- rule: `P.MM.01.MSG.002.R22`; field/rule identifier: `hcsdo:ChildJuvenileIndicator`
- declaration: `message_rules/P.MM.01.MSG.002.yaml`, rule R22.

**Claim A.** The filling rule says that the requisite “Признак применимости
лекарственного препарата в ювенильном периоде”
(`hcsdo:ChildJuvenileIndicator`) is not filled.

**Local Source A.** `err_22042022_68_doc.pdf`; Decision No. 68 dated
19.04.2022; section IX; table 19, item 22, page 219; version context
`P.MM.01 1.1.0`. This exact source reference is stored with R22.

**Claim B.** The local definition of the same active structure has separate
`hcsdo:ChildIndicator` and `hcsdo:JuvenileIndicator` requisites; it has no
`ChildJuvenileIndicator` requisite.

**Local Source B.** The same local PDF; structure table 10 for
`R.HC.MM.01.001 v1.1.0`, reflected in
`structures/R.HC.MM.01.001/1.1.0.yaml`. The two rows are table 10 items
`2.4.2.3.2` (page 347) and `2.4.2.3.3` (page 348); the same pair also occurs
at items `2.4.3.2.3.2` and `2.4.3.2.3.3` on page 351. Structure identity is
table 8, item `R.HC.MM.01.001`, page 319. No local alias or transition note is
recorded.

**Classification and implementation.** `REAL_NORMATIVE_CONFLICT`, not a
demonstrated model error, mapping error, placeholder, or edition conflict. The
current code follows neither candidate: R22 is retained with empty
`field_paths`, marked `INTERNAL_NORMATIVE_CONFLICT`, and blocks MSG.002.

**Can resolve from local documents:** NO — `NOT_ENOUGH_LOCAL_EVIDENCE` to map
the combined name to either separate field, both fields, or another requisite.
An incorrect choice would silently change the meaning and validation of
TRN.002 XML.

**Required model/code change:** None in this audit. Retain the explicit rule
and its `NORMATIVE_CONFLICT` blocker until the missing local evidence exists.

### NORMATIVE_CONFLICT-002

**Affected**

- process: `P.MM.01`; transaction: `P.MM.01.TRN.016`; procedure: `P.MM.01.PRC.016`
- message: `P.MM.01.MSG.023`; structure: `R.HC.MM.01.002`, active version `1.1.0`
- rule: `P.MM.01.MSG.023.R4`; identifiers: `hcsdo:DrugAttributeEnumText`,
  `AttributeKindCode`, `AttributeKindName`
- declaration: `message_rules/P.MM.01.MSG.023.yaml`, rule R4.

**Claim A.** When `DrugAttributeEnumText` is populated, the rule requires
`AttributeKindCode` or `AttributeKindName` in it.

**Local Source A.** `err_22042022_68_doc.pdf`; Decision No. 68 dated
19.04.2022; section IX; table 21, item 4, page 298; version context
`P.MM.01 1.1.0`.

**Claim B.** The complete local requisite table for the same active structure
does not define those three identifiers in `R.HC.MM.01.002`.

**Local Source B.** The same local PDF; table 13 for
`R.HC.MM.01.002 v1.1.0`, represented by
`structures/R.HC.MM.01.002/1.1.0.yaml` (table begins page 414; its structure
identity is table 11, item `R.HC.MM.01.002`, page 413; requisite rows begin
page 415). The local audit records no same-structure alias, version transition,
or cross-structure mapping.

**Classification and implementation.** `REAL_NORMATIVE_CONFLICT`. Current
code does not import similarly named fields from another structure; it retains
R4 as an explicit conflict and blocks MSG.023.

**Can resolve from local documents:** NO — `NOT_ENOUGH_LOCAL_EVIDENCE` to add
the fields or redirect the rule. An incorrect resolution would manufacture an
unsupported Body shape or validation condition.

**Required model/code change:** None in this audit. Retain the explicit rule
and its `NORMATIVE_CONFLICT` blocker until the missing local evidence exists.

### NORMATIVE_CONFLICT-003

**Affected**

- process: `P.MM.01`; transaction: `P.MM.01.TRN.016`; procedure: `P.MM.01.PRC.016`
- message: `P.MM.01.MSG.023`; structure: `R.HC.MM.01.002`, active version `1.1.0`
- rule: `P.MM.01.MSG.023.R5`; identifiers: `hcsdo:DrugAttributeEnumText`,
  `AttributeKindCode`, `AttributeKindName`
- declaration: `message_rules/P.MM.01.MSG.023.yaml`, rule R5.

**Claim A.** For a populated `DrugAttributeEnumText`, the rule constrains the
code or name to “Номер документа основания”.

**Local Source A.** `err_22042022_68_doc.pdf`; Decision No. 68 dated
19.04.2022; section IX; table 21, item 5, page 298; version context
`P.MM.01 1.1.0`.

**Claim B.** Table 13 for the same `R.HC.MM.01.002 v1.1.0` has no local
definition of these identifiers.

**Local Source B.** Same file and table-13 evidence as conflict 002: table 13,
from page 414; structure identity table 11, item `R.HC.MM.01.002`, page 413.

**Classification and implementation.** `REAL_NORMATIVE_CONFLICT`. The current
implementation retains R5 with no guessed field path and blocks MSG.023.

**Can resolve from local documents:** NO — `NOT_ENOUGH_LOCAL_EVIDENCE` to
prove a target path and allowed semantic value. A wrong repair changes the
meaning of the expert-report decision data.

**Required model/code change:** None in this audit. Retain the explicit rule
and its `NORMATIVE_CONFLICT` blocker until the missing local evidence exists.

### NORMATIVE_CONFLICT-004

**Affected**

- process: `P.MM.01`; transaction: `P.MM.01.TRN.015`; procedure: `P.MM.01.PRC.015`
- message: `P.MM.01.MSG.024`; structure: `R.HC.MM.01.002`, active version `1.1.0`
- rule: `P.MM.01.MSG.024.R6`; identifiers: `hcsdo:DrugAttributeEnumText`,
  `AttributeKindCode`, `AttributeKindName`
- declaration: `message_rules/P.MM.01.MSG.024.yaml`, rule R6.

**Claim A.** When `DrugAttributeEnumText` is populated, R6 requires one of
`AttributeKindCode` or `AttributeKindName`.

**Local Source A.** `err_22042022_68_doc.pdf`; Decision No. 68 dated
19.04.2022; section IX; table 22, item 6, page 300; version context
`P.MM.01 1.1.0`.

**Claim B.** The local table 13 definition of `R.HC.MM.01.002 v1.1.0` lacks
the referenced requisite and attributes.

**Local Source B.** Same local PDF: table 13 from page 414; structure identity
table 11, item `R.HC.MM.01.002`, page 413. The complete local audit reports no
same-structure alias or alternative declared version.

**Classification and implementation.** `REAL_NORMATIVE_CONFLICT`. The current
implementation retains R6 as a conflict and blocks MSG.024 rather than adding
fields from a different structure.

**Can resolve from local documents:** NO — `NOT_ENOUGH_LOCAL_EVIDENCE` to
prove an intended requisite. A wrong repair produces an unsupported XML Body.

**Required model/code change:** None in this audit. Retain the explicit rule
and its `NORMATIVE_CONFLICT` blocker until the missing local evidence exists.

### NORMATIVE_CONFLICT-005

**Affected**

- process: `P.MM.01`; transaction: `P.MM.01.TRN.015`; procedure: `P.MM.01.PRC.015`
- message: `P.MM.01.MSG.024`; structure: `R.HC.MM.01.002`, active version `1.1.0`
- rule: `P.MM.01.MSG.024.R7`; identifiers: `AttributeKindCode`,
  `AttributeKindName`
- declaration: `message_rules/P.MM.01.MSG.024.yaml`, rule R7.

**Claim A.** If `AttributeKindCode` equals “другое”, R7 requires
`AttributeKindName`.

**Local Source A.** `err_22042022_68_doc.pdf`; Decision No. 68 dated
19.04.2022; section IX; table 22, item 7, page 300; version context
`P.MM.01 1.1.0`.

**Claim B.** Table 13 for the same active structure contains neither of these
attributes.

**Local Source B.** Same local PDF: table 13 from page 414; structure identity
table 11, item `R.HC.MM.01.002`, page 413. No local alias, transition, or
same-structure occurrence is recorded.

**Classification and implementation.** `REAL_NORMATIVE_CONFLICT`. Current
code retains R7 as an explicit conflict and blocks MSG.024.

**Can resolve from local documents:** NO — `NOT_ENOUGH_LOCAL_EVIDENCE` to
assign a parent/requisite for the attributes. A wrong choice changes a
conditional requiredness rule.

**Required model/code change:** None in this audit. Retain the explicit rule
and its `NORMATIVE_CONFLICT` blocker until the missing local evidence exists.

## MISSING_LOCAL_EVIDENCE

No supplied local file establishes which side is the intended authoritative
correction. The following evidence is required before a BLOCKED state could be
removed; it was not searched for outside the workspace.

| Conflict | Missing assertion | Required local document/evidence | Why BLOCKED cannot be removed |
|---|---|---|---|
| `001` | Whether `ChildJuvenileIndicator` is a valid requisite, an alias, or must map to one/both separate indicators | Official corrigendum/amendment or explicitly applicable replacement table for table 10, identifying R22/table 19 | No safe target field can be inferred. |
| `002` | Parent/path and existence of the three rule-4 identifiers in R.HC.MM.01.002 | Official corrigendum/amendment or replacement of table 13 explicitly linked to table 21 item 4 | The rule cannot be implemented without inventing Body fields. |
| `003` | Same identifiers and the intended “Номер документа основания” constraint | Official correction/replacement explicitly linked to table 21 item 5 | The condition has no proven target. |
| `004` | Parent/path and existence of the R6 requisite and attributes | Official correction/replacement explicitly linked to table 22 item 6 | No safe XML/validation rule can be constructed. |
| `005` | Parent/path and existence of the two R7 attributes | Official correction/replacement explicitly linked to table 22 item 7 | Requiredness cannot be attached to an unproved field. |

## Final status

```text
NORMATIVE_CONFLICT_001_CLASSIFIED = YES
NORMATIVE_CONFLICT_002_CLASSIFIED = YES
NORMATIVE_CONFLICT_003_CLASSIFIED = YES
NORMATIVE_CONFLICT_004_CLASSIFIED = YES
NORMATIVE_CONFLICT_005_CLASSIFIED = YES
ALL_CONFLICTS_HAVE_LOCAL_SOURCE_EVIDENCE = YES
SAFE_TO_FIX_CONFLICT_001 = NO
SAFE_TO_FIX_CONFLICT_002 = NO
SAFE_TO_FIX_CONFLICT_003 = NO
SAFE_TO_FIX_CONFLICT_004 = NO
SAFE_TO_FIX_CONFLICT_005 = NO
SAFE_TO_REMOVE_ANY_NORMATIVE_CONFLICT_BLOCKER = NO
EXTERNAL_WEB_SEARCH_USED = NO
P.MM.01_PRODUCTION_READY = NO
```

No production rule, structure, version profile, Decision No. 5 component, XML
serializer, session artifact, or GUI file was changed by this audit.
