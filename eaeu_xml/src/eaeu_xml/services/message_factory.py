from datetime import datetime, timezone

from eaeu_xml.core.enums import MessageKind, TransactionState
from eaeu_xml.decision5.models.envelope import ApplicationMessage, BodyPayload
from eaeu_xml.decision5.models.header import EndpointReference, RelatesTo, SoapHeader
from eaeu_xml.decision5.models.address import LogicalAddress
from eaeu_xml.decision5.models.transaction import MessageRecord, TransactionInstance
from eaeu_xml.decision5.validation.header_validator import HeaderValidator
from eaeu_xml.services.action_builder import ActionBuilder
from eaeu_xml.services.correlation_service import CorrelationService
from eaeu_xml.services.identifier_service import IdentifierService


class MessageFactory:
    def __init__(self, identifier_service: IdentifierService | None = None) -> None:
        self.identifiers = identifier_service or IdentifierService()
        self.actions = ActionBuilder()
        self.correlation = CorrelationService()
        self.headers = HeaderValidator()

    def create_initial_application_message(
        self, *, transaction: TransactionInstance, process_code: str, process_version: str,
        message_code: str, to: LogicalAddress, reply_to: LogicalAddress, body_payload: BodyPayload,
    ) -> ApplicationMessage:
        relates_to = self.correlation.for_initial(transaction)
        return self._create(transaction, process_code, process_version, message_code, to, reply_to, body_payload, relates_to)

    def create_followup_application_message(
        self, *, transaction: TransactionInstance, process_code: str, process_version: str,
        message_code: str, to: LogicalAddress, reply_to: LogicalAddress, body_payload: BodyPayload,
    ) -> ApplicationMessage:
        relates_to = self.correlation.for_followup(transaction)
        return self._create(transaction, process_code, process_version, message_code, to, reply_to, body_payload, relates_to)

    def create_retry_application_message(self,*,transaction,process_code,process_version,message_code,to,reply_to,body_payload,original):
        relates_to=None if original.relates_to is None else RelatesTo(original.relates_to)
        return self._create(transaction,process_code,process_version,message_code,to,reply_to,body_payload,relates_to,retry_of=original.message_id,attempt_number=original.attempt_number+1)

    def _create(self, transaction, process_code, process_version, message_code, to, reply_to, body_payload, relates_to,retry_of=None,attempt_number=1):
        action = self.actions.build_application(
            process_code=process_code, process_version=process_version,
            procedure_code=transaction.procedure_instance.procedure_code,
            transaction_code=transaction.transaction_code, message_code=message_code,
        )
        message_id = self.identifiers.new_message_id()
        header = SoapHeader(
            to=to, reply_to=EndpointReference(reply_to), action=action, message_id=message_id,
            procedure_id=transaction.procedure_instance.procedure_id,
            conversation_id=transaction.conversation_id, relates_to=relates_to,
        )
        self.headers.validate_application(header)
        transaction.message_history.append(MessageRecord(
            message_id=message_id, action=action, created_at=datetime.now(timezone.utc),
            sequence_number=len(transaction.message_history) + 1, message_kind=MessageKind.APPLICATION,
            relates_to=relates_to.message_id if relates_to else None,retry_of=retry_of,attempt_number=attempt_number,
        ))
        transaction.state = TransactionState.ACTIVE
        return ApplicationMessage(header, body_payload)
