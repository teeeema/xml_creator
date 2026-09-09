from dataclasses import dataclass
from enum import Enum
from xml.etree import ElementTree as ET

from eaeu_xml.core.errors import FaultValidationError
from eaeu_xml.core.namespaces import NamespaceRegistry


class FaultSubcode(str, Enum):
    INVALID_ADDRESSING_HEADER = "wsa:InvalidAddressingHeader"
    MESSAGE_ADDRESSING_HEADER_REQUIRED = "wsa:MessageAddressingHeaderRequired"
    DESTINATION_UNREACHABLE = "wsa:DestinationUnreachable"
    ACTION_NOT_SUPPORTED = "wsa:ActionNotSupported"
    INVALID_HEADER = "int:InvalidHeader"
    ENDPOINT_UNAVAILABLE = "wsa:EndpointUnavailable"
    INTERNAL_ERROR = "int:InternalError"
    DATA_ERROR = "int:DataError"

    @property
    def soap_code(self) -> str:
        return "soap:Receiver" if self in {self.ENDPOINT_UNAVAILABLE, self.INTERNAL_ERROR} else "soap:Sender"


@dataclass(frozen=True)
class FaultReasonText:
    text: str
    language: str

    def __post_init__(self) -> None:
        if not self.text or not self.language:
            raise FaultValidationError(code="D5_FAULT_REASON", rule_id="D5-FAULT-REASON", message="Fault Reason требует текст и xml:lang.")


@dataclass(frozen=True)
class ProblemMessage:
    element: ET.Element

    def __post_init__(self) -> None:
        try:
            ET.fromstring(ET.tostring(self.element))
        except ET.ParseError as error:
            raise FaultValidationError(code="D5_PROBLEM_XML", rule_id="D5-FAULT-DETAIL", message="ProblemMessage должен быть well-formed XML.") from error

    def serialize_source(self) -> str:
        return ET.tostring(self.element, encoding="unicode")


@dataclass(frozen=True)
class SoapFault:
    subcode: FaultSubcode
    reasons: tuple[FaultReasonText, ...]
    problem_message: ProblemMessage | None = None

    def __post_init__(self) -> None:
        languages = [reason.language for reason in self.reasons]
        if not self.reasons or "ru" not in languages or len(languages) != len(set(languages)):
            raise FaultValidationError(code="D5_FAULT_LANG", rule_id="D5-FAULT-REASON", message="Нужен уникальный русский текст причины.")

    def serialize_xml_element(self) -> ET.Element:
        ns = NamespaceRegistry()
        fault = ET.Element(ET.QName(ns.SOAP, "Fault"))
        code = ET.SubElement(fault, ET.QName(ns.SOAP, "Code"))
        ET.SubElement(code, ET.QName(ns.SOAP, "Value")).text = self.subcode.soap_code
        subcode = ET.SubElement(code, ET.QName(ns.SOAP, "Subcode"))
        ET.SubElement(subcode, ET.QName(ns.SOAP, "Value")).text = self.subcode.value
        reason = ET.SubElement(fault, ET.QName(ns.SOAP, "Reason"))
        xml_lang = "{http://www.w3.org/XML/1998/namespace}lang"
        for item in self.reasons:
            text = ET.SubElement(reason, ET.QName(ns.SOAP, "Text"), {xml_lang: item.language})
            text.text = item.text
        if self.problem_message:
            detail = ET.SubElement(fault, ET.QName(ns.SOAP, "Detail"))
            problem = ET.SubElement(detail, ET.QName(ns.INT, "ProblemMessage"))
            # Paragraph 76 defines message text inside CDATA. ElementTree does not
            # preserve CDATA lexically; escaped text has the same parsed value.
            problem.text = self.problem_message.serialize_source()
        return fault
