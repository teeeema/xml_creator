from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.core.enums import SignalKind, TransactionPattern, TransactionState
from eaeu_xml.decision5.models import (
    AcceptTime, DummyBodyPayload, FaultReasonText, FaultSubcode, IntegrationMetadata,
    LogicalAddress, ProcedureId, ProcedureInstance, SignalError, SignalErrorCode,
    SoapFault, TrackId, TransactionDefinition, TransactionInstance, TransactionParameters,
)
from eaeu_xml.services.fault_factory import FaultFactory
from eaeu_xml.services.identifier_service import IdentifierService
from eaeu_xml.services.message_factory import MessageFactory
from eaeu_xml.services.platform_context import IntegrationPlatformContext
from eaeu_xml.services.signal_factory import SignalFactory
from eaeu_xml.services.transaction_engine import RetryService
from eaeu_xml.services.xml_serializer import XmlSerializer


def generate(project_root: Path) -> tuple[Path, ...]:
    ids = IdentifierService(); factory = MessageFactory(ids); serializer = XmlSerializer()
    procedure = ProcedureInstance("P.SP.03.PRC.001", ProcedureId.root(ids))
    definition = TransactionDefinition(TransactionPattern.QUESTION_RESPONSE, TransactionParameters(retry_count=1))
    transaction = TransactionInstance("P.SP.03.TRN.002", ids.new_conversation_id(), procedure, definition=definition)
    to = LogicalAddress.parse("EAEU://EEC/CP/P.SP.03/P.ACT.001")
    reply = LogicalAddress.parse("EAEU://RU/CP/P.SP.03/P.SP.03.ACT.002")
    initial = factory.create_initial_application_message(transaction=transaction, process_code="P.SP.03", process_version="0.1", message_code="P.CC.04.MSG.003", to=to, reply_to=reply, body_payload=DummyBodyPayload("reference initial"))
    followup = factory.create_followup_application_message(transaction=transaction, process_code="P.SP.03", process_version="0.1", message_code="P.CC.04.MSG.004", to=reply, reply_to=to, body_payload=DummyBodyPayload("reference follow-up"))
    metadata = IntegrationMetadata(TrackId("urn:uuid:00000000-0000-4000-8000-000000000010"), AcceptTime(datetime(2026, 8, 20, tzinfo=timezone.utc)))
    enriched = IntegrationPlatformContext().enrich(initial, metadata)
    signals = SignalFactory(ids)
    received = signals.create(transaction=transaction, source_message=initial, kind=SignalKind.RECEIVED, to=reply, reply_to=to)
    processing = signals.create(transaction=transaction, source_message=initial, kind=SignalKind.ACCEPTED_FOR_PROCESSING, to=reply, reply_to=to)
    error = signals.create(transaction=transaction, source_message=initial, kind=SignalKind.ERROR, to=reply, reply_to=to, errors=(SignalError(SignalErrorCode.DATA_ERROR, "Ошибка структуры данных"),))
    faults = FaultFactory(ids)
    fault_body = SoapFault(FaultSubcode.INTERNAL_ERROR, (FaultReasonText("Внутренняя ошибка", "ru"),))
    wsa_fault = faults.create(source_message=initial, sender=to, fault=fault_body, wsa_fault=True)
    generic_fault = faults.create(source_message=initial, sender=to, fault=fault_body)
    child = procedure.start_child("P.SP.03.PRC.002", ids)
    nested_tx = TransactionInstance("P.SP.03.TRN.002", ids.new_conversation_id(), child)
    nested = factory.create_initial_application_message(transaction=nested_tx, process_code="P.SP.03", process_version="0.1", message_code="P.CC.04.MSG.003", to=to, reply_to=reply, body_payload=DummyBodyPayload("nested procedure"))
    transaction.state = TransactionState.WAITING_RESPONSE
    retry_record = RetryService().retry_record(transaction, transaction.message_history[0], ids.new_message_id())
    retry = replace(initial, header=replace(initial.header, message_id=retry_record.message_id))
    documents = {
        "01_initial_application.xml": serializer.serialize_application(initial),
        "02_followup_application.xml": serializer.serialize_application(followup),
        "03_platform_enriched_application.xml": serializer.serialize_application(enriched),
        "04_received_signal.xml": serializer.serialize_signal(received),
        "05_processing_signal.xml": serializer.serialize_signal(processing),
        "06_error_signal.xml": serializer.serialize_signal(error),
        "07_wsa_fault.xml": serializer.serialize_fault(wsa_fault),
        "08_generic_fault.xml": serializer.serialize_fault(generic_fault),
        "09_nested_procedure.xml": serializer.serialize_application(nested),
        "10_retry.xml": serializer.serialize_application(retry),
    }
    output = project_root / "examples/decision5"; output.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, xml in documents.items():
        ET.fromstring(xml)
        path = output / name; path.write_text(xml, encoding="utf-8"); paths.append(path)
    return tuple(paths)


if __name__ == "__main__":
    generated = generate(Path(__file__).parents[1])
    print(f"generated={len(generated)}")
