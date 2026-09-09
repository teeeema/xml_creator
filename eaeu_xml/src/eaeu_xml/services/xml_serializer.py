from copy import deepcopy
import re
from xml.dom import minidom
from xml.etree import ElementTree as ET

from eaeu_xml.core.namespaces import NamespaceRegistry
from eaeu_xml.decision5.models.envelope import ApplicationMessage
from eaeu_xml.decision5.models.signal import SignalMessage, TechnicalFaultMessage
from eaeu_xml.decision5.models.header import HEADER_ELEMENT_ORDER, EndpointReference, SoapHeader
from eaeu_xml.decision5.validation.header_validator import HeaderValidator
from eaeu_xml.decision5.validation.fault_validator import FaultValidator
from eaeu_xml.decision5.validation.signal_validator import SignalValidator
from eaeu_xml.decision5.validation.envelope_validator import EnvelopeValidator
from eaeu_xml.decision5.validation.integration_validator import IntegrationValidator


class XmlSerializer:
    def __init__(self) -> None:
        self.namespaces = NamespaceRegistry()
        self.namespaces.register()
        self.validator = HeaderValidator()

    def serialize_application(self, message: ApplicationMessage, *, placeholder_versions=(), placeholder_sources=(), placeholder_structure_id=None, placeholder_model_prefixes=()) -> str:
        self.validator.validate_application(message.header, platform_enriched=message.header.integration is not None)
        return self._serialize(message,placeholder_versions=placeholder_versions,placeholder_sources=placeholder_sources,placeholder_structure_id=placeholder_structure_id,placeholder_model_prefixes=placeholder_model_prefixes)

    def serialize_signal(self, message: SignalMessage) -> str:
        SignalValidator().validate(message)
        return self._serialize(message)

    def serialize_fault(self, message: TechnicalFaultMessage) -> str:
        FaultValidator().validate(message)
        return self._serialize(message)

    def _serialize(self, message: object, *, placeholder_versions=(), placeholder_sources=(), placeholder_structure_id=None, placeholder_model_prefixes=()) -> str:
        EnvelopeValidator().validate(message)
        if message.header.integration is not None:
            IntegrationValidator().validate(message.header.integration)
        soap = self.namespaces.SOAP
        root = ET.Element(ET.QName(soap, "Envelope"))
        placeholders=tuple(dict.fromkeys(str(value) for value in placeholder_versions if value))
        if placeholders:
            structure_label=f" {placeholder_structure_id}" if placeholder_structure_id else ""
            prefixes=", ".join(dict.fromkeys(str(value) for value in placeholder_model_prefixes if value)) or "импортируемых моделей данных"
            root.append(ET.Comment(
                f"\n      Y.Y.Y — версия структуры электронного документа{structure_label}.\n"
                "      Определяется с учетом версии базисной модели данных,\n"
                "      использованной при разработке технической схемы структуры.\n\n"
                "      X.X.X — версия базисной модели данных,\n"
                f"      использованной для импортируемых пространств имен {prefixes}.\n\n"
                "      Значения определяются в соответствии с п. 2 Решения\n"
                "      Коллегии ЕЭК от 25.10.2016 № 122.\n    "
            ))
        header_element = ET.SubElement(root, ET.QName(soap, "Header"))
        for field_name in HEADER_ELEMENT_ORDER:
            value = getattr(message.header, field_name)
            if value is not None:
                self._append_header(header_element, field_name, value)
        body = ET.SubElement(root, ET.QName(soap, "Body"))
        body.append(deepcopy(message.body_payload.serialize_xml_element()))
        rough = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        pretty=minidom.parseString(rough).toprettyxml(indent="    ", encoding="UTF-8").decode("UTF-8")
        return self._format_envelope_namespaces(pretty)

    @staticmethod
    def _format_envelope_namespaces(xml: str) -> str:
        """Put namespace declarations on separate lines, grouped by responsibility."""
        match=re.search(r"(?m)^<([^\s>]+:)?Envelope(?P<attrs>[^>]*)>",xml)
        if not match:return xml
        attributes=re.findall(r'(xmlns(?::[^=\s]+)?="[^"]*")',match.group("attrs"))
        if not attributes:return xml
        def prefix(attribute):
            name=attribute.split("=",1)[0]
            return name.split(":",1)[1] if ":" in name else ""
        order={"soap":0,"wsa":1,"int":2}
        technology=sorted((attribute for attribute in attributes if prefix(attribute) in order),key=lambda item:order[prefix(item)])
        payload=[attribute for attribute in attributes if attribute not in technology]
        lines=[f"<{match.group(1) or ''}Envelope",*(f"    {item}" for item in technology)]
        if technology and payload:lines.append("")
        lines.extend(f"    {item}" for item in payload); lines[-1]+='>'
        return xml[:match.start()]+"\n".join(lines)+xml[match.end():]

    def _append_header(self, parent: ET.Element, field_name: str, value: object) -> None:
        wsa, interaction = self.namespaces.WSA, self.namespaces.INT
        if field_name == "to":
            ET.SubElement(parent, ET.QName(wsa, "To")).text = value.serialize()
        elif field_name in ("reply_to", "from_", "fault_to"):
            names = {"reply_to": "ReplyTo", "from_": "From", "fault_to": "FaultTo"}
            wrapper = ET.SubElement(parent, ET.QName(wsa, names[field_name]))
            ET.SubElement(wrapper, ET.QName(wsa, "Address")).text = value.address.serialize()
        elif field_name == "message_id":
            ET.SubElement(parent, ET.QName(wsa, "MessageID")).text = value.serialize()
        elif field_name == "relates_to":
            element = ET.SubElement(parent, ET.QName(wsa, "RelatesTo"))
            element.text = value.message_id.serialize()
            if value.relates_action:
                element.set(ET.QName(interaction, "RelatesAction"), value.relates_action)
        elif field_name == "action":
            ET.SubElement(parent, ET.QName(wsa, "Action")).text = value.serialize()
        elif field_name == "procedure_id":
            ET.SubElement(parent, ET.QName(interaction, "ProcedureID")).text = value.serialize()
        elif field_name == "conversation_id":
            ET.SubElement(parent, ET.QName(interaction, "ConversationID")).text = value.serialize()
        elif field_name == "integration":
            wrapper = ET.SubElement(parent, ET.QName(interaction, "Integration"))
            ET.SubElement(wrapper, ET.QName(interaction, "TrackID")).text = value.track_id.serialize()
            ET.SubElement(wrapper, ET.QName(interaction, "AcceptTime")).text = value.accept_time.serialize()
