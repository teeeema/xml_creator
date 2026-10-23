# OP35.1 / P.TS.01 — Initial audit final

STATUS: COMPLETE_WITH_EXPLICIT_SOURCE_GAPS

## Scope

Audit scope is restricted to `/Users/tema/Documents/Work/Документы_xml/35.1 ОП.pdf` and the process `P.TS.01` concerning the unified register of issued conformity certificates and registered declarations of conformity. No facts from other parts of common process No. 35 were used to fill gaps.

## Confirmed inventory

- ACT: 5
- PRC: 6
- OPR: 14 directly source-confirmed; the PRC.002 operation table is absent from the scoped PDF copy and is recorded as a source gap.
- TRN: 6 directly source-confirmed; no TRN.003 is inferred.
- MSG: 11 source-confirmed catalog entries; MSG.004-.006 are not inferred.
- Structures: 5
- Structure field rows: 389
- Atomic requirements: 1196

## Requirement atomization proof

- Field rows by structure: {'R.004': 42, 'R.006': 10, 'R.007': 11, 'R.TR.TS.01.001': 307, 'R.TR.TS.01.002': 19}
- Requirement atoms by structure: {'R.004': 122, 'R.006': 23, 'R.007': 30, 'R.TR.TS.01.001': 973, 'R.TR.TS.01.002': 48}
- Requirement atoms by kind: {'CARDINALITY': 389, 'PATTERN': 56, 'ISO_8601': 41, 'ISO_639_1': 6, 'REFERENCE_DATA': 74, 'MIN_LENGTH': 217, 'MAX_LENGTH': 217, 'NORMALIZED_STRING': 169, 'MAX_DIGITS': 7, 'NONNEGATIVE_INTEGER': 6, 'ANY_NAMESPACE': 2, 'ALWAYS_VALIDATE': 2, 'ISO_IEC_9834_8': 4, 'MAX_FRACTION_DIGITS': 1, 'BOOLEAN_ENUM': 5}
- CARDINALITY atoms: 389 (expected 389 from 389 field rows)
- Recovered source prefix QName/attribute token on field rows: 387/389; unresolved rows remain explicit and no Clark QName is synthesized.
- Duplicate canonical IDs: 0
- Orphan requirements by unknown structure: 0
- Classifier dependencies absent from `09_CLASSIFIERS.csv`: 0
- Pattern rows with detected cross-column QName/type bleed: 0

`field_path` in `08_REQUIREMENTS.csv` is an audit source-row locator (`structure/table/row/QName`), not a synthesized normative XML XPath.

## Source/material blockers

- `P.TS.01.PRC.002`: the PDF confirms the procedure and participants but the promised detailed transaction table is absent before the next approved document begins. Missing OPR/TRN/MSG codes and semantics are not reconstructed.
- XSD files: 0 found locally for the 5 declared structures; all 5 remain missing.
- Generic structures `R.004`, `R.006`, `R.007` use placeholder version `Y.Y.Y`.
- Imported base/domain model versions `X.X.X` / `Z.Z.Z` are unresolved.
- Classifier/reference payload identifiers, registry codes, versions and decision metadata are not established by the scoped PDF unless explicitly stated; unknown values remain `UNKNOWN`.
- Decision No. 5 is referenced, but concrete P.TS.01 integration-header and Action/routing values are not established by this PDF.
- Current revision No.109 dated 23.09.2024 is confirmed; its effective calendar date is not established by this scoped source.

## Integrity

- OPR -> PRC orphan count: 0
- TRN -> PRC/OPR orphan count: 0
- MSG -> unknown structure orphan count: 0
- MSG transaction links explicitly marked `UNRESOLVED_SOURCE_GAP`: 11/11
- SOURCE_CONFLICT records: 0
- External dependencies: 7

## Implementability

All 11 source-confirmed messages are `BLOCKED_BY_XSD_MODEL` at this audit boundary. `READY_FOR_IMPLEMENTATION = 0`, `PARTIAL_IMPLEMENTABLE = 0`, `GOLDEN_READY = 0`.

Recommended first message after material closure: `P.TS.01.MSG.002` because it uses the comparatively small `R.007` structure. Before implementation, obtain a concrete `R.007` version/XSD, required imported base-model package(s), the required classifier/reference payloads for its fields, and the source-confirmed P.TS.01 integration-header/routing contract.
