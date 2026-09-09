from eaeu_xml.core.errors import CorrelationError
from eaeu_xml.decision5.models.header import RelatesTo
from eaeu_xml.decision5.models.transaction import TransactionInstance
from eaeu_xml.decision5.rules.pattern_rules import TransactionStateMachine


class CorrelationService:
    def __init__(self, state_machine: TransactionStateMachine | None = None) -> None:
        self.state_machine = state_machine
    def for_initial(self, transaction: TransactionInstance) -> None:
        if transaction.message_history:
            raise CorrelationError(code="D5_INITIAL_HISTORY_NOT_EMPTY", rule_id="D5-CORR-INITIAL", message="Initial message допустимо только для пустой истории.")
        return None

    def for_followup(self, transaction: TransactionInstance) -> RelatesTo:
        if not transaction.message_history:
            raise CorrelationError(code="D5_FOLLOWUP_HISTORY_EMPTY", rule_id="D5-CORR-FOLLOWUP", message="Для follow-up отсутствует предыдущее сообщение.")
        source = self.state_machine.correlation_source(transaction) if self.state_machine and transaction.definition else transaction.message_history[-1]
        return RelatesTo(source.message_id)
