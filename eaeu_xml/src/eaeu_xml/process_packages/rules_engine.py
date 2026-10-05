from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any, Mapping


class RuleStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_EVALUATED_EXTERNAL_CONTEXT = "NOT_EVALUATED_EXTERNAL_CONTEXT"
    NOT_EVALUATED_EXTERNAL_REFERENCE = "NOT_EVALUATED_EXTERNAL_REFERENCE"
    UNSUPPORTED_RULE = "UNSUPPORTED_RULE"


@dataclass(frozen=True)
class RuleEvaluation:
    rule_id: str | None
    status: RuleStatus
    message: str
    source_refs: tuple[Mapping[str, Any], ...] = ()


@dataclass(frozen=True)
class RuleContext:
    path: str
    indexes: tuple[int, ...]
    fields: Mapping[str, Any]


class StructuredRuleEvaluator:
    def evaluate_all(self, rules, values):
        return tuple(self.evaluate(rule, values) for rule in rules)

    def evaluate(self, rule, values):
        external_statuses = {
            "EXTERNAL_CONTEXT_REQUIRED": RuleStatus.NOT_EVALUATED_EXTERNAL_CONTEXT,
            "EXTERNAL_REFERENCE_REQUIRED": RuleStatus.NOT_EVALUATED_EXTERNAL_REFERENCE,
        }
        evaluation_status = rule.get("evaluation_status")
        if evaluation_status in external_statuses:
            status = external_statuses[evaluation_status]
            return self.out(rule, status, "External dependency required.")

        kind = rule.get("kind")
        if kind in {"cardinality", "presence", "fixed_value"}:
            value = values.get(rule.get("target"))
            count = len(value) if isinstance(value, list) else int(value is not None)

            if kind == "cardinality":
                minimum = rule.get("min_occurs", 0)
                maximum = rule.get("max_occurs")
                passed = minimum <= count and (maximum is None or count <= maximum)
            elif kind == "presence":
                required = rule.get("state") == "REQUIRED"
                passed = (count > 0) == required
            else:
                passed = value == rule.get("value")

            status = RuleStatus.PASS if passed else RuleStatus.FAIL
            return self.out(rule, status, "Rule evaluated.")

        if kind == "selection_cardinality":
            try:
                if "when" in rule and not self.evaluate_condition(rule["when"], None, values):
                    return self.out(rule, RuleStatus.PASS, "Selection cardinality condition does not apply.")
                selected_items = self.select(rule["selector"], values)
                count = len(selected_items)
                minimum = rule.get("min_occurs", 0)
                maximum = rule.get("max_occurs")
                passed = minimum <= count and (maximum is None or count <= maximum)
            except (KeyError, TypeError, ValueError):
                passed = False
            status = RuleStatus.PASS if passed else RuleStatus.FAIL
            return self.out(rule, status, "Selection cardinality evaluated.")

        if kind == "conditional_presence":
            try:
                scope_items = self._select_contexts(rule["scope"], values, apply_where=False)
                target = rule["target"]
                forbidden = rule["state"] == "FORBIDDEN"
                passed = True
                for item in scope_items:
                    if not self.evaluate_condition(rule["condition"], item, values):
                        continue
                    target_is_present = self._target_value(target, item, values) is not None
                    if target_is_present == forbidden:
                        passed = False
                        break
            except (KeyError, TypeError, ValueError):
                passed = False
            status = RuleStatus.PASS if passed else RuleStatus.FAIL
            message = "Conditional presence evaluated." if passed else "Conditional presence failed."
            return self.out(rule, status, message)

        if kind == "conditional_fixed_value":
            try:
                scope_items = self._select_contexts(rule["scope"], values, apply_where=False)
                passed = True
                for item in scope_items:
                    if not self.evaluate_condition(rule["condition"], item, values):
                        continue
                    target_value = self._target_value(rule["target"], item, values)
                    if target_value is None or target_value != rule.get("value"):
                        passed = False
                        break
            except (KeyError, TypeError, ValueError):
                passed = False
            status = RuleStatus.PASS if passed else RuleStatus.FAIL
            message = "Conditional fixed value evaluated." if passed else "Conditional fixed value failed."
            return self.out(rule, status, message)

        if kind == "for_each":
            try:
                contexts = self._select_contexts(rule["selector"], values)
                passed = all(
                    self._assertion_passes(assertion, context, values)
                    for context in contexts
                    for assertion in rule["assertions"]
                )
            except (KeyError, TypeError, ValueError):
                passed = False
            status = RuleStatus.PASS if passed else RuleStatus.FAIL
            message = "For-each evaluated." if passed else "For-each assertion failed."
            return self.out(rule, status, message)

        if kind == "aggregate_comparison":
            try:
                left_value = self.agg(rule["left"], values)
                right_value = self.agg(rule["right"], values)
                passed = self.c(left_value, rule["operator"], right_value)
            except (InvalidOperation, KeyError, ValueError, TypeError):
                passed = False

            status = RuleStatus.PASS if passed else RuleStatus.FAIL
            return self.out(rule, status, "Aggregate comparison evaluated.")

        if kind == "comparison":
            try:
                left_value = values.get(rule["left"])
                right_key = rule.get("right")
                right_value = values.get(right_key, rule.get("right_value"))
                passed = self._compare(left_value, rule["operator"], right_value, rule.get("value_type"))
            except (KeyError, TypeError, ValueError):
                passed = False

            status = RuleStatus.PASS if passed else RuleStatus.FAIL
            return self.out(rule, status, "Comparison evaluated.")

        if kind == "cross_instance_comparison":
            try:
                left_operand = rule["left"]
                right_operand = rule["right"]
                operator = rule["operator"]

                left_items = self._select_contexts(left_operand["selector"], values)
                right_items = self._select_contexts(right_operand["selector"], values)

                if len(left_items) != 1 or len(right_items) != 1:
                    passed = False
                else:
                    left_val = self._context_field_value(left_operand["field"], left_items[0])
                    right_val = self._context_field_value(right_operand["field"], right_items[0])
                    if left_val is None or right_val is None:
                        passed = False
                    else:
                        passed = self._compare(left_val, operator, right_val, rule.get("value_type"))
            except (KeyError, TypeError, ValueError):
                passed = False

            status = RuleStatus.PASS if passed else RuleStatus.FAIL
            message = "Cross-instance comparison evaluated." if passed else "Cross-instance comparison failed."
            return self.out(rule, status, message)

        return self.out(rule, RuleStatus.UNSUPPORTED_RULE, "Unsupported structured rule.")

    def select(self, selector, values, all=False):
        return [dict(item.fields) for item in self._select_contexts(selector, values, apply_where=not all)]

    def _select_contexts(self, selector, values, *, apply_where=True):
        if "collection" in selector:
            contexts = self._contexts_for_path(selector["collection"], values)
        elif "qname" in selector:
            qname = selector["qname"]
            under = selector.get("under")
            paths = set()
            for path in values:
                segments = path.split("/")
                for index, segment in enumerate(segments):
                    if segment != qname:
                        continue
                    candidate = "/".join(segments[:index + 1])
                    if under and candidate != under and not candidate.startswith(under + "/"):
                        continue
                    paths.add(candidate)
            contexts = []
            for path in sorted(paths):
                path_contexts = self._contexts_for_path(path, values)
                raw = values.get(path)
                if isinstance(raw, list) and self._has_present_leaf(raw):
                    path_contexts = [
                        item for item in path_contexts
                        if self._value_at(raw, item.indexes) is not None
                    ]
                elif path not in values:
                    path_contexts = [
                        item for item in path_contexts
                        if any(value is not None for value in item.fields.values())
                    ]
                contexts.extend(path_contexts)
        else:
            raise ValueError("selector requires collection or qname")

        if "parent" in selector:
            parent_selector = selector["parent"]
            if not isinstance(parent_selector, Mapping):
                raise ValueError("parent selector must be a mapping")
            parent_collection = parent_selector.get("collection")
            if not parent_collection:
                raise ValueError("parent selector requires collection")
            child_collection = selector.get("collection")
            if not child_collection:
                raise ValueError("parent-scoped selector requires collection on child")
            if not child_collection.startswith(parent_collection + "/"):
                raise ValueError(
                    f"Parent collection '{parent_collection}' is not an ancestor of '{child_collection}'"
                )
            parent_contexts = self._select_contexts(parent_selector, values)
            allowed_parent_indexes = {ctx.indexes for ctx in parent_contexts}
            scalar_parent = bool(parent_contexts) and len(self._contexts_for_path(parent_collection, values)) == 1
            contexts = [
                ctx for ctx in contexts
                if scalar_parent or any(ctx.indexes[:len(pidx)] == pidx for pidx in allowed_parent_indexes)
            ]

        if "position" in selector:
            position = selector["position"]
            if position != "last" and (type(position) is not int or position < 1):
                raise ValueError("position must be a positive one-based index or 'last'")
            siblings = {}
            for context in contexts:
                siblings.setdefault((context.path, context.indexes[:-1]), []).append(context)
            contexts = [
                item
                for group in siblings.values()
                for item in ([group[-1]] if position == "last" else group[position - 1:position])
            ]

        where = selector.get("where")
        if apply_where and where:
            contexts = [item for item in contexts if self.evaluate_condition(where, item, values)]
        return contexts

    def _contexts_for_path(self, path, values):
        missing = object()
        raw = values.get(path, missing)
        descendants = [value for key, value in values.items() if key.startswith(path + "/")]

        if raw is missing:
            if not descendants:
                return []
            index_candidates = set()
            for value in descendants:
                index_candidates.update(self._leaf_indexes(value))
            indexes = sorted(index_candidates) or [()]
        elif raw is None:
            if not descendants:
                return []
            index_candidates = set()
            for value in descendants:
                index_candidates.update(self._leaf_indexes(value))
            indexes = sorted(index_candidates) or [()]
        else:
            indexes = list(self._leaf_indexes(raw))

        return [RuleContext(path, indexes_, self._context_fields(path, indexes_, values)) for indexes_ in indexes]

    @classmethod
    def _leaf_indexes(cls, value, prefix=()):
        if isinstance(value, list):
            result = []
            for index, item in enumerate(value):
                if isinstance(item, list):
                    result.extend(cls._leaf_indexes(item, prefix + (index,)))
                else:
                    result.append(prefix + (index,))
            return tuple(result)
        return (prefix,)

    @classmethod
    def _has_present_leaf(cls, value):
        if isinstance(value, list):
            return any(cls._has_present_leaf(item) for item in value)
        return value is not None

    @staticmethod
    def _value_at(value, indexes):
        current = value
        for index in indexes:
            if not isinstance(current, list):
                return current
            if index >= len(current):
                return None
            current = current[index]
        return current

    def _context_fields(self, path, indexes, values):
        fields = {}
        if path in values:
            fields["#text"] = self._value_at(values[path], indexes)
        prefix = path + "/"
        for absolute_path, value in values.items():
            if not absolute_path.startswith(prefix):
                continue
            relative_path = absolute_path[len(prefix):]
            fields[relative_path] = self._value_at(value, indexes)
        return fields

    def evaluate_condition(self, condition, context, values):
        if "all" in condition:
            return all(self.evaluate_condition(item, context, values) for item in condition["all"])
        if "any" in condition:
            return any(self.evaluate_condition(item, context, values) for item in condition["any"])
        if "not" in condition:
            return not self.evaluate_condition(condition["not"], context, values)
        if "count" in condition:
            count = self._selected_child_count(condition["count"], context, values)
            return self.c(count, condition["operator"], condition["value"])
        left = self._field_value(condition["field"], context, values)
        if "position" in condition:
            left = self._at_position(left, condition["position"])
        return self.c(left, condition["operator"], condition.get("value"))

    @staticmethod
    def _at_position(value, position):
        if position != "last" and (type(position) is not int or position < 1):
            raise ValueError("position must be a positive one-based index or 'last'")
        if not isinstance(value, list):
            return value if position == 1 or position == "last" else None
        if not value:
            return None
        return value[-1] if position == "last" else (value[position - 1] if position <= len(value) else None)

    @classmethod
    def _context_field_value(cls, field, context):
        if context is not None and field in context.fields:
            return context.fields.get(field)
        if context is not None and context.path:
            prefix = context.path + "/"
            if field.startswith(prefix) and field[len(prefix):] in context.fields:
                return context.fields.get(field[len(prefix):])
        return None

    @classmethod
    def _field_value(cls, field, context, values):
        val = cls._context_field_value(field, context)
        if val is not None or (context is not None and field in context.fields):
            return val
        return values.get(field)

    def _target_value(self, target, context, values):
        if isinstance(target, Mapping):
            value = self._field_value(target["field"], context, values)
            return self._at_position(value, target["position"]) if "position" in target else value
        return self._field_value(target, context, values)

    def _operand_value(self, operand, context, values):
        if isinstance(operand, Mapping):
            if "field" not in operand:
                raise ValueError("operand requires field")
            if "selector" in operand:
                selected = self._select_contexts(operand["selector"], values)
                if len(selected) != 1:
                    raise ValueError("comparison operand requires exactly one selected owner")
                value = self._context_field_value(operand["field"], selected[0])
                if value is None:
                    raise ValueError("selected comparison field is missing")
                return value
            return self._field_value(operand["field"], context, values)
        if context is not None and operand in context.fields:
            return context.fields.get(operand)
        return values.get(operand)

    def _assertion_passes(self, assertion, context, values):
        kind = assertion.get("kind")
        if kind == "selection_cardinality":
            count = self._selected_child_count(assertion["selector"], context, values)
            minimum = assertion.get("min_occurs", 0)
            maximum = assertion.get("max_occurs")
            return minimum <= count and (maximum is None or count <= maximum)
        if kind in {"cardinality", "presence", "fixed_value"}:
            value = self._target_value(assertion["target"], context, values)
            count = len(value) if isinstance(value, list) else int(value is not None)
            if kind == "cardinality":
                minimum = assertion.get("min_occurs", 0)
                maximum = assertion.get("max_occurs")
                return minimum <= count and (maximum is None or count <= maximum)
            if kind == "presence":
                required = assertion.get("state") == "REQUIRED"
                return (count > 0) == required
            return value == assertion.get("value")

        if kind == "comparison":
            left = self._operand_value(assertion["left"], context, values)
            if "right" in assertion:
                right = self._operand_value(assertion["right"], context, values)
            else:
                right = assertion.get("right_value")
            return self._compare(left, assertion["operator"], right, assertion.get("value_type"))

        if kind == "conditional_presence":
            if not self.evaluate_condition(assertion["condition"], context, values):
                return True
            present = self._target_value(assertion["target"], context, values) is not None
            forbidden = assertion["state"] == "FORBIDDEN"
            return present != forbidden

        if kind == "conditional_fixed_value":
            if not self.evaluate_condition(assertion["condition"], context, values):
                return True
            target = self._target_value(assertion["target"], context, values)
            return target is not None and target == assertion.get("value")

        if kind == "condition":
            return self.evaluate_condition(assertion["condition"], context, values)

        raise ValueError(f"Unsupported for_each assertion: {kind}")

    def _selected_child_count(self, selector, context, values):
        children = [
            child for child in self._select_contexts(selector, values)
            if any(self._has_present_leaf(value) for value in child.fields.values())
        ]
        if context is None:
            return len(children)
        prefix = context.path + "/"
        scalar_parent = len(self._contexts_for_path(context.path, values)) == 1
        return sum(child.path.startswith(prefix) and (scalar_parent or child.indexes[:len(context.indexes)] == context.indexes) for child in children)

    def agg(self, aggregate, values):
        selected_items = self.select(aggregate["selector"], values)
        decimals = [
            Decimal(str(item[aggregate["value_field"]]))
            for item in selected_items
        ]
        if aggregate["aggregation"] == "SUM":
            return sum(decimals, Decimal())
        if len(decimals) == 1:
            return decimals[0]
        raise ValueError()

    @staticmethod
    def _compare(left, operator, right, value_type=None):
        if value_type == "DATETIME":
            left = datetime.fromisoformat(left)
            right = datetime.fromisoformat(right)
            if (left.tzinfo is None) != (right.tzinfo is None):
                raise ValueError("Cannot compare zoned and unzoned date-times")
        elif value_type is not None:
            raise ValueError("Unknown comparison value_type")
        return StructuredRuleEvaluator.c(left, operator, right)

    @staticmethod
    def c(left, operator, right):
        if operator == "EQ":
            return left == right
        if operator == "NE":
            return left != right
        if operator == "GT":
            return left > right
        if operator == "GE":
            return left >= right
        if operator == "LT":
            return left < right
        if operator == "LE":
            return left <= right
        if operator in {"IN", "NOT_IN"}:
            if not isinstance(right, (list, tuple, set, frozenset)):
                raise TypeError(f"{operator} requires a collection RHS")
            contained = left in right
            return contained if operator == "IN" else not contained
        raise ValueError(operator)

    @staticmethod
    def out(rule, status, message):
        return RuleEvaluation(
            rule.get("rule_id"),
            status,
            message,
            tuple(rule.get("source_refs", ())),
        )
