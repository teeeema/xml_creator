# Shared Engine Capability Wave — Next OP Rules

Engine capability and normative closure are intentionally separated below.

## OP23 — technically engine-unblocked

| Requirement | Engine capability | Engine status | Remaining blocker |
| --- | --- | --- | --- |
| `P.SP.03.MSG.007.REQ.036` | TYPED_DATE | ENGINE_UNBLOCKED | Production/source mapping must still be applied and proved before closure. |
| `P.SP.03.MSG.014.REQ.039` | TYPED_DATE | ENGINE_UNBLOCKED | Production/source mapping must still be applied and proved before closure. |
| `P.SP.03.MSG.004.REQ.007` | CONDITIONAL_CROSS_INSTANCE | ENGINE_UNBLOCKED_BUT_SOURCE_BLOCKED | Classifier-dependent semantics/source evidence remain unresolved. |
| `P.SP.03.MSG.011.REQ.007` | CONDITIONAL_CROSS_INSTANCE | ENGINE_UNBLOCKED_BUT_SOURCE_BLOCKED | Classifier-dependent semantics/source evidence remain unresolved. |
| `P.SP.03.MSG.004.REQ.034` | SET_EQUIVALENCE | ENGINE_UNBLOCKED_BUT_SOURCE_BLOCKED | Classifier-dependent semantics/source evidence remain unresolved. |
| `P.SP.03.MSG.011.REQ.034` | SET_EQUIVALENCE | ENGINE_UNBLOCKED_BUT_SOURCE_BLOCKED | Classifier-dependent semantics/source evidence remain unresolved. |
| `P.SP.03.MSG.023.REQ.019` | DECODED_BINARY_BYTE_LENGTH | ENGINE_UNBLOCKED_BUT_SOURCE_BLOCKED | “5 MB” threshold interpretation remains unresolved; engine intentionally has no hardcoded threshold. |
| `P.SP.03.MSG.024.REQ.019` | DECODED_BINARY_BYTE_LENGTH | ENGINE_UNBLOCKED_BUT_SOURCE_BLOCKED | “5 MB” threshold interpretation remains unresolved; engine intentionally has no hardcoded threshold. |

## OP49 — technically engine-unblocked

| Requirement group | Engine capability | Engine status | Remaining blocker |
| --- | --- | --- | --- |
| `P.DS.01.MSG.002.REQ.006` | CALENDAR_MONTH_RELATION | ENGINE_UNBLOCKED_BUT_SOURCE_BLOCKED | Exact source/XSD/QName evidence remains required before production mapping. |
| `P.DS.01.MSG.005.REQ.023/.029/.036` | CONTEXT_SCOPED_AGGREGATE | ENGINE_UNBLOCKED_BUT_SOURCE_BLOCKED | Exact source/XSD/QName evidence remains required. |
| `P.DS.01.MSG.006.REQ.019/.025/.032` | CONTEXT_SCOPED_AGGREGATE | ENGINE_UNBLOCKED_BUT_SOURCE_BLOCKED | Exact source/XSD/QName evidence remains required. |
| `P.DS.01.MSG.005.REQ.041` + `REQ.042–054` | CONTEXT_RELATIVE_SELECTOR + DECIMAL | ENGINE_UNBLOCKED_BUT_SOURCE_BLOCKED | Applicability/source/XSD exact-QName blockers remain. REQ.041 governs applicability/existence. |
| `P.DS.01.MSG.005.REQ.003` | Existing ALL_EQUAL composition | ALREADY_EXISTING_ENGINE_CAPABILITY / SOURCE_BLOCKED | Source conflict and XSD/QName evidence remain unresolved. |
| `P.DS.01.MSG.006.REQ.008` | Existing singleton reduction; no MAX primitive required | ALREADY_EXISTING_ENGINE_CAPABILITY / SOURCE_BLOCKED | Source conflict and XSD/QName evidence remain unresolved. |

## Remaining engine blockers

`OP49_STILL_ENGINE_BLOCKED: None identified among the requirement shapes targeted by this shared-engine wave.`

This statement is limited to engine expressiveness. It does not close any source, classifier, QName, XSD, production-mapping, or proof blocker.
