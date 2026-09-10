import json
from pathlib import Path
from typing import Any

from eaeu_xml.core.errors import ProcessPackageFormatError, ProcessPackagePathError, ProcessPackageValidationError
from eaeu_xml.process_packages.models import (
    EmbeddedStructuresDefinition, FieldInputPolicyDefinition, UiInputPolicyDefinition, MessageDefinition, MessageRules, OperationDefinition, ParticipantDefinition, ProcedureDefinition, ProcessDefinition,
    ProcessPackage, SourceReference, StructureDefinition, TransactionDefinition,
    VersionProfile, StructureFieldDefinition, DatatypeFacets,
    StructureVersionSelection,
)
from eaeu_xml.process_packages.validator import ProcessPackageValidator


def _refs(values: list[dict[str, Any]] | None) -> tuple[SourceReference, ...]:
    return tuple(SourceReference(**item) for item in (values or []))


def _embedded_structures(value: Any) -> EmbeddedStructuresDefinition | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ProcessPackageFormatError(
            code="INVALID_EMBEDDED_STRUCTURES_FORMAT",
            message="embedded_structures должен быть объектом.",
        )
    structures = value.get("structures", ())
    if not isinstance(structures, list):
        raise ProcessPackageFormatError(
            code="INVALID_EMBEDDED_STRUCTURES_FORMAT",
            message="embedded_structures.structures должен быть массивом строк.",
        )
    return EmbeddedStructuresDefinition(selection=value.get("selection", ""), structures=tuple(structures))


def _occurs(value: Any) -> int | None | Any:
    """Preserve absent/unbounded cardinality and normalize JSON-compatible numerals."""
    if value == "*":
        return None
    if isinstance(value, str) and value.isdecimal():
        return int(value)
    return value


def _message_has_field(message: MessageDefinition | None, field_path: str,
                       structures: dict[tuple[str, str], StructureDefinition]) -> bool:
    """Return whether a root or embedded message structure defines field_path."""
    if message is None:
        return False

    for (structure_id, _version), structure in structures.items():
        if structure_id not in message.structure_ids:
            continue
        for field in structure.fields:
            if field.path == field_path:
                return True
    return False


class ProcessPackageLoader:
    REQUIRED_FILES = ("process.yaml", "procedures.yaml", "transactions.yaml", "messages.yaml")

    @classmethod
    def load(cls, package_path: Path, *, shared_structures=None) -> ProcessPackage:
        if not isinstance(package_path, Path):
            raise ProcessPackagePathError(code="EXPLICIT_PATH_REQUIRED", message="ProcessPackageLoader требует явно переданный pathlib.Path.")
        path = package_path.expanduser().resolve()
        if not path.is_dir():
            raise ProcessPackagePathError(code="PACKAGE_NOT_FOUND", message=f"Process package не найден: {path}")
        for name in cls.REQUIRED_FILES:
            if not (path / name).is_file():
                raise ProcessPackagePathError(code="REQUIRED_MANIFEST_MISSING", message=f"Обязательный manifest отсутствует: {name}")
        process_data = cls._read(path / "process.yaml")
        process = ProcessDefinition(
            process_code=process_data.get("process_code", ""), name=process_data.get("name"),
            active_profile=process_data.get("active_profile", ""), status=process_data.get("status", ""),
            source_refs=_refs(process_data.get("source_refs")), normative_document_number=process_data.get("normative_document_number"),
        )
        procedures = {item["procedure_code"]: ProcedureDefinition(
            procedure_code=item["procedure_code"], name=item.get("name", ""),
            source_refs=_refs(item.get("source_refs")), status=item.get("status", "CONFIRMED"),
        ) for item in cls._read(path / "procedures.yaml").get("procedures", [])}
        operations_path = path / "operations.yaml"
        operations_data = cls._read(operations_path) if operations_path.is_file() else {"operations": []}
        operations = {item["operation_code"]: OperationDefinition(
            operation_code=item["operation_code"], name=item.get("name", ""),
            participant_role=item.get("participant_role"), source_refs=_refs(item.get("source_refs")),
            status=item.get("status", "CONFIRMED"),
        ) for item in operations_data.get("operations", [])}
        participants_path = path / "participants.yaml"
        participants_data = cls._read(participants_path) if participants_path.is_file() else {"participants": []}
        participants = {item["participant_code"]: ParticipantDefinition(
            participant_code=item["participant_code"], name=item.get("name", ""),
            logical_address_space=item.get("logical_address_space", "CP"),
            segment_policy=item.get("segment_policy", "MEMBER_STATE_ISO_ALPHA2"),
            fixed_segment=item.get("fixed_segment"), test_segment=item.get("test_segment"),
            source_refs=_refs(item.get("source_refs")), status=item.get("status", "CONFIRMED"),
        ) for item in participants_data.get("participants", [])}
        transactions = {item["transaction_code"]: TransactionDefinition(
            transaction_code=item["transaction_code"], name=item.get("name", ""), procedure_code=item.get("procedure_code", ""),
            pattern=item.get("pattern"), initiating_role=item.get("initiating_role"), responding_role=item.get("responding_role"),
            initiating_operation=item.get("initiating_operation"), responding_operation=item.get("responding_operation"),
            initiating_participant=item.get("initiating_participant"), responding_participant=item.get("responding_participant"),
            initiating_message=item.get("initiating_message"), response_messages=tuple(item.get("response_messages", [])),
            timeouts=item.get("timeouts", {}), retry_count=item.get("retry_count"), authorization=item.get("authorization", {}),
            signature_requirements=item.get("signature_requirements", {}), guaranteed_delivery=item.get("guaranteed_delivery"),
            source_refs=_refs(item.get("source_refs")), status=item.get("status", "NEEDS_VERIFICATION"),
        ) for item in cls._read(path / "transactions.yaml").get("transactions", [])}
        rules_audit_path = path / "message_rules_audit.yaml"
        rules_audit = (cls._read(rules_audit_path).get("messages", {})
                       if rules_audit_path.is_file() else {})
        messages = {}
        messages_data = cls._read(path / "messages.yaml").get("messages", [])
        for item in messages_data:
            message_code = item["message_code"]
            audit_entry = rules_audit.get(message_code, {})
            rules_status = (
                audit_entry.get("status")
                or item.get("message_rules_status", "NEEDS_VERIFICATION")
            )
            rules_source_refs = (
                audit_entry.get("source_refs")
                or item.get("message_rules_source_refs")
            )
            messages[message_code] = MessageDefinition(
                message_code=message_code, name=item.get("name", ""), structure_id=item.get("structure_id"),
                embedded_structures=_embedded_structures(item.get("embedded_structures")),
                structure_version=item.get("structure_version"),
                structure_version_source=item.get("structure_version_source"), direction=item.get("direction"), role=item.get("role"),
                purpose=item.get("purpose"), context=tuple(item.get("context", [])),
                source_refs=_refs(item.get("source_refs")), status=item.get("status", "NEEDS_VERIFICATION"),
                message_rules_status=rules_status,
                message_rules_source_refs=_refs(rules_source_refs),
            )
        profile_path = path / "version_profiles" / f"{process.active_profile}.yaml"
        if not profile_path.is_file():
            raise ProcessPackagePathError(code="ACTIVE_PROFILE_MISSING", message=f"Active profile отсутствует: {profile_path.name}")
        profile_data = cls._read(profile_path)
        profile_structures = {}
        for structure_id, selection in profile_data.get("structures", {}).items():
            if isinstance(selection, dict):
                active_version = selection.get("active_version")
                source = selection.get("source")
            else:
                active_version = selection
                source = None
            profile_structures[structure_id] = StructureVersionSelection(active_version=active_version, source=source)
        profile = VersionProfile(process.active_profile, profile_data.get("process_version"), profile_data.get("models", {}), profile_structures)
        local_structures = cls.load_structures(path / "structures")
        shared_structures = dict(shared_structures or {})
        structures = dict(local_structures)
        for key, definition in shared_structures.items():
            selection = profile.structures.get(key[0])
            if selection is None:
                continue
            if key in local_structures and selection and selection.source is None:
                raise ProcessPackageValidationError(
                    code="AMBIGUOUS_STRUCTURE_SOURCE",
                    message=f"Структура {key[0]} версии {key[1]} существует local и shared; укажите source в version profile.",
                )
            if key not in local_structures or (selection and selection.source == "shared"):
                structures[key] = definition
        for structure_id, selection in profile.structures.items():
            if selection.source not in {None, "local", "shared"}:
                raise ProcessPackageValidationError(code="UNKNOWN_STRUCTURE_SOURCE", message=f"Неизвестный source структуры {structure_id}: {selection.source}.")
            if selection.active_version is None:
                continue
            key = (structure_id, selection.active_version)
            if selection.source == "local" and key not in local_structures:
                raise ProcessPackageValidationError(code="LOCAL_STRUCTURE_NOT_FOUND", message=f"Local структура {structure_id} версии {selection.active_version} не найдена.")
            if selection.source == "shared" and key not in shared_structures:
                raise ProcessPackageValidationError(code="SHARED_STRUCTURE_NOT_FOUND", message=f"Shared структура {structure_id} версии {selection.active_version} не найдена.")
        rules = {}
        for file in sorted((path / "message_rules").glob("*.yaml")):
            item = cls._read(file); code = item.get("message_code", file.stem)
            rules[code] = MessageRules(
                message_code=code, structure_id=item.get("structure_id"), fixed_values=item.get("fixed_values", {}),
                applies_to_structure=item.get("applies_to_structure"),
                field_usage=item.get("field_usage", {}), business_rules=tuple(item.get("business_rules", [])), structured_rules=tuple(item.get("structured_rules", [])),
                correlation_rules=tuple(item.get("correlation_rules", [])), classifier_refs=tuple(item.get("classifier_refs", [])),
                source_text=item.get("source_text"), normalized_field_reference=item.get("normalized_field_reference"),
                source_refs=_refs(item.get("source_refs")),
            )
        input_policies = {}
        policy_path = path / "field_input_policies.yaml"
        if policy_path.is_file():
            for item in cls._read(policy_path).get("field_input_policies", []):
                message_codes = item.get("message_codes", [item.get("message_code")])
                if message_codes == ["*"]:
                    message_codes = sorted(messages)
                for message_code in message_codes:
                    message = messages.get(message_code)
                    if not _message_has_field(message, item["field_path"], structures):
                        continue
                    definition = FieldInputPolicyDefinition(
                        message_code=message_code, field_path=item["field_path"],
                        input_policy=item["input_policy"], value_source=item.get("value_source", "UNKNOWN"),
                        help_text=item.get("help_text"), example_value=item.get("example_value"),
                        condition_description=item.get("condition_description"), condition_ref=item.get("condition_ref"),
                        generated_value=item.get("generated_value"), allowed_values=tuple(item.get("allowed_values", [])),
                        correlation_source_path=item.get("correlation_source_path"),correlation_source_message=item.get("correlation_source_message"),
                        source_refs=_refs(item.get("source_refs")),
                        status=item.get("status", "CONFIRMED"),
                    )
                    input_policies[(definition.message_code, definition.field_path)] = definition
        ui_input_policies = {}
        ui_policy_path = path / "ui_input_policies.yaml"
        if ui_policy_path.is_file():
            for item in cls._read(ui_policy_path).get("ui_input_policies", []):
                message_codes = item.get("message_codes", [item.get("message_code")])
                if message_codes == ["*"]:
                    message_codes = sorted(messages)
                for message_code in message_codes:
                    message = messages.get(message_code)
                    if not _message_has_field(message, item["field_path"], structures):
                        continue
                    definition = UiInputPolicyDefinition(
                        message_code=message_code, field_path=item["field_path"],
                        ui_input_policy=item["ui_input_policy"],
                        policy_origin=item.get("policy_origin", "MANUAL_OVERRIDE"),
                        reason=item.get("reason", "Explicit process UI override."),
                        source_refs=_refs(item.get("source_refs")),
                        capabilities=tuple(item.get("capabilities", [])),
                    )
                    ui_input_policies[(message_code, definition.field_path)] = definition
        package = ProcessPackage(
            path=path, process=process, procedures=procedures, operations=operations, participants=participants, transactions=transactions, messages=messages,
            structures=structures, rules=rules, input_policies=input_policies, ui_input_policies=ui_input_policies, profile=profile,
            classifiers_available=any(item.is_file() and not item.name.startswith(".") for item in (path / "classifiers").glob("*")),
            xsd_available=any((path / "xsd").glob("*.xsd")),
        )
        ProcessPackageValidator().validate(package)
        return package

    @classmethod
    def load_structures(cls, structures_path: Path) -> dict[tuple[str, str], StructureDefinition]:
        """Parse a structure catalog using the package loader's canonical parser."""
        structures = {}
        for file in sorted(structures_path.glob("*/*.yaml")):
            item = cls._read(file)
            fields = tuple(StructureFieldDefinition(
                field_id=field["field_id"], order=int(field["order"]), depth=int(field["depth"]),
                parent=field.get("parent"), path=field.get("path", ""), official_name=field.get("official_name", ""),
                xml_name=field.get("xml_name"), namespace_prefix=field.get("namespace_prefix"), kind=field.get("kind", "ELEMENT"),
                datatype=field.get("datatype"), datatype_text=field.get("datatype_text"),
                min_occurs=_occurs(field.get("min_occurs")), max_occurs=_occurs(field.get("max_occurs")),
                description=field.get("description"), constraints=field.get("constraints"), classifier_ref=field.get("classifier_ref"),
                identifier=field.get("identifier"), facets=DatatypeFacets(**field["facets"]) if field.get("facets") else None,
                source_refs=_refs(field.get("source_refs")), status=field.get("status", "CONFIRMED"),
                interpretation_status=field.get("interpretation_status", "VERIFIED"), reason_code=field.get("reason_code"),
            ) for field in item.get("fields", []))
            definition = StructureDefinition(
                structure_id=item.get("structure_id", file.parent.name), version=str(item.get("version", file.stem)),
                namespace=item.get("namespace"), root_element=item.get("root_element"), xsd_file=item.get("xsd_file"),
                official_name=item.get("official_name"), imported_namespaces=item.get("imported_namespaces", {}),
                field_table_reference=item.get("field_table_reference", {}),
                fields=fields, expected_normative_rows=int(item.get("expected_normative_rows", len(fields))),
                imported_normative_rows=int(item.get("imported_normative_rows", len(fields))),
                excluded_rows=tuple(item.get("excluded_rows", [])),
                source_refs=_refs(item.get("source_refs")), status=item.get("status", "NEEDS_VERIFICATION"),
            )
            structures[(definition.structure_id, definition.version)] = definition
        return structures

    @staticmethod
    def _read(path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ProcessPackageFormatError(code="MANIFEST_INVALID", message=f"{path.name}: требуется JSON-compatible YAML 1.2 manifest.") from error
        if not isinstance(value, dict):
            raise ProcessPackageFormatError(code="MANIFEST_OBJECT_REQUIRED", message=f"{path.name}: корнем manifest должен быть object/mapping.")
        return value
