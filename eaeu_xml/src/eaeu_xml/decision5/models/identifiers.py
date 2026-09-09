from dataclasses import dataclass
from uuid import UUID

from eaeu_xml.core.errors import IdentifierValidationError, ProcedureIdError


URN_PREFIX = "urn:uuid:"


def _parse_uuid_uri(value: str, *, code: str, rule_id: str) -> UUID:
    if not value.startswith(URN_PREFIX):
        raise IdentifierValidationError(code=code, rule_id=rule_id, message="Ожидается URI urn:uuid:<UUID>.")
    try:
        return UUID(value[len(URN_PREFIX):])
    except ValueError as error:
        raise IdentifierValidationError(code=code, rule_id=rule_id, message="Некорректный UUID.") from error


@dataclass(frozen=True)
class MessageId:
    value: UUID

    def serialize(self) -> str:
        return f"{URN_PREFIX}{self.value}"

    @classmethod
    def parse(cls, value: str) -> "MessageId":
        return cls(_parse_uuid_uri(value, code="D5_MESSAGE_ID_INVALID", rule_id="D5-ID-MESSAGE"))


@dataclass(frozen=True)
class ConversationId:
    value: UUID

    def serialize(self) -> str:
        return f"{URN_PREFIX}{self.value}"

    @classmethod
    def parse(cls, value: str) -> "ConversationId":
        return cls(_parse_uuid_uri(value, code="D5_CONVERSATION_ID_INVALID", rule_id="D5-ID-CONVERSATION"))


@dataclass(frozen=True)
class ProcedureId:
    components: tuple[UUID, ...]

    def __post_init__(self) -> None:
        if not self.components:
            raise ProcedureIdError(code="D5_PROCEDURE_ID_EMPTY", rule_id="D5-ID-PROCEDURE", message="ProcedureID не может быть пустым.")

    @classmethod
    def root(cls, identifier_service: object) -> "ProcedureId":
        return cls((identifier_service.new_procedure_component(),))

    def child(self, identifier_service: object) -> "ProcedureId":
        return ProcedureId(self.components + (identifier_service.new_procedure_component(),))

    def parent(self) -> "ProcedureId | None":
        return ProcedureId(self.components[:-1]) if len(self.components) > 1 else None

    @property
    def depth(self) -> int:
        return len(self.components)

    def serialize(self) -> str:
        return "/".join(f"{URN_PREFIX}{component}" for component in self.components)

    @classmethod
    def parse(cls, value: str) -> "ProcedureId":
        if not value or "//" in value:
            raise ProcedureIdError(code="D5_PROCEDURE_ID_INVALID", rule_id="D5-ID-PROCEDURE", message="Повреждена цепочка ProcedureID.")
        try:
            return cls(tuple(_parse_uuid_uri(item, code="D5_PROCEDURE_ID_INVALID", rule_id="D5-ID-PROCEDURE") for item in value.split("/")))
        except IdentifierValidationError as error:
            raise ProcedureIdError(code=error.code, rule_id=error.rule_id, message=error.message) from error
