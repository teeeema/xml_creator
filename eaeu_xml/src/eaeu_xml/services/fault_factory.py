from eaeu_xml.core.errors import FaultCorrelationError
from eaeu_xml.decision5.models.action import FaultAction
from eaeu_xml.decision5.models.fault import SoapFault
from eaeu_xml.decision5.models.header import EndpointReference, RelatesTo, SoapHeader
from eaeu_xml.decision5.models.signal import TechnicalFaultMessage
from eaeu_xml.services.identifier_service import IdentifierService


class FaultFactory:
    def __init__(self, identifiers: IdentifierService | None = None) -> None:
        self.identifiers = identifiers or IdentifierService()

    def create(self, *, source_message, sender, fault: SoapFault, wsa_fault: bool = False) -> TechnicalFaultMessage:
        source = source_message.header
        destination = source.fault_to or source.reply_to
        if destination is None:
            raise FaultCorrelationError(code="D5_FAULT_DESTINATION", rule_id="D5-FAULT-TO", message="В исходном сообщении отсутствуют FaultTo и ReplyTo.")
        source_action = source.action.serialize()
        header = SoapHeader(
            to=destination.address, reply_to=None, from_=EndpointReference(sender), fault_to=None,
            action=FaultAction(FaultAction.WSA if wsa_fault else FaultAction.GENERIC),
            message_id=self.identifiers.new_message_id(), procedure_id=source.procedure_id,
            conversation_id=source.conversation_id,
            relates_to=RelatesTo(source.message_id, source_action),
        )
        return TechnicalFaultMessage(header, fault, source.message_id, source_action)
