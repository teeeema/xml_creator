# Unresolved rules

## PROMPT_RULE_CONFLICTS_WITH_DECISION_5 — ProcedureID representation

- Prompt concept: slash-separated bare UUID values.
- Decision №5: paragraph 39 defines UUID components; appendix 3 serializes each component as `urn:uuid:<UUID>`.
- Implemented: the document representation.

## PROMPT_RULE_CONFLICTS_WITH_DECISION_5 — Message code prefix in Action

- Prompt proposed that message_code must have the same process prefix.
- Appendix 3 example combines process `P.SP.03` with message `P.CC.04.MSG.003`.
- Implemented: syntax validation of message_code without same-prefix restriction; procedure and transaction remain consistent with process_code.

## Header XML order

- Known: paragraph 29 lists Header elements and the application example shows an order.
- Missing: an explicit statement that this listing is an XML sequence constraint.
- Current deterministic serializer mirrors paragraph 29; status: NEEDS_CLARIFICATION before claiming schema-level order.

## CA and non-gate SR identifier registries

- Decision №5 defines spaces and confirms `gate`, but external lists/technical solutions govern other identifiers.
- Current result: structural validation only; identifier membership unverified.
- Status: NEEDS_EXTERNAL_SOURCE.

## Member-state membership

- Decision №5 references ISO 3166-1 alpha-2 but does not provide a member-state code registry.
- Current result: alpha-2 syntax only.
- Status: NEEDS_EXTERNAL_SOURCE.

## Duplicate detection

- Paragraph 101 delegates duplicate control to application data and technological documents of a common process.
- No universal hash/MessageID duplicate detector is implemented.
- Status: NEEDS_PROCESS_SPECIFIC_RULES.

## Format-logical signal error codes

- Paragraph 119 delegates the exact rule code to the information-interaction regulation.
- Common codes are typed; nonempty external rule codes are accepted.
- Status: NEEDS_PROCESS_SPECIFIC_RULES.

## ProblemMessage lexical CDATA

- Paragraph 76 recommends embedding the source message as CDATA in int:ProblemMessage.
- The safe model accepts well-formed XML and serializes its complete XML representation as the text value of int:ProblemMessage.
- CDATA is explicitly recommended, not required. Escaped text has the same parsed string value.
- Status: VERIFIED_RECOMMENDATION; lexical CDATA form intentionally not claimed.

## Retry payload reconstruction

- Paragraph 100 confirms a new MessageID for a repeated message. The document does not define a universal payload-copy API across concrete process bodies.
- Retry metadata preserves the transaction and original Action; concrete payload reconstruction remains external.
- Status: NEEDS_PROCESS_SPECIFIC_RULES.

## Transport-specific guaranteed delivery

- Transaction-level confirmations/timeouts are modeled. Persistent MQ delivery and transport behavior are separate and not implemented.
- Status: OUT_OF_STAGE_3_SCOPE.

## Final audit status

No known internal implementation mismatch remains. Header ordering ambiguity and rules delegated to registries, technical solutions or concrete common-process documents require the final status `DECISION_5_CORE_VERIFIED_WITH_UNRESOLVED_ITEMS` rather than an unconditional production claim.
# Restored-session Body and retry XML persistence

Snapshot v1 intentionally excludes Body values. P.MM.01 proves that a response
may require the request EDocId for Body EDocRefId correlation after restart.
Also, runtime retry records do not currently retain/reconstruct the Body payload
needed for final retry XML. SOAP runtime restore remains correct, but full
production session continuation is blocked until these application persistence
boundaries are explicitly designed without mixing Body and SOAP identifiers.
