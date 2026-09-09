from eaeu_xml.core.errors import CorrelationError
from eaeu_xml.decision5.models.transaction import TransactionInstance


class CorrelationValidator:
    def validate_history(self, transaction: TransactionInstance) -> None:
        known_ids = set()
        for index, record in enumerate(transaction.message_history):
            if record.sequence_number != index + 1:
                    raise CorrelationError(code="D5_CORRELATION_SEQUENCE", rule_id="D5-CORR-HISTORY", message="Нарушена последовательность истории сообщений.")
            if record.message_id in known_ids:
                raise CorrelationError(code="D5_MESSAGE_ID_REUSED", rule_id="D5-ID-MESSAGE", message="Каждое новое сообщение требует новый MessageID.")
            if index == 0 and record.relates_to is not None:
                raise CorrelationError(code="D5_INITIAL_RELATES_TO", rule_id="D5-CORR-INITIAL", message="Initial message не должен иметь RelatesTo.")
            if index > 0 and record.relates_to is not None and record.relates_to not in known_ids:
                raise CorrelationError(code="D5_FOLLOWUP_RELATES_TO", rule_id="D5-CORR-FOLLOWUP", message="RelatesTo должен ссылаться на известное сообщение предыдущего этапа.")
            known_ids.add(record.message_id)
