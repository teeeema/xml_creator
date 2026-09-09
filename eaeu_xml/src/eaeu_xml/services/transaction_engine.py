from dataclasses import replace

from eaeu_xml.core.enums import MessageKind, SignalKind, TimeoutKind, TimeoutOutcome, TransactionState
from eaeu_xml.core.errors import RetryNotAllowedError, TimeoutTransitionError
from eaeu_xml.decision5.rules.pattern_rules import TransactionStateMachine
from eaeu_xml.decision5.models.transaction import TransactionInstance


class RetryService:
    def prepare_retry(self,transaction,original):
        if transaction.definition is None or transaction.retry_attempts >= transaction.definition.parameters.retry_count:
            raise RetryNotAllowedError(code="D5_RETRY_EXHAUSTED", rule_id="D5-TRN-RETRY", message="Количество повторов исчерпано.")
        allowed = {TransactionState.WAITING_RECEIVED, TransactionState.WAITING_PROCESSING, TransactionState.WAITING_RESPONSE, TransactionState.WAITING_RESPONSE_RECEIVED, TransactionState.WAITING_RESPONSE_PROCESSING, TransactionState.FAILED, TransactionState.ACTIVE}
        if transaction.state not in allowed or original.message_kind is not MessageKind.APPLICATION:
            raise RetryNotAllowedError(code="D5_RETRY_STATE", rule_id="D5-TRN-RETRY", message="Повтор допустим только для сообщения общего процесса при ожидании ответа/подтверждения или после Fault.")
        transaction.retry_attempts += 1

    def retry_record(self, transaction: TransactionInstance, original, new_message_id):
        self.prepare_retry(transaction,original)
        retry = replace(original, message_id=new_message_id, retry_of=original.message_id, attempt_number=original.attempt_number + 1, sequence_number=len(transaction.message_history) + 1)
        transaction.message_history.append(retry)
        return retry


class TransactionEngine:
    def __init__(self) -> None:
        self.state_machine = TransactionStateMachine()
        self.retry_service = RetryService()

    def start_transaction(self, transaction: TransactionInstance) -> TransactionState:
        if transaction.state is not TransactionState.NEW:
            raise TimeoutTransitionError(code="D5_ALREADY_STARTED", rule_id="D5-TRN-PATTERNS", message="Транзакция уже начата.")
        transaction.state = self.state_machine.after_initial(transaction)
        return transaction.state

    def receive_signal(self, transaction: TransactionInstance, kind: SignalKind) -> TransactionState:
        transaction.state = self.state_machine.receive_signal(transaction, kind)
        return transaction.state

    def send_signal(self, transaction: TransactionInstance, kind: SignalKind) -> TransactionState:
        """Record a normative signal transition initiated by the local participant."""
        transaction.state = self.state_machine.receive_signal(transaction, kind)
        return transaction.state

    def receive_application_message(self, transaction: TransactionInstance) -> TransactionState:
        transaction.state = self.state_machine.receive_response(transaction)
        return transaction.state

    def receive_fault(self, transaction: TransactionInstance) -> TransactionState:
        transaction.state = TransactionState.FAILED
        return transaction.state

    def complete(self, transaction: TransactionInstance) -> TransactionState:
        transaction.state = TransactionState.COMPLETED
        return transaction.state

    def fail(self, transaction: TransactionInstance) -> TransactionState:
        transaction.state = TransactionState.FAILED
        return transaction.state

    def cancel(self, transaction: TransactionInstance, *, rollback_required: bool = False) -> TransactionState:
        transaction.state = TransactionState.ROLLBACK_REQUIRED if rollback_required else TransactionState.CANCELLED
        return transaction.state

    def handle_timeout(self, transaction: TransactionInstance, kind: TimeoutKind) -> TimeoutOutcome:
        if transaction.state is TransactionState.WAITING_FINAL_ERROR_WINDOW and kind is TimeoutKind.PROCESSING_CONFIRMATION:
            transaction.state = TransactionState.COMPLETED
            return TimeoutOutcome.COMPLETE
        expected = {
            TimeoutKind.RECEIVE_CONFIRMATION: {TransactionState.WAITING_RECEIVED, TransactionState.WAITING_RESPONSE_RECEIVED},
            TimeoutKind.PROCESSING_CONFIRMATION: {TransactionState.WAITING_PROCESSING, TransactionState.WAITING_RESPONSE_PROCESSING},
            TimeoutKind.RESPONSE: {TransactionState.WAITING_RESPONSE},
        }
        if transaction.state not in expected[kind]:
            raise TimeoutTransitionError(code="D5_TIMEOUT_STATE", rule_id="D5-TRN-TIMEOUT", message="Тайм-аут не соответствует текущему состоянию.")
        if transaction.definition and transaction.retry_attempts < transaction.definition.parameters.retry_count:
            return TimeoutOutcome.RETRY
        transaction.state = TransactionState.FAILED
        return TimeoutOutcome.FAIL
