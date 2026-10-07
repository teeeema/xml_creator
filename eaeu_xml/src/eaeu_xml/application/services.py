from datetime import date, datetime, timedelta
from pathlib import Path
from random import Random
import re
from typing import Mapping
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
                 structured_rules=(), mode: str = "test",
                 existing_values: Mapping[str, object] | None = None) -> dict[str, object]:
        if mode not in {"test", "required"}:
            raise ValueError(f"Unknown form data mode: {mode}")
        if form.generation_status == "NORMATIVE_CONFLICT":
            return dict(existing_values or {}) if mode == "required" else {}
        random = Random(seed)
        result: dict[str, object] = dict(existing_values or {}) if mode == "required" else {}
        fields_by_path = {field.path: field for field in self._walk(form.fields)}
        required_cardinalities = {}
        for rule in structured_rules:
            if (rule.get("kind") == "cardinality" and rule.get("min_occurs", 0) > 0
                    and rule.get("target") in fields_by_path
                    and rule.get("applies_to_structure", form.structure_id) == form.structure_id):
                target = rule["target"]
                required_cardinalities[target] = max(required_cardinalities.get(target, 0),
                                                     rule["min_occurs"])
        rule_paths = set(required_cardinalities)
        structural_presence_paths: set[str] = set()
        for rule in structured_rules:
            kind = rule.get("kind")
            if kind == "selection_cardinality" and rule.get("min_occurs", 0) > 0 and not rule.get("when"):
                selector = rule.get("selector") or {}
                collection = selector.get("collection")
                if collection in fields_by_path:
                    rule_paths.add(collection)
                    where_field = (selector.get("where") or {}).get("field")
                    if where_field and f"{collection}/{where_field}" in fields_by_path:
                        rule_paths.add(f"{collection}/{where_field}")
            elif kind == "presence" and rule.get("state") == "REQUIRED" and rule.get("target") in fields_by_path:
                rule_paths.add(rule["target"])
                structural_presence_paths.add(rule["target"])
            elif kind == "fixed_value" and rule.get("target") in fields_by_path:
                rule_paths.add(rule["target"])
            elif kind == "cross_instance_comparison" and rule.get("operator") == "EQ":
                for operand in (rule.get("left") or {}, rule.get("right") or {}):
                    selector = operand.get("selector") or {}
                    collection = selector.get("collection")
                    if collection not in fields_by_path:
                        continue
                    rule_paths.add(collection)
                    where_field = (selector.get("where") or {}).get("field")
                    if where_field and f"{collection}/{where_field}" in fields_by_path:
                        rule_paths.add(f"{collection}/{where_field}")
                    operand_field = operand.get("field")
                    if operand_field and f"{collection}/{operand_field}" in fields_by_path:
                        rule_paths.add(f"{collection}/{operand_field}")
        changed = True
        while changed:
            before = len(rule_paths)
            for rule in structured_rules:
                if rule.get("kind") != "for_each":
                    continue
                selector = rule.get("selector") or {}
                collections = ([selector["collection"]] if selector.get("collection") in fields_by_path else
                               [path for path in fields_by_path if path.split("/")[-1] == selector.get("qname")])
                for collection in collections:
                    prefixes = ["/".join(collection.split("/")[:i]) for i in range(1, len(collection.split("/")) + 1)]
                    if any(
                        not fields_by_path[path].required
                        and not any(selected == path or selected.startswith(path + "/") for selected in rule_paths)
                        for path in prefixes[:-1]
                    ):
                        continue
                    owner_selected = (
                        collection in rule_paths
                        or fields_by_path[collection].required
                        or any(path.startswith(collection + "/") for path in rule_paths)
                    )
                    if not owner_selected:
                        continue
                    for assertion in rule.get("assertions", ()):
                        kind = assertion.get("kind")
                        target = assertion.get("target") or {}
                        if kind in {"presence", "fixed_value"} and isinstance(target, dict):
                            if kind == "presence" and assertion.get("state") != "REQUIRED":
                                continue
                            path = f"{collection}/{target.get('field', '')}"
                            if path not in fields_by_path and target.get("field") in fields_by_path:
                                path = target["field"]
                            if path in fields_by_path:
                                rule_paths.add(path)
                                if kind == "presence":
                                    structural_presence_paths.add(path)
                        elif kind == "comparison" and assertion.get("operator") == "IN" and assertion.get("right_value"):
                            left = assertion.get("left")
                            left_field = (left.get("field") if isinstance(left, dict)
                                          else left if isinstance(left, str) else None)
                            path = f"{collection}/{left_field}" if left_field else ""
                            if path not in fields_by_path and left_field in fields_by_path:
                                path = left_field
                            if path in fields_by_path:
                                rule_paths.add(path)
                        elif kind == "selection_cardinality" and assertion.get("min_occurs", 0) > 0:
                            nested = assertion.get("selector") or {}
                            path = nested.get("collection")
                            if path in fields_by_path:
                                rule_paths.add(path)
                                where_field = (nested.get("where") or {}).get("field")
                                if where_field and f"{path}/{where_field}" in fields_by_path:
                                    rule_paths.add(f"{path}/{where_field}")
                        elif kind == "condition":
                            alternatives = (assertion.get("condition") or {}).get("any") or ()
                            for alternative in alternatives:
                                count = alternative.get("count") or {}
                                count_collection = count.get("collection")
                                if (count_collection in fields_by_path
                                        and alternative.get("operator") in {"GE", "GT"}
                                        and alternative.get("value", 0) >= 1):
                                    rule_paths.add(count_collection)
                                    break
                                if alternative.get("operator") != "NE" or alternative.get("value") is not None:
                                    continue
                                raw_field = alternative.get("field", "")
                                candidate = f"{collection}/{raw_field}"
                                if candidate not in fields_by_path and raw_field in fields_by_path:
                                    candidate = raw_field
                                field = fields_by_path.get(candidate)
                                if field and field.children:
                                    # ``field != null`` may select a complex group rather than a scalar.
                                    # Mark the group as required-by-rule so the normal form walk
                                    # materializes it and its required descendants.
                                    rule_paths.add(candidate)
                                    structural_presence_paths.add(candidate)
                                    break
                                if field and (field.fixed_value is not None or field.allowed_values or field.example_value is not None):
                                    rule_paths.add(candidate)
                                    break
            changed = len(rule_paths) > before

        def explicitly_required(field: FieldView) -> bool:
            return any(hint == "message_rule=REQUIRED" for hint in field.validation_hints)

        def any_explicit_descendant(field: FieldView) -> bool:
            return any(explicitly_required(child) or child.fixed_value is not None or any_explicit_descendant(child)
                       for child in field.children)

        def should_include(field: FieldView) -> bool:
            if field.path in result or any(path.startswith(field.path + "/") for path in result):
                return True
            if mode == "required":
                return ((field.required and field.normative_input_policy != "CONDITIONAL") or
                        any(path == field.path or path.startswith(field.path + "/")
                            for path in rule_paths) or any_explicit_descendant(field))
            required_by_structured_rule = any(
                path == field.path or path.startswith(field.path + "/")
                for path in rule_paths
            )
            return required_by_structured_rule or field.required or field.fixed_value is not None or any(
                explicitly_required(child) or child.fixed_value is not None or any_explicit_descendant(child)
                for child in field.children
            )

        def visit(field: FieldView) -> None:
            if field.visibility == "HIDDEN" or not should_include(field):
                return
            if mode == "required" and field.classifier and field.fixed_value is None and not field.allowed_values:
                return
            if field.children:
                if field.path not in result:
                    if field.ui_input_policy == "GROUP":
                        requires_structural_presence = field.path in structural_presence_paths
                        item = ((field.example_value if field.example_value is not None else self._value(field, random))
                                if all(child.is_attribute for child in field.children)
                                else ("" if requires_structural_presence and not field.repeatable else None))
                        result[field.path] = ([item] * max(1, field.min_occurs or 0)
                                              if mode == "required" and field.repeatable else
                                              [item] * field.min_occurs if field.repeatable and (field.min_occurs or 0) > 1 else item)
                    else:
                        value = field.fixed_value if field.fixed_value is not None else self._value(field, random)
                        result[field.path] = [value] * field.min_occurs if field.repeatable and (field.min_occurs or 0) > 1 else value
                for child in field.children:
                    visit(child)
                return
            if result.get(field.path) not in (None, "", [], ()):
                return
            value = field.fixed_value if field.fixed_value is not None else self._value(field, random)
            if mode == "required" and field.allowed_values and field.fixed_value is None:
                value = field.allowed_values[0]
            if mode == "required" and field.pattern:
                try:
                    matches = re.fullmatch(field.pattern, str(value)) is not None
                except re.error:
                    matches = False
                if not matches:
                    candidate = field.example_value
                    if candidate is None:
                        return
                    try:
                        if re.fullmatch(field.pattern, str(candidate)) is None:
                            return
                    except re.error:
                        return
                    value = candidate
            result[field.path] = [value] * field.min_occurs if field.repeatable and (field.min_occurs or 0) > 1 else value

        for field in form.fields:
            visit(field)
        for field in self._walk(form.fields):
            if field.path not in result:
                continue
            if mode == "required" and existing_values and existing_values.get(field.path) not in (None, "", [], ()):
                continue
            if field.xml_name == "InfEnvelopeCode": result[field.path] = form.message_code
            elif field.xml_name == "EDocCode": result[field.path] = form.structure_id
        if mode == "required":
            for path, minimum in required_cardinalities.items():
                if not fields_by_path[path].children:
                    continue
                value = result.get(path)
                if value is None:
                    result[path] = [None] * minimum
                elif isinstance(value, list) and len(value) < minimum:
                    result[path] = [*value, *([None] * (minimum - len(value)))]
        self._apply_structured_rules(result, fields_by_path, structured_rules, random,
                                     existing_values or {})
        for field in form.fields:
            visit(field)
        for field in fields_by_path.values():
            if (not field.children or field.repeatable or field.path not in structural_presence_paths
                    or field.path not in result
                    or (existing_values and field.path in existing_values)):
                continue
            current = result[field.path]
            if current is None:
                result[field.path] = ""
            elif isinstance(current, list):
                result[field.path] = ["" if item is None else item for item in current]
        for field in sorted(fields_by_path.values(), key=lambda item: item.path.count("/")):
            if field.path not in result or (existing_values and field.path in existing_values):
                continue
            parent_path = field.path.rpartition("/")[0]
            parent_value = result.get(parent_path)
            if isinstance(parent_value, list) and len(parent_value) > 1 and not isinstance(result[field.path], list):
                result[field.path] = [result[field.path]] * len(parent_value)
        self._apply_literal_rules(result, fields_by_path, structured_rules, existing_values or {})
        for field in sorted(fields_by_path.values(), key=lambda item: item.path.count("/")):
            if field.path not in result or (existing_values and field.path in existing_values):
                continue
            parent_path = field.path.rpartition("/")[0]
            parent_value = result.get(parent_path)
            if isinstance(parent_value, list) and len(parent_value) > 1 and not isinstance(result[field.path], list):
                result[field.path] = [result[field.path]] * len(parent_value)
        return result

    @staticmethod
    def _apply_literal_rules(values, fields_by_path, rules, existing_values) -> None:
        """Use explicit rule literals for fields the form helper already selected."""
        from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator

        evaluator = StructuredRuleEvaluator()

        def resolve_field_path(owner_path, field_name):
            candidate = f"{owner_path}/{field_name}" if owner_path and field_name else ""
            if candidate in fields_by_path:
                return candidate
            if field_name in fields_by_path:
                return field_name
            return candidate

        def assign(path, value):
            if path not in values or path in existing_values or path not in fields_by_path:
                return
            current = values[path]
            if isinstance(current, list):
                def replace(items):
                    return [replace(item) if isinstance(item, list) else value for item in items]
                values[path] = replace(current)
            else:
                values[path] = value

        def ensure_group_present(path, owner_path, contexts):
            if path in existing_values or path not in fields_by_path:
                return
            selected = [context for context in contexts if context.path == owner_path]
            if not selected:
                return

            def ensure_at_indexes(current, indexes):
                if not indexes:
                    if isinstance(current, list):
                        if not current:
                            return [""]
                        return ["" if item is None else item for item in current]
                    return "" if current is None else current
                index = indexes[0]
                updated = (list(current) if isinstance(current, list)
                           else [current] if index == 0 and current is not None else [])
                while len(updated) <= index:
                    updated.append(None)
                updated[index] = ensure_at_indexes(updated[index], indexes[1:])
                return updated

            current = values.get(path)
            for context in selected:
                current = ensure_at_indexes(current, context.indexes)
            values[path] = current

        def assign_to_contexts(path, owner_path, contexts, value, *, condition=None):
            """Assign a rule literal only to the selected repeatable owner instances."""
            if path in existing_values or path not in fields_by_path:
                return
            selected = [context for context in contexts if context.path == owner_path]
            if condition is not None:
                selected = [context for context in selected
                            if evaluator.evaluate_condition(condition, context, values)]
            if not selected:
                return

            def assign_at_indexes(current, indexes):
                if not indexes:
                    return value
                index = indexes[0]
                updated = list(current) if isinstance(current, list) else []
                while len(updated) <= index:
                    updated.append(None)
                updated[index] = assign_at_indexes(updated[index], indexes[1:])
                return updated

            current = values.get(path)
            for context in selected:
                current = assign_at_indexes(current, context.indexes)
            for context in evaluator._contexts_for_path(owner_path, values):
                if not context.indexes:
                    continue
                cursor = current
                indexes = context.indexes
                if not isinstance(cursor, list):
                    cursor = []
                    current = cursor
                for depth, index in enumerate(indexes):
                    while len(cursor) <= index:
                        cursor.append(None)
                    if depth == len(indexes) - 1:
                        break
                    if not isinstance(cursor[index], list):
                        cursor[index] = []
                    cursor = cursor[index]
            values[path] = current

        def safe_literal(path):
            field = fields_by_path.get(path)
            if not field or field.classifier:
                return None
            if field.fixed_value is not None:
                return field.fixed_value
            if field.allowed_values:
                return field.allowed_values[0]
            for rule in rules:
                if rule.get("kind") != "for_each":
                    continue
                selector = rule.get("selector") or {}
                if selector.get("collection") != path:
                    continue
                for assertion in rule.get("assertions", ()):
                    if assertion.get("kind") != "condition":
                        continue
                    condition = assertion.get("condition") or {}
                    alternatives = condition.get("any") or (condition,)
                    for alternative in alternatives:
                        options = alternative.get("value") or ()
                        if (alternative.get("field") == "#text"
                                and alternative.get("operator") == "IN"
                                and isinstance(options, (list, tuple)) and options):
                            return options[0]
            return field.example_value

        def operand_contexts(owner_path, selected_contexts, operand):
            if not isinstance(operand, dict) or not operand.get("field"):
                return None, None, ()
            selector = operand.get("selector")
            if selector:
                try:
                    contexts = evaluator._select_contexts(selector, values)
                except (KeyError, TypeError, ValueError):
                    return None, None, ()
                collection = selector.get("collection")
                if not collection:
                    return None, None, ()
                return f"{collection}/{operand['field']}", collection, contexts
            return f"{owner_path}/{operand['field']}", owner_path, selected_contexts

        def context_value(path, context):
            raw = values.get(path)
            return evaluator._value_at(raw, context.indexes)

        def materialize_contexts(path, owner_path, contexts, value):
            if path in existing_values:
                return
            for context in contexts:
                if context_value(path, context) is None:
                    assign_to_contexts(path, owner_path, (context,), value)

        def complete_comparison(owner_path, selected_contexts, assertion):
            operator = assertion.get("operator")
            value_type = assertion.get("value_type")
            left = assertion.get("left")
            right = assertion.get("right")
            cross_selected = (
                isinstance(left, dict) and left.get("selector")
                or isinstance(right, dict) and right.get("selector")
            )
            if not ((operator in {"GT", "GE", "LT", "LE"} and value_type in {"DATE", "DATETIME"})
                    or (operator == "EQ" and cross_selected)):
                return

            left_path, left_owner, left_contexts = operand_contexts(owner_path, selected_contexts, left)
            right_path, right_owner, right_contexts = operand_contexts(owner_path, selected_contexts, right)
            if not left_path or not right_path or not left_contexts or not right_contexts:
                return

            left_default = safe_literal(left_path)
            right_default = safe_literal(right_path)
            if left_default is None or right_default is None:
                return
            materialize_contexts(left_path, left_owner, left_contexts, left_default)
            materialize_contexts(right_path, right_owner, right_contexts, right_default)

            if operator == "EQ":
                if left_path in existing_values and right_path in existing_values:
                    return
                left_value = context_value(left_path, left_contexts[0])
                right_value = context_value(right_path, right_contexts[0])
                common = left_value if left_value is not None else right_value
                if common is None:
                    return
                if left_path not in existing_values:
                    assign_to_contexts(left_path, left_owner, left_contexts, common)
                if right_path not in existing_values:
                    assign_to_contexts(right_path, right_owner, right_contexts, common)
                return

            try:
                parse = datetime.fromisoformat if value_type == "DATETIME" else date.fromisoformat
                left_value = parse(str(context_value(left_path, left_contexts[0])))
                right_value = parse(str(context_value(right_path, right_contexts[0])))
            except (TypeError, ValueError):
                return

            if evaluator._compare(left_value, operator, right_value):
                return
            delta = timedelta(seconds=1) if value_type == "DATETIME" else timedelta(days=1)
            if left_path not in existing_values and not (isinstance(left, dict) and left.get("selector")):
                desired = right_value + delta if operator in {"GT", "GE"} else right_value - delta
                assign_to_contexts(left_path, left_owner, left_contexts, desired.isoformat())
            elif right_path not in existing_values and not (isinstance(right, dict) and right.get("selector")):
                desired = left_value - delta if operator in {"GT", "GE"} else left_value + delta
                assign_to_contexts(right_path, right_owner, right_contexts, desired.isoformat())

        for rule in rules:
            if rule.get("kind") != "fixed_value":
                continue
            target = rule.get("target")
            if isinstance(target, str):
                assign(target, rule.get("value"))

        # Group-presence rules can be ordered before the rule that creates their
        # parent contexts. Materialize only explicit REQUIRED groups to a fixed
        # point before applying value literals to those contexts.
        for _ in range(len(rules) + 1):
            changed = False
            for rule in rules:
                if rule.get("kind") != "for_each":
                    continue
                selector = rule.get("selector") or {}
                try:
                    selected_contexts = evaluator._select_contexts(selector, values)
                except (KeyError, TypeError, ValueError):
                    continue
                if not selected_contexts:
                    continue
                collection = selector.get("collection")
                collections = ([collection] if collection else
                               [path for path in values if path.split("/")[-1] == selector.get("qname")])
                for owner_path in collections:
                    if owner_path not in values:
                        continue
                    for assertion in rule.get("assertions", ()):
                        target = assertion.get("target") or {}
                        if (assertion.get("kind") != "presence"
                                or assertion.get("state") != "REQUIRED"
                                or not isinstance(target, dict)):
                            continue
                        target_path = f"{owner_path}/{target.get('field', '')}"
                        field = fields_by_path.get(target_path)
                        if not field or not field.children or target_path in existing_values:
                            continue
                        previous = values.get(target_path)
                        ensure_group_present(target_path, owner_path, selected_contexts)
                        if values.get(target_path) != previous:
                            changed = True
            if not changed:
                break

        for rule in rules:
            if rule.get("kind") == "conditional_presence" and rule.get("state") == "REQUIRED":
                scope = rule.get("scope") or {}
                collection = scope.get("collection")
                target = rule.get("target") or {}
                if not collection or not isinstance(target, dict) or not target.get("field"):
                    continue
                try:
                    contexts = evaluator._select_contexts(scope, values, apply_where=False)
                except (KeyError, TypeError, ValueError):
                    continue
                selected = [
                    context for context in contexts
                    if evaluator.evaluate_condition(rule.get("condition") or {}, context, values)
                ]
                target_path = resolve_field_path(collection, target["field"])
                literal = safe_literal(target_path)
                if selected and literal is not None:
                    assign_to_contexts(target_path, collection, selected, literal)
                continue
            if rule.get("kind") == "conditional_fixed_value":
                scope = rule.get("scope") or {}
                collection = scope.get("collection")
                target = rule.get("target") or {}
                path = f"{collection}/{target.get('field', '')}" if collection else ""
                if path in fields_by_path and path not in existing_values:
                    contexts = evaluator._select_contexts(scope, values, apply_where=False)
                    if contexts and all(evaluator.evaluate_condition(rule["condition"], context, values) for context in contexts):
                        values[path] = [rule.get("value")] * len(contexts) if len(contexts) > 1 else rule.get("value")
                continue
            if rule.get("kind") != "for_each":
                continue
            selector = rule.get("selector") or {}
            try:
                selected_contexts = evaluator._select_contexts(selector, values)
            except (KeyError, TypeError, ValueError):
                selected_contexts = []
            if not selected_contexts:
                continue
            collection = selector.get("collection")
            collections = ([collection] if collection else
                           [path for path in values if path.split("/")[-1] == selector.get("qname")])
            for path in collections:
                if path not in values:
                    continue
                for assertion in rule.get("assertions", ()):
                    kind = assertion.get("kind")
                    target = assertion.get("target") or assertion.get("left") or {}
                    if kind == "presence" and assertion.get("state") == "REQUIRED" and isinstance(target, dict):
                        target_path = f"{path}/{target.get('field', '')}"
                        field = fields_by_path.get(target_path)
                        if field and field.children and target_path not in existing_values:
                            ensure_group_present(target_path, path, selected_contexts)
                    elif kind == "fixed_value" and isinstance(target, dict):
                        where = selector.get("where") or {}
                        if (where.get("operator") == "EQ"
                                and target.get("field") == where.get("field")
                                and assertion.get("value") == where.get("value")):
                            continue
                        assign(f"{path}/{target.get('field', '')}", assertion.get("value"))
                    elif kind == "conditional_fixed_value" and isinstance(target, dict):
                        condition = assertion.get("condition") or {}
                        if (target.get("position") is not None
                                or condition.get("operator") != "EQ"
                                or condition.get("value") is not None
                                or not condition.get("field")):
                            continue
                        assign_to_contexts(
                            f"{path}/{target.get('field', '')}",
                            path,
                            selected_contexts,
                            assertion.get("value"),
                            condition=condition,
                        )
                    elif kind == "comparison" and assertion.get("operator") == "IN":
                        options = assertion.get("right_value") or ()
                        left = assertion.get("left")
                        left_field = (left.get("field") if isinstance(left, dict)
                                      else left if isinstance(left, str) else None)
                        if options and left_field:
                            candidate = resolve_field_path(path, left_field)
                            if candidate in existing_values:
                                continue
                            current = values.get(candidate)
                            if isinstance(current, list):
                                values[candidate] = [
                                    item if item in options else options[0]
                                    for item in current
                                ]
                            elif current not in options:
                                assign(candidate, options[0])
                    elif kind == "comparison":
                        complete_comparison(path, selected_contexts, assertion)
                    elif kind == "selection_cardinality" and assertion.get("min_occurs", 0) > 0:
                        nested = assertion.get("selector") or {}
                        collection_path = nested.get("collection")
                        where = nested.get("where") or {}
                        if collection_path and where.get("operator") == "EQ":
                            candidate = f"{collection_path}/{where.get('field', '')}"
                            desired = where.get("value")
                            current = values.get(candidate)
                            if isinstance(current, list):
                                if desired not in current and candidate not in existing_values and current:
                                    current = list(current)
                                    current[-1] = desired
                                    values[candidate] = current
                            elif current != desired:
                                assign(candidate, desired)
                    elif kind == "condition":
                        alternatives = (assertion.get("condition") or {}).get("any") or ()
                        for alternative in alternatives:
                            options = alternative.get("value") or ()
                            if alternative.get("operator") == "IN" and options:
                                field_name = alternative.get("field", "")
                                candidate = path if field_name == "#text" else resolve_field_path(path, field_name)
                                assign(candidate, options[0])
                                break
                            if alternative.get("operator") == "NE" and alternative.get("value") is None:
                                candidate = f"{path}/{alternative.get('field', '')}"
                                field = fields_by_path.get(candidate)
                                if not field or candidate in existing_values:
                                    continue
                                safe_value = (field.fixed_value if field.fixed_value is not None else
                                              field.allowed_values[0] if field.allowed_values else
                                              field.example_value)
                                if safe_value is not None:
                                    assign(candidate, safe_value)
                                    break
                    elif kind == "conditional_presence" and assertion.get("state") == "REQUIRED":
                        condition = assertion.get("condition") or {}
                        if target.get("position", 1) != 1 and condition.get("all"):
                            for predicate in condition["all"]:
                                if predicate.get("operator") == "NE" and predicate.get("value") is not None:
                                    assign(f"{path}/{predicate.get('field', '')}", predicate["value"])
                                    break

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

    def _apply_structured_rules(self, values, fields_by_path, rules, random,
                                existing_values=None) -> None:
        """Make generated values satisfy the executable declarative rule subset.

        The form remains the source of datatype examples; rules only say which
        optional fields and collection instances are required for a coherent
        test document.
        """
        collections: dict[str, list[object]] = {}
        existing_values = existing_values or {}
        from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator
        evaluator = StructuredRuleEvaluator()

        def default_value(path):
            field = fields_by_path.get(path)
            return self._value(field, random) if field else "TEST"

        def ensure_collection(path, count):
            field = fields_by_path.get(path)
            if field is None:
                return []
            if not field.repeatable:
                if count and values.get(path) is None:
                    values[path] = "" if field.children else default_value(path)
                return [values[path]] if path in values else []
            count = max(0, count, field.min_occurs or 0)
            current = collections.get(path)
            if current is None:
                existing = values.get(path)
                has_descendants = any(key.startswith(path + "/") for key in values)
                existing_count = len(existing) if isinstance(existing, list) else int(existing is not None or has_descendants)
                current = [None] * max(count, existing_count)
                collections[path] = current
            elif len(current) < count:
                current.extend([None] * (count - len(current)))
            values[path] = current
            return current

        def set_collection_field(collection, field_name, index, value):
            items = ensure_collection(collection, index + 1)
            path = f"{collection}/{field_name}"
            if path not in fields_by_path:
                return
            if path in existing_values:
                return
            if not fields_by_path[collection].repeatable:
                if index == 0:
                    values[path] = value
                return
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

        for rule in rules:
            if rule.get("kind") != "selection_cardinality":
                continue
            selector = rule.get("selector") or {}
            if rule.get("min_occurs", 0) > 0 and not selector.get("where"):
                collection = selector.get("collection")
                if collection in fields_by_path:
                    ensure_collection(collection, rule["min_occurs"])

        selection_rules: dict[str, dict[tuple[object, object], tuple[dict, int]]] = {}

        def collect_selection(rule):
            selector = rule.get("selector") or {}
            collection = selector.get("collection")
            if collection is None:
                return
            where = selector.get("where") or {}
            minimum = rule.get("min_occurs", 0)
            if not where or not minimum or where.get("operator") not in {"EQ", "IN"}:
                return
            desired = where.get("value")
            if where.get("operator") == "IN":
                if not isinstance(desired, (list, tuple)) or not desired:
                    return
                desired = desired[0]
            normalized_where = {**where, "operator": "EQ", "value": desired}
            key = (where.get("field"), desired)
            entries = selection_rules.setdefault(collection, {})
            entries[key] = (normalized_where, max(minimum, entries.get(key, ({}, 0))[1]))

        for rule in rules:
            if rule.get("kind") == "selection_cardinality":
                collect_selection(rule)
                continue
            if rule.get("kind") != "for_each":
                continue
            try:
                from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator
                contexts = StructuredRuleEvaluator()._select_contexts(rule.get("selector") or {}, values)
            except (KeyError, TypeError, ValueError):
                contexts = []
            if not contexts:
                continue
            for assertion in rule.get("assertions", ()):
                if assertion.get("kind") == "selection_cardinality":
                    collect_selection(assertion)

        for collection, groups in selection_rules.items():
            selectors = [where for where, count in groups.values() for _ in range(count)]
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
            if condition_path not in fields_by_path and condition["field"] in fields_by_path:
                condition_path = condition["field"]
            target_path = f"{collection}/{target}"
            if target_path not in fields_by_path and target in fields_by_path:
                target_path = target
            condition_values = values.get(condition_path)
            for index in range(len(items)):
                value = condition_values[index] if isinstance(condition_values, list) else condition_values
                if not evaluator._compare(
                    value,
                    condition.get("operator"),
                    condition.get("value"),
                    condition.get("value_type"),
                ):
                    continue
                required = rule.get("state") == "REQUIRED"
                if target_path.startswith(collection + "/"):
                    if required:
                        set_collection_field(collection, target, index, default_value(target_path))
                    elif target_path not in existing_values:
                        if fields_by_path[collection].repeatable:
                            set_collection_field(collection, target, index, None)
                        else:
                            values.pop(target_path, None)
                elif index == 0 and target_path in fields_by_path and target_path not in existing_values:
                    if required:
                        values[target_path] = default_value(target_path)
                    else:
                        values.pop(target_path, None)

        for rule in rules:
            if rule.get("kind") == "comparison":
                self._satisfy_comparison(values, fields_by_path, rule)
            elif rule.get("kind") == "aggregate_comparison" and rule.get("operator") == "EQ":
                self._satisfy_equal_aggregate(values, rule, collections, default_value, set_collection_field)
            elif rule.get("kind") == "cross_instance_comparison" and rule.get("operator") == "EQ":
                self._satisfy_cross_instance_equality(
                    values, rule, collections, existing_values,
                    default_value, set_collection_field,
                )

    @staticmethod
    def _satisfy_cross_instance_equality(values, rule, collections, existing_values,
                                         default_value, set_collection_field) -> None:
        def selected_index(operand):
            selector = operand.get("selector") or {}
            collection = selector.get("collection")
            where = selector.get("where") or {}
            if (not collection or where.get("operator") != "EQ"
                    or not where.get("field")):
                return None
            count = len(collections.get(collection, ()))
            if count == 0:
                raw_collection = values.get(collection)
                count = (len(raw_collection) if isinstance(raw_collection, list)
                         else int(raw_collection is not None))
            raw = values.get(f"{collection}/{where['field']}")
            if isinstance(raw, list):
                matches = [index for index, value in enumerate(raw[:count])
                           if value == where.get("value")]
                return (collection, matches[0]) if len(matches) == 1 else None
            if count == 1 and raw == where.get("value"):
                return collection, 0
            return None

        def operand_value(operand, selected):
            collection, index = selected
            field_name = operand.get("field")
            if not field_name:
                return None, None
            path = f"{collection}/{field_name}"
            raw = values.get(path)
            value = raw[index] if isinstance(raw, list) and index < len(raw) else raw
            return path, value

        left = rule.get("left") or {}
        right = rule.get("right") or {}
        left_selected = selected_index(left)
        right_selected = selected_index(right)
        if left_selected is None or right_selected is None:
            return

        left_path, left_value = operand_value(left, left_selected)
        right_path, right_value = operand_value(right, right_selected)
        if left_path is None or right_path is None:
            return

        left_user = left_path in existing_values
        right_user = right_path in existing_values
        if left_user and right_user:
            return
        if left_user:
            common = left_value
        elif right_user:
            common = right_value
        elif left_value not in (None, ""):
            common = left_value
        elif right_value not in (None, ""):
            common = right_value
        else:
            common = default_value(left_path)

        if not left_user:
            set_collection_field(left_selected[0], left.get("field"), left_selected[1], common)
        if not right_user:
            set_collection_field(right_selected[0], right.get("field"), right_selected[1], common)

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
        if "uuid" in datatype or "universallyuniqueid" in datatype:
            return str(UUID(int=random.getrandbits(128),version=4))
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
