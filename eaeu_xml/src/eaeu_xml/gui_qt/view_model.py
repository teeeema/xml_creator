"""QObject bridge between QML and the existing application/controller layer."""

from __future__ import annotations

from pathlib import Path
from xml.dom import minidom

from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtGui import QGuiApplication

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.application.xml_validation_service import XmlValidationService
from eaeu_xml.application.xml_formatter import XmlFormatter
from eaeu_xml.presentation.controller import GuiController


class GuiViewModel(QObject):
    """Expose presentation state only; all domain work stays in GuiController."""

    changed = Signal()
    noticeChanged = Signal()
    navigateToXmlPosition = Signal(int, int)

    def __init__(self, processes_root: Path, *, application=None) -> None:
        super().__init__()
        self.controller = GuiController(application or EaeuXmlApplication(Path(processes_root)))
        self._xml = ""
        self._xml_font_size = 14
        self._formatter_xml = ""
        self._formatter_font_size = 14
        self._xml_validation_error = ""
        self._xml_validation = None
        self._notice = ""
        self._selected_field = None

    @staticmethod
    def _choice(code, name):
        return {"code": code, "label": f"{code} — {name or ''}".rstrip(" —")}

    @Property("QVariantList", notify=changed)
    def processes(self):
        return [self._choice(item.process_code, item.name) for item in self.controller.processes]

    @Property("QVariantList", notify=changed)
    def transactions(self):
        return [self._choice(item.transaction_code, item.name) for item in self.controller.transactions]

    @Property("QVariantList", notify=changed)
    def messages(self):
        return [self._choice(item.message_code, item.name) for item in self.controller.messages]

    @Property(str, notify=changed)
    def processCode(self): return self.controller.process_code or ""

    @Property(str, notify=changed)
    def transactionCode(self): return self.controller.transaction_code or ""

    @Property(str, notify=changed)
    def messageCode(self): return self.controller.message_code or ""

    @Property("QVariantList", notify=changed)
    def fields(self):
        result = []
        def add(model, level=0):
            if model.visibility == "HIDDEN": return
            if model.children:
                result.append({"path": model.path, "label": model.label, "kind": "GROUP", "level": level,
                               "required": model.required, "readOnly": model.read_only, "value": "", "choices": [],
                               "help": model.tooltip})
                for child in model.children: add(child, level + 1)
                return
            field = self.controller.find_field(model.path)
            value = self.controller.values.get(model.path, "")
            if isinstance(value, bool): value = "true" if value else "false"
            elif value is None: value = ""
            elif isinstance(value, list): value = ", ".join(map(str, value))
            result.append({"path": model.path, "label": model.label, "kind": model.control_kind, "level": level,
                           "required": model.required, "readOnly": model.read_only, "value": str(value),
                           "choices": [str(item) for item in (field.allowed_values if field else ())],
                           "help": model.tooltip, "placeholder": str(model.example_value or "")})
        for model in self.controller.visible_control_models(): add(model)
        return result

    @Property(str, notify=changed)
    def messageSummary(self):
        message = self.controller.current_message
        if not message: return "Сообщение не выбрано."
        return f"{message.message_code}\n{message.name or ''}\n\nСтруктура: {message.structure_id or 'не указана'}\nСтатус: {message.generation_status}"

    @Property(str, notify=changed)
    def selectedFieldInfo(self):
        field = self.controller.find_field(self._selected_field) if self._selected_field else None
        return self.controller.field_help(field) if field else self.messageSummary

    @Property(str, notify=changed)
    def xml(self): return self._xml

    @Property(int, notify=changed)
    def xmlFontSize(self): return self._xml_font_size

    @Property(str, notify=changed)
    def formatterXml(self): return self._formatter_xml

    @Property(int, notify=changed)
    def formatterFontSize(self): return self._formatter_font_size

    @Property("QVariantList", notify=changed)
    def validationItems(self):
        if self._xml_validation_error:
            return [{"severity": "ERROR", "code": "XML_PARSE_ERROR", "message": self._xml_validation_error,
                     "path": "XML", "location": "XML"}]
        xml_items = [] if self._xml_validation is None else [
            {"severity": item.severity, "code": item.code, "message": item.message,
             "path": item.location, "location": item.location + (f" (Строка {item.line}, столбец {item.column})" if item.line and item.column else f" (Строка {item.line})" if item.line else ""),
             "line": item.line or 0, "column": item.column or 0}
            for item in self._xml_validation.diagnostics]
        validation = self.controller.validation
        if not validation: return xml_items
        return xml_items + [{"severity": item.severity, "code": item.code, "message": item.message,
                 "path": item.field_path or "—", "location": item.field_path or "—"}
                for item in (*validation.errors, *validation.warnings)]

    @Property(str, notify=changed)
    def validationSummary(self):
        if self._xml_validation_error:
            return "XML содержит синтаксическую ошибку."
        if self._xml_validation is not None and not self._xml_validation.is_valid:
            return "Доступные проверки выявили ошибки XML."
        validation = self.controller.validation
        if not validation: return "Проверка ещё не выполнялась."
        return "Проверка пройдена" if validation.is_valid else f"Ошибки: {len(validation.errors)} · Предупреждения: {len(validation.warnings)}"

    @Property(str, notify=changed)
    def validationMode(self): return self.controller.settings.mode

    @Property("QVariantList", notify=changed)
    def information(self):
        message = self.controller.current_message
        if not message: return []
        process = next((item for item in self.controller.processes if item.process_code == self.controller.process_code), None)
        transaction = next((item for item in self.controller.transactions if item.transaction_code == self.controller.transaction_code), None)
        guide = self.controller.application.get_message_guide(self.controller.process_code, self.controller.message_code)
        return [
            {"section": "Общие сведения", "text": "\n".join(filter(None, (f"Код процесса: {process.process_code}", f"Наименование: {process.name}", f"Версия: {process.version}", f"Код транзакции: {transaction.transaction_code}", f"Наименование транзакции: {transaction.name}", f"Код сообщения: {message.message_code}", f"Наименование сообщения: {message.name}")))},
            {"section": "Участники", "text": "\n".join(f"{item.role}: {item.initiating_participant or '—'} → {item.responding_participant or '—'}" for item in guide.usages) or "Сведения отсутствуют."},
            {"section": "Структура сообщения", "text": f"Корневой элемент: {guide.root_element or '—'}\nСтруктура: {guide.structure_id}\nРеквизитов: {guide.total_fields}"},
            {"section": "Правила и ограничения", "text": f"Статус правил: {guide.message_rules_status_display}\nСтатус генерации: {message.generation_status}"},
            {"section": "Связанные сообщения", "text": "\n".join(f"{item.transaction_code}: {item.role}" for item in guide.usages) or "Связанные сообщения отсутствуют."},
            {"section": "Примеры", "text": guide.body_example or guide.body_example_status},
            {"section": "Техническая информация", "text": f"PROCESS: {self.controller.process_code}\nTRN: {self.controller.transaction_code}\nMSG: {self.controller.message_code}\nВерсия структуры: {guide.version_description}"},
        ]

    @Property(str, notify=noticeChanged)
    def notice(self): return self._notice

    def _refresh(self, notice=""):
        self._notice = notice
        self.noticeChanged.emit()
        self.changed.emit()

    @Slot(str)
    def selectProcess(self, code):
        if code and code != self.controller.process_code:
            self.controller.select_process(code)
        self._selected_field = None
        self._refresh()

    @Slot(str)
    def selectTransaction(self, code):
        if code and code != self.controller.transaction_code:
            self.controller.select_transaction(code)
        self._selected_field = None
        self._refresh()

    @Slot(str)
    def selectMessage(self, code):
        if code and code != self.controller.message_code:
            self.controller.select_message(code)
        self._selected_field = None
        self._refresh()

    @Slot(str, str)
    def setFieldValue(self, path, value):
        field = self.controller.find_field(path)
        if not field or not field.editable: return
        if "indicator" in (field.datatype or "").lower() or "boolean" in (field.datatype or "").lower():
            value = value == "true"
        values = self.controller.get_values()
        values[path] = value
        self.controller.set_values(values)
        self._selected_field = path
        self._refresh()

    @Slot(str)
    def selectField(self, path):
        self._selected_field = path
        self.changed.emit()

    @Slot()
    def applyTestData(self):
        self.controller.apply_test_data()
        self._refresh("Тестовые данные заполнены.")

    @Slot()
    def generateXml(self):
        result = self.controller.generate_xml()
        self._xml = result.xml or ""
        self._refresh("XML сформирован." if result.success else f"XML не сформирован: {result.status}")

    @Slot(str)
    def setXml(self, value):
        """Keep the editor text as the canonical XML until a new generation."""
        value = str(value)
        if value != self._xml:
            self._xml = value
            self.changed.emit()

    @Slot(str)
    def setFormatterXml(self, value):
        value = str(value)
        if value != self._formatter_xml:
            self._formatter_xml = value
            self.changed.emit()

    @Slot(str, result=str)
    def formattedFormatterXml(self, value):
        try:
            return XmlFormatter().format(str(value)) if value else ""
        except Exception as error:
            self._refresh(f"Ошибка XML: {error}")
            return ""

    @Slot()
    def formatFormatterXml(self):
        """Format the current formatter document and notify QML of the result."""
        formatted = self.formattedFormatterXml(self._formatter_xml)
        if formatted:
            self._formatter_xml = formatted
            self._refresh("XML отформатирован.")

    @Slot()
    def copyFormatterXml(self):
        if self._formatter_xml:
            QGuiApplication.clipboard().setText(self._formatter_xml)
            self._refresh("XML скопирован.")

    @Slot()
    def clearFormatterXml(self):
        self._formatter_xml = ""
        self._refresh()

    @Slot(str)
    def loadFormatterXml(self, path):
        try:
            self._formatter_xml = Path(path).read_text(encoding="utf-8")
            self._refresh()
        except OSError as error:
            self._refresh(f"Не удалось открыть XML: {error}")

    @Slot(str)
    def saveFormatterXml(self, path):
        if path:
            Path(path).write_text(self._formatter_xml, encoding="utf-8")
            self._refresh(f"XML сохранён: {Path(path).name}")

    @Slot(int)
    def changeFormatterFontSize(self, delta):
        self._formatter_font_size = max(9, min(32, self._formatter_font_size + delta))
        self.changed.emit()

    @Slot()
    def resetFormatterFontSize(self):
        self._formatter_font_size = 14
        self.changed.emit()

    @Slot()
    def copyXml(self):
        if self._xml:
            QGuiApplication.clipboard().setText(self._xml)
            self._refresh("XML скопирован.")

    @Slot()
    def validate(self):
        self._xml_validation_error = ""
        self._xml_validation = None
        if self._xml:
            engine = self.controller.application._engine(self.controller.process_code)
            self._xml_validation = XmlValidationService().validate(
                self._xml, engine=engine, transaction_code=self.controller.transaction_code,
                message_code=self.controller.message_code, mode=self.controller.settings.mode)
            parse_error = next((item for item in self._xml_validation.diagnostics if item.code == "XML_PARSE_ERROR"), None)
            if parse_error:
                self._xml_validation_error = parse_error.message
                self._refresh("XML содержит синтаксическую ошибку.")
                return
        self.controller.validate()
        self._refresh("Проверка завершена.")

    @Slot(int, int)
    def goToXmlDiagnostic(self, line, column=0):
        if line > 0:
            self.navigateToXmlPosition.emit(line, max(0, column))

    @Slot(str)
    def setValidationMode(self, mode):
        if mode in {"TEST", "STRICT"}:
            self.controller.settings = self.controller.settings.__class__(
                **{**self.controller.settings.__dict__, "mode": mode})
        self._refresh()

    @Slot()
    def formatXml(self):
        formatted = self.formattedXml(self._xml)
        if formatted:
            self._xml = formatted
            self._refresh("XML отформатирован.")

    @staticmethod
    def _normalize_formatting_whitespace(node):
        """Remove indentation-only text nodes without touching mixed content."""
        children = list(node.childNodes)
        element_children = [child for child in children if child.nodeType == child.ELEMENT_NODE]
        meaningful_text = [child for child in children if child.nodeType == child.TEXT_NODE and child.data.strip()]
        if element_children and not meaningful_text:
            for child in children:
                if child.nodeType == child.TEXT_NODE and not child.data.strip():
                    node.removeChild(child)
        for child in list(node.childNodes):
            if child.nodeType == child.ELEMENT_NODE:
                GuiViewModel._normalize_formatting_whitespace(child)

    @Slot(str, result=str)
    def formattedXml(self, value):
        """Return canonical, idempotent pretty XML; leave invalid source untouched."""
        if not value:
            return ""
        try:
            document = minidom.parseString(value)
            self._normalize_formatting_whitespace(document)
            return document.toprettyxml(indent="  ")
        except Exception:
            self._refresh("XML не удалось отформатировать.")
            return ""

    @Slot(int)
    def changeXmlFontSize(self, delta):
        self._xml_font_size = max(9, min(32, self._xml_font_size + delta))
        self.changed.emit()

    @Slot()
    def resetXmlFontSize(self):
        self._xml_font_size = 14
        self.changed.emit()

    @Slot(str)
    def saveXml(self, path):
        if path and self._xml:
            Path(path).write_text(self._xml, encoding="utf-8")
            self._refresh(f"XML сохранён: {Path(path).name}")

    @Slot(str)
    def saveDraft(self, path):
        if path:
            self.controller.save_draft(Path(path))
            self._refresh(f"Черновик сохранён: {Path(path).name}")
