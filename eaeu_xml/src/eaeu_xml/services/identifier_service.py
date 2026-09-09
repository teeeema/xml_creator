from uuid import UUID, uuid4

from eaeu_xml.decision5.models.identifiers import ConversationId, MessageId


class IdentifierService:
    def new_identifier(self) -> UUID:
        """Create a generic UUID value for editable identifier fields."""
        return uuid4()

    def new_message_id(self) -> MessageId:
        return MessageId(uuid4())

    def new_procedure_component(self) -> UUID:
        return uuid4()

    def new_conversation_id(self) -> ConversationId:
        return ConversationId(uuid4())

    def new_signal_id(self) -> UUID:
        return uuid4()
