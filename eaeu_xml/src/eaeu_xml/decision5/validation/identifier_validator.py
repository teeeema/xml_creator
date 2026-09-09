from eaeu_xml.decision5.models.identifiers import ConversationId, MessageId, ProcedureId


class IdentifierValidator:
    def validate_message_id(self, value: MessageId) -> None:
        MessageId.parse(value.serialize())

    def validate_conversation_id(self, value: ConversationId) -> None:
        ConversationId.parse(value.serialize())

    def validate_procedure_id(self, value: ProcedureId) -> None:
        ProcedureId.parse(value.serialize())
