from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import ast
import re


class CoverageStatus(str, Enum):
    VERIFIED = "VERIFIED"
    IMPLEMENTED_NOT_TESTED = "IMPLEMENTED_NOT_TESTED"
    SOURCE_NOT_PRECISE = "SOURCE_NOT_PRECISE"
    IMPLEMENTATION_MISMATCH = "IMPLEMENTATION_MISMATCH"
    TEST_MISSING = "TEST_MISSING"
    NEEDS_EXTERNAL_SOURCE = "NEEDS_EXTERNAL_SOURCE"


@dataclass(frozen=True)
class RuleCoverage:
    rule_id: str
    source: str
    implemented_by: str
    tested_by: str
    status: CoverageStatus


def _mapping(rule_id: str) -> tuple[str, str]:
    mappings = (
        ("D5-NS-", "NamespaceRegistry", "test_namespaces_match_decision_5_table_1"),
        ("D5-XML-", "XmlSerializer", "test_soap_serialization_is_well_formed_and_deterministic"),
        ("D5-HDR-", "HeaderValidator", "test_forbidden_application_headers_raise_domain_errors"),
        ("D5-ID-MESSAGE", "MessageId/IdentifierService", "test_message_and_conversation_ids_are_uuid_uris"),
        ("D5-ID-PROCEDURE", "ProcedureId", "test_nested_procedure_id_is_immutable_and_roundtrips"),
        ("D5-ID-CONVERSATION", "ConversationId", "test_message_and_conversation_ids_are_uuid_uris"),
        ("D5-ACTION-", "ApplicationAction", "test_action_build_parse_and_serialize"),
        ("D5-ADDR-", "LogicalAddress", "test_cp_ca_sr_address_roundtrip"),
        ("D5-CORR-INITIAL", "CorrelationService", "test_initial_and_followup_correlation"),
        ("D5-CORR-FOLLOWUP", "TransactionStateMachine/CorrelationService", "test_initial_and_followup_correlation"),
        ("D5-BODY-", "BodyPayload", "test_soap_serialization_is_well_formed_and_deterministic"),
        ("D5-INTEGRATION-", "IntegrationPlatformContext", "test_platform_integration"),
        ("D5-SIGNAL-BODY", "SignalPayload", "test_error_signal_codes"),
        ("D5-SIGNAL-", "SignalFactory/SignalValidator", "test_signal_messages"),
        ("D5-FAULT-DETAIL", "ProblemMessage/SoapFault", "test_fault_reason_and_problem_message"),
        ("D5-FAULT-", "FaultFactory/FaultValidator", "test_fault_header_and_xml_attributes"),
        ("D5-TRN-PARAMETERS", "TransactionParameters", "test_invalid_transaction_parameters"),
        ("D5-TRN-RETRY", "RetryService/RetryValidator", "test_timeout_and_retry_metadata"),
        ("D5-TRN-MUTUAL", "TransactionStateMachine", "test_mutual_obligations_full_sequence_and_rollback"),
        ("D5-TRN-QUESTION", "TransactionStateMachine", "test_all_pattern_start_states"),
        ("D5-TRN-REQUEST", "TransactionStateMachine", "test_guaranteed_request_response_and_invalid_transition"),
        ("D5-TRN-CONFIRMATION", "TransactionStateMachine", "test_request_confirmation_guaranteed_completion"),
        ("D5-TRN-NOTIFICATION", "TransactionStateMachine", "test_notification_and_distribution_completion"),
        ("D5-TRN-DISTRIBUTION", "TransactionStateMachine", "test_notification_and_distribution_completion"),
        ("D5-TRN-", "TransactionStateMachine", "test_all_pattern_start_states"),
    )
    for prefix, implementation, test in mappings:
        if rule_id.startswith(prefix):
            return implementation, test
    return "", ""


class Decision5RuleCoverage:
    def __init__(self, rows: tuple[RuleCoverage, ...]) -> None:
        self.rows = rows

    @classmethod
    def build(cls, project_root: Path) -> "Decision5RuleCoverage":
        registry = project_root / "src/eaeu_xml/decision5/rules/source_rules.yaml"
        test_names: set[str] = set()
        for path in (project_root / "tests").glob("test_*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            test_names.update(node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"))
        rows = []
        for line in registry.read_text(encoding="utf-8").splitlines():
            match = re.search(r"rule_id:\s*([^,}]+)", line)
            if not match:
                continue
            rule_id = match.group(1).strip()
            source_match = re.search(r'source_paragraph:\s*"([^"]+)"', line)
            implementation, test = _mapping(rule_id)
            if not source_match:
                status = CoverageStatus.SOURCE_NOT_PRECISE
            elif not implementation:
                status = CoverageStatus.IMPLEMENTATION_MISMATCH
            elif not test:
                status = CoverageStatus.IMPLEMENTED_NOT_TESTED
            elif test not in test_names:
                status = CoverageStatus.TEST_MISSING
            else:
                status = CoverageStatus.VERIFIED
            rows.append(RuleCoverage(rule_id, source_match.group(1) if source_match else "", implementation, test, status))
        return cls(tuple(rows))

    @property
    def summary(self) -> dict[str, int]:
        return {
            "total_rules": len(self.rows),
            "verified": sum(row.status is CoverageStatus.VERIFIED for row in self.rows),
            "unresolved": sum(row.status in {CoverageStatus.SOURCE_NOT_PRECISE, CoverageStatus.NEEDS_EXTERNAL_SOURCE} for row in self.rows),
            "mismatches": sum(row.status is CoverageStatus.IMPLEMENTATION_MISMATCH for row in self.rows),
            "missing_tests": sum(row.status in {CoverageStatus.IMPLEMENTED_NOT_TESTED, CoverageStatus.TEST_MISSING} for row in self.rows),
        }

    def render_markdown(self) -> str:
        lines = ["| Rule ID | Source | Implemented by | Tested by | Status |", "|---|---|---|---|---|"]
        lines.extend(f"| {row.rule_id} | {row.source} | {row.implemented_by} | {row.tested_by} | {row.status.value} |" for row in self.rows)
        return "\n".join(lines)
