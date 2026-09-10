from dataclasses import dataclass
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
            selected_items = self.select(rule["selector"], values)
            count = len(selected_items)
            minimum = rule.get("min_occurs", 0)
            maximum = rule.get("max_occurs")
            passed = minimum <= count and (maximum is None or count <= maximum)
            status = RuleStatus.PASS if passed else RuleStatus.FAIL
            return self.out(rule, status, "Selection cardinality evaluated.")

        if kind == "conditional_presence":
            scope_items = self.select(rule["scope"], values, True)
            condition = rule["condition"]
            target = rule["target"]
            forbidden = rule["state"] == "FORBIDDEN"

            for item in scope_items:
                condition_matches = self.c(
                    item.get(condition["field"]),
                    condition["operator"],
                    condition.get("value"),
                )
                target_is_present = item.get(target["field"]) is not None
                if condition_matches and target_is_present == forbidden:
                    return self.out(rule, RuleStatus.FAIL, "Conditional presence failed.")

            return self.out(rule, RuleStatus.PASS, "Conditional presence evaluated.")

        if kind == "aggregate_comparison":
            try:
                left_value = self.agg(rule["left"], values)
                right_value = self.agg(rule["right"], values)
                passed = self.c(left_value, rule["operator"], right_value)
            except (InvalidOperation, ValueError, TypeError):
                passed = False

            status = RuleStatus.PASS if passed else RuleStatus.FAIL
            return self.out(rule, status, "Aggregate comparison evaluated.")

        if kind == "comparison":
            try:
                left_value = values.get(rule["left"])
                right_key = rule.get("right")
                right_value = values.get(right_key, rule.get("right_value"))
                passed = self.c(left_value, rule["operator"], right_value)
            except (KeyError, TypeError, ValueError):
                passed = False

            status = RuleStatus.PASS if passed else RuleStatus.FAIL
            return self.out(rule, status, "Comparison evaluated.")

        return self.out(rule, RuleStatus.UNSUPPORTED_RULE, "Unsupported structured rule.")

    def select(self, selector, values, all=False):
        collection_path = selector["collection"]
        collection_value = values.get(collection_path)
        count = (
            len(collection_value)
            if isinstance(collection_value, list)
            else int(collection_value is not None)
        )
        where = selector.get("where")
        selected_items = []

        for index in range(count):
            if not all and where:
                condition_path = collection_path + "/" + where["field"]
                condition_value = values.get(condition_path)
                if isinstance(condition_value, list):
                    condition_value = condition_value[index]
                if not self.c(condition_value, where["operator"], where.get("value")):
                    continue

            item = {}
            for path, value in values.items():
                if not path.startswith(collection_path + "/"):
                    continue
                field_name = path[len(collection_path) + 1:]
                if isinstance(value, list) and index < len(value):
                    item[field_name] = value[index]
                else:
                    item[field_name] = value
            selected_items.append(item)

        return selected_items

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
        raise ValueError(operator)

    @staticmethod
    def out(rule, status, message):
        return RuleEvaluation(
            rule.get("rule_id"),
            status,
            message,
            tuple(rule.get("source_refs", ())),
        )
