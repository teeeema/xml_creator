"""Data-driven P.MM.01 E2E matrix support; contains no transaction mappings."""

from dataclasses import dataclass
from pathlib import Path
from uuid import UUID
from xml.etree import ElementTree as ET

from eaeu_xml.core.errors import UnresolvedStructureVersionError
from eaeu_xml.decision5.models import ConversationId, MessageId, ProcedureId, ProcedureInstance, TransactionInstance
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.services.message_factory import MessageFactory
from eaeu_xml.services.logical_address_builder import LogicalAddressBuilder
from eaeu_xml.services.xml_serializer import XmlSerializer


PACKAGE = Path(__file__).parents[1]
EXAMPLES = PACKAGE / "examples/all_transactions"


def participant_address(engine, participant_code):
    participant=engine.participants[participant_code]
    segment=participant.fixed_segment if participant.segment_policy == "FIXED" else participant.test_segment
    return LogicalAddressBuilder().build_common_process(segment=segment,process_code=engine.process.process_code,participant_code=participant_code)


class FixedIdentifierService:
    def __init__(self, start: int) -> None:
        self.next_value = start

    def _uuid(self) -> UUID:
        value = UUID(int=self.next_value)
        self.next_value += 1
        return value

    def new_procedure_component(self) -> UUID: return self._uuid()
    def new_conversation_id(self) -> ConversationId: return ConversationId(self._uuid())
    def new_message_id(self) -> MessageId: return MessageId(self._uuid())


def sample_value(field):
    datatype = (field.datatype or "").lower()
    if field.kind == "ARBITRARY_XML": return ET.Element("{urn:test:external}Payload")
    if "indicator" in datatype: return True
    if "datetime" in datatype: return "2026-08-24T00:00:00"
    if datatype.endswith("datetype"): return "2026-08-24"
    if "quantity" in datatype or "integer" in datatype: return 1
    if "unifiedcountry" in datatype: return "RU"
    return "TEST"


def test_values(engine, message_code: str) -> dict:
    """Build the smallest generic value tree satisfying structure and MessageRules."""
    structure = engine.get_structure(message_code,mode=GenerationMode.TEST)
    by_path = {field.path: field for field in structure.fields}
    by_id = {field.field_id: field for field in structure.fields}
    parent_ids = {field.parent for field in structure.fields if field.parent}
    values = {}

    def add(field):
        values.setdefault(field.path, None if field.field_id in parent_ids else sample_value(field))

    # Top-down structural closure.
    present_ids = set()
    for field in sorted(structure.fields, key=lambda item: item.order):
        if (field.min_occurs or 0) > 0 and (field.parent is None or field.parent in present_ids):
            add(field)
            present_ids.add(field.field_id)

    # Message-required optional branches, including their ancestors.
    rules = engine.rules.get(message_code)
    for path, usage in (rules.field_usage.items() if rules else ()):
        if usage != "REQUIRED" or path not in by_path:
            continue
        current = by_path[path]
        while current:
            add(current)
            current = by_id.get(current.parent)

    # Required descendants of branches introduced by MessageRules.
    for _ in range(3):
        present_ids = {field.field_id for field in structure.fields if field.path in values or any(path.startswith(field.path + "/") for path in values)}
        for field in sorted(structure.fields, key=lambda item: item.order):
            if (field.min_occurs or 0) > 0 and (field.parent is None or field.parent in present_ids):
                add(field)

    message = engine.get_message(message_code)
    suffix = int(message_code.rsplit(".", 1)[-1])
    for field in structure.fields:
        if field.xml_name == "InfEnvelopeCode": values[field.path] = message_code
        elif field.xml_name == "EDocCode": values[field.path] = message.structure_id
        elif field.xml_name == "EDocId": values[field.path] = f"00000000-0000-0000-0000-{suffix:012d}"
    return values


@dataclass(frozen=True)
class BranchResult:
    transaction_code: str
    procedure_code: str
    branch: str
    message_code: str
    structure_id: str
    active_version: str | None
    strict_status: str
    test_status: str
    status: str
    blocking_rule: str
    source_refs: tuple[str, ...]
    xml: str | None = None
    request_message_id: str | None = None
    response_message_id: str | None = None
    request_edoc_id: str | None = None

    @property
    def transaction_short(self): return self.transaction_code.rsplit(".", 1)[-1]


def source_ids(*items) -> tuple[str, ...]:
    return tuple(dict.fromkeys(ref.source_id for item in items for ref in item.source_refs))


def classify(engine, message_code, values):
    try:
        test = engine.validate_body(message_code, values, mode=GenerationMode.TEST)
    except UnresolvedStructureVersionError:
        return "UNRESOLVED_STRUCTURE_VERSION", "UNRESOLVED_STRUCTURE_VERSION", "UNRESOLVED_STRUCTURE_VERSION", "UNRESOLVED_STRUCTURE_VERSION"
    try:strict = engine.validate_body(message_code, values, mode=GenerationMode.STRICT)
    except UnresolvedStructureVersionError:strict=None
    test_errors = [issue for issue in test.issues if issue.severity.value == "ERROR"]
    strict_errors = [issue for issue in strict.issues if issue.severity.value == "ERROR"] if strict else []
    if any(issue.code == "NORMATIVE_CONFLICT" for issue in test_errors):
        rules = ", ".join(sorted({issue.rule_id or issue.code for issue in test_errors if issue.code == "NORMATIVE_CONFLICT"}))
        return "NORMATIVE_CONFLICT", "NORMATIVE_CONFLICT", "NORMATIVE_CONFLICT", rules
    if test_errors:
        rules = ", ".join(sorted({issue.rule_id or issue.code for issue in test_errors}))
        return "NEEDS_EXTERNAL_SOURCE", "NEEDS_EXTERNAL_SOURCE", "NEEDS_EXTERNAL_SOURCE", rules
    resolution=engine.resolve_structure(engine.get_message(message_code).structure_id,mode=GenerationMode.TEST)
    if resolution.uses_version_placeholders:
        return "UNRESOLVED_STRUCTURE_VERSION", "VERSION_PLACEHOLDER_TEST", "VERSION_PLACEHOLDER_TEST", ", ".join(resolution.placeholder_versions)
    if strict_errors:
        rules = ", ".join(sorted({issue.code for issue in strict_errors}))
        return "NEEDS_EXTERNAL_SOURCE", "VERIFIED_SOAP", "TEST_ONLY", rules
    return "VERIFIED_SOAP", "VERIFIED_SOAP", "VERIFIED_SOAP", "none"


def evaluate_matrix(engine) -> list[BranchResult]:
    results = []
    serializer = XmlSerializer()
    for tx_index, transaction in enumerate(sorted(engine.transactions.values(), key=lambda item: item.transaction_code), 1):
        initiator_address=participant_address(engine,transaction.initiating_participant)
        respondent_address=participant_address(engine,transaction.responding_participant)
        branches = [("initiating", transaction.initiating_message), *(("response", code) for code in transaction.response_messages)]
        for branch_index, (branch, message_code) in enumerate(branches, 1):
            message = engine.get_message(message_code)
            active = engine.package.profile.structures[message.structure_id].active_version
            try:
                values = test_values(engine, message_code)
            except UnresolvedStructureVersionError:
                values = {}
            strict_status, test_status, status, rule = classify(engine, message_code, values)
            xml = request_id = response_id = request_edoc = None
            if branch == "response":
                request_code=transaction.initiating_message; request_values=test_values(engine,request_code)
                _,_,request_status,request_rule=classify(engine,request_code,request_values)
                if request_status not in {"VERIFIED_SOAP","TEST_ONLY","VERSION_PLACEHOLDER_TEST"}:
                    status="INITIAL_MESSAGE_BLOCKED"; rule=f"{request_code}: {request_status} ({request_rule})"
            if status in {"VERIFIED_SOAP", "TEST_ONLY", "VERSION_PLACEHOLDER_TEST"}:
                ids = FixedIdentifierService(tx_index * 1000 + branch_index * 10)
                procedure = ProcedureInstance(transaction.procedure_code, ProcedureId.root(ids))
                instance = TransactionInstance(transaction.transaction_code, ids.new_conversation_id(), procedure)
                factory = MessageFactory(ids)
                mode = GenerationMode.STRICT if status == "VERIFIED_SOAP" else GenerationMode.TEST
                if branch == "initiating":
                    envelope = factory.create_initial_application_message(
                        transaction=instance, process_code=engine.process.process_code,
                        process_version=engine.package.profile.process_version, message_code=message_code,
                        to=respondent_address, reply_to=initiator_address, body_payload=engine.build_body(message_code, values, mode=mode),
                    )
                    request_id = envelope.header.message_id.serialize()
                else:
                    request = factory.create_initial_application_message(
                        transaction=instance, process_code=engine.process.process_code,
                        process_version=engine.package.profile.process_version, message_code=request_code,
                        to=respondent_address, reply_to=initiator_address, body_payload=engine.build_body(request_code, request_values, mode=GenerationMode.TEST),
                    )
                    request_edoc = next((value for path, value in request_values.items() if path.endswith("/EDocId")), None)
                    response_structure = engine.get_structure(message_code,mode=GenerationMode.TEST)
                    ref_path = next((field.path for field in response_structure.fields if field.xml_name == "EDocRefId"), None)
                    if ref_path and request_edoc: values[ref_path] = request_edoc
                    envelope = factory.create_followup_application_message(
                        transaction=instance, process_code=engine.process.process_code,
                        process_version=engine.package.profile.process_version, message_code=message_code,
                        to=initiator_address, reply_to=respondent_address, body_payload=engine.build_body(message_code, values, mode=mode),
                    )
                    request_id = request.header.message_id.serialize()
                    response_id = envelope.header.message_id.serialize()
                resolution=engine.resolve_structure(message.structure_id,mode=GenerationMode.TEST)
                placeholder_sources=tuple(f"{ref.document}, {ref.section or ref.location}" for ref in resolution.definition.source_refs)
                placeholder_prefixes=tuple(prefix for prefix,namespace in resolution.definition.imported_namespaces.items() if any(token in namespace for token in resolution.placeholder_versions))
                xml = serializer.serialize_application(envelope,placeholder_versions=resolution.placeholder_versions,placeholder_sources=placeholder_sources,placeholder_structure_id=resolution.definition.structure_id,placeholder_model_prefixes=placeholder_prefixes)
            structure = engine.resolve_structure(message.structure_id,mode=GenerationMode.TEST).definition
            refs = source_ids(transaction, message, *(tuple([structure]) if structure else ()))
            results.append(BranchResult(transaction.transaction_code, transaction.procedure_code, branch, message_code,
                                        message.structure_id, active, strict_status, test_status, status, rule, refs,
                                        xml, request_id, response_id, request_edoc))
    return results


def artifact_path(result: BranchResult) -> Path:
    directory = EXAMPLES / f"TRN.{result.transaction_short}"
    stem = f"{result.branch.upper()}_{result.message_code.rsplit('.', 1)[-1]}"
    return directory / (stem + (".xml" if result.xml else ".blocked.txt"))


def blocked_text(result: BranchResult) -> str:
    return "\n".join((
        f"transaction: {result.transaction_code}", f"procedure: {result.procedure_code}",
        f"branch: {result.branch}", f"message: {result.message_code}", f"structure: {result.structure_id}",
        f"active_version: {result.active_version if result.active_version is not None else 'null'}",
        f"status: {result.status}", f"blocking_rule: {result.blocking_rule}",
        f"source_refs: {', '.join(result.source_refs) or 'none'}",
        f"strict_mode: {result.strict_status}", f"test_mode: {result.test_status}", "",
    ))
