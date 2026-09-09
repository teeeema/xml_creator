from eaeu_xml.core.errors import RetryNotAllowedError


class RetryValidator:
    def validate(self, original, retry) -> None:
        if retry.message_id == original.message_id or retry.retry_of != original.message_id:
            raise RetryNotAllowedError(code="D5_RETRY_ID", rule_id="D5-TRN-RETRY", message="Retry требует новый MessageID и retry_of исходной попытки.")
        if retry.action != original.action or retry.attempt_number != original.attempt_number + 1:
            raise RetryNotAllowedError(code="D5_RETRY_METADATA", rule_id="D5-TRN-RETRY", message="Retry должен сохранять Action и увеличивать номер попытки.")
