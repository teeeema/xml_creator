from dataclasses import dataclass
from typing import Protocol
from xml.etree import ElementTree as ET

from eaeu_xml.decision5.models.header import SoapHeader


class BodyPayload(Protocol):
    def serialize_xml_element(self) -> ET.Element: ...


@dataclass(frozen=True)
class DummyBodyPayload:
    text: str
    namespace: str = "urn:test:payload"

    def serialize_xml_element(self) -> ET.Element:
        ET.register_namespace("test", self.namespace)
        element = ET.Element(ET.QName(self.namespace, "Payload"))
        element.text = self.text
        return element


@dataclass(frozen=True)
class ApplicationMessage:
    header: SoapHeader
    body_payload: BodyPayload


@dataclass(frozen=True)
class SoapEnvelope:
    header: SoapHeader
    body_payload: BodyPayload
