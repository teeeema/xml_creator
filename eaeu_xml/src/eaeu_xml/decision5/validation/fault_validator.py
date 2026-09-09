from eaeu_xml.core.errors import FaultValidationError
from eaeu_xml.decision5.models.action import FaultAction


class FaultValidator:
    def validate(self, message) -> None:
        header = message.header
        if header.reply_to is not None or header.fault_to is not None or header.from_ is None:
            raise FaultValidationError(code="D5_FAULT_HEADER", rule_id="D5-FAULT-HEADER", message="Fault требует From и запрещает ReplyTo/FaultTo.")
        if not isinstance(header.action, FaultAction) or header.relates_to is None or not header.relates_to.relates_action:
            raise FaultValidationError(code="D5_FAULT_CORRELATION", rule_id="D5-FAULT-CORRELATION", message="Fault требует typed Action, RelatesTo и RelatesAction.")
        if message.source_message_id is None or header.message_id == message.source_message_id or header.relates_to.message_id != message.source_message_id:
            raise FaultValidationError(code="D5_FAULT_MESSAGE_ID", rule_id="D5-FAULT-CORRELATION", message="Fault требует новый MessageID и RelatesTo исходного сообщения.")
        if message.source_action is None or header.relates_to.relates_action != message.source_action:
            raise FaultValidationError(code="D5_FAULT_RELATES_ACTION", rule_id="D5-FAULT-CORRELATION", message="RelatesAction должен совпадать с Action исходного сообщения.")
