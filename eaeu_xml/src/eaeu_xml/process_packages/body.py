from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from enum import Enum
import re
from typing import Any, Mapping, Protocol
from xml.etree import ElementTree as ET

from eaeu_xml.core.errors import BodyValidationError, ProcessBodyNotImplementedError
from eaeu_xml.decision5.models.envelope import BodyPayload
from eaeu_xml.process_packages.models import MessageDefinition, ProcessPackage, SourceReference, StructureDefinition, StructureFieldDefinition
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


class GenerationMode(str, Enum):
    STRICT = "STRICT"
    TEST = "TEST"


class IssueSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass(frozen=True)
class BodyValidationIssue:
    code: str
    severity: IssueSeverity
    field_path: str
    message: str
    source_ref: SourceReference | None = None
    rule_id: str | None = None


@dataclass(frozen=True)
class BodyValidationResult:
    issues: tuple[BodyValidationIssue, ...]
    rule_evaluations: tuple[object, ...] = ()

    @property
    def is_valid(self) -> bool:
        return not any(issue.severity == IssueSeverity.ERROR for issue in self.issues)

    @property
    def is_complete(self) -> bool:
        return not any(getattr(item, "status", None) not in {RuleStatus.PASS} for item in self.rule_evaluations)


@dataclass(frozen=True)
class StructuredBodyPayload:
    element: ET.Element

    def serialize_xml_element(self) -> ET.Element:
        return self.element


class ProcessBodyProvider(Protocol):
    def build_body(self, message_definition: MessageDefinition, structure_definition: StructureDefinition, user_values: Mapping[str, object], *, mode: GenerationMode = GenerationMode.STRICT) -> BodyPayload: ...


class NotImplementedProcessBodyProvider:
    def build_body(self, message_definition: MessageDefinition, structure_definition: StructureDefinition, user_values: Mapping[str, object], *, mode: GenerationMode = GenerationMode.STRICT) -> BodyPayload:
        raise ProcessBodyNotImplementedError(code="PROCESS_BODY_NOT_IMPLEMENTED", message=f"Body provider отсутствует для {message_definition.message_code}.")


class StructuredProcessBodyProvider:
    def __init__(self, package: ProcessPackage) -> None:
        self.package = package

    def validate_body(self, message_definition: MessageDefinition, structure_definition: StructureDefinition,
                      user_values: Mapping[str, object], *, mode: GenerationMode = GenerationMode.STRICT) -> BodyValidationResult:
        values = self._flatten(user_values)
        issues: list[BodyValidationIssue] = []
        fields_by_path = {field.path: field for field in structure_definition.fields}
        rules = self.package.rules.get(message_definition.message_code)
        supplied_values = dict(values)
        rule_evaluations=()
        if rules:
            for rule in rules.business_rules:
                if rule.get("interpretation_status") == "INTERNAL_NORMATIVE_CONFLICT":
                    raw_source = (rule.get("source_refs") or [None])[0]
                    source = None
                    if raw_source:
                        allowed = SourceReference.__dataclass_fields__
                        source = SourceReference(**{key: value for key, value in raw_source.items() if key in allowed})
                    identifiers = rule.get("referenced_identifiers") or ()
                    issues.append(BodyValidationIssue(
                        code="NORMATIVE_CONFLICT", severity=IssueSeverity.ERROR,
                        field_path=", ".join(identifiers),
                        message=rule.get("conflict_details") or "MessageRule противоречит объявленной StructureDefinition.",
                        source_ref=source, rule_id=rule.get("conflict_id") or rule.get("rule_id"),
                    ))
            for path, expected in rules.fixed_values.items(): values.setdefault(path, expected)
        for path in values:
            if path not in fields_by_path:
                issues.append(self._issue("UNKNOWN_FIELD", path, "Поле отсутствует в StructureDefinition."))
        for field in structure_definition.fields:
            if field.status != "CONFIRMED":
                issues.append(self._issue("NEEDS_NORMATIVE_INTERPRETATION", field.path, "Строка нормативной таблицы требует ручной интерпретации.", field))
                continue
            present = field.path in values or any(path.startswith(field.path + "/") for path in values)
            raw = values.get(field.path)
            count = len(raw) if isinstance(raw, list) else (1 if present else 0)
            parent_path = self._parent_path(field.path)
            parent_present = not parent_path or parent_path in values or any(path.startswith(parent_path + "/") for path in values)
            parent_raw = values.get(parent_path)
            parent_count = len(parent_raw) if isinstance(parent_raw, list) else 1
            if parent_count > 1 and isinstance(raw, list) and len(raw) == parent_count:
                count = 1
            if parent_present and field.min_occurs is not None and count < field.min_occurs:
                issues.append(self._issue("MIN_OCCURS", field.path, f"Требуется минимум {field.min_occurs} значений, получено {count}.", field))
            if field.max_occurs is not None and count > field.max_occurs:
                issues.append(self._issue("MAX_OCCURS", field.path, f"Допустимо максимум {field.max_occurs} значений, получено {count}.", field))
            if present:
                for value in raw if isinstance(raw, list) else [raw]:
                    self._validate_datatype(field, value, issues)
            if field.classifier_ref and present:
                severity = IssueSeverity.ERROR if mode == GenerationMode.STRICT else IssueSeverity.WARNING
                issues.append(self._issue("CLASSIFIER_DATASET_NOT_AVAILABLE", field.path, "Набор данных классификатора отсутствует; значение не проверено.", field, severity))
        if rules:
            for path, usage in rules.field_usage.items():
                present = path in values
                if usage == "REQUIRED" and not present:
                    issues.append(self._issue("MESSAGE_RULE_REQUIRED", path, "Поле обязательно для сообщения.", rule_id=f"{message_definition.message_code}:{path}"))
                if usage == "FORBIDDEN" and present:
                    issues.append(self._issue("FORBIDDEN_FIELD", path, "Поле запрещено для сообщения.", rule_id=f"{message_definition.message_code}:{path}"))
            for path, expected in rules.fixed_values.items():
                supplied = supplied_values.get(path)
                mismatch = any(value != expected for value in supplied) if isinstance(supplied, list) else supplied != expected
                if path in supplied_values and mismatch:
                    issues.append(self._issue("FIXED_VALUE_MISMATCH", path, f"Ожидается фиксированное значение {expected!r}.", rule_id=f"{message_definition.message_code}:{path}"))
            rule_evaluations=StructuredRuleEvaluator().evaluate_all(rules.structured_rules, values)
            for evaluation in rule_evaluations:
                if evaluation.status is RuleStatus.FAIL:
                    issues.append(self._issue("STRUCTURED_RULE_FAILED", "", evaluation.message, rule_id=evaluation.rule_id))
        return BodyValidationResult(tuple(issues),rule_evaluations)

    def build_body(self, message_definition: MessageDefinition, structure_definition: StructureDefinition,
                   user_values: Mapping[str, object], *, mode: GenerationMode = GenerationMode.STRICT) -> BodyPayload:
        values = self._flatten(user_values)
        rules = self.package.rules.get(message_definition.message_code)
        if rules:
            for path, expected in rules.fixed_values.items(): values.setdefault(path, expected)
        result = self.validate_body(message_definition, structure_definition, values, mode=mode)
        if not result.is_valid:
            raise BodyValidationError(code="BODY_VALIDATION_FAILED", message=f"Body содержит {len(result.issues)} issue(s).", issues=result.issues)
        return StructuredBodyPayload(self._serialize(structure_definition, values))

    def _serialize(self, structure: StructureDefinition, values: Mapping[str, Any]) -> ET.Element:
        if not structure.namespace or not structure.root_element:
            raise BodyValidationError(code="STRUCTURE_XML_METADATA_UNRESOLVED", message="Root element или namespace не разрешены.")
        ET.register_namespace("", structure.namespace)
        for prefix, uri in structure.imported_namespaces.items():
            if prefix and uri: ET.register_namespace(prefix, uri)
        root = ET.Element(ET.QName(structure.namespace, structure.root_element))
        elements: dict[str, list[ET.Element]] = {}
        fields = sorted(structure.fields, key=lambda field: field.order)
        for field in fields:
            if field.kind == "ATTRIBUTE": continue
            if field.kind == "ARBITRARY_XML":
                if field.path not in values: continue
                parent_elements = elements.get(self._parent_path(field.path), [root])
                raw = values[field.path]; instances = raw if isinstance(raw, list) else [raw]
                for parent in parent_elements:
                    for value in instances:
                        if isinstance(value, ET.Element): parent.append(value)
                continue
            if not field.xml_name: continue
            descendants_present = any(path.startswith(field.path + "/") for path in values)
            if field.path not in values and not descendants_present: continue
            raw = values.get(field.path); instances = raw if isinstance(raw, list) else [raw]
            if raw is None and descendants_present: instances = [None]
            parent_elements = elements.get(self._parent_path(field.path), [root]); created=[]
            if len(parent_elements) > 1 and len(instances) == len(parent_elements):
                placements = zip(parent_elements, ([value] for value in instances))
            else:
                placements = ((parent, instances) for parent in parent_elements)
            for parent, parent_values in placements:
                for value in parent_values:
                    namespace = structure.imported_namespaces.get(field.namespace_prefix, structure.namespace)
                    element = ET.SubElement(parent, ET.QName(namespace, field.xml_name))
                    if value is not None and not isinstance(value, Mapping):
                        if isinstance(value, ET.Element): element.append(value)
                        elif isinstance(value, bool): element.text = "true" if value else "false"
                        elif isinstance(value, (date, datetime)): element.text = value.isoformat()
                        else: element.text = str(value)
                    created.append(element)
            elements[field.path]=created
        for field in fields:
            if field.kind != "ATTRIBUTE" or field.path not in values or not field.xml_name: continue
            targets=elements.get(self._parent_path(field.path), []); raw=values[field.path]; vals=raw if isinstance(raw,list) else [raw]
            for index,target in enumerate(targets): target.set(field.xml_name, str(vals[min(index,len(vals)-1)]))
        return root

    @staticmethod
    def _parent_path(path: str) -> str:
        return path.rsplit("/", 1)[0] if "/" in path else ""

    @classmethod
    def _flatten(cls, values: Mapping[str, object], prefix: str = "") -> dict[str, object]:
        result={}
        for key,value in values.items():
            if key == "#text":
                if prefix: result[prefix] = value
                continue
            path=f"{prefix}/{key}" if prefix else key
            if isinstance(value, Mapping): result.update(cls._flatten(value,path))
            elif isinstance(value, list) and value and all(isinstance(item, Mapping) for item in value):
                result[path] = [None] * len(value)
                collected: dict[str, list[object]] = {}
                for item in value:
                    flat_item = cls._flatten(item, path)
                    for item_path, item_value in flat_item.items():
                        collected.setdefault(item_path, []).append(item_value)
                result.update(collected)
            else: result[path]=value
        return result

    def _validate_datatype(self, field: StructureFieldDefinition, value: object, issues: list[BodyValidationIssue]) -> None:
        dtype=(field.datatype or "").lower(); valid=True
        if "indicatortype" in dtype: valid=isinstance(value,bool) or str(value).lower() in {"true","false","0","1"}
        elif "datetimetype" in dtype:
            try: datetime.fromisoformat(str(value).replace("Z","+00:00"))
            except ValueError: valid=False
        elif dtype.endswith("datetype"):
            try: date.fromisoformat(str(value))
            except ValueError: valid=False
        elif "quantity" in dtype or "integer" in dtype:
            try: int(value)
            except (TypeError,ValueError): valid=False
        elif field.datatype == "ANY_XML": valid=isinstance(value,ET.Element)
        if not valid: issues.append(self._issue("DATATYPE_INVALID", field.path, f"Значение не соответствует {field.datatype}.", field))
        facets=field.facets
        if not facets or value is None:return
        text=str(value)
        def fail(code): issues.append(self._issue(code,field.path,f"Значение нарушает facet {code}.",field))
        if facets.min_length is not None and len(text)<facets.min_length: fail("MIN_LENGTH")
        if facets.max_length is not None and len(text)>facets.max_length: fail("MAX_LENGTH")
        if facets.pattern and not re.fullmatch(facets.pattern,text): fail("PATTERN")
        if facets.enum and text not in facets.enum: fail("ENUM")
        if any(item is not None for item in (facets.total_digits,facets.fraction_digits,facets.min_value,facets.max_value)):
            try:
                number=Decimal(text); digits=len(number.as_tuple().digits); fraction=max(0,-number.as_tuple().exponent)
                if facets.total_digits is not None and digits>facets.total_digits: fail("TOTAL_DIGITS")
                if facets.fraction_digits is not None and fraction>facets.fraction_digits: fail("FRACTION_DIGITS")
                if facets.min_value is not None and number<Decimal(facets.min_value): fail("MIN_VALUE")
                if facets.max_value is not None and number>Decimal(facets.max_value): fail("MAX_VALUE")
            except (InvalidOperation,ValueError): fail("DECIMAL")

    @staticmethod
    def _issue(code, path, message, field=None, severity=IssueSeverity.ERROR, rule_id=None):
        source = field.source_refs[0] if field and field.source_refs else None
        return BodyValidationIssue(code,severity,path,message,source,rule_id)
