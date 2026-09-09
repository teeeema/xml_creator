from dataclasses import dataclass
from typing import Any

from eaeu_xml.process_packages.models import FieldInputPolicyDefinition, MessageRules, StructureFieldDefinition


@dataclass(frozen=True)
class ResolvedFieldInputPolicy:
    input_policy: str
    value_source: str
    editable: bool
    visible: bool
    help_text: str | None = None
    example_value: Any = None
    condition_description: str | None = None
    condition_ref: str | None = None
    status: str = "CONFIRMED"
    reason: str | None = None
    source_refs: tuple[str, ...] = ()


class FieldInputPolicyResolver:
    """Resolves field origin from explicit process metadata; never from XML names."""

    READ_ONLY = {"AUTO_GENERATED", "AUTO_FIXED", "AUTO_DATETIME", "CORRELATION", "INTEGRATION_PLATFORM"}

    def resolve(self, *, message_code: str, field: StructureFieldDefinition, rules: MessageRules | None,
                explicit: FieldInputPolicyDefinition | None, has_children: bool) -> ResolvedFieldInputPolicy:
        usage = rules.field_usage.get(field.path) if rules else None
        visible = usage not in {"FORBIDDEN", "NOT_USED"}
        sources = tuple(dict.fromkeys(ref.source_id for ref in (
            *(field.source_refs or ()), *((explicit.source_refs if explicit else ())))))
        if rules and field.path in rules.fixed_values:
            return ResolvedFieldInputPolicy("AUTO_FIXED", "MESSAGE_METADATA", False, visible,
                                            example_value=rules.fixed_values[field.path], source_refs=sources)
        if explicit:
            editable = explicit.input_policy in {"USER_INPUT", "USER_SELECT", "CLASSIFIER", "CONDITIONAL"}
            return ResolvedFieldInputPolicy(
                explicit.input_policy, explicit.value_source, editable and visible, visible,
                explicit.help_text, explicit.example_value, explicit.condition_description,
                explicit.condition_ref, explicit.status, source_refs=sources,
            )
        classifier_paths = set(rules.classifier_refs if rules else ())
        if field.classifier_ref or field.path in classifier_paths:
            return ResolvedFieldInputPolicy("CLASSIFIER", "CLASSIFIER_DATASET", visible, visible,
                                            status="CONFIRMED", source_refs=sources)
        if has_children:
            return ResolvedFieldInputPolicy("STRUCTURAL_CONTAINER", "NOT_APPLICABLE", False, visible,
                                            status="CONFIRMED", source_refs=sources)
        if rules:
            for rule in rules.business_rules:
                referenced = rule.get("field_paths") or rule.get("referenced_fields") or rule.get("referenced_identifiers") or ()
                if field.path in referenced and rule.get("condition"):
                    return ResolvedFieldInputPolicy(
                        "CONDITIONAL", "UNKNOWN", visible, visible,
                        condition_description=rule.get("condition"),
                        condition_ref=rule.get("rule_id") or rule.get("conflict_id"),
                        status=rule.get("interpretation_status", "CONFIRMED"), source_refs=sources,
                    )
        return ResolvedFieldInputPolicy(
            "UNRESOLVED_INPUT_POLICY", "UNKNOWN", False, visible,
            status="UNRESOLVED_INPUT_POLICY",
            reason="Существующая модель не определяет, кто предоставляет значение; автоматизация не предполагается.",
            source_refs=sources,
        )
