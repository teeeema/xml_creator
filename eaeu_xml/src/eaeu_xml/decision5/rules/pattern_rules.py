from dataclasses import dataclass

from eaeu_xml.core.enums import SignalKind, TransactionPattern, TransactionState
from eaeu_xml.core.errors import InvalidStateTransitionError
from eaeu_xml.decision5.models.transaction import MessageRecord, TransactionDefinition, TransactionInstance


@dataclass(frozen=True)
class PatternPlan:
    initial_wait: TransactionState
    after_received: TransactionState | None
    after_processing: TransactionState | None
    after_response: TransactionState
    response_received_required: bool = False
    response_processing_required: bool = False


def plan_for(definition: TransactionDefinition) -> PatternPlan:
    pattern, guaranteed = definition.pattern, definition.guaranteed_delivery
    if pattern is TransactionPattern.INFORMATION_DISTRIBUTION:
        return PatternPlan(TransactionState.COMPLETED, None, None, TransactionState.COMPLETED)
    if pattern is TransactionPattern.NOTIFICATION:
        return PatternPlan(TransactionState.WAITING_RECEIVED, TransactionState.COMPLETED, None, TransactionState.COMPLETED)
    if pattern is TransactionPattern.MUTUAL_OBLIGATIONS:
        return PatternPlan(TransactionState.WAITING_RECEIVED, TransactionState.WAITING_PROCESSING, TransactionState.WAITING_RESPONSE, TransactionState.WAITING_RESPONSE_RECEIVED, True, True)
    if pattern is TransactionPattern.REQUEST_RESPONSE and guaranteed:
        initial = TransactionState.WAITING_RECEIVED if definition.parameters.receive_confirmation_timeout else TransactionState.WAITING_PROCESSING
        return PatternPlan(initial, TransactionState.WAITING_PROCESSING, TransactionState.WAITING_RESPONSE, TransactionState.COMPLETED)
    if pattern is TransactionPattern.REQUEST_CONFIRMATION and guaranteed:
        return PatternPlan(TransactionState.WAITING_RESPONSE, None, None, TransactionState.WAITING_RESPONSE_RECEIVED, True)
    return PatternPlan(TransactionState.WAITING_RESPONSE, None, None, TransactionState.COMPLETED)


class TransactionStateMachine:
    def after_initial(self, transaction: TransactionInstance) -> TransactionState:
        self._require_definition(transaction)
        return plan_for(transaction.definition).initial_wait

    def receive_signal(self, transaction: TransactionInstance, kind: SignalKind) -> TransactionState:
        if kind is SignalKind.ERROR:
            definition = self._require_definition(transaction)
            return TransactionState.ROLLBACK_REQUIRED if definition.pattern is TransactionPattern.MUTUAL_OBLIGATIONS else TransactionState.FAILED
        plan = plan_for(self._require_definition(transaction))
        if kind is SignalKind.RECEIVED:
            expected = {TransactionState.WAITING_RECEIVED, TransactionState.WAITING_RESPONSE_RECEIVED}
            if transaction.state not in expected:
                self._invalid(transaction, kind.value)
            if transaction.state is TransactionState.WAITING_RESPONSE_RECEIVED:
                return TransactionState.WAITING_RESPONSE_PROCESSING if plan.response_processing_required else TransactionState.COMPLETED
            return plan.after_received or TransactionState.COMPLETED
        if transaction.state not in {TransactionState.WAITING_PROCESSING, TransactionState.WAITING_RESPONSE_PROCESSING}:
            self._invalid(transaction, kind.value)
        if transaction.state is TransactionState.WAITING_RESPONSE_PROCESSING:
            return TransactionState.WAITING_FINAL_ERROR_WINDOW
        return plan.after_processing or TransactionState.WAITING_RESPONSE

    def receive_response(self, transaction: TransactionInstance) -> TransactionState:
        if transaction.state is not TransactionState.WAITING_RESPONSE:
            self._invalid(transaction, "response")
        return plan_for(self._require_definition(transaction)).after_response

    def correlation_source(self, transaction: TransactionInstance) -> MessageRecord:
        if not transaction.message_history:
            self._invalid(transaction, "follow-up")
        # Paragraph 102: source is the message received at the preceding transaction stage.
        return transaction.message_history[-1]

    @staticmethod
    def _require_definition(transaction: TransactionInstance) -> TransactionDefinition:
        if transaction.definition is None:
            from eaeu_xml.core.errors import TransactionPatternError
            raise TransactionPatternError(code="D5_PATTERN_REQUIRED", rule_id="D5-TRN-PATTERNS", message="Для state machine требуется TransactionDefinition.")
        return transaction.definition

    @staticmethod
    def _invalid(transaction: TransactionInstance, event: str) -> None:
        raise InvalidStateTransitionError(code="D5_INVALID_TRANSITION", rule_id="D5-TRN-PATTERNS", message=f"Событие {event} недопустимо в состоянии {transaction.state.value}.")
