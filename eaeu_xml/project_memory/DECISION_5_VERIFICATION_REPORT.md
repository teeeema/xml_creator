# Decision №5 verification report

Generated: 2026-08-20

## Source

`./15kr0005.doc`, Решение Коллегии ЕЭК от 27 января 2015 г. №5. SHA-256: `bca94f5db76962bf46f6f5569d2d18872dc6e5355b01bd77d79edb985263043e`. Source policy: READ ONLY.

## Summary

- total rules: 45
- verified: 45
- unresolved registry rules: 0
- implementation mismatches remaining: 0
- missing tests: 0
- mismatches found and fixed during audit: 5
- core status: `DECISION_5_CORE_VERIFIED_WITH_UNRESOLVED_ITEMS`

The remaining items are explicit source ambiguity or rules delegated to process/technical documents; no known internal implementation mismatch remains.

## Rule coverage

| Rule ID | Source | Implemented by | Tested by | Status |
|---|---|---|---|---|
| D5-NS-SOAP | пункт 18, таблица 1 | NamespaceRegistry | test_namespaces_match_decision_5_table_1 | VERIFIED |
| D5-NS-WSA | пункт 18, таблица 1 | NamespaceRegistry | test_namespaces_match_decision_5_table_1 | VERIFIED |
| D5-NS-INT | пункт 18, таблица 1 | NamespaceRegistry | test_namespaces_match_decision_5_table_1 | VERIFIED |
| D5-XML-ENVELOPE | пункты 19 и 26 | XmlSerializer | test_soap_serialization_is_well_formed_and_deterministic | VERIFIED |
| D5-HDR-TO | пункт 30 | HeaderValidator | test_forbidden_application_headers_raise_domain_errors | VERIFIED |
| D5-HDR-APP-REPLYTO | пункты 32, 34, 58 и 62 | HeaderValidator | test_forbidden_application_headers_raise_domain_errors | VERIFIED |
| D5-HDR-APP-FROM | пункт 58 | HeaderValidator | test_forbidden_application_headers_raise_domain_errors | VERIFIED |
| D5-HDR-APP-FAULTTO | пункт 58 | HeaderValidator | test_forbidden_application_headers_raise_domain_errors | VERIFIED |
| D5-ID-MESSAGE | пункт 36 и приложение №3 | MessageId/IdentifierService | test_message_and_conversation_ids_are_uuid_uris | VERIFIED |
| D5-ACTION-APPLICATION | пункты 38, 59 и 60 | ApplicationAction | test_action_build_parse_and_serialize | VERIFIED |
| D5-ID-PROCEDURE | пункт 39, таблица 3 и приложение №3 | ProcedureId | test_nested_procedure_id_is_immutable_and_roundtrips | VERIFIED |
| D5-ID-CONVERSATION | пункт 40, таблица 4 и приложение №3 | ConversationId | test_message_and_conversation_ids_are_uuid_uris | VERIFIED |
| D5-HDR-INTEGRATION | пункты 41–44 | HeaderValidator | test_forbidden_application_headers_raise_domain_errors | VERIFIED |
| D5-ADDR-FORMAT | пункты 45–47 | LogicalAddress | test_cp_ca_sr_address_roundtrip | VERIFIED |
| D5-ADDR-SEGMENT | пункт 48, таблица 6 | LogicalAddress | test_cp_ca_sr_address_roundtrip | VERIFIED |
| D5-ADDR-SPACE | пункт 49 | LogicalAddress | test_cp_ca_sr_address_roundtrip | VERIFIED |
| D5-ADDR-CP | пункты 50–53 | LogicalAddress | test_cp_ca_sr_address_roundtrip | VERIFIED |
| D5-ADDR-SR-GATE | пункт 56 | LogicalAddress | test_cp_ca_sr_address_roundtrip | VERIFIED |
| D5-CORR-INITIAL | пункт 102 | CorrelationService | test_initial_and_followup_correlation | VERIFIED |
| D5-CORR-FOLLOWUP | пункты 37 и 102 | TransactionStateMachine/CorrelationService | test_initial_and_followup_correlation | VERIFIED |
| D5-BODY-EXTERNAL | пункт 63 | BodyPayload | test_soap_serialization_is_well_formed_and_deterministic | VERIFIED |
| D5-INTEGRATION-STRUCTURE | пункты 41–42, таблица 5 | IntegrationPlatformContext | test_platform_integration | VERIFIED |
| D5-INTEGRATION-TRACK | пункт 43 | IntegrationPlatformContext | test_platform_integration | VERIFIED |
| D5-INTEGRATION-TIME | пункт 44 | IntegrationPlatformContext | test_platform_integration | VERIFIED |
| D5-SIGNAL-RCV | пункты 113–114 | SignalFactory/SignalValidator | test_signal_messages | VERIFIED |
| D5-SIGNAL-PRS | пункты 113 и 115 | SignalFactory/SignalValidator | test_signal_messages | VERIFIED |
| D5-SIGNAL-ERR | пункты 116–121 | SignalFactory/SignalValidator | test_signal_messages | VERIFIED |
| D5-SIGNAL-ACTION | пункты 114, 115 и 121 | SignalFactory/SignalValidator | test_signal_messages | VERIFIED |
| D5-SIGNAL-BODY | приложение №5, таблицы 1–5 | SignalPayload | test_error_signal_codes | VERIFIED |
| D5-FAULT-TO | пункт 66 | FaultFactory/FaultValidator | test_fault_header_and_xml_attributes | VERIFIED |
| D5-FAULT-CORRELATION | пункт 68 | FaultFactory/FaultValidator | test_fault_header_and_xml_attributes | VERIFIED |
| D5-FAULT-HEADER | пункт 69 | FaultFactory/FaultValidator | test_fault_header_and_xml_attributes | VERIFIED |
| D5-FAULT-ACTION | пункт 70 | FaultFactory/FaultValidator | test_fault_header_and_xml_attributes | VERIFIED |
| D5-FAULT-BODY | пункт 72, таблица 7 | FaultFactory/FaultValidator | test_fault_header_and_xml_attributes | VERIFIED |
| D5-FAULT-CODES | пункт 74, таблица 8 | FaultFactory/FaultValidator | test_fault_header_and_xml_attributes | VERIFIED |
| D5-FAULT-REASON | пункт 75 | FaultFactory/FaultValidator | test_fault_header_and_xml_attributes | VERIFIED |
| D5-FAULT-DETAIL | пункт 76 | ProblemMessage/SoapFault | test_fault_reason_and_problem_message | VERIFIED |
| D5-TRN-PARAMETERS | пункты 104–110 | TransactionParameters | test_invalid_transaction_parameters | VERIFIED |
| D5-TRN-RETRY | пункты 100, 105–110 | RetryService/RetryValidator | test_timeout_and_retry_metadata | VERIFIED |
| D5-TRN-MUTUAL | пункты 122–124 | TransactionStateMachine | test_mutual_obligations_full_sequence_and_rollback | VERIFIED |
| D5-TRN-QUESTION | пункты 125–126 | TransactionStateMachine | test_all_pattern_start_states | VERIFIED |
| D5-TRN-REQUEST | пункты 127–130 | TransactionStateMachine | test_guaranteed_request_response_and_invalid_transition | VERIFIED |
| D5-TRN-CONFIRMATION | пункты 131–135 | TransactionStateMachine | test_request_confirmation_guaranteed_completion | VERIFIED |
| D5-TRN-NOTIFICATION | пункты 136–137 | TransactionStateMachine | test_notification_and_distribution_completion | VERIFIED |
| D5-TRN-DISTRIBUTION | пункты 138–139 | TransactionStateMachine | test_notification_and_distribution_completion | VERIFIED |

## Transaction patterns

| Pattern | Start / sequence | Completion | Timeout / retry | Rollback |
|---|---|---|---|---|
| MUTUAL_OBLIGATIONS | request → RCV → PRS → response → RCV → PRS → final error window | processing-confirmation window expires without ERR | missing expected signal/response → retry while attempts remain | ERR → ROLLBACK_REQUIRED |
| QUESTION_RESPONSE | request → response | response received | response timeout → retry | external application rollback boundary |
| REQUEST_RESPONSE | without guarantee: request → response; guaranteed: request → optional RCV → PRS → response | response received | expected confirmation/response timeout → retry | external application rollback boundary |
| REQUEST_CONFIRMATION | without guarantee: request → response; guaranteed: request → response → RCV | response, or RCV when required | response/RCV failure → re-initiation while attempts remain | external application rollback boundary |
| NOTIFICATION | notification → RCV | RCV received | receive-confirmation timeout → retry | external application rollback boundary |
| INFORMATION_DISTRIBUTION | notification | immediately after send | no confirmation/response timeout | external application rollback boundary |

Transition correlation follows paragraph 102: the source is the message received by the participant at the preceding transaction stage, not arbitrary list adjacency. Retry is available only for an application message in a waiting/active state or following a technological Fault, while the configured repeat count remains.

## XML verification

Ten generated reference documents are stored in `examples/decision5/`. Tests parse all documents and structurally verify SOAP 1.2 namespaces, signal appendix 5 sequences, Fault attributes, Russian reason text and absence of attribute names as standalone elements. UUID values are intentionally not compared literally with appendix 3.

## Mismatches found and fixed

1. ProblemMessage changed from child XML content to string content representing the source XML; CDATA remains a recommendation, not a mandatory lexical requirement.
2. Correlation history no longer assumes that the previous list item is always the normative previous received stage.
3. Retry now rejects non-application records and forbidden states.
4. Fault validation now rejects a reused MessageID, wrong RelatesTo and wrong RelatesAction.
5. Duplicate Integration ownership rule was consolidated, and stale Stage 2 notes/source scope were corrected.

## Known delegated and unresolved items

- Header order follows paragraph 29 and appendix 3 deterministically, but no explicit schema sequence for the complete Header was found.
- Member-state, CA and non-`gate` SR membership depend on external registries/technical solutions.
- Duplicate detection and format-logical codes depend on a concrete common-process specification.
- Concrete retry payload reconstruction requires a Body model.
- CDATA is recommended for ProblemMessage; escaped string content preserves the parsed value but not CDATA lexical form.
- Transaction-level guaranteed delivery remains separate from MQ persistence; real transport is out of scope.

## Final status

`DECISION_5_CORE_VERIFIED_WITH_UNRESOLVED_ITEMS`

## Project autonomy addendum

The original 41-test self-containment suite and the current 56-test engine suite pass from the `eaeu_xml/` boundary. The normative source is local at `./15kr0005.doc`; external process packages are loaded only from an explicit caller-supplied Path.
