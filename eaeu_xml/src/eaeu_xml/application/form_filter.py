"""Generic presentation filtering for large hierarchical message forms."""

from dataclasses import replace
from typing import Iterable, Mapping

from eaeu_xml.application.models import (
    FieldView, FormDefinition, FormDisplayMode, FormPresentation, IssueView,
)
from eaeu_xml.application.conditions import ConditionEvaluator


INTERACTIVE_POLICIES = {
    "USER_INPUT", "USER_SELECT", "EXTERNAL_SYSTEM", "CONDITIONAL",
    "UNRESOLVED_UI_POLICY",
}


class FieldVisibilityFilter:
    """Prunes only the presentation tree and always retains matching ancestors."""

    def apply(
        self,
        form: FormDefinition,
        *,
        mode: FormDisplayMode | str = FormDisplayMode.ALL,
        query: str = "",
        issues: Iterable[IssueView] = (),
        values: Mapping[str, object] | None = None,
        reveal_paths: Iterable[str] = (),
        conditional_rules=(),
        condition_evaluator: ConditionEvaluator | None = None,
        condition_results=None,
    ) -> FormPresentation:
        mode = FormDisplayMode(mode)
        needle = query.strip().casefold()
        issue_paths = {issue.field_path for issue in issues if issue.field_path}
        reveal = {path for path in reveal_paths if path}
        current_values = values or {}
        matching: list[str] = []
        evaluator=condition_evaluator or ConditionEvaluator()
        condition_projection=evaluator.project(form.fields,conditional_rules,current_values,diagnostic_paths=reveal,
                                               precomputed_results=condition_results)

        def has_value(path: str) -> bool:
            value = current_values.get(path)
            return value not in (None, "", (), [], {})

        def mode_match(field: FieldView) -> bool:
            if field.path in reveal:
                return True
            if mode is FormDisplayMode.ALL:
                return True
            if mode is FormDisplayMode.REQUIRED:
                return field.required
            if mode is FormDisplayMode.USER_FIELDS:
                return field.ui_input_policy in INTERACTIVE_POLICIES
            if mode is FormDisplayMode.ERRORS:
                return field.path in issue_paths
            if mode is FormDisplayMode.FILLED:
                return has_value(field.path)
            return False

        def search_match(field: FieldView) -> bool:
            if not needle or field.path in reveal:
                return True
            haystack = " ".join(filter(None, (
                field.display_name, field.xml_name, field.path,
                field.description, field.help_text,
            )))
            return needle in haystack.casefold()

        def visit(field: FieldView) -> tuple[FieldView, ...]:
            children = visit_list(field.children)
            if field.visibility == "HIDDEN":
                return children
            direct = mode_match(field) and search_match(field)
            if direct:
                matching.append(field.path)
            if direct or children:
                return (replace(field, children=children),)
            return ()

        def visit_list(fields):
            result = []
            for field in fields:
                result.extend(visit(field))
            return tuple(result)

        fields = visit_list(condition_projection.fields)
        visible_paths = tuple(field.path for field in self.walk(fields))
        hidden_search=[]
        if needle:
            hidden=set(condition_projection.hidden_paths)
            for field in self.walk(form.fields):
                if field.path in hidden and search_match(field):hidden_search.append(field.path)
        empty = None
        if not fields:
            if mode is FormDisplayMode.ERRORS and not issue_paths:
                empty = "Ошибок заполнения не обнаружено."
            elif needle:
                empty = "По вашему запросу реквизиты не найдены."
            else:
                empty = "В выбранном режиме реквизиты отсутствуют."
        return FormPresentation(mode, query, fields, visible_paths, tuple(matching), empty,
                                tuple(hidden_search),condition_projection.evaluations)

    @staticmethod
    def walk(fields: Iterable[FieldView]):
        for field in fields:
            yield field
            yield from FieldVisibilityFilter.walk(field.children)
