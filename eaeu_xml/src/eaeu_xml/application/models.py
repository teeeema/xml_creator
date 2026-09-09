from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class ProcessView:
    process_code: str
    name: str | None
    version: str | None
    status: str
    path: Path
    normative_document_number: int | None = None


@dataclass(frozen=True)
class TransactionView:
    transaction_code: str
    name: str
    procedure_code: str
    pattern: str | None
    initiating_message: str | None
    response_messages: tuple[str, ...]
    status: str


@dataclass(frozen=True)
class MessageView:
    message_code: str
    name: str
    direction: str
    structure_id: str | None
    active_version: str | None
    generation_status: str
    blocking_reason: str | None = None
    message_rules_status: str = "NEEDS_VERIFICATION"
    message_rules_status_display: str = "Статус правил требует проверки"


@dataclass(frozen=True)
class ProcessIssueView:
    code: str
    severity: str
    category: str
    title: str
    description: str
    affected_messages: tuple[str, ...] = ()
    affected_structures: tuple[str, ...] = ()
    referenced_fields: tuple[str, ...] = ()
    source_display: tuple[str, ...] = ()
    suggested_action: str | None = None
    blocks_generation: bool = False
    blocks_test_generation: bool = False
    blocks_strict_generation: bool = False


@dataclass(frozen=True)
class FieldView:
    path: str
    xml_name: str | None
    display_name: str
    description: str | None
    kind: str
    datatype: str | None
    required: bool
    min_occurs: int | None
    max_occurs: int | None
    is_attribute: bool
    repeatable: bool
    allowed_values: tuple[Any, ...] = ()
    fixed_value: Any = None
    default_value: Any = None
    classifier: str | None = None
    editable: bool = True
    visibility: str = "VISIBLE"
    validation_hints: tuple[str, ...] = ()
    status: str = "CONFIRMED"
    source_refs: tuple[str, ...] = ()
    children: tuple["FieldView", ...] = ()
    official_name: str | None = None
    xml_qname: str | None = None
    example_value: Any = None
    cardinality_display: str | None = None
    input_policy: str = "UNRESOLVED_INPUT_POLICY"
    value_source: str = "UNKNOWN"
    help_text: str | None = None
    condition_description: str | None = None
    condition_ref: str | None = None
    policy_reason: str | None = None
    normative_input_policy: str = "UNRESOLVED_INPUT_POLICY"
    ui_input_policy: str = "UNRESOLVED_UI_POLICY"
    ui_policy_origin: str = "PROJECT_UI_DEFAULT"
    ui_policy_reason: str | None = None
    example_origin: str = "UNAVAILABLE"
    no_example_reason: str | None = None
    unresolved_ui_reason: str | None = None
    conditional_machine_evaluable: bool = False
    condition_result: str | None = None
    manual_edit_allowed: bool = False
    show_today_button: bool = False
    show_date_picker: bool = False
    show_now_button: bool = False
    show_timezone_picker: bool = False
    show_identifier_generator: bool = False
    supports_file_picker: bool = False
    assisted_input_kind: str | None = None


@dataclass(frozen=True)
class MessageInputSummary:
    total_fields: int
    user_input: int
    user_select: int
    automatic: int
    read_only: int
    external_system: int
    conditional: int
    unresolved: int
    group: int
    hidden: int
    conditional_total: int = 0
    conditional_active: int = 0
    conditional_inactive: int = 0
    conditional_unknown: int = 0

    @property
    def visible_fields(self): return self.total_fields - self.hidden

    @property
    def manual_fields(self): return self.user_input + self.user_select

    @property
    def automatic_fields(self): return self.automatic + self.read_only

    @property
    def classifier_fields(self): return self.user_select

    @property
    def conditional_fields(self): return self.conditional

    @property
    def external_system_fields(self): return self.external_system

    @property
    def unresolved_fields(self): return self.unresolved


@dataclass(frozen=True)
class FormDefinition:
    process_code: str
    transaction_code: str
    message_code: str
    structure_id: str
    active_version: str | None
    generation_status: str
    blocking_reason: str | None
    fields: tuple[FieldView, ...]


class FormDisplayMode(str, Enum):
    ALL = "ALL"
    REQUIRED = "REQUIRED"
    USER_FIELDS = "USER_FIELDS"
    ERRORS = "ERRORS"
    FILLED = "FILLED"


@dataclass(frozen=True)
class FormPresentation:
    """Presentation-only projection; the source FormDefinition stays complete."""

    mode: FormDisplayMode
    query: str
    fields: tuple[FieldView, ...]
    visible_paths: tuple[str, ...]
    matching_paths: tuple[str, ...]
    empty_message: str | None = None
    conditionally_hidden_search_paths: tuple[str, ...] = ()
    condition_evaluations: tuple["ConditionEvaluation", ...] = ()


class ConditionResult(str, Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ConditionalFieldRule:
    target_field_path: str
    condition_type: str
    source_field_path: str
    operator: str
    expected_value: Any = None
    values: tuple[Any, ...] = ()
    effect: str = "SHOW"
    source_refs: tuple[str, ...] = ()
    evaluation_status: str = "MACHINE_EVALUABLE"
    original_description: str | None = None
    rule_id: str | None = None


@dataclass(frozen=True)
class ConditionEvaluation:
    rule: ConditionalFieldRule
    result: ConditionResult


@dataclass(frozen=True)
class ConditionProjection:
    fields: tuple[FieldView, ...]
    evaluations: tuple[ConditionEvaluation, ...]
    hidden_paths: tuple[str, ...]


@dataclass(frozen=True)
class IssueView:
    code: str
    field_path: str
    message: str
    severity: str
    source_ref: str | None = None
    rule_id: str | None = None


@dataclass(frozen=True)
class ValidationView:
    is_valid: bool
    errors: tuple[IssueView, ...] = ()
    warnings: tuple[IssueView, ...] = ()
    status: str = "VALID"


@dataclass(frozen=True)
class GenerationResult:
    success: bool
    xml: str | None
    status: str
    errors: tuple[IssueView, ...] = ()
    warnings: tuple[IssueView, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GuideSourceView:
    document: str
    location: str
    table: str | None = None
    item: str | None = None
    page: int | None = None


@dataclass(frozen=True)
class FieldGuide:
    message_code: str
    path: str
    xml_name: str | None
    display_name: str
    description: str
    datatype: str | None
    xml_kind: str
    requirement: str
    cardinality: str
    repeatable: bool
    who_fills: str
    normative_input_policy: str
    ui_input_policy: str
    value_source: str
    what_to_enter: str
    example_value: Any = None
    example_label: str = "Пример"
    example_origin: str = "UNAVAILABLE"
    no_example_reason: str | None = None
    unresolved_ui_reason: str | None = None
    condition: str | None = None
    classifier: str | None = None
    classifier_dataset_available: bool = False
    sources: tuple[GuideSourceView, ...] = ()
    children: tuple["FieldGuide", ...] = ()
    automatic_condition_check: bool = False
    condition_result: str | None = None
    condition_source_field: str | None = None
    condition_operator_description: str | None = None
    condition_expected_value: Any = None
    xml_qname: str | None = None
    input_assistance: str | None = None


@dataclass(frozen=True)
class MessageUsageGuide:
    transaction_code: str
    procedure_code: str
    role: str
    initiating_participant: str | None
    responding_participant: str | None


@dataclass(frozen=True)
class ConflictGuide:
    conflict_id: str
    referenced_fields: tuple[str, ...]
    description: str
    sources: tuple[GuideSourceView, ...] = ()


@dataclass(frozen=True)
class MessageGuide:
    message_code: str
    name: str
    purpose: str
    structure_id: str
    structure_version: str | None
    version_description: str
    root_element: str | None
    usages: tuple[MessageUsageGuide, ...]
    fields: tuple[FieldGuide, ...]
    total_fields: int
    user_input: int
    user_select: int
    automatic: int
    classifier_fields: int
    conditional: int
    external_system: int
    unresolved: int
    body_example: str | None
    body_example_status: str
    conflicts: tuple[ConflictGuide, ...] = ()
    sources: tuple[GuideSourceView, ...] = ()
    message_rules_status: str = "NEEDS_VERIFICATION"
    message_rules_status_display: str = "Статус правил требует проверки"
    message_rules_sources: tuple[GuideSourceView, ...] = ()


@dataclass(frozen=True)
class TransactionGuide:
    transaction_code: str
    procedure_code: str
    pattern: str | None
    initiating_message: str | None
    response_messages: tuple[str, ...]
    initiating_participant: str | None
    responding_participant: str | None
    initiating_to: str | None = None
    initiating_reply_to: str | None = None
    initiating_action: str | None = None
    response_to: str | None = None
    response_reply_to: str | None = None


@dataclass(frozen=True)
class ProcessGuide:
    process_code: str
    name: str
    version: str | None
    procedure_count: int
    transaction_count: int
    message_count: int
    transactions: tuple[TransactionGuide, ...]
    messages: tuple[MessageGuide, ...]


@dataclass(frozen=True)
class GuideSearchHit:
    message_code: str
    field_path: str | None
    title: str
    excerpt: str
