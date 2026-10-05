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
    def build_body(
        self, message_definition: MessageDefinition, structure_definition: StructureDefinition,
        user_values: Mapping[str, object], *, mode: GenerationMode = GenerationMode.STRICT,
        embedded_structure_definitions: Mapping[str, StructureDefinition] | None = None,
        embedded_structure_id: str | None = None,
        embedded_values: Mapping[str, object] | None = None,
    ) -> BodyPayload: ...


class NotImplementedProcessBodyProvider:
    def build_body(
        self, message_definition: MessageDefinition, structure_definition: StructureDefinition,
        user_values: Mapping[str, object], *, mode: GenerationMode = GenerationMode.STRICT,
        embedded_structure_definitions: Mapping[str, StructureDefinition] | None = None,
        embedded_structure_id: str | None = None,
        embedded_values: Mapping[str, object] | None = None,
    ) -> BodyPayload:
        raise ProcessBodyNotImplementedError(code="PROCESS_BODY_NOT_IMPLEMENTED", message=f"Body provider отсутствует для {message_definition.message_code}.")


class StructuredProcessBodyProvider:
    def __init__(self, package: ProcessPackage) -> None:
        self.package = package

    def validate_body(self, message_definition: MessageDefinition, structure_definition: StructureDefinition,
                      user_values: Mapping[str, object], *, mode: GenerationMode = GenerationMode.STRICT,
                      embedded_structure_definitions: Mapping[str, StructureDefinition] | None = None) -> BodyValidationResult:
        values = self._flatten(user_values)
        issues: list[BodyValidationIssue] = []
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
        issues.extend(self._validate_structure_values(structure_definition, values, mode=mode))

        selected_structure_id = None
        embedded_values: dict[str, object] | None = None
        if message_definition.embedded_structures:
            selected_structure_id, embedded_definition, embedded_element, selection_issues = self._select_embedded_payload(
                message_definition, structure_definition, values, embedded_structure_definitions or {},
            )
            issues.extend(selection_issues)
            if embedded_definition is not None and embedded_element is not None:
                embedded_values, extraction_issues = self._values_from_element(embedded_definition, embedded_element)
                issues.extend(extraction_issues)
                issues.extend(self._validate_structure_values(embedded_definition, embedded_values, mode=mode))
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
            evaluations = []
            evaluator = StructuredRuleEvaluator()
            for rule in rules.structured_rules:
                applies_to = rule.get("applies_to_structure")
                if applies_to and applies_to != structure_definition.structure_id:
                    if applies_to != selected_structure_id or embedded_values is None:
                        continue
                    evaluation_values = embedded_values
                else:
                    evaluation_values = values
                evaluations.extend(evaluator.evaluate_all((rule,), evaluation_values))
            rule_evaluations=tuple(evaluations)
            for evaluation in rule_evaluations:
                if evaluation.status is RuleStatus.FAIL:
                    issues.append(self._issue("STRUCTURED_RULE_FAILED", "", evaluation.message, rule_id=evaluation.rule_id))
        return BodyValidationResult(tuple(issues),rule_evaluations)

    def build_body(self, message_definition: MessageDefinition, structure_definition: StructureDefinition,
                   user_values: Mapping[str, object], *, mode: GenerationMode = GenerationMode.STRICT,
                   embedded_structure_definitions: Mapping[str, StructureDefinition] | None = None,
                   embedded_structure_id: str | None = None,
                   embedded_values: Mapping[str, object] | None = None) -> BodyPayload:
        values = self._flatten(user_values)
        if message_definition.embedded_structures:
            definitions = embedded_structure_definitions or {}
            if not embedded_structure_id:
                raise BodyValidationError(
                    code="EMBEDDED_STRUCTURE_SELECTION_REQUIRED",
                    message=f"Для {message_definition.message_code} требуется явно выбрать embedded structure.",
                )
            if embedded_structure_id not in message_definition.embedded_structures.structures:
                raise BodyValidationError(
                    code="EMBEDDED_STRUCTURE_NOT_ALLOWED",
                    message=f"Структура {embedded_structure_id} не разрешена для {message_definition.message_code}.",
                )
            embedded_definition = definitions.get(embedded_structure_id)
            if embedded_definition is None:
                raise BodyValidationError(
                    code="EMBEDDED_STRUCTURE_UNRESOLVED",
                    message=f"Не удалось разрешить StructureDefinition для {embedded_structure_id}.",
                )
            if embedded_values is not None:
                any_fields = [field for field in structure_definition.fields if field.kind == "ANY"]
                if len(any_fields) != 1:
                    raise BodyValidationError(
                        code="EMBEDDED_STRUCTURE_WILDCARD_UNRESOLVED",
                        message=f"Для {message_definition.message_code} требуется ровно один ANY wildcard контейнера.",
                    )
                values[any_fields[0].path] = self._serialize(embedded_definition, self._flatten(embedded_values))
        rules = self.package.rules.get(message_definition.message_code)
        if rules:
            for path, expected in rules.fixed_values.items(): values.setdefault(path, expected)
        result = self.validate_body(
            message_definition, structure_definition, values, mode=mode,
            embedded_structure_definitions=embedded_structure_definitions,
        )
        if not result.is_valid:
            raise BodyValidationError(code="BODY_VALIDATION_FAILED", message=f"Body содержит {len(result.issues)} issue(s).", issues=result.issues)
        if message_definition.embedded_structures:
            selected_structure_id, _, _, selection_issues = self._select_embedded_payload(
                message_definition, structure_definition, values, embedded_structure_definitions or {},
            )
            if selection_issues or selected_structure_id != embedded_structure_id:
                raise BodyValidationError(
                    code="EMBEDDED_STRUCTURE_SELECTION_MISMATCH",
                    message=f"Embedded root QName не соответствует выбранной структуре {embedded_structure_id}.",
                    issues=selection_issues,
                )
        return StructuredBodyPayload(self._serialize(structure_definition, values))

    def _serialize(self, structure: StructureDefinition, values: Mapping[str, Any]) -> ET.Element:
        if not structure.namespace or not structure.root_element:
            raise BodyValidationError(code="STRUCTURE_XML_METADATA_UNRESOLVED", message="Root element или namespace не разрешены.")
        ET.register_namespace("", structure.namespace)
        for prefix, uri in structure.imported_namespaces.items():
            if prefix and uri: ET.register_namespace(prefix, uri)
        root = ET.Element(ET.QName(structure.namespace, structure.root_element))
        elements: dict[str, list[ET.Element | None]] = {}
        fields = sorted(structure.fields, key=lambda field: field.order)
        for field in fields:
            if field.kind == "ATTRIBUTE": continue
            if field.kind in {"ARBITRARY_XML", "ANY"}:
                if field.path not in values: continue
                parent_elements = elements.get(self._parent_path(field.path), [root])
                raw = values[field.path]; instances = raw if isinstance(raw, list) else [raw]
                for parent in parent_elements:
                    if parent is None:
                        continue
                    for value in instances:
                        if isinstance(value, ET.Element):
                            parent.append(value)
                        elif field.kind == "ANY":
                            raise BodyValidationError(
                                code="ANY_XML_ELEMENT_REQUIRED",
                                message=f"Wildcard {field.path} принимает только XML Element.",
                            )
                continue
            if not field.xml_name: continue
            descendants_present = any(path.startswith(field.path + "/") for path in values)
            has_element_children = any(
                item.parent == field.field_id and item.kind != "ATTRIBUTE"
                for item in structure.fields
            )
            if field.path not in values and not descendants_present: continue
            raw = values.get(field.path); instances = raw if isinstance(raw, list) else [raw]
            if raw is None and descendants_present: instances = [None]
            parent_elements = elements.get(self._parent_path(field.path), [root]); created=[]
            if len(parent_elements) > 1 and len(instances) == len(parent_elements):
                placements = zip(parent_elements, ([value] for value in instances))
            else:
                placements = ((parent, instances) for parent in parent_elements)
            for parent_index, (parent, parent_values) in enumerate(placements):
                for value_index, value in enumerate(parent_values):
                    if parent is None:
                        created.append(None)
                        continue
                    if value is None:
                        if len(parent_elements) > 1 or len(instances) > 1:
                            slot_index = parent_index if len(parent_elements) > 1 else value_index
                            if not self._descendant_slot_has_value(values, field.path, slot_index):
                                created.append(None)
                                continue
                        if not descendants_present and not has_element_children:
                            created.append(None)
                            continue
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
            for index,target in enumerate(targets):
                if target is None:
                    continue
                value = vals[min(index,len(vals)-1)]
                if value is None:
                    continue
                target.set(field.xml_name, str(value))
        return root

    @classmethod
    def _descendant_slot_has_value(
        cls,
        values: Mapping[str, object],
        parent_path: str,
        index: int,
    ) -> bool:
        """Return whether descendants prove that this positional complex parent exists."""
        prefix = parent_path + "/"
        for path, descendant in values.items():
            if not path.startswith(prefix):
                continue
            if isinstance(descendant, list):
                if index >= len(descendant):
                    continue
                candidate = descendant[index]
            elif index == 0:
                candidate = descendant
            else:
                continue
            if any(True for _ in cls._present_leaf_values(candidate)):
                return True
        return False

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
    def _positional_slot_count(cls, value: object) -> int:
        if not isinstance(value, list):
            return 1
        total = 0
        for item in value:
            total += cls._positional_slot_count(item) if isinstance(item, list) else 1
        return total

    @classmethod
    def _aligned_child_counts(
        cls,
        parent_value: object,
        child_value: object,
        child_present: bool,
        *,
        parent_path: str,
        values: Mapping[str, object],
    ) -> list[int]:
        """Return child cardinality for each concrete occurrence of a repeated parent."""
        counts: list[int] = []

        def slot_count(value: object, present: bool) -> int:
            if not present or value is None:
                return 0
            if isinstance(value, list):
                return sum(item is not None for item in value)
            return 1

        def value_at_indexes(value: object, indexes: tuple[int, ...]) -> tuple[object, bool]:
            current = value
            for index in indexes:
                if isinstance(current, list):
                    if index >= len(current):
                        return None, False
                    current = current[index]
                elif index != 0:
                    return None, False
            return current, True

        def contains_real_value(value: object) -> bool:
            if isinstance(value, list):
                return any(contains_real_value(item) for item in value)
            return value is not None

        def parent_occurrence_present(parent_slot: object, indexes: tuple[int, ...]) -> bool:
            if parent_slot is not None:
                return True
            prefix = parent_path + "/"
            for path, descendant in values.items():
                if not path.startswith(prefix):
                    continue
                slot, exists = value_at_indexes(descendant, indexes)
                if exists and contains_real_value(slot):
                    return True
            return False

        def walk(parent_slot: object, child_slot: object, present: bool, indexes: tuple[int, ...]) -> None:
            if isinstance(parent_slot, list):
                for index, item in enumerate(parent_slot):
                    if isinstance(child_slot, list) and index < len(child_slot):
                        walk(item, child_slot[index], True, indexes + (index,))
                    else:
                        walk(item, None, False, indexes + (index,))
                return
            if parent_occurrence_present(parent_slot, indexes):
                counts.append(slot_count(child_slot, present))

        walk(parent_value, child_value, child_present, ())
        return counts

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

    def _validate_structure_values(self, structure: StructureDefinition, values: Mapping[str, object],
                                   *, mode: GenerationMode) -> list[BodyValidationIssue]:
        issues: list[BodyValidationIssue] = []
        fields_by_path = {field.path: field for field in structure.fields}
        for path in values:
            if path not in fields_by_path:
                issues.append(self._issue("UNKNOWN_FIELD", path, f"Поле отсутствует в StructureDefinition {structure.structure_id}."))
        for field in structure.fields:
            if field.status != "CONFIRMED":
                issues.append(self._issue("NEEDS_NORMATIVE_INTERPRETATION", field.path, "Строка нормативной таблицы требует ручной интерпретации.", field))
                continue
            present = self._field_is_present(values, field.path)
            raw = values.get(field.path)
            count = self._value_count(raw, present)
            parent_path = self._parent_path(field.path)
            parent_present = not parent_path or self._field_is_present(values, parent_path)
            parent_raw = values.get(parent_path)
            aligned_counts = None
            if (
                parent_present
                and isinstance(parent_raw, list)
                and self._positional_slot_count(parent_raw) > 1
                and (isinstance(raw, list) or not present)
            ):
                candidate_counts = self._aligned_child_counts(
                    parent_raw,
                    raw,
                    present,
                    parent_path=parent_path,
                    values=values,
                )
                if candidate_counts:
                    aligned_counts = candidate_counts
            counts = aligned_counts if aligned_counts is not None else [count]
            if parent_present and field.min_occurs is not None:
                for item_count in counts:
                    if item_count < field.min_occurs:
                        issues.append(self._issue("MIN_OCCURS", field.path, f"Требуется минимум {field.min_occurs} значений, получено {item_count}.", field))
            if field.max_occurs is not None:
                for item_count in counts:
                    if item_count > field.max_occurs:
                        issues.append(self._issue("MAX_OCCURS", field.path, f"Допустимо максимум {field.max_occurs} значений, получено {item_count}.", field))
            if present:
                for value in self._present_leaf_values(raw):
                    self._validate_datatype(field, value, issues)
            if field.classifier_ref and present:
                severity = IssueSeverity.ERROR if mode == GenerationMode.STRICT else IssueSeverity.WARNING
                issues.append(self._issue("CLASSIFIER_DATASET_NOT_AVAILABLE", field.path, "Набор данных классификатора отсутствует; значение не проверено.", field, severity))
        return issues

    @classmethod
    def _present_leaf_values(cls, value: object):
        """Yield real values while keeping sparse repeatable placeholders out of datatype checks."""
        if isinstance(value, list):
            for item in value:
                yield from cls._present_leaf_values(item)
        elif value is not None:
            yield value

    def _select_embedded_payload(
        self, message: MessageDefinition, container: StructureDefinition, values: Mapping[str, object],
        definitions: Mapping[str, StructureDefinition],
    ) -> tuple[str | None, StructureDefinition | None, ET.Element | None, list[BodyValidationIssue]]:
        issues: list[BodyValidationIssue] = []
        embedded = message.embedded_structures
        if not embedded:
            return None, None, None, issues
        wildcard_paths = [field.path for field in container.fields if field.kind == "ANY"]
        payloads: list[ET.Element] = []
        for path in wildcard_paths:
            raw = values.get(path)
            for value in raw if isinstance(raw, list) else [raw]:
                if isinstance(value, ET.Element):
                    payloads.append(value)
        if len(payloads) != 1:
            issues.append(self._issue(
                "EMBEDDED_STRUCTURE_CARDINALITY", ", ".join(wildcard_paths),
                f"ONE_OF требует ровно один embedded XML root; получено {len(payloads)}.",
            ))
            return None, None, None, issues
        element = payloads[0]
        matches = []
        for structure_id in embedded.structures:
            definition = definitions.get(structure_id)
            if definition is None or not definition.namespace or not definition.root_element:
                continue
            if element.tag == f"{{{definition.namespace}}}{definition.root_element}":
                matches.append((structure_id, definition))
        if not matches:
            issues.append(self._issue(
                "UNKNOWN_EMBEDDED_STRUCTURE", wildcard_paths[0] if wildcard_paths else "",
                f"Embedded root QName {element.tag!r} не входит в ONE_OF для {message.message_code}.",
            ))
            return None, None, element, issues
        if len(matches) != 1:
            issues.append(self._issue(
                "AMBIGUOUS_EMBEDDED_STRUCTURE", wildcard_paths[0] if wildcard_paths else "",
                f"Embedded root QName {element.tag!r} соответствует нескольким разрешённым структурам.",
            ))
            return None, None, element, issues
        structure_id, definition = matches[0]
        return structure_id, definition, element, issues

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

    def _validate_datatype(self, field: StructureFieldDefinition, value: object, issues: list[BodyValidationIssue]) -> None:
        dtype=(field.datatype or "").lower(); valid=True
        if field.kind in {"ANY", "ARBITRARY_XML"} or field.datatype == "ANY_XML" or dtype == "xs:any": valid=isinstance(value,ET.Element)
        elif "indicatortype" in dtype: valid=isinstance(value,bool) or str(value).lower() in {"true","false","0","1"}
        elif "datetimetype" in dtype:
            try: datetime.fromisoformat(str(value).replace("Z","+00:00"))
            except ValueError: valid=False
        elif dtype.endswith("datetype"):
            try: date.fromisoformat(str(value))
            except ValueError: valid=False
        elif "quantity" in dtype or "integer" in dtype:
            try: int(value)
            except (TypeError,ValueError): valid=False
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
