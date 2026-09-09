from datetime import datetime, timezone

from eaeu_xml.core.enums import MessageKind, SignalKind
from eaeu_xml.decision5.models.action import SignalAction
from eaeu_xml.decision5.models.header import EndpointReference, RelatesTo, SoapHeader
from eaeu_xml.decision5.models.signal import SignalMessage, SignalPayload
from eaeu_xml.decision5.models.transaction import MessageRecord, TransactionInstance
from eaeu_xml.services.identifier_service import IdentifierService


class SignalFactory:
    def __init__(self, identifiers: IdentifierService | None = None) -> None:
        self.identifiers = identifiers or IdentifierService()

    def create(self, *, transaction: TransactionInstance, source_message, kind: SignalKind, to, reply_to, errors=()) -> SignalMessage:
        action = SignalAction(source_message.header.action.application_context if isinstance(source_message.header.action, SignalAction) else source_message.header.action, kind.value)
        message_id = self.identifiers.new_message_id()
        header = SoapHeader(
            to=to, reply_to=EndpointReference(reply_to), action=action, message_id=message_id,
            procedure_id=transaction.procedure_instance.procedure_id, conversation_id=transaction.conversation_id,
            relates_to=RelatesTo(source_message.header.message_id),
        )
        payload = SignalPayload(kind, self.identifiers.new_signal_id(), datetime.now(timezone.utc), tuple(errors))
        transaction.message_history.append(MessageRecord(message_id, action, datetime.now(timezone.utc), len(transaction.message_history)+1, MessageKind.SIGNAL, source_message.header.message_id))
        return SignalMessage(header, payload)
