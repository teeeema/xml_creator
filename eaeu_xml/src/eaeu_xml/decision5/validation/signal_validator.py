from eaeu_xml.core.errors import SignalValidationError
from eaeu_xml.decision5.models.action import SignalAction


class SignalValidator:
    def validate(self, message) -> None:
        if not isinstance(message.header.action, SignalAction) or message.header.relates_to is None:
            raise SignalValidationError(code="D5_SIGNAL_HEADER", rule_id="D5-SIGNAL-ACTION", message="Сигнал требует SignalAction и RelatesTo.")
        if message.header.action.signal_code != message.body_payload.kind.value:
            raise SignalValidationError(code="D5_SIGNAL_KIND_MISMATCH", rule_id="D5-SIGNAL-ACTION", message="Action и Body сигнала не согласованы.")
        header = message.header
        if header.reply_to is None or header.from_ is not None or header.fault_to is not None:
            raise SignalValidationError(code="D5_SIGNAL_APP_HEADER", rule_id="D5-HDR-APP-FROM", message="Сигнал является прикладным сообщением: ReplyTo обязателен, From/FaultTo запрещены.")
