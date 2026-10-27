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
from eaeu_xml.process_packages.value_context import MISSING, at_context, contexts, present as context_present, leaf_values, node_values


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
    complete: bool | None = None

    @property
    def is_valid(self) -> bool:
        return not any(issue.severity == IssueSeverity.ERROR for issue in self.issues)

    @property
    def is_complete(self) -> bool:
        if self.complete is not None:
            return self.complete
        if any(issue.severity == IssueSeverity.ERROR for issue in self.issues):
            return False
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
            for path, expected in rules.fixed_values.items():
                if path not in values:
                    self._set_fixed_value(values, path, expected)
        for path in values:
            if path not in fields_by_path:
                issues.append(self._issue("UNKNOWN_FIELD", path, "Поле отсутствует в StructureDefinition."))
        children = {field.parent for field in structure_definition.fields if field.parent and field.kind != "ATTRIBUTE"}
        fields_by_id = {field.field_id: field for field in structure_definition.fields}
        if any(re.search(r"[XYZ](?:\.[XYZ]){2}", text) for text in
               (structure_definition.namespace or "", *structure_definition.imported_namespaces.values())):
            severity = IssueSeverity.ERROR if mode == GenerationMode.STRICT else IssueSeverity.WARNING
            issues.append(self._issue("UNRESOLVED_NAMESPACE_VERSION", "", "Версия namespace модели не подтверждена; XML доступен только для внутренней проверки.", severity=severity))
        for field in structure_definition.fields:
            if field.status != "CONFIRMED":
                issues.append(self._issue("NEEDS_NORMATIVE_INTERPRETATION", field.path, "Строка нормативной таблицы требует ручной интерпретации.", field))
                continue
            ancestors = []
            parent = fields_by_id.get(field.parent)
            while parent:
                ancestors.insert(0, parent.path)
                parent = fields_by_id.get(parent.parent)
            for context in contexts(values, ancestors):
                raw = at_context(values, field.path, context)
                if raw is MISSING and field.path in values:
                    issues.append(self._issue("VALUE_CONTEXT_ALIGNMENT", field.path, "Число значений не соответствует повторяющимся родительским контекстам; scalar broadcast запрещён.", field))
                is_container = field.field_id in children
                exists = context_present(values, field.path, context)
                count = len(node_values(values, field.path, context))
                if field.min_occurs is not None and count < field.min_occurs:
                    issues.append(self._issue("MIN_OCCURS", field.path, f"Требуется минимум {field.min_occurs} значений, получено {count}.", field))
                if field.max_occurs is not None and count > field.max_occurs:
                    issues.append(self._issue("MAX_OCCURS", field.path, f"Допустимо максимум {field.max_occurs} значений, получено {count}.", field))
                if count:
                    if raw is None and not is_container:
                        self._validate_datatype(field, "", issues)
                    for value in leaf_values(raw):
                        if value is not None:
                            self._validate_datatype(field, value, issues)
                    if field.classifier_ref:
                        dataset = getattr(self.package, "classifier_values", {}).get(field.classifier_ref)
                        if dataset is None:
                            severity = IssueSeverity.ERROR if mode == GenerationMode.STRICT else IssueSeverity.WARNING
                            issues.append(self._issue("CLASSIFIER_DATASET_NOT_AVAILABLE", field.path, "Набор данных классификатора отсутствует; значение не проверено.", field, severity))
                        elif any(str(v) not in dataset for v in leaf_values(raw) if v is not None):
                            issues.append(self._issue("CLASSIFIER_VALUE_INVALID", field.path, "Код отсутствует в загруженном официальном snapshot классификатора.", field))
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
            # Presence means filled text for scalar fields, but structural
            # presence for complex containers; the structure owns that distinction.
            complex_paths = {field.path for field in structure_definition.fields
                             if field.field_id in children}
            rule_evaluations = StructuredRuleEvaluator(
                getattr(self.package, "classifier_values", {}), complex_paths=complex_paths,
            ).evaluate_all(rules.structured_rules, values)
            for evaluation in rule_evaluations:
                if evaluation.status is RuleStatus.FAIL:
                    issues.append(self._issue("STRUCTURED_RULE_FAILED", "", evaluation.message, rule_id=evaluation.rule_id))
                elif evaluation.status is not RuleStatus.PASS:
                    severity = IssueSeverity.ERROR if mode == GenerationMode.STRICT else IssueSeverity.WARNING
                    issues.append(self._issue("STRUCTURED_RULE_NOT_EVALUATED", "", f"{evaluation.status.value}: {evaluation.message}", severity=severity, rule_id=evaluation.rule_id))
        is_complete = not any(issue.severity == IssueSeverity.ERROR for issue in issues)
        if "DRAFT" in getattr(structure_definition, "status", ""):
            is_complete = False
        elif any(getattr(item, "status", None) not in {RuleStatus.PASS} for item in rule_evaluations):
            is_complete = False
        return BodyValidationResult(tuple(issues), rule_evaluations, complete=is_complete)

    def build_body(self, message_definition: MessageDefinition, structure_definition: StructureDefinition,
                   user_values: Mapping[str, object], *, mode: GenerationMode = GenerationMode.STRICT) -> BodyPayload:
        values = self._flatten(user_values)
        rules = self.package.rules.get(message_definition.message_code)
        if rules:
            for path, expected in rules.fixed_values.items():
                if path not in values:
                    self._set_fixed_value(values, path, expected)
        result = self.validate_body(message_definition, structure_definition, values, mode=mode)
        if not result.is_valid:
            raise BodyValidationError(code="BODY_VALIDATION_FAILED", message=f"Body содержит {len(result.issues)} issue(s).", issues=result.issues)
        return StructuredBodyPayload(self._serialize(structure_definition, values))

    def extract_values(self, structure: StructureDefinition, element: ET.Element) -> dict[str, Any]:
        """Extract exact QNames and aligned parent contexts from a Body root.

        Unknown names and order violations are rejected, not matched by local name.
        Cardinality/datatype/business diagnostics remain owned by validate_body.
        """
        from copy import deepcopy
        def qname(field):
            if field.kind == "ATTRIBUTE" and not field.namespace_prefix: return field.xml_name
            return f"{{{structure.imported_namespaces.get(field.namespace_prefix, structure.namespace)}}}{field.xml_name}"
        if element.tag != f"{{{structure.namespace}}}{structure.root_element}":
            raise BodyValidationError(code="ROOT_QNAME_MISMATCH", message="QName корневого элемента не соответствует структуре.")
        children = {}
        for field in sorted(structure.fields, key=lambda f: f.order): children.setdefault(field.parent, []).append(field)
        def group(parent, parent_id):
            fields = children.get(parent_id, ())
            # Legacy RELATIVE rows are declared child elements, emitted by the
            # serializer just like ELEMENT rows; accept only their exact QNames.
            known = {qname(f): f for f in fields if f.kind in {"ELEMENT", "RELATIVE"}}
            attrs = {qname(f): f for f in fields if f.kind == "ATTRIBUTE"}
            wildcard = next((f for f in fields if f.kind == "ARBITRARY_XML"), None)
            if set(parent.attrib)-set(attrs):
                raise BodyValidationError(code="UNKNOWN_XML_ATTRIBUTE", message="Атрибут отсутствует в нормативном дереве.")
            last = -1
            for child in parent:
                field = known.get(child.tag)
                if field is None:
                    if wildcard is None: raise BodyValidationError(code="UNKNOWN_XML_QNAME", message=f"Неизвестный QName: {child.tag}")
                    field = wildcard
                if field.order < last: raise BodyValidationError(code="XML_SEQUENCE_ORDER", message="Нарушен порядок реквизитов нормативной таблицы.")
                last = field.order
            result = {f.path: parent.attrib[key] for key,f in attrs.items() if key in parent.attrib}
            for field in fields:
                if field.kind == "ATTRIBUTE": continue
                nodes = [n for n in parent if n.tag == qname(field)] if field.kind != "ARBITRARY_XML" else [n for n in parent if n.tag not in known]
                if not nodes: continue
                if field.kind == "ARBITRARY_XML":
                    result[field.path] = [deepcopy(n) for n in nodes] if len(nodes)>1 or field.max_occurs != 1 else deepcopy(nodes[0])
                    continue
                is_container = any(c.kind != "ATTRIBUTE" for c in children.get(field.field_id, ()))
                values = []
                nested = []
                for node in nodes:
                    value = {} if is_container else (node.text if node.text is not None else "")
                    if "indicator" in (field.datatype or "").lower() and value in ("true", "false", "1", "0"):
                        value = value in ("true", "1")
                    values.append(value); nested.append(group(node, field.field_id))
                repeat = field.max_occurs != 1 or len(nodes)>1
                result[field.path] = values if repeat else values[0]
                for path in set().union(*(item.keys() for item in nested)):
                    result[path] = [item.get(path) for item in nested] if repeat else nested[0][path]
            return result
        return group(element, None)

    def _values_from_element(self, structure: StructureDefinition, root: ET.Element) -> tuple[dict[str, object], list[BodyValidationIssue]]:
        issues: list[BodyValidationIssue] = []
        if not structure.namespace or not structure.root_element:
            return {}, [self._issue("STRUCTURE_XML_METADATA_UNRESOLVED", "", "Root element или namespace не разрешены.")]
        expected_root = f"{{{structure.namespace}}}{structure.root_element}"
        if root.tag != expected_root:
            return {}, [self._issue(
                "EMBEDDED_ROOT_QNAME_MISMATCH", "",
                f"Ожидается root QName {expected_root!r}, получен {root.tag!r}.",
            )]
        values: dict[str, object] = {}
        elements: dict[str, list[tuple[tuple[int, ...], ET.Element]]] = {}
        for field in sorted(structure.fields, key=lambda item: item.order):
            parent_occurrences = elements.get(self._parent_path(field.path), [((), root)])
            if field.kind == "ATTRIBUTE":
                aligned = [
                    (indexes, parent.attrib.get(field.xml_name))
                    for indexes, parent in parent_occurrences
                ]
                if any(value is not None for _, value in aligned):
                    values[field.path] = self._pack_indexed_values(aligned)
                continue
            if field.kind in {"ANY", "ARBITRARY_XML"}:
                continue
            if not field.xml_name:
                continue
            namespace = structure.imported_namespaces.get(field.namespace_prefix, structure.namespace)
            qname = f"{{{namespace}}}{field.xml_name}"
            found_by_parent = [
                (indexes, [child for child in list(parent) if child.tag == qname])
                for indexes, parent in parent_occurrences
            ]
            branching = any(len(found) > 1 for _, found in found_by_parent)
            occurrences: list[tuple[tuple[int, ...], ET.Element]] = []
            aligned_values: list[tuple[tuple[int, ...], object]] = []
            has_element_children = any(
                item.parent == field.field_id and item.kind != "ATTRIBUTE"
                for item in structure.fields
            )

            for parent_indexes, found in found_by_parent:
                if branching:
                    if not found and parent_indexes:
                        aligned_values.append((parent_indexes, []))
                    for local_index, child in enumerate(found):
                        indexes = parent_indexes + (local_index,)
                        occurrences.append((indexes, child))
                        aligned_values.append((indexes, "" if has_element_children else child.text))
                elif found:
                    child = found[0]
                    occurrences.append((parent_indexes, child))
                    aligned_values.append((parent_indexes, "" if has_element_children else child.text))
                elif parent_indexes:
                    aligned_values.append((parent_indexes, None))

            elements[field.path] = occurrences
            if not occurrences:
                continue
            values[field.path] = self._pack_indexed_values(aligned_values)
        return values, issues

    @staticmethod
    def _pack_indexed_values(indexed_values: list[tuple[tuple[int, ...], object]]) -> object:
        """Build the evaluator's nested-list representation without losing sparse parent indexes."""
        if len(indexed_values) == 1 and indexed_values[0][0] == ():
            return indexed_values[0][1]

        packed: list[object] = []
        for indexes, value in indexed_values:
            if not indexes:
                return value
            current = packed
            for depth, index in enumerate(indexes):
                while len(current) <= index:
                    current.append(None)
                if depth == len(indexes) - 1:
                    current[index] = value
                    continue
                child = current[index]
                if not isinstance(child, list):
                    child = []
                    current[index] = child
                current = child
        return packed

    def _serialize(self, structure: StructureDefinition, values: Mapping[str, Any]) -> ET.Element:
        from copy import deepcopy
        if not structure.namespace or not structure.root_element:
            raise BodyValidationError(code="STRUCTURE_XML_METADATA_UNRESOLVED", message="Root element или namespace не разрешены.")
        ET.register_namespace("", structure.namespace)
        for prefix, uri in structure.imported_namespaces.items():
            if prefix and uri: ET.register_namespace(prefix, uri)
        root = ET.Element(ET.QName(structure.namespace, structure.root_element))
        children = {}
        for field in sorted(structure.fields, key=lambda field: field.order):
            children.setdefault(field.parent, []).append(field)

        def emit(field, parent, context):
            raw = at_context(values, field.path, context)
            if raw is MISSING and not context_present(values, field.path, context): return
            if raw is None and not context_present(values, field.path, context): return
            if field.kind == "ATTRIBUTE":
                if raw is not MISSING and raw is not None:
                    key = ET.QName(structure.imported_namespaces[field.namespace_prefix], field.xml_name) if field.namespace_prefix else field.xml_name
                    parent.set(key, str(raw))
                return
            if field.kind == "ARBITRARY_XML":
                for value in raw if isinstance(raw, list) else [raw]:
                    if isinstance(value, ET.Element): parent.append(deepcopy(value))
                return
            if not field.xml_name: return
            container = any(child.kind != "ATTRIBUTE" for child in children.get(field.field_id, ()))
            if raw is MISSING and not container: return
            instances = raw if isinstance(raw, list) else [raw]
            for index, value in enumerate(instances):
                next_context = (*context, (field.path, index, len(instances), isinstance(raw, list)))
                if value is None and isinstance(raw, list) and not any(
                        p.startswith(field.path + "/") and at_context(values, p, next_context) not in (MISSING, None) for p in values):
                    continue
                namespace = structure.imported_namespaces.get(field.namespace_prefix, structure.namespace)
                element = ET.SubElement(parent, ET.QName(namespace, field.xml_name))
                if value is not MISSING and value is not None and not isinstance(value, Mapping):
                    if isinstance(value, ET.Element): element.append(deepcopy(value))
                    elif isinstance(value, bool): element.text = "true" if value else "false"
                    elif isinstance(value, (date, datetime)): element.text = value.isoformat()
                    else: element.text = str(value)
                for child in children.get(field.field_id, ()):
                    emit(child, element, next_context)
        for field in children.get(None, ()):
            emit(field, root, ())
        return root

    @staticmethod
    def _set_fixed_value(values, path, expected):
        parent_path = path.rsplit("/", 1)[0] if "/" in path else ""
        parent = values.get(parent_path)
        def fill(shape):
            return [fill(v) for v in shape] if isinstance(shape, list) else expected
        values[path] = fill(parent) if isinstance(parent, list) else expected

    @staticmethod
    def _parent_path(path: str) -> str:
        return path.rsplit("/", 1)[0] if "/" in path else ""

    @staticmethod
    def _field_is_present(values: Mapping[str, object], field_path: str) -> bool:
        """Match direct or descendant field values using the existing path semantics."""
        return field_path in values or any(
            path.startswith(field_path + "/")
            for path in values
        )

    @staticmethod
    def _value_count(value: object, present: bool) -> int:
        """Preserve the existing list-versus-scalar cardinality counting rule."""
        if isinstance(value, list):
            return len(value)
        return 1 if present else 0

    @classmethod
    def _flatten(cls, values: Mapping[str, object], prefix: str = "") -> dict[str, object]:
        result={}
        for key,value in values.items():
            if key == "#text":
                if prefix: result[prefix] = value
                continue
            path=f"{prefix}/{key}" if prefix else key
            if isinstance(value, Mapping):
                result[path] = {}  # explicit container, including a present empty object
                result.update(cls._flatten(value,path))
            elif isinstance(value, list) and value and all(isinstance(item, Mapping) for item in value):
                result[path] = [{} for _ in value]
                flat_items = [cls._flatten(item, path) for item in value]
                keys = set().union(*(item.keys() for item in flat_items))
                for item_path in sorted(keys):
                    result[item_path] = [item.get(item_path) for item in flat_items]
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
