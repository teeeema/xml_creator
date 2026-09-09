# Normative conflict report

| ID | Structure / MSG | Table | Page | Row | Reason code | Current interpretation | Why unresolved | Required source/action |
|---|---|---:|---:|---:|---|---|---|---|
| NORMATIVE_CONFLICT-001 | R.HC.MM.01.001 / MSG.002 | 19 | 219 | 22 | INTERNAL_NORMATIVE_CONFLICT | Rule names `hcsdo:ChildJuvenileIndicator` | Full-document search finds this identifier only in rule 22. Table 10 v1.1.0 separately defines `ChildIndicator` and `JuvenileIndicator`; no alias, note or version transition is stated | Official EEC corrigendum/amendment identifying the intended table-10 requisite |
| NORMATIVE_CONFLICT-002 | R.HC.MM.01.002 / MSG.023 | 21 | 298 | 4 | INTERNAL_NORMATIVE_CONFLICT | Rule names `DrugAttributeEnumText`, `AttributeKindCode`, `AttributeKindName` | The identifiers are visually present in table 21 but absent from the complete table 13 v1.1.0. They occur in other structures, without a cross-structure mapping rule | Official EEC corrigendum/amendment defining the intended R.HC.MM.01.002 requisites |
| NORMATIVE_CONFLICT-003 | R.HC.MM.01.002 / MSG.023 | 21 | 298 | 5 | INTERNAL_NORMATIVE_CONFLICT | Same absent identifiers plus required semantic value | Same internal table-21/table-13 contradiction; no alternate version is declared | Official EEC corrigendum/amendment |
| NORMATIVE_CONFLICT-004 | R.HC.MM.01.002 / MSG.024 | 22 | 300 | 6 | INTERNAL_NORMATIVE_CONFLICT | Rule names the same absent complex requisite and attributes | Original page visibly contains the identifiers; complete table 13 does not | Official EEC corrigendum/amendment |
| NORMATIVE_CONFLICT-005 | R.HC.MM.01.002 / MSG.024 | 22 | 300 | 7 | INTERNAL_NORMATIVE_CONFLICT | Rule names absent `AttributeKindCode` and `AttributeKindName` | No alias, transition or same-structure occurrence exists in Decision No. 68 | Official EEC corrigendum/amendment |
| P.MM.01.MSG.014.R2 | R.HC.MM.01.004 / MSG.014 | 22 | 235 | 2 | EXTERNAL_REGISTRY_FIELD_REFERENCE | Allowed values constrain the application-stage field used by the registry lookup | `ApplicationStatusCode` is intentionally not part of request structure R.HC.MM.01.004 | Registry data/context provider; does not block Body serialization |

No interpretation remains generically unresolved. The five conflicts are
retained as first-class normative conflicts and block only MSG.002, MSG.023 and
MSG.024 with runtime code `NORMATIVE_CONFLICT`. The 64
`EXTERNAL_CLASSIFIER_DATASET` rows are structurally verified and block only
classifier-membership validation, not XML hierarchy or serialization.
