"""Validation of an already serialized application XML document.

This service intentionally reuses the Decision No. 5 vocabulary and process
definition metadata.  It does not attempt to reverse arbitrary XML into form
values, so body cardinality/business rules remain owned by the existing body
validator.
"""

from dataclasses import dataclass
from xml.etree import ElementTree as ET

from eaeu_xml.core.namespaces import NamespaceRegistry
from eaeu_xml.decision5.models.action import ApplicationAction
from eaeu_xml.decision5.models.header import HEADER_ELEMENT_ORDER
from eaeu_xml.decision5.rules.header_rules import APPLICATION_HEADER_POLICY
from eaeu_xml.core.enums import HeaderFieldStatus


@dataclass(frozen=True)
class XmlDiagnostic:
    severity: str
    code: str
    message: str
    location: str = "XML"
    line: int | None = None
    column: int | None = None


@dataclass(frozen=True)
class XmlValidationResult:
    diagnostics: tuple[XmlDiagnostic, ...]

    @property
    def is_valid(self):
        return not any(item.severity == "ERROR" for item in self.diagnostics)


class XmlValidationService:
    """Validate the checks that can be reliably evaluated from XML text."""

    _header_names = {
        "To": "to", "ReplyTo": "reply_to", "From": "from_", "FaultTo": "fault_to",
        "MessageID": "message_id", "RelatesTo": "relates_to", "Action": "action",
        "ProcedureID": "procedure_id", "ConversationID": "conversation_id", "Integration": "integration",
    }

    @staticmethod
    def _start_tag_positions(text):
        """Return source positions for start tags without changing XML text."""
        result, index, line, column = [], 0, 1, 1
        length = len(text)
        while index < length:
            if text[index] != "<":
                if text[index] == "\n": line, column = line + 1, 1
                else: column += 1
                index += 1
                continue
            if text.startswith("<!--", index):
                end = text.find("-->", index + 4)
            elif text.startswith("<![CDATA[", index):
                end = text.find("]]>", index + 9)
            elif text.startswith("<?", index):
                end = text.find("?>", index + 2)
            elif text.startswith("</", index) or text.startswith("<!", index):
                end = text.find(">", index + 2)
            else:
                start_line, start_column, cursor, quote = line, column, index + 1, None
                while cursor < length:
                    char = text[cursor]
                    if quote:
                        if char == quote: quote = None
                    elif char in "\"'": quote = char
                    elif char == ">": break
                    cursor += 1
                if cursor >= length: break
                name = text[index + 1:cursor].lstrip().split(None, 1)[0].rstrip("/")
                result.append((name.rsplit(":", 1)[-1], start_line, start_column))
                end = cursor
            if end < 0: break
            segment = text[index:end + (3 if text.startswith(("<!--", "<![CDATA["), index) else 2 if text.startswith("<?", index) else 1)]
            newlines = segment.count("\n")
            line = line + newlines
            column = (len(segment.rsplit("\n", 1)[-1]) + 1) if newlines else column + len(segment)
            index += len(segment)
        return result

    def _positions(self, root, text):
        tags = self._start_tag_positions(text)
        positions = {}
        for element, (name, line, column) in zip(root.iter(), tags):
            if self._local(element.tag) != name:
                return {}
            positions[id(element)] = (line, column)
        return positions

    @staticmethod
    def _issue(code, message, location, element, positions):
        line_column = positions.get(id(element)) if element is not None else None
        return XmlDiagnostic("ERROR", code, message, location, *(line_column or (None, None)))

    def validate(self, xml_text, *, engine, transaction_code, message_code, mode):
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as error:
            line, column = error.position
            return XmlValidationResult((XmlDiagnostic("ERROR", "XML_PARSE_ERROR", str(error), "XML", line, column),))

        ns = NamespaceRegistry()
        positions = self._positions(root, xml_text)
        issues = []
        if root.tag != f"{{{ns.SOAP}}}Envelope":
            issues.append(self._issue("D5_SOAP_ENVELOPE_NAMESPACE", "Ожидается SOAP 1.2 Envelope.", "Envelope", root, positions))
            return XmlValidationResult(tuple(issues))
        header = root.find(f"{{{ns.SOAP}}}Header")
        body = root.find(f"{{{ns.SOAP}}}Body")
        if header is None or body is None:
            issues.append(self._issue("D5_ENVELOPE_PART", "SOAP Envelope требует Header и Body.", "Envelope", root, positions))
            return XmlValidationResult(tuple(issues))

        names = [self._header_names.get(self._local(child.tag)) for child in list(header)]
        known = [name for name in names if name]
        expected_order = [name for name in HEADER_ELEMENT_ORDER if name in known]
        if known != expected_order:
            issues.append(self._issue("D5_HEADER_ORDER", "Нарушен нормативный порядок элементов SOAP Header.", "Header", header, positions))
        present = set(known)
        for name, status in APPLICATION_HEADER_POLICY.items():
            if status in (HeaderFieldStatus.REQUIRED, HeaderFieldStatus.DERIVED) and name != "relates_to" and name not in present:
                issues.append(XmlDiagnostic("ERROR", f"D5_HEADER_{name.upper()}_REQUIRED", f"Отсутствует заголовок {name}.", "Header"))
            if status is HeaderFieldStatus.FORBIDDEN and name in present:
                issues.append(XmlDiagnostic("ERROR", f"D5_HEADER_{name.upper()}_FORBIDDEN", f"Поле {name} запрещено для прикладного сообщения общего процесса.", "Header"))

        action_element = header.find(f"{{{ns.WSA}}}Action")
        action = action_element.text if action_element is not None else None
        if action:
            try:
                parsed = ApplicationAction.parse(action)
                expected = engine.build_application_action(transaction_code, message_code)
                if parsed.serialize() != expected.serialize():
                    issues.append(self._issue("D5_ACTION_UNEXPECTED", "Action не соответствует выбранному PROCESS/TRN/MSG.", "Header/Action", action_element, positions))
            except Exception as error:
                issues.append(self._issue(getattr(error, "code", "D5_ACTION_FORMAT"), getattr(error, "message", str(error)), "Header/Action", action_element, positions))

        children = list(body)
        structure = engine.get_structure(message_code, mode=mode)
        if structure.root_element and children:
            expected_tag = f"{{{structure.namespace}}}{structure.root_element}" if structure.namespace else structure.root_element
            if children[0].tag != expected_tag:
                issues.append(self._issue("BODY_ROOT_UNEXPECTED", "Корневой элемент Body не соответствует выбранному сообщению.", "Body", children[0], positions))
        elif structure.root_element:
            issues.append(XmlDiagnostic("ERROR", "BODY_ROOT_MISSING", "SOAP Body не содержит прикладное сообщение.", "Body"))
        return XmlValidationResult(tuple(issues))

    @staticmethod
    def _local(tag):
        return tag.rsplit("}", 1)[-1]
