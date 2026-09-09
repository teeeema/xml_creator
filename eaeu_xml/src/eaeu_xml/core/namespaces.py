from dataclasses import dataclass
from xml.etree import ElementTree as ET


@dataclass(frozen=True)
class NamespaceRegistry:
    SOAP: str = "http://www.w3.org/2003/05/soap-envelope"
    WSA: str = "http://www.w3.org/2005/08/addressing"
    INT: str = "urn:EEC:Interaction:v1.0"
    SIGNAL: str = "urn:EEC:signal:v1.0"

    @classmethod
    def register(cls) -> None:
        registry = cls()
        ET.register_namespace("soap", registry.SOAP)
        ET.register_namespace("wsa", registry.WSA)
        ET.register_namespace("int", registry.INT)
        ET.register_namespace("sgn", registry.SIGNAL)
