from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


FIELD_INPUT_POLICIES = {
    "USER_INPUT", "USER_SELECT", "AUTO_GENERATED", "AUTO_FIXED", "AUTO_DATETIME",
    "CORRELATION", "CLASSIFIER", "CONDITIONAL", "EXTERNAL_SYSTEM",
    "INTEGRATION_PLATFORM", "UNRESOLVED_INPUT_POLICY", "STRUCTURAL_CONTAINER",
}

VALUE_SOURCES = {
    "USER", "PROCESS_METADATA", "MESSAGE_METADATA", "GENERATED_UUID", "CURRENT_DATETIME",
    "PREVIOUS_BODY", "CLASSIFIER_DATASET", "EXTERNAL_INFORMATION_SYSTEM",
    "INTEGRATION_PLATFORM", "UNKNOWN", "NOT_APPLICABLE",
}

UI_INPUT_POLICIES = {
    "USER_INPUT", "USER_SELECT", "AUTO", "READ_ONLY", "EXTERNAL_SYSTEM",
    "CONDITIONAL", "HIDDEN", "UNRESOLVED_UI_POLICY", "GROUP",
}

UI_POLICY_ORIGINS = {"NORMATIVE", "DERIVED_FROM_MODEL", "PROJECT_UI_DEFAULT", "MANUAL_OVERRIDE"}
UI_PRESENTATION_CAPABILITIES = {"GENERATE_IDENTIFIER"}
MESSAGE_RULES_STATUSES = {
    "HAS_SEPARATE_RULE_TABLE", "NO_SEPARATE_RULE_TABLE",
    "NEEDS_VERIFICATION", "NORMATIVE_CONFLICT",
}


@dataclass(frozen=True)
class SourceReference:
    source_id: str
    document: str
    location: str
    status: str = "CONFIRMED"
    section: str | None = None
    table: str | None = None
    item: str | None = None
    page: int | None = None
    version_context: str | None = None


@dataclass(frozen=True)
class ProcessDefinition:
    process_code: str
    name: str | None
    active_profile: str
    status: str
    source_refs: tuple[SourceReference, ...] = ()
    normative_document_number: int | None = None


@dataclass(frozen=True)
class ProcedureDefinition:
    procedure_code: str
    name: str
    source_refs: tuple[SourceReference, ...] = ()
    status: str = "CONFIRMED"


@dataclass(frozen=True)
class OperationDefinition:
    operation_code: str
    name: str
    participant_role: str | None
    source_refs: tuple[SourceReference, ...] = ()
    status: str = "CONFIRMED"


@dataclass(frozen=True)
class ParticipantDefinition:
    participant_code: str
    name: str
    logical_address_space: str
    segment_policy: str
    fixed_segment: str | None = None
    test_segment: str | None = None
    source_refs: tuple[SourceReference, ...] = ()
    status: str = "CONFIRMED"


@dataclass(frozen=True)
class TransactionDefinition:
    transaction_code: str
    name: str
    procedure_code: str
    pattern: str | None
    initiating_role: str | None
    responding_role: str | None
    initiating_operation: str | None
    responding_operation: str | None
    initiating_participant: str | None
    responding_participant: str | None
    initiating_message: str | None
    response_messages: tuple[str, ...] = ()
    timeouts: Mapping[str, Any] = field(default_factory=dict)
    retry_count: int | None = None
    authorization: Mapping[str, Any] = field(default_factory=dict)
    signature_requirements: Mapping[str, Any] = field(default_factory=dict)
    guaranteed_delivery: bool | None = None
    source_refs: tuple[SourceReference, ...] = ()
    status: str = "NEEDS_VERIFICATION"


@dataclass(frozen=True)
class MessageDefinition:
    message_code: str
    name: str
    structure_id: str | None
    structure_version: str | None = None
    structure_version_source: str | None = None
    direction: str | None = None
    role: str | None = None
    purpose: str | None = None
    context: tuple[str, ...] = ()
    source_refs: tuple[SourceReference, ...] = ()
    status: str = "NEEDS_VERIFICATION"
    message_rules_status: str = "NEEDS_VERIFICATION"
    message_rules_source_refs: tuple[SourceReference, ...] = ()


@dataclass(frozen=True)
class DatatypeFacets:
    pattern: str | None = None
    min_length: int | None = None
    max_length: int | None = None
    enum: tuple[str, ...] = ()
    total_digits: int | None = None
    fraction_digits: int | None = None
    min_value: str | None = None
    max_value: str | None = None
    default_value: str | int | bool | None = None


@dataclass(frozen=True)
class StructureFieldDefinition:
    field_id: str
    order: int
    depth: int
    parent: str | None
    path: str
    official_name: str
    xml_name: str | None
    namespace_prefix: str | None
    kind: str
    datatype: str | None
    datatype_text: str | None
    min_occurs: int | None
    max_occurs: int | None
    description: str | None = None
    constraints: str | None = None
    classifier_ref: str | None = None
    identifier: str | None = None
    facets: DatatypeFacets | None = None
    source_refs: tuple[SourceReference, ...] = ()
    status: str = "CONFIRMED"
    interpretation_status: str = "VERIFIED"
    reason_code: str | None = None


@dataclass(frozen=True)
class StructureDefinition:
    structure_id: str
    version: str
    namespace: str | None
    root_element: str | None
    xsd_file: str | None
    official_name: str | None = None
    imported_namespaces: Mapping[str, str] = field(default_factory=dict)
    field_table_reference: Mapping[str, Any] = field(default_factory=dict)
    fields: tuple[StructureFieldDefinition, ...] = ()
    expected_normative_rows: int = 0
    imported_normative_rows: int = 0
    excluded_rows: tuple[Mapping[str, Any], ...] = ()
    source_refs: tuple[SourceReference, ...] = ()
    status: str = "NEEDS_VERIFICATION"


@dataclass(frozen=True)
class MessageRules:
    message_code: str
    structure_id: str | None
    fixed_values: Mapping[str, Any] = field(default_factory=dict)
    field_usage: Mapping[str, str] = field(default_factory=dict)
    business_rules: tuple[Mapping[str, Any], ...] = ()
    structured_rules: tuple[Mapping[str, Any], ...] = ()
    correlation_rules: tuple[Mapping[str, Any], ...] = ()
    classifier_refs: tuple[str, ...] = ()
    source_text: str | None = None
    normalized_field_reference: str | None = None
    source_refs: tuple[SourceReference, ...] = ()


@dataclass(frozen=True)
class FieldInputPolicyDefinition:
    message_code: str
    field_path: str
    input_policy: str
    value_source: str
    help_text: str | None = None
    example_value: Any = None
    condition_description: str | None = None
    condition_ref: str | None = None
    generated_value: str | None = None
    correlation_source_path: str | None = None
    correlation_source_message: str | None = None
    allowed_values: tuple[Any, ...] = ()
    source_refs: tuple[SourceReference, ...] = ()
    status: str = "CONFIRMED"


@dataclass(frozen=True)
class UiInputPolicyDefinition:
    message_code: str
    field_path: str
    ui_input_policy: str
    policy_origin: str
    reason: str
    source_refs: tuple[SourceReference, ...] = ()
    capabilities: tuple[str, ...] = ()


@dataclass(frozen=True)
class StructureVersionSelection:
    active_version: str | None
    source: str | None = None


@dataclass(frozen=True)
class VersionProfile:
    profile_id: str
    process_version: str | None
    models: Mapping[str, str] = field(default_factory=dict)
    structures: Mapping[str, StructureVersionSelection] = field(default_factory=dict)


@dataclass(frozen=True)
class ProcessPackage:
    path: Path
    process: ProcessDefinition
    procedures: Mapping[str, ProcedureDefinition]
    operations: Mapping[str, OperationDefinition]
    participants: Mapping[str, ParticipantDefinition]
    transactions: Mapping[str, TransactionDefinition]
    messages: Mapping[str, MessageDefinition]
    structures: Mapping[tuple[str, str], StructureDefinition]
    rules: Mapping[str, MessageRules]
    input_policies: Mapping[tuple[str, str], FieldInputPolicyDefinition]
    ui_input_policies: Mapping[tuple[str, str], UiInputPolicyDefinition]
    profile: VersionProfile
    classifiers_available: bool
    xsd_available: bool
