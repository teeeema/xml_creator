from datetime import date, timedelta
from pathlib import Path
from random import Random
from uuid import UUID
from xml.etree import ElementTree as ET

from eaeu_xml.application.models import FieldView, FormDefinition, ProcessView
from eaeu_xml.core.errors import ProcessPackageError
from eaeu_xml.process_packages.loader import ProcessPackageLoader


class ProcessDiscoveryService:
    """Discovers valid packages below an explicit caller-owned root."""

    def discover_processes(self, root: Path) -> tuple[ProcessView, ...]:
        if not isinstance(root, Path):
            raise TypeError("processes_root must be pathlib.Path")
        if not root.is_dir():
            return ()
        results = []
        for path in sorted((item for item in root.iterdir() if item.is_dir()), key=lambda item: item.name):
            if not all((path / name).is_file() for name in ProcessPackageLoader.REQUIRED_FILES):
                continue
            try:
                package = ProcessPackageLoader.load(path)
            except ProcessPackageError:
                continue
            results.append(ProcessView(package.process.process_code, package.process.name,
                                       package.profile.process_version, package.process.status, package.path,
                                       package.process.normative_document_number))
        return tuple(results)


class TestDataGenerator:
    """Creates reproducible minimal values from a public FormDefinition."""

    def generate(self, form: FormDefinition, *, seed: int = 0,
                 structured_rules=()) -> dict[str, object]:
        if form.generation_status == "NORMATIVE_CONFLICT":
            return {}
        random = Random(seed)
        result: dict[str, object] = {}
        fields_by_path = {field.path: field for field in self._walk(form.fields)}
        rule_paths = self._structured_rule_paths(structured_rules)

        def explicitly_required(field: FieldView) -> bool:
            return any(hint == "message_rule=REQUIRED" for hint in field.validation_hints)

        def should_include(field: FieldView) -> bool:
            required_by_structured_rule = any(
                path == field.path or path.startswith(field.path + "/")
                for path in rule_paths
            )
            return required_by_structured_rule or field.required or field.fixed_value is not None or any(
                explicitly_required(child) or child.fixed_value is not None or any_explicit_descendant(child)
                for child in field.children
            )

        def any_explicit_descendant(field: FieldView) -> bool:
            return any(explicitly_required(child) or child.fixed_value is not None or any_explicit_descendant(child)
                       for child in field.children)

        def visit(field: FieldView) -> None:
            if field.visibility == "HIDDEN" or not should_include(field):
                return
            if field.children:
                if field.ui_input_policy == "GROUP":
                    result[field.path] = [None] * field.min_occurs if field.repeatable and (field.min_occurs or 0) > 1 else None
                else:
                    value = field.fixed_value if field.fixed_value is not None else self._value(field, random)
                    result[field.path] = [value] * field.min_occurs if field.repeatable and (field.min_occurs or 0) > 1 else value
                for child in field.children:
                    visit(child)
                return
            value = field.fixed_value if field.fixed_value is not None else self._value(field, random)
            result[field.path] = [value] * field.min_occurs if field.repeatable and (field.min_occurs or 0) > 1 else value

        for field in form.fields:
            visit(field)
        for field in self._walk(form.fields):
            if field.path not in result:
                continue
            if field.xml_name == "InfEnvelopeCode": result[field.path] = form.message_code
            elif field.xml_name == "EDocCode": result[field.path] = form.structure_id
        self._apply_structured_rules(result, fields_by_path, structured_rules, random)
        return result

    @staticmethod
    def _structured_rule_paths(rules) -> set[str]:
        """Return the concrete form paths used by executable structured rules."""
        paths: set[str] = set()

        def selector_paths(selector):
            if not selector:
                return
            collection = selector.get("collection")
            if not collection:
                return
            paths.add(collection)
            where = selector.get("where") or {}
            if where.get("field"):
                paths.add(f"{collection}/{where['field']}")

        for rule in rules:
            kind = rule.get("kind")
            if kind in {"cardinality", "fixed_value"}:
                if rule.get("target"):
                    paths.add(rule["target"])
            elif kind == "presence" and rule.get("state") == "REQUIRED":
                if rule.get("target"):
                    paths.add(rule["target"])
            elif kind == "comparison":
                if isinstance(rule.get("left"), str):
                    paths.add(rule["left"])
                if isinstance(rule.get("right"), str):
                    paths.add(rule["right"])
            elif kind == "selection_cardinality":
                selector_paths(rule.get("selector"))
            elif kind == "conditional_presence":
                scope = rule.get("scope") or {}
                collection = scope.get("collection")
                if collection:
                    paths.add(collection)
                    condition = rule.get("condition") or {}
                    target = rule.get("target") or {}
                    if condition.get("field"):
                        paths.add(f"{collection}/{condition['field']}")
                    if target.get("field"):
                        paths.add(f"{collection}/{target['field']}")
            elif kind == "aggregate_comparison":
                for aggregate in (rule.get("left") or {}, rule.get("right") or {}):
                    selector = aggregate.get("selector") or {}
                    selector_paths(selector)
                    collection = selector.get("collection")
                    value_field = aggregate.get("value_field")
                    if collection and value_field:
                        paths.add(f"{collection}/{value_field}")
        return paths

    def _apply_structured_rules(self, values, fields_by_path, rules, random) -> None:
        """Make generated values satisfy the executable declarative rule subset.

        The form remains the source of datatype examples; rules only say which
        optional fields and collection instances are required for a coherent
        test document.
        """
        collections: dict[str, list[object]] = {}

        def default_value(path):
            field = fields_by_path.get(path)
            return self._value(field, random) if field else "TEST"

        def ensure_collection(path, count):
            count = max(0, count)
            current = collections.get(path)
            if current is None:
                existing = values.get(path)
                existing_count = len(existing) if isinstance(existing, list) else int(existing is not None)
                current = [None] * max(count, existing_count)
                collections[path] = current
            elif len(current) < count:
                current.extend([None] * (count - len(current)))
            values[path] = current
            return current

        def set_collection_field(collection, field_name, index, value):
            items = ensure_collection(collection, index + 1)
            path = f"{collection}/{field_name}"
            existing = values.get(path)
            if isinstance(existing, list):
                field_values = list(existing)
            else:
                initial = existing if existing is not None else default_value(path)
                field_values = [initial] * len(items)
            if len(field_values) < len(items):
                field_values.extend([default_value(path)] * (len(items) - len(field_values)))
            field_values[index] = value
            values[path] = field_values

        for rule in rules:
            if rule.get("kind") != "cardinality":
                continue
            minimum = rule.get("min_occurs", 0)
            if minimum:
                ensure_collection(rule["target"], minimum)

        selection_rules: dict[str, list[object]] = {}
        for rule in rules:
            if rule.get("kind") != "selection_cardinality":
                continue
            selector = rule["selector"]
            collection = selector["collection"]
            where = selector.get("where") or {}
            minimum = rule.get("min_occurs", 0)
            if not where or not minimum:
                continue
            entries = selection_rules.setdefault(collection, [])
            for _ in range(minimum):
                entries.append(where)

        for collection, selectors in selection_rules.items():
            ensure_collection(collection, len(selectors))
            for index, selector in enumerate(selectors):
                set_collection_field(collection, selector["field"], index, selector.get("value"))

        for rule in rules:
            if rule.get("kind") != "conditional_presence":
                continue
            collection = rule["scope"]["collection"]
            condition = rule["condition"]
            target = rule["target"]["field"]
            items = ensure_collection(collection, len(collections.get(collection, ())))
            condition_path = f"{collection}/{condition['field']}"
            condition_values = values.get(condition_path, ())
            for index in range(len(items)):
                value = condition_values[index] if isinstance(condition_values, list) else condition_values
                if value != condition.get("value"):
                    continue
                required = rule.get("state") == "REQUIRED"
                set_collection_field(collection, target, index, default_value(f"{collection}/{target}") if required else None)

        for rule in rules:
            if rule.get("kind") == "comparison":
                self._satisfy_comparison(values, fields_by_path, rule)
            elif rule.get("kind") == "aggregate_comparison" and rule.get("operator") == "EQ":
                self._satisfy_equal_aggregate(values, rule, collections, default_value, set_collection_field)

    @staticmethod
    def _satisfy_comparison(values, fields_by_path, rule) -> None:
        left_path = rule.get("left")
        right_path = rule.get("right")
        if not isinstance(left_path, str) or not isinstance(right_path, str):
            return
        operator = rule.get("operator")
        left_value = values.get(left_path)
        right_value = values.get(right_path)
        if operator not in {"GT", "GE", "LT", "LE"} or left_value is None or right_value is None:
            return
        if isinstance(left_value, str) and isinstance(right_value, str):
            try:
                right_date = date.fromisoformat(right_value)
            except ValueError:
                return
            delta = timedelta(days=1)
            values[left_path] = (right_date + delta).isoformat() if operator in {"GT", "GE"} else (right_date - delta).isoformat()
            return
        if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
            values[left_path] = right_value + 1 if operator in {"GT", "GE"} else right_value - 1

    @staticmethod
    def _satisfy_equal_aggregate(values, rule, collections, default_value, set_collection_field) -> None:
        aggregates = (rule.get("left") or {}, rule.get("right") or {})
        for aggregate in aggregates:
            selector = aggregate.get("selector") or {}
            collection = selector.get("collection")
            value_field = aggregate.get("value_field")
            if not collection or not value_field:
                return
            items = collections.get(collection, [])
            where = selector.get("where") or {}
            for index in range(len(items)):
                condition_path = f"{collection}/{where.get('field', '')}"
                condition_values = values.get(condition_path, ())
                condition_value = condition_values[index] if isinstance(condition_values, list) else condition_values
                if where and condition_value != where.get("value"):
                    continue
                set_collection_field(collection, value_field, index, "10.50")

    @classmethod
    def _walk(cls, fields):
        for field in fields:
            yield field
            yield from cls._walk(field.children)

    @staticmethod
    def _value(field: FieldView, random: Random):
        if field.input_policy == "AUTO_GENERATED" and field.value_source == "GENERATED_UUID":
            return str(UUID(int=random.getrandbits(128), version=4))
        datatype = (field.datatype or "").lower()
        if datatype == "any_xml": return ET.Element("{urn:test:external}Payload")
        if "uuid" in datatype:return str(UUID(int=random.getrandbits(128),version=4))
        if "indicator" in datatype or "boolean" in datatype:return True
        if "countrycode" in datatype:return "AA"
        if "datetime" in datatype:return "2026-08-24T00:00:00"
        if datatype.endswith("datetype") or datatype=="date":return "2026-08-24"
        local_type=datatype.rsplit(":",1)[-1]
        if "identifier" in datatype or "idtype" in datatype or (local_type.startswith("id") and local_type.endswith("type")):return "TEST"
        if "decimal" in datatype or "paymentamount" in datatype:return "10.50"
        if "quantity" in datatype or "integer" in datatype or "number" in datatype:return 1
        if field.classifier: return "TEST_CLASSIFIER_PLACEHOLDER"
        return "TEST"

    @staticmethod
    def example_value(*, datatype: str | None, xml_name: str | None, classifier: str | None = None):
        """Stable non-normative example used by presentation clients."""
        from eaeu_xml.application.examples import ExampleValueResolver
        return ExampleValueResolver().resolve(datatype=datatype,description=None,classifier=bool(classifier)).value
