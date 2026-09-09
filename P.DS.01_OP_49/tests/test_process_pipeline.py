"""Batch integration coverage for the P.DS.01 catalog and generic SOAP pipeline."""

from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.core.namespaces import NamespaceRegistry
from eaeu_xml.decision5.models import AcceptTime, ConversationId, MessageId, ProcedureId, ProcedureInstance, TrackId, TransactionInstance
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.services.logical_address_builder import LogicalAddressBuilder
from eaeu_xml.services.message_factory import MessageFactory
from eaeu_xml.services.platform_context import IntegrationPlatformContext
from eaeu_xml.services.xml_serializer import XmlSerializer


PACKAGE = Path(__file__).parents[1]
REQUEST_MESSAGES = ("P.DS.01.MSG.002", "P.DS.01.MSG.004", "P.DS.01.MSG.005", "P.DS.01.MSG.006")
TRANSACTIONS = (
    "P.DS.01.TRN.001", "P.DS.01.TRN.002", "P.DS.01.TRN.003", "P.DS.01.TRN.004",
    "P.DS.01.TRN.005", "P.DS.01.TRN.006", "P.DS.01.TRN.007",
)


class FixedIdentifierService:
    def __init__(self, start: int = 100) -> None:
        self.value = start

    def _next(self) -> UUID:
        result = UUID(int=self.value)
        self.value += 1
        return result

    def new_procedure_component(self) -> UUID: return self._next()
    def new_conversation_id(self) -> ConversationId: return ConversationId(self._next())
    def new_message_id(self) -> MessageId: return MessageId(self._next())


def report_values(engine: EaeuXmlEngine, message_code: str) -> dict[str, object]:
    structure = engine.get_structure(message_code, mode=GenerationMode.TEST)
    values: dict[str, object] = {}
    for field in structure.fields:
        if field.kind == "ATTRIBUTE":
            values[field.path] = "AAA" if field.xml_name == "currencyCode" else ("0" if field.xml_name == "scaleNumber" else "ID")
        elif field.min_occurs:
            datatype = field.datatype or ""
            values[field.path] = ("2024-01-03T00:00:00" if "DateTime" in datatype else "2024-01-03" if "DateType" in datatype else True if "Indicator" in datatype else "0.00" if "PaymentAmount" in datatype else "AA" if "CountryCode" in datatype else "x")
    by = {field.field_id: field.path for field in structure.fields}
    values.update({by["3"]: [None], by["3.5"]: [None], by["3.5"] + "/ds01sdo:DailyInfoIndicator": [True], by["3.2"]: "2024-01-03", by["3.1"]: "2024-01-02"})
    for field_id, amount in (("3.5.9", "DistributableDutyAmount"), ("3.5.10", "TransferDistributedDutyAmount"), ("3.5.12", "StopTransferDistributedDutyAmount")):
        path = by[field_id]
        values.update({path: [None, None], path + "/ds01sdo:TotalAmountIndicator": [True, False], path + "/csdo:UnifiedCountryCode": [None, "AA"], path + "/ds01sdo:" + amount: ["10.00", "10.00"]})
    if message_code == "P.DS.01.MSG.005":
        values[by["3.4"]] = "2024-01-04T00:00:00"
    return values


def protocol_values(engine: EaeuXmlEngine) -> dict[str, object]:
    structure = engine.get_structure("P.DS.01.MSG.004", mode=GenerationMode.TEST)
    values: dict[str, object] = {}
    for field in structure.fields:
        if field.kind == "ATTRIBUTE": values[field.path] = "ID"
        elif field.min_occurs:
            typ = field.datatype or ""
            values[field.path] = ("2024-01-03T00:00:00" if "DateTime" in typ else "2024-01-03" if "DateType" in typ else "AA" if "CountryCode" in typ else "00000000-0000-0000-0000-000000000010" if "EDocRefId" in field.xml_name else "x")
    ref = next(field for field in structure.fields if field.xml_name == "EDocRefId")
    values[ref.path] = "00000000-0000-0000-0000-000000000010"
    return values


def values_for(engine: EaeuXmlEngine, message_code: str) -> dict[str, object]:
    if message_code == "P.DS.01.MSG.004": return protocol_values(engine)
    if message_code == "P.DS.01.MSG.003":
        structure = engine.get_structure(message_code, mode=GenerationMode.TEST)
        values = {}
        for field in structure.fields:
            if not field.min_occurs: continue
            typ = field.datatype or ""
            values[field.path] = ("2024-01-03T00:00:00" if "DateTime" in typ else "P.DS.01.MSG.003" if field.xml_name == "InfEnvelopeCode" else "R.006" if field.xml_name == "EDocCode" else "00000000-0000-0000-0000-000000000011" if field.xml_name == "EDocId" else "SUCCESS" if field.xml_name == "ProcessingResultV2Code" else "x")
        return values
    return report_values(engine, message_code)


def q(ns: str, local: str) -> str: return f"{{{ns}}}{local}"


@pytest.mark.parametrize("message_code", REQUEST_MESSAGES)
def test_available_request_bodies_validate_and_serialize(message_code: str) -> None:
    engine = EaeuXmlEngine.load_process(PACKAGE)
    result = engine.validate_body(message_code, values_for(engine, message_code), mode=GenerationMode.TEST)
    assert result.is_valid
    body = engine.build_body(message_code, values_for(engine, message_code), mode=GenerationMode.TEST)
    structure = engine.get_structure(message_code, mode=GenerationMode.TEST)
    assert body.serialize_xml_element().tag == q(structure.namespace, structure.root_element)


@pytest.mark.parametrize("transaction_code", TRANSACTIONS)
def test_all_transactions_preserve_generic_request_response_correlation(transaction_code: str) -> None:
    engine = EaeuXmlEngine.load_process(PACKAGE)
    definition = engine.get_transaction(transaction_code)
    request_code, response_code = definition.initiating_message, definition.response_messages[0]
    ids = FixedIdentifierService(100 + int(transaction_code[-3:]) * 10)
    procedure = ProcedureInstance(definition.procedure_code, ProcedureId.root(ids))
    transaction = TransactionInstance(transaction_code, ids.new_conversation_id(), procedure)
    addresses = LogicalAddressBuilder()
    to = addresses.build_common_process(segment="EEC", process_code="P.DS.01", participant_code="TEST_TO")
    reply = addresses.build_common_process(segment="EEC", process_code="P.DS.01", participant_code="TEST_REPLY")
    factory = MessageFactory(ids)
    request = factory.create_initial_application_message(transaction=transaction, process_code="P.DS.01", process_version=engine.package.profile.process_version, message_code=request_code, to=to, reply_to=reply, body_payload=engine.build_body(request_code, values_for(engine, request_code), mode=GenerationMode.TEST))
    response = factory.create_followup_application_message(transaction=transaction, process_code="P.DS.01", process_version=engine.package.profile.process_version, message_code=response_code, to=reply, reply_to=to, body_payload=engine.build_body(response_code, values_for(engine, response_code), mode=GenerationMode.TEST))
    context = IntegrationPlatformContext()
    request = context.enrich(request, context.create_metadata(track_id=TrackId("urn:uuid:00000000-0000-0000-0000-000000000099"), accept_time=AcceptTime(datetime(2024, 1, 2, tzinfo=timezone.utc))))
    response = context.enrich(response, context.create_metadata(track_id=TrackId("urn:uuid:00000000-0000-0000-0000-000000000098"), accept_time=AcceptTime(datetime(2024, 1, 2, tzinfo=timezone.utc))))
    assert request.header.relates_to is None
    assert response.header.message_id != request.header.message_id
    assert response.header.relates_to.message_id == request.header.message_id
    assert response.header.conversation_id == request.header.conversation_id == transaction.conversation_id
    assert response.header.procedure_id == request.header.procedure_id == procedure.procedure_id
    assert request.header.action == engine.build_application_action(transaction_code, request_code)
    assert response.header.action == engine.build_application_action(transaction_code, response_code)
    serializer, namespaces = XmlSerializer(), NamespaceRegistry()
    for message, code in ((request, request_code), (response, response_code)):
        resolution = engine.resolve_structure(engine.get_message(code).structure_id, mode=GenerationMode.TEST)
        root = ET.fromstring(serializer.serialize_application(message, placeholder_versions=resolution.placeholder_versions, placeholder_structure_id=resolution.definition.structure_id, placeholder_model_prefixes=tuple(resolution.definition.imported_namespaces)))
        assert root.tag == q(namespaces.SOAP, "Envelope")
        assert root.find(q(namespaces.SOAP, "Header")) is not None
        body = root.find(q(namespaces.SOAP, "Body"))
        assert body is not None and len(body) == 1
        assert body[0].tag == q(resolution.definition.namespace, resolution.definition.root_element)


def test_catalog_reuses_messages_without_transaction_state() -> None:
    engine = EaeuXmlEngine.load_process(PACKAGE)
    transactions = engine.transactions
    assert [code for code, item in transactions.items() if item.initiating_message == "P.DS.01.MSG.002"] == ["P.DS.01.TRN.002", "P.DS.01.TRN.003"]
    assert [code for code, item in transactions.items() if item.initiating_message == "P.DS.01.MSG.005"] == ["P.DS.01.TRN.005", "P.DS.01.TRN.006"]
    assert all(item.response_messages == ("P.DS.01.MSG.003",) for item in transactions.values())
    assert not hasattr(engine.get_message("P.DS.01.MSG.002"), "transaction_id")
