# Session persistence final audit

Дата: 2026-08-25.

Fresh application restart was verified with a bundle containing snapshot and
historical artifacts. TRN.004 request artifact preserves `EDocId`; restored
response gets the same `EDocRefId` from that artifact, not SOAP RelatesTo.
Payload-backed retry uses the original immutable Body with a new SOAP MessageID,
preserved ProcedureID/ConversationID and correct retry_of link. Continuous and
restored response/retry semantic Body/Header invariants pass. Invalid/missing/
corrupt artifacts block payload retry with no fallback to current form.

The outcome covers session persistence only. It does not resolve P.MM.01
normative conflicts, unresolved structure versions, external classifiers/sources
or unavailable XSD.

SOAP_SESSION_RESTORE_PROVEN = YES

HISTORICAL_BODY_PERSISTENCE_PROVEN = YES

EDOC_REFERENCE_AFTER_RESTORE_PROVEN = YES

RETRY_XML_AFTER_RESTORE_PROVEN = YES

CONTINUOUS_VS_RESTORED_RESPONSE_EQUIVALENT = YES

CONTINUOUS_VS_RESTORED_RETRY_EQUIVALENT = YES

SESSION_PERSISTENCE_END_TO_END_PROVEN = YES

SAFE_FOR_PRODUCTION_SESSION_CONTINUATION = YES
