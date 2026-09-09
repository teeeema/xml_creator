from pathlib import Path
from urllib.parse import urlparse

from eaeu_xml.core.enums import TransactionPattern
from eaeu_xml.core.errors import ProcessPackageValidationError
from eaeu_xml.process_packages.models import FIELD_INPUT_POLICIES, MESSAGE_RULES_STATUSES, UI_INPUT_POLICIES, UI_POLICY_ORIGINS, UI_PRESENTATION_CAPABILITIES, VALUE_SOURCES, ProcessPackage


class ProcessPackageValidator:
    def validate(self, package: ProcessPackage) -> None:
        if not package.process.process_code or not package.process.active_profile:
            self._fail("PROCESS_REQUIRED", "process_code и active_profile обязательны.")
        if package.profile.profile_id != package.process.active_profile:
            self._fail("PROFILE_MISMATCH", "Загруженный профиль не совпадает с active_profile.")
        self._validate_sources(package)
        for participant in package.participants.values():
            if participant.logical_address_space != "CP":
                self._fail("PARTICIPANT_ADDRESS_SPACE", "Process participant должен использовать пространство CP.")
            if participant.segment_policy == "FIXED":
                if not participant.fixed_segment:
                    self._fail("PARTICIPANT_FIXED_SEGMENT_REQUIRED", f"Для {participant.participant_code} не задан fixed_segment.")
            elif participant.segment_policy == "MEMBER_STATE_ISO_ALPHA2":
                if participant.test_segment and (len(participant.test_segment) != 2 or not participant.test_segment.isupper()):
                    self._fail("PARTICIPANT_TEST_SEGMENT_INVALID", f"test_segment {participant.participant_code} должен иметь синтаксис ISO alpha-2.")
            else:
                self._fail("PARTICIPANT_SEGMENT_POLICY", f"Неизвестная segment policy: {participant.segment_policy}.")
        for transaction in package.transactions.values():
            if transaction.procedure_code not in package.procedures:
                self._fail("UNKNOWN_PROCEDURE", f"{transaction.transaction_code} ссылается на неизвестную процедуру {transaction.procedure_code}.")
            if transaction.pattern and transaction.pattern not in TransactionPattern.__members__:
                self._fail("UNKNOWN_PATTERN", f"Неизвестный универсальный шаблон {transaction.pattern}.")
            if transaction.initiating_operation and transaction.initiating_operation not in package.operations:
                self._fail("UNKNOWN_INITIATING_OPERATION", f"Неизвестная инициирующая операция {transaction.initiating_operation}.")
            if transaction.responding_operation and transaction.responding_operation not in package.operations:
                self._fail("UNKNOWN_RESPONDING_OPERATION", f"Неизвестная принимающая операция {transaction.responding_operation}.")
            if bool(transaction.initiating_participant) != bool(transaction.responding_participant):
                self._fail("TRANSACTION_PARTICIPANTS_INCOMPLETE", f"Для {transaction.transaction_code} участники должны быть заданы парой.")
            for participant_code in (transaction.initiating_participant, transaction.responding_participant):
                if participant_code and participant_code not in package.participants:
                    self._fail("UNKNOWN_TRANSACTION_PARTICIPANT", f"{transaction.transaction_code} ссылается на неизвестного участника {participant_code}.")
            if transaction.initiating_message and transaction.initiating_message not in package.messages:
                self._fail("UNKNOWN_INITIATING_MESSAGE", f"Неизвестное инициирующее сообщение {transaction.initiating_message}.")
            for message_code in transaction.response_messages:
                if message_code not in package.messages:
                    self._fail("UNKNOWN_RESPONSE_MESSAGE", f"Неизвестное ответное сообщение {message_code}.")
            if transaction.retry_count is not None and transaction.retry_count < 0:
                self._fail("INVALID_RETRY_COUNT", "retry_count не может быть отрицательным.")
        for message in package.messages.values():
            if message.structure_id is not None and not isinstance(message.structure_id, str):
                self._fail(
                    "INVALID_MESSAGE_STRUCTURE_ID",
                    f"{message.message_code}: structure_id должен быть строкой или null; "
                    f"получен {type(message.structure_id).__name__}.",
                )
            if message.message_rules_status not in MESSAGE_RULES_STATUSES:
                self._fail("UNKNOWN_MESSAGE_RULES_STATUS", f"Неизвестный статус правил {message.message_code}: {message.message_rules_status}.")
            if not message.message_rules_source_refs:
                self._fail("MESSAGE_RULES_STATUS_SOURCE_REQUIRED", f"Для статуса правил {message.message_code} отсутствуют source_refs.")
            has_rules = message.message_code in package.rules
            if message.message_rules_status == "HAS_SEPARATE_RULE_TABLE" and not has_rules:
                self._fail("MESSAGE_RULES_FILE_REQUIRED", f"Для {message.message_code} подтверждена отдельная таблица, но YAML правил отсутствует.")
            if message.message_rules_status == "NO_SEPARATE_RULE_TABLE" and has_rules:
                self._fail("UNEXPECTED_MESSAGE_RULES_FILE", f"Для {message.message_code} отдельная таблица не предусмотрена, но YAML правил существует.")
            if message.message_rules_status == "NEEDS_VERIFICATION":
                self._fail("MESSAGE_RULES_STATUS_UNVERIFIED", f"Статус отдельных правил {message.message_code} требует проверки.")
            if message.message_rules_status == "NORMATIVE_CONFLICT":
                self._fail("MESSAGE_RULES_NORMATIVE_CONFLICT", f"Статус правил {message.message_code} содержит нормативный конфликт.")
            if message.structure_id and message.structure_id not in package.profile.structures:
                self._fail("STRUCTURE_NOT_IN_PROFILE", f"Для {message.structure_id} отсутствует активная версия в профиле.")
            if message.structure_id:
                selection = package.profile.structures[message.structure_id]
                version = selection.active_version
                if version is not None and (message.structure_id, version) not in package.structures:
                    self._fail("UNKNOWN_STRUCTURE_VERSION", f"Структура {message.structure_id} версии {version} отсутствует.")
                if version is not None and message.structure_version and message.structure_version != version:
                    self._fail("MESSAGE_STRUCTURE_VERSION_MISMATCH", f"{message.message_code} ссылается не на active version {message.structure_id}.")
                if version is None and not any(key[0] == message.structure_id for key in package.structures):
                    self._fail("STRUCTURE_DEFINITION_MISSING", f"Для неразрешённой структуры {message.structure_id} отсутствуют определения.")
        for key, structure in package.structures.items():
            if structure.namespace and not urlparse(structure.namespace).scheme:
                self._fail("INVALID_NAMESPACE", f"Namespace структуры {key} не является URI.")
            self._validate_structure_fields(structure)
        for message_code, rules in package.rules.items():
            if message_code not in package.messages:
                self._fail("ORPHAN_MESSAGE_RULES", f"MessageRules ссылаются на неизвестное сообщение {message_code}.")
            message = package.messages.get(message_code)
            if rules.structure_id and message and rules.structure_id != message.structure_id:
                self._fail("RULES_STRUCTURE_MISMATCH", f"MessageRules {message_code} ссылаются на другую структуру.")
            if message and message.structure_id:
                definitions = [item for (structure_id, _), item in package.structures.items() if structure_id == message.structure_id]
                known_paths = {field.path for definition in definitions for field in definition.fields}
                for path in (*rules.field_usage, *rules.fixed_values):
                    if path not in known_paths:
                        self._fail("UNKNOWN_RULE_FIELD", f"MessageRules {message_code} ссылаются на неизвестное поле {path}.")
            for rule in (*rules.business_rules, *rules.correlation_rules):
                if not rule.get("source_refs"):
                    self._fail("RULE_SOURCE_REQUIRED", f"Детальное правило {message_code} не имеет source_refs.")
                if rule.get("interpretation_status") == "INTERNAL_NORMATIVE_CONFLICT":
                    if not rule.get("conflict_id") or not rule.get("referenced_identifiers") or not rule.get("conflict_details"):
                        self._fail("NORMATIVE_CONFLICT_METADATA_REQUIRED", f"Конфликт {rule.get('rule_id')} описан неполно.")
        for (message_code, field_path), policy in package.input_policies.items():
            if message_code not in package.messages:
                self._fail("UNKNOWN_INPUT_POLICY_MESSAGE", f"Input policy ссылается на неизвестное сообщение {message_code}.")
            message = package.messages.get(message_code)
            known_paths = {field.path for (structure_id, _), definition in package.structures.items()
                           if message and structure_id == message.structure_id for field in definition.fields}
            if field_path not in known_paths:
                self._fail("UNKNOWN_INPUT_POLICY_FIELD", f"Input policy {message_code} ссылается на неизвестное поле {field_path}.")
            if policy.input_policy not in FIELD_INPUT_POLICIES:
                self._fail("UNKNOWN_INPUT_POLICY", f"Неизвестная input policy {policy.input_policy}.")
            if policy.value_source not in VALUE_SOURCES:
                self._fail("UNKNOWN_VALUE_SOURCE", f"Неизвестный value source {policy.value_source}.")
            if policy.input_policy == "USER_SELECT" and not policy.allowed_values:
                self._fail("USER_SELECT_VALUES_REQUIRED", f"USER_SELECT {message_code}/{field_path} требует allowed_values.")
            if not policy.source_refs:
                self._fail("INPUT_POLICY_SOURCE_REQUIRED", f"Input policy {message_code}/{field_path} не имеет source_refs.")
        for (message_code, field_path), policy in package.ui_input_policies.items():
            if message_code not in package.messages:
                self._fail("UNKNOWN_UI_POLICY_MESSAGE", f"UI policy ссылается на неизвестное сообщение {message_code}.")
            message = package.messages.get(message_code)
            known_paths = {field.path for (structure_id, _), definition in package.structures.items()
                           if message and structure_id == message.structure_id for field in definition.fields}
            if field_path not in known_paths:
                self._fail("UNKNOWN_UI_POLICY_FIELD", f"UI policy {message_code} ссылается на неизвестное поле {field_path}.")
            if policy.ui_input_policy not in UI_INPUT_POLICIES:
                self._fail("UNKNOWN_UI_POLICY", f"Неизвестная UI policy {policy.ui_input_policy}.")
            if policy.policy_origin not in UI_POLICY_ORIGINS:
                self._fail("UNKNOWN_UI_POLICY_ORIGIN", f"Неизвестный UI policy origin {policy.policy_origin}.")
            if set(policy.capabilities) - UI_PRESENTATION_CAPABILITIES:
                self._fail("UNKNOWN_UI_PRESENTATION_CAPABILITY", f"Неизвестная UI capability для {message_code}/{field_path}.")
            if "GENERATE_IDENTIFIER" in policy.capabilities and policy.ui_input_policy != "USER_INPUT":
                self._fail("IDENTIFIER_GENERATOR_REQUIRES_EDITABLE_INPUT", f"Generator capability требует USER_INPUT: {message_code}/{field_path}.")
            if not policy.source_refs:
                self._fail("UI_POLICY_SOURCE_REQUIRED", f"UI policy {message_code}/{field_path} не имеет source_refs.")
        self._validate_orphans(package)

    def _validate_orphans(self, package: ProcessPackage) -> None:
        used_procedures = {item.procedure_code for item in package.transactions.values()}
        used_messages = {item.initiating_message for item in package.transactions.values() if item.initiating_message}
        used_messages.update(code for item in package.transactions.values() for code in item.response_messages)
        used_structures = {item.structure_id for item in package.messages.values() if item.structure_id}
        if set(package.procedures) - used_procedures:
            self._fail("ORPHAN_PROCEDURE", "Обнаружена процедура без транзакций.")
        if set(package.messages) - used_messages:
            self._fail("ORPHAN_MESSAGE", "Обнаружено сообщение вне транзакций.")
        if {key[0] for key in package.structures} - used_structures:
            self._fail("ORPHAN_STRUCTURE", "Обнаружена структура вне сообщений.")

    def _validate_sources(self, package: ProcessPackage) -> None:
        entities = [package.process, *package.procedures.values(), *package.operations.values(), *package.participants.values(), *package.transactions.values(), *package.messages.values(), *package.structures.values(), *package.rules.values(), *package.input_policies.values(), *package.ui_input_policies.values()]
        for entity in entities:
            for ref in (*entity.source_refs, *getattr(entity, "message_rules_source_refs", ())):
                if not ref.source_id or not ref.document or not ref.location or not ref.status:
                    self._fail("INVALID_SOURCE_REF", "SourceReference требует source_id, document, location и status.")

    def _validate_structure_fields(self, structure) -> None:
        if structure.expected_normative_rows != structure.imported_normative_rows:
            self._fail("STRUCTURE_SOURCE_COVERAGE_MISMATCH", f"Неполное покрытие таблицы {structure.structure_id}.")
        if structure.imported_normative_rows != len(structure.fields):
            self._fail("STRUCTURE_FIELD_COUNT_MISMATCH", f"Число fields не совпадает с imported rows: {structure.structure_id}.")
        ids = [field.field_id for field in structure.fields]
        if len(ids) != len(set(ids)):
            self._fail("DUPLICATE_FIELD_ID", f"Повтор field_id в {structure.structure_id}.")
        orders = [field.order for field in structure.fields]
        if orders != list(range(1, len(orders) + 1)):
            self._fail("INVALID_FIELD_ORDER", f"Нарушен порядок fields в {structure.structure_id}.")
        known = set(ids)
        for field in structure.fields:
            if field.interpretation_status not in {"VERIFIED", "NEEDS_EXTERNAL_SOURCE", "NEEDS_NORMATIVE_INTERPRETATION"}:
                self._fail("UNKNOWN_INTERPRETATION_STATUS", f"Неизвестен статус интерпретации {field.field_id}.")
            if field.interpretation_status != "VERIFIED" and not field.reason_code:
                self._fail("INTERPRETATION_REASON_REQUIRED", f"Для {field.field_id} не указан reason_code.")
            if field.parent and field.parent not in known:
                self._fail("UNKNOWN_FIELD_PARENT", f"{field.field_id} ссылается на неизвестного parent.")
            if field.kind == "ATTRIBUTE" and not field.parent:
                self._fail("ATTRIBUTE_PARENT_REQUIRED", f"Атрибут {field.field_id} не имеет parent.")
            if field.kind == "ARBITRARY_XML" and (field.datatype != "ANY_XML" or field.xml_name is not None):
                self._fail("INVALID_ARBITRARY_XML_FIELD", f"Некорректное arbitrary XML поле {field.field_id}.")
            if field.min_occurs is not None and field.max_occurs is not None and field.min_occurs > field.max_occurs:
                self._fail("INVALID_FIELD_CARDINALITY", f"Некорректная cardinality {field.field_id}.")
            if not field.source_refs:
                self._fail("FIELD_SOURCE_REQUIRED", f"Отсутствует source_ref для {field.field_id}.")

    @staticmethod
    def _fail(code: str, message: str) -> None:
        raise ProcessPackageValidationError(code=code, message=message)
