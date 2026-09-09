from eaeu_xml.core.enums import HeaderFieldStatus
from eaeu_xml.core.errors import ForbiddenHeaderFieldError, MissingRequiredHeaderFieldError
from eaeu_xml.decision5.models.header import SoapHeader
from eaeu_xml.decision5.rules.header_rules import APPLICATION_HEADER_POLICY
from eaeu_xml.decision5.validation.action_validator import ActionValidator
from eaeu_xml.decision5.validation.address_validator import LogicalAddressValidator
from eaeu_xml.decision5.validation.identifier_validator import IdentifierValidator


class HeaderValidator:
    def validate_application(self, header: SoapHeader, *, platform_enriched: bool = False) -> None:
        for field_name, status in APPLICATION_HEADER_POLICY.items():
            value = getattr(header, field_name)
            if status is HeaderFieldStatus.FORBIDDEN and value is not None:
                raise ForbiddenHeaderFieldError(
                    code=f"D5_HEADER_{field_name.upper()}_FORBIDDEN",
                    rule_id="D5-HDR-APP-FROM" if field_name == "from_" else "D5-HDR-APP-FAULTTO",
                    message=f"Поле {field_name} запрещено для прикладного сообщения общего процесса.",
                )
            if status is HeaderFieldStatus.PLATFORM_GENERATED and value is not None and not platform_enriched:
                raise ForbiddenHeaderFieldError(code="D5_HEADER_INTEGRATION_PLATFORM_ONLY", rule_id="D5-HDR-INTEGRATION", message="Integration формируется только интеграционной платформой.")
            if status in (HeaderFieldStatus.REQUIRED, HeaderFieldStatus.DERIVED) and field_name != "relates_to" and value is None:
                raise MissingRequiredHeaderFieldError(code=f"D5_HEADER_{field_name.upper()}_REQUIRED", rule_id="D5-HDR-BASE", message=f"Отсутствует заголовок {field_name}.")
        addresses = LogicalAddressValidator()
        addresses.validate(header.to)
        if header.reply_to is not None:
            addresses.validate(header.reply_to.address)
        identifiers = IdentifierValidator()
        identifiers.validate_message_id(header.message_id)
        identifiers.validate_procedure_id(header.procedure_id)
        identifiers.validate_conversation_id(header.conversation_id)
        ActionValidator().validate(header.action)
