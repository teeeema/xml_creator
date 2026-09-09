from eaeu_xml.core.enums import HeaderFieldStatus


APPLICATION_HEADER_POLICY = {
    "to": HeaderFieldStatus.REQUIRED,
    "reply_to": HeaderFieldStatus.REQUIRED,
    "from_": HeaderFieldStatus.FORBIDDEN,
    "fault_to": HeaderFieldStatus.FORBIDDEN,
    "message_id": HeaderFieldStatus.REQUIRED,
    "relates_to": HeaderFieldStatus.DERIVED,
    "action": HeaderFieldStatus.REQUIRED,
    "procedure_id": HeaderFieldStatus.DERIVED,
    "conversation_id": HeaderFieldStatus.DERIVED,
    "integration": HeaderFieldStatus.PLATFORM_GENERATED,
}
