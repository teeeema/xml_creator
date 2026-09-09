"""Production-pipeline integration coverage for the P.DS.01 MSG.001 test body."""

from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID
from xml.etree import ElementTree as ET

from eaeu_xml.core.namespaces import NamespaceRegistry
from eaeu_xml.decision5.models import (
    AcceptTime,
    ConversationId,
    MessageId,
    ProcedureId,
    ProcedureInstance,
    TrackId,
    TransactionInstance,
)
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.rules_engine import RuleStatus
from eaeu_xml.services.logical_address_builder import LogicalAddressBuilder
from eaeu_xml.services.message_factory import MessageFactory
from eaeu_xml.services.platform_context import IntegrationPlatformContext
from eaeu_xml.services.xml_serializer import XmlSerializer


PACKAGE = Path(__file__).parents[1]
EXPECTED_ACTION = "int://CP/P.DS.01/1.0.0/P.DS.01.PRC.001/P.DS.01.TRN.001/P.DS.01.MSG.001"
EXECUTABLE_RULE_IDS = {
    "R001", "R002", "R003", "R005", "R006", "R014", "R015", "R016", "R017", "R018",
    "R020", "R021", "R022", "R023", "R024", "R027", "R028", "R029", "R030", "R031",
}
EXTERNAL_CONTEXT_RULE_IDS = {"R004"}
EXTERNAL_REFERENCE_RULE_IDS = {
    "R007", "R008", "R009", "R010", "R011", "R012", "R013", "R019", "R025", "R026",
    "R032", "R033", "R034",
}


class FixedIdentifierService:
    """Deterministic test double for the generic identifier-service protocol."""

    def __init__(self, start: int = 1) -> None:
        self.next_value = start

    def _uuid(self) -> UUID:
        value = UUID(int=self.next_value)
        self.next_value += 1
        return value

    def new_procedure_component(self) -> UUID:
        return self._uuid()

    def new_conversation_id(self) -> ConversationId:
        return ConversationId(self._uuid())

    def new_message_id(self) -> MessageId:
        return MessageId(self._uuid())


def msg001_values(engine: EaeuXmlEngine) -> dict[str, object]:
    """A deterministic body satisfying every locally executable MSG.001 rule."""
    structure = engine.get_structure("P.DS.01.MSG.001", mode=GenerationMode.TEST)
    values: dict[str, object] = {}
    for field in structure.fields:
        if field.kind == "ATTRIBUTE":
            values[field.path] = (
                "AAA" if field.xml_name == "currencyCode"
                else "0" if field.xml_name == "scaleNumber" else "ID"
            )
        elif field.min_occurs:
            datatype = field.datatype or ""
            values[field.path] = (
                "2024-01-02T00:00:00" if "DateTime" in datatype
                else "2024-01-02" if "DateType" in datatype
                else True if "Indicator" in datatype
                else "0.00" if "PaymentAmount" in datatype
                else "AA" if "CountryCode" in datatype
                else "x"
            )

    by_id = {field.field_id: field.path for field in structure.fields}
    values.update({
        by_id["3"]: [None],
        by_id["3.5"]: [None],
        by_id["3.5"] + "/ds01sdo:DailyInfoIndicator": [True],
        by_id["3.2"]: "2024-01-02",
        by_id["3.1"]: "2024-01-01",
    })
    for field_id, amount_name in (
        ("3.5.9", "DistributableDutyAmount"),
        ("3.5.10", "TransferDistributedDutyAmount"),
        ("3.5.12", "StopTransferDistributedDutyAmount"),
    ):
        path = by_id[field_id]
        values.update({
            path: [None, None],
            path + "/ds01sdo:TotalAmountIndicator": [True, False],
            path + "/csdo:UnifiedCountryCode": [None, "AA"],
            path + "/ds01sdo:" + amount_name: ["10.00", "10.00"],
        })
    return values


def qualified(namespace: str, local_name: str) -> str:
    return f"{{{namespace}}}{local_name}"


def full_rule_ids(short_ids: set[str]) -> set[str]:
    return {f"P.DS.01.MSG.001.{rule_id}" for rule_id in short_ids}


def test_msg001_full_message_uses_the_generic_production_pipeline() -> None:
    engine = EaeuXmlEngine.load_process(PACKAGE)
    values = msg001_values(engine)

    validation = engine.validate_body("P.DS.01.MSG.001", values, mode=GenerationMode.TEST)
    assert validation.is_valid
    assert not validation.is_complete
    evaluations = {item.rule_id: item for item in validation.rule_evaluations}
    assert set(evaluations) == full_rule_ids(EXECUTABLE_RULE_IDS | EXTERNAL_CONTEXT_RULE_IDS | EXTERNAL_REFERENCE_RULE_IDS)
    assert {rule_id for rule_id, item in evaluations.items() if item.status is RuleStatus.PASS} == full_rule_ids(EXECUTABLE_RULE_IDS)
    assert {rule_id for rule_id, item in evaluations.items() if item.status is RuleStatus.NOT_EVALUATED_EXTERNAL_CONTEXT} == full_rule_ids(EXTERNAL_CONTEXT_RULE_IDS)
    assert {rule_id for rule_id, item in evaluations.items() if item.status is RuleStatus.NOT_EVALUATED_EXTERNAL_REFERENCE} == full_rule_ids(EXTERNAL_REFERENCE_RULE_IDS)

    identifiers = FixedIdentifierService()
    procedure = ProcedureInstance("P.DS.01.PRC.001", ProcedureId.root(identifiers))
    transaction = TransactionInstance("P.DS.01.TRN.001", identifiers.new_conversation_id(), procedure)
    addresses = LogicalAddressBuilder()
    message = MessageFactory(identifiers).create_initial_application_message(
        transaction=transaction,
        process_code="P.DS.01",
        process_version="1.0.0",
        message_code="P.DS.01.MSG.001",
        to=addresses.build_common_process(segment="EEC", process_code="P.DS.01", participant_code="TEST_TO"),
        reply_to=addresses.build_common_process(segment="EEC", process_code="P.DS.01", participant_code="TEST_REPLY"),
        body_payload=engine.build_body("P.DS.01.MSG.001", values, mode=GenerationMode.TEST),
    )
    track_id = TrackId("urn:uuid:00000000-0000-0000-0000-000000000099")
    accept_time = AcceptTime(datetime(2024, 1, 2, tzinfo=timezone.utc))
    message = IntegrationPlatformContext().enrich(
        message, IntegrationPlatformContext().create_metadata(track_id=track_id, accept_time=accept_time)
    )

    assert message.header.action.serialize() == EXPECTED_ACTION
    assert message.header.message_id.serialize() == "urn:uuid:00000000-0000-0000-0000-000000000003"
    assert message.header.procedure_id.serialize() == "urn:uuid:00000000-0000-0000-0000-000000000001"
    assert message.header.conversation_id.serialize() == "urn:uuid:00000000-0000-0000-0000-000000000002"
    assert message.header.relates_to is None

    resolution = engine.resolve_structure("R.FP.DS.01.001", mode=GenerationMode.TEST)
    xml = XmlSerializer().serialize_application(
        message,
        placeholder_versions=resolution.placeholder_versions,
        placeholder_structure_id=resolution.definition.structure_id,
        placeholder_model_prefixes=tuple(resolution.definition.imported_namespaces),
    )
    root = ET.fromstring(xml)
    namespaces = NamespaceRegistry()
    header = root.find(qualified(namespaces.SOAP, "Header"))
    body = root.find(qualified(namespaces.SOAP, "Body"))
    assert root.tag == qualified(namespaces.SOAP, "Envelope")
    assert header is not None
    assert body is not None
    assert header.findtext(qualified(namespaces.WSA, "MessageID")) == message.header.message_id.serialize()
    assert header.findtext(qualified(namespaces.WSA, "Action")) == EXPECTED_ACTION
    assert len(header.findall(qualified(namespaces.WSA, "RelatesTo"))) == 0
    assert header.findtext(qualified(namespaces.INT, "ProcedureID")) == procedure.procedure_id.serialize()
    assert header.findtext(qualified(namespaces.INT, "ConversationID")) == transaction.conversation_id.serialize()
    integration = header.find(qualified(namespaces.INT, "Integration"))
    assert integration is not None
    assert integration.findtext(qualified(namespaces.INT, "TrackID")) == track_id.serialize()
    assert integration.findtext(qualified(namespaces.INT, "AcceptTime")) == accept_time.serialize()

    structure = resolution.definition
    assert len(body) == 1
    assert body[0].tag == qualified(structure.namespace, "ChargedDistributedReport")
