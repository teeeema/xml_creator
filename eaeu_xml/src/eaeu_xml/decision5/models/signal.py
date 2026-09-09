from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID
from xml.etree import ElementTree as ET

from eaeu_xml.core.enums import SignalKind
from eaeu_xml.core.errors import SignalValidationError
from eaeu_xml.core.namespaces import NamespaceRegistry
from eaeu_xml.decision5.models.header import SoapHeader


class SignalErrorCode(str, Enum):
    UNEXPECTED_MESSAGE = "Common:UnexpectedMessage"
    DATA_ERROR = "Common:DataError"
    FATAL_ERROR = "Common:FatalError"


@dataclass(frozen=True)
class SignalError:
    code: SignalErrorCode | str
    description: str
    details: str | None = None
    document_id: UUID | None = None
    reference: str | None = None

    def __post_init__(self) -> None:
        code = self.code.value if isinstance(self.code, SignalErrorCode) else self.code
        if not 1 <= len(code) <= 255 or not self.description:
            raise SignalValidationError(code="D5_SIGNAL_ERROR", rule_id="D5-SIGNAL-BODY", message="Ошибка требует code (1..255) и description.")


@dataclass(frozen=True)
class SignalPayload:
    kind: SignalKind
    signal_id: UUID
    created_at: datetime
    errors: tuple[SignalError, ...] = ()

    def __post_init__(self) -> None:
        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise SignalValidationError(code="D5_SIGNAL_TIME", rule_id="D5-SIGNAL-BODY", message="DateTime должен содержать часовой пояс.")
        if self.kind is SignalKind.ERROR and not self.errors:
            raise SignalValidationError(code="D5_SIGNAL_ERRORS_REQUIRED", rule_id="D5-SIGNAL-BODY", message="ValidationError требует минимум один Error.")
        if self.kind is not SignalKind.ERROR and self.errors:
            raise SignalValidationError(code="D5_SIGNAL_ERRORS_FORBIDDEN", rule_id="D5-SIGNAL-BODY", message="Error допустим только в ValidationError.")

    def serialize_xml_element(self) -> ET.Element:
        ns = NamespaceRegistry().SIGNAL
        wrapper_names = {SignalKind.RECEIVED: "DeliveryReceipt", SignalKind.ACCEPTED_FOR_PROCESSING: "ProcessingReceipt", SignalKind.ERROR: "ValidationError"}
        root = ET.Element(ET.QName(ns, wrapper_names[self.kind]))
        ET.SubElement(root, ET.QName(ns, "SignalId")).text = str(self.signal_id)
        ET.SubElement(root, ET.QName(ns, "DateTime")).text = self.created_at.isoformat()
        for item in self.errors:
            error = ET.SubElement(root, ET.QName(ns, "Error"))
            ET.SubElement(error, ET.QName(ns, "Code")).text = item.code.value if isinstance(item.code, SignalErrorCode) else item.code
            ET.SubElement(error, ET.QName(ns, "Description")).text = item.description
            for name, value in (("Details", item.details), ("EDocId", str(item.document_id) if item.document_id else None), ("Reference", item.reference)):
                if value is not None: ET.SubElement(error, ET.QName(ns, name)).text = value
        return root


@dataclass(frozen=True)
class SignalMessage:
    header: SoapHeader
    body_payload: SignalPayload


@dataclass(frozen=True)
class TechnicalFaultMessage:
    header: SoapHeader
    body_payload: object
    source_message_id: object | None = None
    source_action: str | None = None
