from dataclasses import dataclass
import re

from eaeu_xml.core.enums import LogicalAddressSpace, SegmentKind
from eaeu_xml.core.errors import AddressValidationError


CODE = re.compile(r"[A-Za-z0-9._~-]+")


@dataclass(frozen=True)
class CommonProcessParticipantId:
    process_code: str
    participant_code: str
    authority_identifier: str | None = None

    def components(self) -> tuple[str, ...]:
        values = (self.process_code, self.participant_code)
        return values + ((self.authority_identifier,) if self.authority_identifier else ())


@dataclass(frozen=True)
class CompetentAuthorityId:
    authority_identifier: str

    def components(self) -> tuple[str, ...]:
        return (self.authority_identifier,)


@dataclass(frozen=True)
class ServiceResourceId:
    resource_identifier: str

    @property
    def identifier_validated(self) -> bool:
        return self.resource_identifier == "gate"

    def components(self) -> tuple[str, ...]:
        return (self.resource_identifier,)


ParticipantId = CommonProcessParticipantId | CompetentAuthorityId | ServiceResourceId


@dataclass(frozen=True)
class LogicalAddress:
    segment: str
    address_space: LogicalAddressSpace
    participant_identifier: ParticipantId
    scheme: str = "EAEU"

    @property
    def segment_kind(self) -> SegmentKind:
        return SegmentKind.EEC if self.segment == "EEC" else SegmentKind.MEMBER_STATE

    @property
    def syntax_valid(self) -> bool:
        return True

    @property
    def membership_validated(self) -> bool:
        return self.segment == "EEC"

    def serialize(self) -> str:
        return "/".join((f"{self.scheme}:/", self.segment, self.address_space.value, *self.participant_identifier.components()))

    @classmethod
    def parse(cls, value: str) -> "LogicalAddress":
        if not value.startswith("EAEU://"):
            raise AddressValidationError(code="D5_ADDRESS_SCHEME", rule_id="D5-ADDR-FORMAT", message="Логический адрес должен начинаться с EAEU://.")
        parts = value[len("EAEU://"):].split("/")
        if len(parts) < 3 or any(not item for item in parts):
            raise AddressValidationError(code="D5_ADDRESS_STRUCTURE", rule_id="D5-ADDR-FORMAT", message="Нарушена структура логического адреса.")
        segment, raw_space, *identifier = parts
        if segment != "EEC" and re.fullmatch(r"[A-Z]{2}", segment) is None:
            raise AddressValidationError(code="D5_ADDRESS_SEGMENT", rule_id="D5-ADDR-SEGMENT", message="Национальный сегмент должен иметь синтаксис ISO alpha-2.")
        try:
            space = LogicalAddressSpace(raw_space)
        except ValueError as error:
            raise AddressValidationError(code="D5_ADDRESS_SPACE", rule_id="D5-ADDR-SPACE", message="Неизвестное пространство логических адресов.") from error
        if any(CODE.fullmatch(item) is None for item in identifier):
            raise AddressValidationError(code="D5_ADDRESS_IDENTIFIER", rule_id="D5-ADDR-FORMAT", message="Некорректный идентификатор участника.")
        if space is LogicalAddressSpace.CP and len(identifier) in (2, 3):
            participant: ParticipantId = CommonProcessParticipantId(*identifier)
        elif space is LogicalAddressSpace.CA and len(identifier) == 1:
            participant = CompetentAuthorityId(identifier[0])
        elif space is LogicalAddressSpace.SR and len(identifier) == 1:
            participant = ServiceResourceId(identifier[0])
        else:
            raise AddressValidationError(code="D5_ADDRESS_IDENTIFIER", rule_id="D5-ADDR-SPACE", message="Количество компонентов не соответствует пространству адреса.")
        return cls(segment, space, participant)
