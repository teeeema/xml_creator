from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
from types import SimpleNamespace
from typing import Mapping
from xml.etree import ElementTree as ET

from eaeu_xml.application.models import FieldView, FormDefinition, GenerationResult, IssueView, MessageInputSummary, MessageView, ProcessIssueView, TransactionView, ValidationView
from eaeu_xml.application.services import ProcessDiscoveryService, TestDataGenerator
from eaeu_xml.application.examples import ExampleValueResolver
from eaeu_xml.application.drafts import DraftError, DraftLoadResult, DraftService
from eaeu_xml.application.conditions import ConditionalRuleCompiler, ConditionEvaluator
from eaeu_xml.core.errors import BodyValidationError, ProcessPackageError, UnresolvedStructureVersionError
from eaeu_xml.core.enums import MessageKind, SignalKind, TransactionPattern, TransactionState
from eaeu_xml.decision5.models import LogicalAddress, ProcedureId, ProcedureInstance, TransactionInstance
from eaeu_xml.decision5.models.transaction import MessageRecord, TransactionDefinition as RuntimeTransactionDefinition, TransactionParameters
from eaeu_xml.decision5.models.header import EndpointReference, RelatesTo, SoapHeader
from eaeu_xml.process_packages import EaeuXmlEngine, GenerationMode
from eaeu_xml.process_packages.input_policy import FieldInputPolicyResolver
from eaeu_xml.process_packages.ui_input_policy import UiInputPolicyResolver
from eaeu_xml.services.identifier_service import IdentifierService
from eaeu_xml.services.message_factory import MessageFactory
from eaeu_xml.services.logical_address_builder import LogicalAddressBuilder
from eaeu_xml.services.xml_serializer import XmlSerializer
from eaeu_xml.services.transaction_engine import TransactionEngine
from eaeu_xml.services.signal_factory import SignalFactory
from eaeu_xml.services.fault_factory import FaultFactory
from eaeu_xml.application.input_helpers import datatype_category
from eaeu_xml.application.file_input import FileInputService
from eaeu_xml.application.session_snapshot import SessionPersistenceService, SessionSnapshotValidator, TransactionSessionSnapshot
from eaeu_xml.application.message_artifacts import PersistedMessageArtifact, SessionBundlePersistenceService


class EaeuXmlApplication:
    def __init__(self, processes_root: Path, *, drafts_root: Path | None = None) -> None:
        self.processes_root = processes_root
        self.discovery = ProcessDiscoveryService()
        self.test_data_generator = TestDataGenerator()
        self.example_value_resolver = ExampleValueResolver()
        self.input_policy_resolver = FieldInputPolicyResolver()
        self.ui_input_policy_resolver = UiInputPolicyResolver()
        self.conditional_rule_compiler = ConditionalRuleCompiler()
        self.condition_evaluator = ConditionEvaluator()
        self.file_input_service = FileInputService()
        self._guide_service_instance = None
        self.drafts = DraftService(drafts_root)
        self._processes = {item.process_code: item for item in self.discovery.discover_processes(processes_root)}
        self._engines = {}

    def list_processes(self):
        return tuple(self._processes[code] for code in sorted(self._processes))

    @property
    def _guide_service(self):
        if self._guide_service_instance is None:
            from eaeu_xml.application.guide import GuideService
            self._guide_service_instance = GuideService(self)
        return self._guide_service_instance

    def get_process_guide(self, process_code: str): return self._guide_service.get_process_guide(process_code)

    def get_message_guide(self, process_code: str, message_code: str): return self._guide_service.get_message_guide(process_code, message_code)

    def get_field_guide(self, process_code: str, message_code: str, field_path: str):
        return self._guide_service.get_field_guide(process_code, message_code, field_path)

    def search_guide(self, process_code: str, query: str): return self._guide_service.search_guide(process_code, query)

    def _engine(self, process_code: str) -> EaeuXmlEngine:
        if process_code not in self._processes:
            raise KeyError(f"Unknown process: {process_code}")
        if process_code not in self._engines:
            self._engines[process_code] = EaeuXmlEngine.load_process(self._processes[process_code].path)
        return self._engines[process_code]

    def save_draft(self, path: Path, *, process_code: str, transaction_code: str, message_code: str,
                   values: Mapping[str, object], generation_mode: str = "TEST", notes: str | None = None,
                   session_metadata: Mapping[str, object] | None = None, previous_document=None):
        engine=self._engine(process_code); transaction=engine.get_transaction(transaction_code)
        if message_code not in (transaction.initiating_message,*transaction.response_messages):
            raise DraftError("DRAFT_MESSAGE_UNKNOWN",f"Message {message_code} is not a branch of {transaction_code}.")
        message=engine.get_message(message_code); active=engine.package.profile.structures[message.structure_id].active_version
        saved_values=dict(values)
        if previous_document:
            current_paths=set()
            def collect(fields):
                for field in fields:current_paths.add(field.path); collect(field.children)
            collect(self.get_form(process_code,transaction_code,message_code).fields)
            saved_values={path:value for path,value in previous_document.values.items() if path not in current_paths}|saved_values
        document=self.drafts.new_document(process_code=process_code,process_version=engine.package.profile.process_version,
            transaction_code=transaction_code,message_code=message_code,structure_id=message.structure_id,structure_version=active,
            generation_mode=generation_mode,values=saved_values,session_metadata=session_metadata,notes=notes,
            created_at=previous_document.created_at if previous_document else None)
        self.drafts.save_draft(document,path); return document

    def autosave_draft(self, **kwargs):
        path=self.drafts.autosave_path
        document=self.save_draft(path,**kwargs)
        return path,document

    def load_draft(self, path: Path) -> DraftLoadResult:
        document=self.drafts.load_draft(path)
        if document.process_code not in self._processes:raise DraftError("DRAFT_PROCESS_UNKNOWN",f"Process not found: {document.process_code}")
        engine=self._engine(document.process_code)
        try:transaction=engine.get_transaction(document.transaction_code)
        except ProcessPackageError as error:raise DraftError("DRAFT_TRANSACTION_UNKNOWN",f"Transaction not found: {document.transaction_code}") from error
        if document.message_code not in (transaction.initiating_message,*transaction.response_messages):
            raise DraftError("DRAFT_MESSAGE_UNKNOWN",f"Message not found in transaction: {document.message_code}")
        try:form=self.get_form(document.process_code,document.transaction_code,document.message_code)
        except (KeyError,ProcessPackageError) as error:raise DraftError("DRAFT_MESSAGE_UNKNOWN",f"Message not found: {document.message_code}") from error
        paths=set()
        def collect(fields):
            for field in fields:paths.add(field.path);collect(field.children)
        collect(form.fields)
        compatible={path:value for path,value in document.values.items() if path in paths}
        unmapped={path:value for path,value in document.values.items() if path not in paths}
        warnings=[]
        current_process_version=engine.package.profile.process_version
        if document.process_version!=current_process_version:warnings.append(f"PROCESS_VERSION_MISMATCH: draft={document.process_version}, current={current_process_version}")
        if document.structure_id!=form.structure_id:warnings.append(f"STRUCTURE_MISMATCH: draft={document.structure_id}, current={form.structure_id}")
        if document.structure_version!=form.active_version:warnings.append(f"STRUCTURE_VERSION_MISMATCH: draft={document.structure_version}, current={form.active_version}")
        if unmapped:warnings.append("UNMAPPED_DRAFT_FIELDS: "+", ".join(sorted(unmapped)))
        if document.session_metadata:warnings.append("SESSION_RESTART_REQUIRED: form values restored; transaction session must be started again")
        validation=self.validate(document.process_code,document.transaction_code,document.message_code,compatible,mode=document.generation_mode)
        return DraftLoadResult(document,compatible,unmapped,tuple(warnings),validation)

    def list_transactions(self, process_code: str) -> tuple[TransactionView, ...]:
        engine = self._engine(process_code)
        return tuple(TransactionView(item.transaction_code, item.name, item.procedure_code, item.pattern,
                                     item.initiating_message, item.response_messages, item.status)
                     for item in sorted(engine.transactions.values(), key=lambda value: value.transaction_code))

    def list_messages(self, process_code: str, transaction_code: str) -> tuple[MessageView, ...]:
        engine = self._engine(process_code); transaction = engine.get_transaction(transaction_code)
        values = [("initiating", transaction.initiating_message), *(("response", code) for code in transaction.response_messages)]
        return tuple(self._message_view(engine, transaction_code, direction, code) for direction, code in values)

    def list_process_issues(self, process_code: str) -> tuple[ProcessIssueView, ...]:
        engine=self._engine(process_code); issues=[]
        messages_by_structure={}
        for message in engine.messages.values(): messages_by_structure.setdefault(message.structure_id,[]).append(message.message_code)

        procedures_with_transactions={transaction.procedure_code for transaction in engine.transactions.values()}
        for procedure in sorted(engine.procedures.values(), key=lambda item: item.procedure_code):
            if procedure.procedure_code in procedures_with_transactions: continue
            issues.append(ProcessIssueView(
                code=f"PROCEDURE_WITHOUT_TRANSACTION:{procedure.procedure_code}", severity="WARNING", category="PROCEDURE_WITHOUT_TRANSACTION",
                title="Процедура не использует межсистемную транзакцию",
                description=f"{procedure.procedure_code} существует в нормативном пакете, но не связана с TRN.",
                source_display=self._source_display(procedure.source_refs),
                suggested_action="Проверьте выполнение процедуры через пользовательский интерфейс или сервисы портала; отсутствие TRN не делает процедуру невалидной.",
                blocks_generation=False,
            ))

        for structure_id,selection in sorted(engine.package.profile.structures.items()):
            if selection.active_version is not None:continue
            definitions=[value for (candidate,_),value in engine.structures.items() if candidate==structure_id]
            sources=self._source_display(ref for definition in definitions for ref in definition.source_refs)
            issues.append(ProcessIssueView(
                code=f"UNRESOLVED_STRUCTURE_VERSION:{structure_id}",severity="WARNING",category="UNRESOLVED_VERSION",
                title="Не задана версия структуры",
                description=f"Для структуры {structure_id} не задана active_version. TEST XML может быть сформирован с нормативным placeholder; STRICT generation недоступна.",
                affected_messages=tuple(sorted(messages_by_structure.get(structure_id,()))),affected_structures=(structure_id,),
                source_display=sources,suggested_action="Перед production-использованием указать подтверждённую active_version.",
                blocks_generation=True,blocks_test_generation=False,blocks_strict_generation=True))

        classifier_structures=[]; classifier_messages=set(); classifier_sources=[]
        for (structure_id,version),structure in engine.structures.items():
            active=engine.package.profile.structures.get(structure_id)
            if not active or active.active_version!=version:continue
            classifier_fields=[field for field in structure.fields if field.classifier_ref]
            if classifier_fields:
                classifier_structures.append(structure_id); classifier_messages.update(messages_by_structure.get(structure_id,()))
                classifier_sources.extend(ref for field in classifier_fields for ref in field.source_refs)
        if classifier_structures and not engine.package.classifiers_available:
            issues.append(ProcessIssueView(
                code="CLASSIFIER_DATASET_NOT_AVAILABLE",severity="WARNING",category="EXTERNAL_CLASSIFIER",
                title="Недоступны внешние классификаторы",
                description="Для части полей невозможно выполнить полную проверку значений по внешним классификаторам.",
                affected_messages=tuple(sorted(classifier_messages)),affected_structures=tuple(sorted(set(classifier_structures))),
                source_display=self._source_display(classifier_sources),
                suggested_action="Подключить подтверждённые наборы классификаторов. До этого XML может использоваться только в тестовом режиме.",blocks_generation=False))

        for message_code,rules in sorted(engine.rules.items()):
            message=engine.get_message(message_code)
            for rule in rules.business_rules:
                state=rule.get("interpretation_status")
                if state not in {"INTERNAL_NORMATIVE_CONFLICT","NEEDS_EXTERNAL_SOURCE"}:continue
                raw_sources=rule.get("source_refs") or ()
                source_display=tuple(self._raw_source_display(source) for source in raw_sources)
                identifiers=tuple(rule.get("referenced_identifiers") or ())
                rule_code=rule.get("conflict_id") or rule.get("rule_id") or state
                if state=="INTERNAL_NORMATIVE_CONFLICT":
                    issues.append(ProcessIssueView(
                        code=rule_code,severity="BLOCKED",category="NORMATIVE_CONFLICT",title="Конфликт нормативного источника",
                        description=rule.get("conflict_details") or "Нормативное правило ссылается на реквизит, отсутствующий в заявленной структуре.",
                        affected_messages=(message_code,),affected_structures=(message.structure_id,),referenced_fields=identifiers,
                        source_display=source_display,suggested_action="Требуется уточнение нормативного источника. Программа намеренно не подменяет реквизит похожим полем.",
                        blocks_generation=True,blocks_test_generation=True,blocks_strict_generation=True))
                else:
                    issues.append(ProcessIssueView(
                        code=rule_code,severity="WARNING",category="EXTERNAL_SOURCE",title="Требуется внешний источник",
                        description=rule.get("description") or "Правило зависит от внешнего делегированного источника.",
                        affected_messages=(message_code,),affected_structures=(message.structure_id,),referenced_fields=identifiers,
                        source_display=source_display,suggested_action="Подключить или проверить указанный внешний источник.",blocks_generation=False))
        return tuple(sorted(issues,key=lambda item:(not item.blocks_generation,item.category,item.code)))

    @staticmethod
    def _source_display(refs):
        return tuple(dict.fromkeys(EaeuXmlApplication._source_ref_display(ref) for ref in refs))

    @staticmethod
    def _source_ref_display(ref):
        parts=[ref.document,ref.section or ref.location]
        if ref.table:parts.append(f"таблица {ref.table}")
        if ref.item:parts.append(f"пункт/строка {ref.item}")
        if ref.page is not None:parts.append(f"страница {ref.page}")
        return ", ".join(part for part in parts if part)

    @staticmethod
    def _raw_source_display(ref):
        parts=[ref.get("document"),ref.get("section") or ref.get("location")]
        if ref.get("table"):parts.append(f"таблица {ref['table']}")
        if ref.get("item"):parts.append(f"пункт/строка {ref['item']}")
        if ref.get("page") is not None:parts.append(f"страница {ref['page']}")
        return ", ".join(part for part in parts if part)

    def _message_view(self, engine, transaction_code, direction, message_code):
        message = engine.get_message(message_code)
        active = engine.package.profile.structures[message.structure_id].active_version
        status, reason = self._preflight(engine, transaction_code, message_code)
        labels = {"HAS_SEPARATE_RULE_TABLE": "Есть отдельная нормативная таблица правил",
                  "NO_SEPARATE_RULE_TABLE": "Отдельная нормативная таблица правил отсутствует",
                  "NEEDS_VERIFICATION": "Статус правил требует проверки",
                  "NORMATIVE_CONFLICT": "Обнаружен нормативный конфликт правил"}
        return MessageView(message_code, message.name, direction, message.structure_id, active, status, reason,
                           message.message_rules_status, labels[message.message_rules_status])

    def _structure_for_form(self, engine, message_code):
        message = engine.get_message(message_code); selection = engine.package.profile.structures[message.structure_id]
        if selection.active_version is not None:
            return engine.structures[(message.structure_id, selection.active_version)]
        candidates = [value for (structure_id, _), value in engine.structures.items() if structure_id == message.structure_id]
        if not candidates: raise KeyError(message.structure_id)
        return sorted(candidates, key=lambda value: value.version)[-1]

    def get_form(self, process_code: str, transaction_code: str, message_code: str) -> FormDefinition:
        engine = self._engine(process_code); transaction = engine.get_transaction(transaction_code)
        if message_code not in (transaction.initiating_message, *transaction.response_messages):
            raise KeyError(f"Message {message_code} is not a branch of {transaction_code}")
        message = engine.get_message(message_code); structure = self._structure_for_form(engine, message_code)
        rules = engine.rules.get(message_code); usage = rules.field_usage if rules else {}; fixed = rules.fixed_values if rules else {}
        children = {}
        for field in structure.fields: children.setdefault(field.parent, []).append(field)

        def display_name(field):
            name = field.official_name or field.xml_name or field.path
            qname = f"{field.namespace_prefix}:{field.xml_name}" if field.namespace_prefix and field.xml_name else field.xml_name
            # Official tables often append human aliases plus a final technical QName.
            # Keep the complete official text separately, but use a clean UI caption.
            if qname and re.search(rf"\({re.escape(qname)}\)\s*$", name):
                name = re.sub(r"(?:\s*\([^()]*\))+\s*$", "", name)
            return name.strip(), qname

        def convert(field):
            usage_policy = usage.get(field.path)
            forbidden = usage_policy in {"FORBIDDEN", "NOT_USED"}
            required = usage_policy == "REQUIRED" or (field.min_occurs or 0) > 0
            hints = tuple(filter(None, (field.constraints, f"message_rule={usage_policy}" if usage_policy else None)))
            caption, qname = display_name(field)
            resolved = self.input_policy_resolver.resolve(
                message_code=message_code, field=field, rules=rules,
                explicit=engine.package.input_policies.get((message_code, field.path)),
                has_children=bool(children.get(field.field_id)),
            )
            ui_resolved = self.ui_input_policy_resolver.resolve(
                normative=resolved,
                explicit=engine.package.ui_input_policies.get((message_code, field.path)),
                forbidden=forbidden, classifier_dataset_available=engine.package.classifiers_available,
            )
            explicit_ui = engine.package.ui_input_policies.get((message_code, field.path))
            capabilities = set(explicit_ui.capabilities if explicit_ui else ())
            category = datatype_category(field.datatype)
            binary_file = "binary" in (field.datatype or "").casefold() and field.kind != "ATTRIBUTE" and ui_resolved.visible
            manual_edit = ui_resolved.editable
            show_identifier = manual_edit and "GENERATE_IDENTIFIER" in capabilities
            date_helpers_allowed = manual_edit and resolved.value_source != "EXTERNAL_INFORMATION_SYSTEM"
            explicit_policy = engine.package.input_policies.get((message_code, field.path))
            automatic_value = None
            if explicit_policy and explicit_policy.generated_value == "MESSAGE_CODE": automatic_value = message_code
            elif explicit_policy and explicit_policy.generated_value == "STRUCTURE_ID": automatic_value = message.structure_id
            example_result = self.example_value_resolver.resolve(
                datatype=field.datatype, description=field.description,
                fixed_value=fixed.get(field.path, automatic_value),
                allowed_values=explicit_policy.allowed_values if explicit_policy else (),
                existing_value=resolved.example_value,
                classifier=resolved.input_policy == "CLASSIFIER",
            ) if not children.get(field.field_id) or resolved.input_policy == "CLASSIFIER" else self.example_value_resolver.resolve(
                datatype=None, description=field.description)
            example = example_result.value
            no_example_reason=example_result.unavailable_reason
            if example is None and ui_resolved.ui_input_policy == "EXTERNAL_SYSTEM": no_example_reason="EXTERNAL_SYSTEM_VALUE"
            elif example is None and resolved.input_policy == "STRUCTURAL_CONTAINER": no_example_reason="OTHER"
            cardinality = f"{field.min_occurs if field.min_occurs is not None else '?'}..{'unbounded' if field.max_occurs is None else field.max_occurs}"
            help_text = self._field_help_text(
                description=field.description, required=required, policy=resolved.input_policy,
                value_source=resolved.value_source, example=example,
                policy_help=resolved.help_text, reason=resolved.reason,
                ui_policy=ui_resolved.ui_input_policy, ui_origin=ui_resolved.policy_origin,
            )
            return FieldView(field.path, field.xml_name, caption,
                             field.description, field.kind, field.datatype, required, field.min_occurs, field.max_occurs,
                             field.kind == "ATTRIBUTE", field.max_occurs is None or (field.max_occurs or 0) > 1,
                             allowed_values=explicit_policy.allowed_values if explicit_policy else (),
                             fixed_value=fixed.get(field.path, automatic_value), classifier=field.classifier_ref,
                             editable=ui_resolved.editable,
                             visibility="VISIBLE" if ui_resolved.visible else "HIDDEN", validation_hints=hints,
                             status=field.status, source_refs=tuple(ref.source_id for ref in field.source_refs),
                             children=tuple(convert(child) for child in sorted(children.get(field.field_id, ()), key=lambda value: value.order)),
                             official_name=field.official_name, xml_qname=qname, example_value=example,
                             cardinality_display=cardinality, input_policy=resolved.input_policy,
                             value_source=resolved.value_source, help_text=help_text,
                             condition_description=resolved.condition_description, condition_ref=resolved.condition_ref,
                             policy_reason=resolved.reason, normative_input_policy=resolved.input_policy,
                             ui_input_policy=ui_resolved.ui_input_policy, ui_policy_origin=ui_resolved.policy_origin,
                             ui_policy_reason=ui_resolved.reason, example_origin=example_result.origin,
                             no_example_reason=no_example_reason,
                             unresolved_ui_reason=ui_resolved.reason_code,
                             manual_edit_allowed=manual_edit,
                             show_today_button=date_helpers_allowed and category == "DATE",
                             show_date_picker=date_helpers_allowed and category == "DATE",
                             show_now_button=date_helpers_allowed and category in {"TIME", "DATETIME"},
                             show_timezone_picker=date_helpers_allowed and category == "DATETIME",
                             show_identifier_generator=show_identifier,
                             supports_file_picker=binary_file,
                             assisted_input_kind=("FILE" if binary_file else "IDENTIFIER" if show_identifier else category if date_helpers_allowed else None))
        status, reason = self._preflight(engine, transaction_code, message_code)
        roots = tuple(convert(field) for field in sorted(children.get(None, ()), key=lambda value: value.order))
        active = engine.package.profile.structures[message.structure_id].active_version
        return FormDefinition(process_code, transaction_code, message_code, message.structure_id, active, status, reason, roots)

    def get_conditional_rules(self, process_code: str, message_code: str):
        engine=self._engine(process_code);rules=engine.rules.get(message_code)
        if not rules:return ()
        refs=tuple(ref.source_id for ref in rules.source_refs)
        return self.conditional_rule_compiler.compile(rules.business_rules,fallback_source_refs=refs)

    @staticmethod
    def generate_identifier_value() -> str:
        return str(IdentifierService().new_identifier())

    def load_file_value(self, path: Path):
        return self.file_input_service.load(path)

    def get_message_input_summary(self, process_code: str, transaction_code: str, message_code: str,
                                  values: Mapping[str,object] | None = None) -> MessageInputSummary:
        form = self.get_form(process_code, transaction_code, message_code)
        fields = tuple(self._walk_fields(form.fields))
        policies = [field.ui_input_policy for field in fields]
        conditional_fields=[field for field in fields if field.normative_input_policy=="CONDITIONAL"]
        evaluations={item.rule.target_field_path:item.result.value for item in self.condition_evaluator.evaluate_all(
            self.get_conditional_rules(process_code,message_code),values or {})}
        active=sum(evaluations.get(field.path)=="TRUE" for field in conditional_fields)
        inactive=sum(evaluations.get(field.path)=="FALSE" for field in conditional_fields)
        return MessageInputSummary(
            total_fields=len(fields), user_input=policies.count("USER_INPUT"), user_select=policies.count("USER_SELECT"),
            automatic=policies.count("AUTO"), read_only=policies.count("READ_ONLY"),
            external_system=policies.count("EXTERNAL_SYSTEM"), conditional=policies.count("CONDITIONAL"),
            unresolved=policies.count("UNRESOLVED_UI_POLICY"), group=policies.count("GROUP"), hidden=policies.count("HIDDEN"),
            conditional_total=len(conditional_fields),conditional_active=active,conditional_inactive=inactive,
            conditional_unknown=len(conditional_fields)-active-inactive,
        )

    @classmethod
    def _walk_fields(cls, fields):
        for field in fields:
            yield field
            yield from cls._walk_fields(field.children)

    @staticmethod
    def _field_help_text(*, description, required, policy, value_source, example, policy_help, reason, ui_policy, ui_origin):
        filling = {
            "USER_INPUT": "Пользователь вводит значение", "USER_SELECT": "Пользователь выбирает значение",
            "CLASSIFIER": "Выбор из классификатора", "AUTO_GENERATED": "Формируется программой",
            "AUTO_FIXED": "Определяется сообщением автоматически", "AUTO_DATETIME": "Текущая дата/время формируется программой",
            "CORRELATION": "Берётся из связанного Body", "EXTERNAL_SYSTEM": "Поступает из информационной системы",
            "INTEGRATION_PLATFORM": "Формируется интеграционной платформой", "CONDITIONAL": "Зависит от условия правила",
            "STRUCTURAL_CONTAINER": "Группа XML-реквизитов", "UNRESOLVED_INPUT_POLICY": "Источник значения не определён",
        }[policy]
        ui_text = {"USER_INPUT":"вводится пользователем", "USER_SELECT":"выбирается пользователем",
                   "AUTO":"заполняется автоматически", "READ_ONLY":"заполняется автоматически и доступно только для чтения",
                   "EXTERNAL_SYSTEM":"поступает из внешней информационной системы", "CONDITIONAL":"зависит от условия",
                   "GROUP":"группа реквизитов", "HIDDEN":"служебное скрытое поле",
                   "UNRESOLVED_UI_POLICY":"способ заполнения требует уточнения"}[ui_policy]
        lines = [f"Назначение: {description or 'см. нормативное наименование реквизита'}",
                 f"Нормативный источник значения: {value_source if policy != 'UNRESOLVED_INPUT_POLICY' else 'не установлен отдельным правилом'}",
                 f"Способ заполнения в программе: {ui_text}",
                 f"Обязательность: {'обязательно' if required else 'необязательно'}",
                 f"Что указать: {policy_help or description or reason or 'требуется уточнение'}"]
        if example is not None: lines.append(f"Пример: {example}")
        return "\n".join(lines)

    def generate_test_data(self, process_code: str, transaction_code: str, message_code: str, *, seed: int = 0):
        values=self.test_data_generator.generate(self.get_form(process_code, transaction_code, message_code), seed=seed)
        for item in self.condition_evaluator.evaluate_all(self.get_conditional_rules(process_code,message_code),values):
            if ((item.rule.effect=="SHOW" and item.result.value=="FALSE") or
                (item.rule.effect=="HIDE" and item.result.value=="TRUE")):
                values.pop(item.rule.target_field_path,None)
        return values

    def validate(self, process_code: str, transaction_code: str, message_code: str,
                 values: Mapping[str, object], *, mode: GenerationMode = GenerationMode.TEST) -> ValidationView:
        engine = self._engine(process_code)
        if isinstance(mode, str): mode = GenerationMode(mode)
        try:
            result = engine.validate_body(message_code, dict(values), mode=mode)
        except UnresolvedStructureVersionError as error:
            issue = IssueView(error.code, "", error.message, "ERROR", rule_id=error.rule_id)
            return ValidationView(False, (issue,), (), error.code)
        issues = tuple(self._issue(issue) for issue in result.issues)
        issues += self.condition_evaluator.validation_issues(self.get_conditional_rules(process_code,message_code),values)
        message=engine.get_message(message_code); resolution=engine.resolve_structure(message.structure_id,mode=mode)
        if resolution.uses_version_placeholders:
            issues+=(IssueView("VERSION_PLACEHOLDER","",f"TEST XML сохраняет нормативные placeholders: {', '.join(resolution.placeholder_versions)}.","WARNING"),)
        errors = tuple(issue for issue in issues if issue.severity == "ERROR")
        warnings = tuple(issue for issue in issues if issue.severity == "WARNING")
        status = "NORMATIVE_CONFLICT" if any(issue.code == "NORMATIVE_CONFLICT" for issue in errors) else ("INVALID" if errors else ("VERSION_PLACEHOLDER_TEST" if resolution.uses_version_placeholders else ("TEST_ONLY" if warnings else "VALID")))
        return ValidationView(not errors, errors, warnings, status)

    def generate_test_xml(self, process_code: str, transaction_code: str, message_code: str,
                          values: Mapping[str, object] | None = None, *, seed: int = 0) -> GenerationResult:
        session = self.start_transaction(process_code, transaction_code, seed=seed)
        transaction = self._engine(process_code).get_transaction(transaction_code)
        if message_code != transaction.initiating_message:
            return GenerationResult(False, None, "INITIAL_MESSAGE_REQUIRED",
                                    (IssueView("INITIAL_MESSAGE_REQUIRED", "", "Use session.generate_response for a response branch.", "ERROR"),))
        return session.generate_initial_message(values if values is not None else self.generate_test_data(process_code, transaction_code, message_code, seed=seed))

    def start_transaction(self, process_code: str, transaction_code: str, *, seed: int = 0):
        from eaeu_xml.application.session_restore import TransactionSessionLifecycleService
        return TransactionSessionLifecycleService(self).create_new(process_code, transaction_code, seed=seed)

    def open_transaction_session(self, path: Path, *, seed: int = 0):
        from eaeu_xml.application.session_restore import TransactionSessionLifecycleService
        return TransactionSessionLifecycleService(self).open_existing(path,seed=seed)

    @staticmethod
    def save_transaction_session(session, path: Path) -> Path:
        return session.save_bundle(path)

    def _preflight(self, engine, transaction_code, message_code):
        message = engine.get_message(message_code); active = engine.package.profile.structures[message.structure_id].active_version
        rules = engine.rules.get(message_code)
        conflicts = [rule for rule in (rules.business_rules if rules else ()) if rule.get("interpretation_status") == "INTERNAL_NORMATIVE_CONFLICT"]
        if conflicts:
            return "NORMATIVE_CONFLICT", ", ".join(rule.get("conflict_id", "NORMATIVE_CONFLICT") for rule in conflicts)
        if active is None:
            try:resolution=engine.resolve_structure(message.structure_id,mode=GenerationMode.TEST)
            except UnresolvedStructureVersionError:return "UNRESOLVED_STRUCTURE_VERSION", "active_version is null and no normative placeholder definition is available"
            return "VERSION_PLACEHOLDER_TEST", ", ".join(resolution.placeholder_versions)
        resolution=engine.resolve_structure(message.structure_id,mode=GenerationMode.TEST); structure=resolution.definition
        if resolution.uses_version_placeholders:return "VERSION_PLACEHOLDER_TEST", ", ".join(resolution.placeholder_versions)
        by_id = {field.field_id: field for field in structure.fields}
        def structurally_required(field):
            current = field
            while current:
                if (current.min_occurs or 0) == 0: return False
                current = by_id.get(current.parent)
            return True
        required_paths = {path for path, policy in (rules.field_usage.items() if rules else ()) if policy == "REQUIRED"}
        fixed_paths = set(rules.fixed_values) if rules else set()
        if any(field.classifier_ref and (structurally_required(field) or field.path in required_paths or field.path in fixed_paths)
               for field in structure.fields):
            return "TEST_ONLY", "CLASSIFIER_DATASET_NOT_AVAILABLE"
        return "VERIFIED_SOAP", None

    @staticmethod
    def _issue(issue):
        source = issue.source_ref.source_id if issue.source_ref else None
        return IssueView(issue.code, issue.field_path, issue.message, issue.severity.value, source, issue.rule_id)


class TransactionSession:
    def __init__(self, application: EaeuXmlApplication, process_code: str, transaction_code: str, seed: int,
                 *, restored_transaction=None, record_metadata=None, snapshot_created_at=None,
                 snapshot_updated_at=None) -> None:
        self.application = application; self.engine = application._engine(process_code)
        self.process_code = process_code; self.definition = self.engine.get_transaction(transaction_code)
        self.identifiers = IdentifierService()
        if restored_transaction is None:
            procedure = ProcedureInstance(self.definition.procedure_code, ProcedureId.root(self.identifiers))
            self.transaction = TransactionInstance(transaction_code, self.identifiers.new_conversation_id(), procedure,
                                                   definition=self._runtime_definition())
        else:
            self.transaction = restored_transaction
        self.factory = MessageFactory(self.identifiers); self.serializer = XmlSerializer(); self.seed = seed
        self.runtime = TransactionEngine()
        self.signal_factory = SignalFactory(self.identifiers)
        self.fault_factory = FaultFactory(self.identifiers)
        self.session_persistence = SessionPersistenceService()
        self.record_metadata = dict(record_metadata or {})
        now = datetime.now(timezone.utc).isoformat()
        self.snapshot_created_at = snapshot_created_at or now
        self.snapshot_updated_at = snapshot_updated_at or now
        self._snapshot_history_length = len(self.transaction.message_history)
        self.request_body_values: dict[str, object] = {}
        self.message_artifacts: dict[str,PersistedMessageArtifact] = {}
        self.artifact_persistence_available=False

    def _runtime_definition(self):
        pattern = TransactionPattern[self.definition.pattern]
        def duration(name):
            value = self.definition.timeouts.get(name)
            seconds = SessionSnapshotValidator._duration_seconds(value) if value else None
            return timedelta(seconds=seconds) if seconds else None
        return RuntimeTransactionDefinition(pattern, TransactionParameters(
            receive_confirmation_timeout=duration("receive_confirmation"),
            processing_confirmation_timeout=duration("processing_confirmation"),
            response_timeout=duration("response"), retry_count=self.definition.retry_count or 0,
        ), bool(self.definition.guaranteed_delivery))

    @classmethod
    def _from_validated_restore(cls, application, snapshot, transaction, record_metadata, *, seed=0):
        return cls(application, snapshot.process_code, snapshot.transaction_code, seed,
                   restored_transaction=transaction, record_metadata=record_metadata,
                   snapshot_created_at=snapshot.created_at, snapshot_updated_at=snapshot.updated_at)

    def create_snapshot(self) -> TransactionSessionSnapshot:
        """Capture only existing runtime facts; Body values are deliberately excluded."""
        return TransactionSessionSnapshot.from_transaction(
            self.transaction,
            process_code=self.process_code,
            process_version=self.engine.package.profile.process_version,
            transaction_pattern=self.definition.pattern,
            guaranteed_delivery=self.definition.guaranteed_delivery,
            transaction_parameters={**self.definition.timeouts, "retry_count": self.definition.retry_count},
            record_metadata=self.record_metadata,
            created_at=self.snapshot_created_at,
            updated_at=(self.snapshot_updated_at if len(self.transaction.message_history) == self._snapshot_history_length
                        else datetime.now(timezone.utc).isoformat()),
        )

    def save_snapshot(self, path: Path) -> Path:
        return self.session_persistence.save(self.create_snapshot(), path)

    def save_bundle(self,path:Path)->Path:
        return SessionBundlePersistenceService().save(self.create_snapshot(),tuple(self.message_artifacts.values()),path)

    def artifact_for(self,message_id):
        key=message_id.serialize() if hasattr(message_id,"serialize") else str(message_id)
        try:return self.message_artifacts[key]
        except KeyError as error:raise ValueError("HISTORICAL_PAYLOAD_UNAVAILABLE") from error

    def generate_initial_message(self, values: Mapping[str, object] | None = None) -> GenerationResult:
        code = self.definition.initiating_message
        if self.transaction.message_history:
            return self._error("INITIAL_ALREADY_GENERATED", "Initial message already exists in this session.")
        values = dict(values) if values is not None else self.application.generate_test_data(self.process_code, self.definition.transaction_code, code, seed=self.seed)
        result = self._generate(code, values, followup=False)
        if result.success:
            self.request_body_values = values
            self.transaction.state = self.runtime.state_machine.after_initial(self.transaction)
        return result

    def generate_response(self, message_code: str, values: Mapping[str, object] | None = None,
                          *, body_correlations: Mapping[str, object] | None = None) -> GenerationResult:
        if message_code not in self.definition.response_messages:
            return self._error("RESPONSE_NOT_ALLOWED", f"{message_code} is not a response branch.")
        if not self.transaction.message_history:
            return self._error("INITIAL_MESSAGE_REQUIRED", "Generate the initial message first.")
        values = dict(values) if values is not None else self.application.generate_test_data(self.process_code, self.definition.transaction_code, message_code, seed=self.seed + 1)
        try:values.update(self.resolve_body_correlations(message_code))
        except ValueError as error:return self._error(str(error),"Historical Body correlation is unavailable.",message_code)
        values.update(body_correlations or {})
        previous_state = self.transaction.state
        result = self._generate(message_code, values, followup=True)
        if result.success:
            self.transaction.state = previous_state
            self.runtime.receive_application_message(self.transaction)
        return result

    def resolve_body_correlations(self,message_code):
        """Apply only source-traced package correlation policies from immutable artifacts."""
        if not self.artifact_persistence_available:return {}
        result={}
        for (code,target_path),policy in self.engine.package.input_policies.items():
            if code!=message_code or policy.input_policy!="CORRELATION" or policy.value_source!="PREVIOUS_BODY":continue
            if not policy.correlation_source_path:raise ValueError("BODY_CORRELATION_UNRESOLVED")
            found=None
            for record in reversed(self.transaction.message_history):
                artifact=self.message_artifacts.get(record.message_id.serialize())
                if not artifact:continue
                values=artifact.values()
                if policy.correlation_source_path in values:
                    found=values[policy.correlation_source_path];break
            if found is None:raise ValueError("BODY_CORRELATION_UNRESOLVED")
            result[target_path]=found
        return result

    def _generate(self, message_code, values, followup):
        validation = self.application.validate(self.process_code, self.definition.transaction_code, message_code, values, mode=GenerationMode.TEST)
        if not validation.is_valid:
            return GenerationResult(False, None, validation.status, validation.errors, validation.warnings, self._metadata(message_code))
        try:
            body = self.engine.build_body(message_code, values, mode=GenerationMode.TEST)
            create = self.factory.create_followup_application_message if followup else self.factory.create_initial_application_message
            envelope = create(transaction=self.transaction, process_code=self.process_code,
                              process_version=self.engine.package.profile.process_version, message_code=message_code,
                              to=self._address(False if followup else True), reply_to=self._address(True if followup else False),
                              body_payload=body)
            record = self.transaction.message_history[-1]
            self.record_metadata[record.message_id.serialize()] = {
                "message_code": message_code, "direction": "SENT",
            }
            resolution=self.engine.resolve_structure(self.engine.get_message(message_code).structure_id,mode=GenerationMode.TEST)
            placeholder_sources=tuple(self.application._source_ref_display(ref) for ref in resolution.definition.source_refs)
            placeholder_prefixes=tuple(prefix for prefix,namespace in resolution.definition.imported_namespaces.items() if any(token in namespace for token in resolution.placeholder_versions))
            xml = self.serializer.serialize_application(envelope,placeholder_versions=resolution.placeholder_versions,placeholder_sources=placeholder_sources,placeholder_structure_id=resolution.definition.structure_id,placeholder_model_prefixes=placeholder_prefixes); ET.fromstring(xml)
        except (ProcessPackageError, BodyValidationError) as error:
            return self._error(error.code, error.message, message_code)
        self.message_artifacts[record.message_id.serialize()]=PersistedMessageArtifact.from_values(message_id_ref=record.message_id.serialize(),transaction_code=self.definition.transaction_code,message_code=message_code,attempt_number=record.attempt_number,values=values)
        self.artifact_persistence_available=True
        metadata = self._metadata(message_code, envelope)
        status = "VERSION_PLACEHOLDER_TEST" if metadata["uses_version_placeholders"] else ("TEST_ONLY" if validation.warnings else "VERIFIED_SOAP")
        return GenerationResult(True, xml, status, (), validation.warnings, metadata)

    def retry(self, original_message_id: str | None = None):
        applications = [record for record in self.transaction.message_history if record.message_kind is MessageKind.APPLICATION]
        if not applications:
            raise ValueError("No application message is available for retry.")
        original = next((record for record in applications if record.message_id.serialize() == original_message_id), applications[-1])
        retry = self.runtime.retry_service.retry_record(self.transaction, original, self.identifiers.new_message_id())
        source = self.record_metadata.get(original.message_id.serialize(), {})
        self.record_metadata[retry.message_id.serialize()] = {**source, "direction": "SENT"}
        return retry

    def retry_with_payload(self,original_message_id:str):
        original=next((item for item in self.transaction.message_history if item.message_id.serialize()==original_message_id),None)
        if original is None:raise ValueError("HISTORICAL_ATTEMPT_NOT_FOUND")
        artifact=self.artifact_for(original_message_id);values=artifact.values()
        message_code=artifact.message_code;body=self.engine.build_body(message_code,values,mode=GenerationMode.TEST)
        self.runtime.retry_service.prepare_retry(self.transaction,original)
        initiating=message_code==self.definition.initiating_message
        envelope=self.factory.create_retry_application_message(transaction=self.transaction,process_code=self.process_code,process_version=self.engine.package.profile.process_version,message_code=message_code,to=self._address(initiating),reply_to=self._address(not initiating),body_payload=body,original=original)
        record=self.transaction.message_history[-1];self.record_metadata[record.message_id.serialize()]={"message_code":message_code,"direction":"SENT"}
        resolution=self.engine.resolve_structure(self.engine.get_message(message_code).structure_id,mode=GenerationMode.TEST)
        xml=self.serializer.serialize_application(envelope,placeholder_versions=resolution.placeholder_versions,placeholder_sources=tuple(self.application._source_ref_display(ref) for ref in resolution.definition.source_refs),placeholder_structure_id=resolution.definition.structure_id,placeholder_model_prefixes=())
        self.message_artifacts[record.message_id.serialize()]=PersistedMessageArtifact.from_values(message_id_ref=record.message_id.serialize(),transaction_code=self.definition.transaction_code,message_code=message_code,attempt_number=record.attempt_number,values=values)
        return GenerationResult(True,xml,"VERSION_PLACEHOLDER_TEST" if resolution.uses_version_placeholders else "VERIFIED_SOAP",(),(),self._metadata(message_code,envelope))

    def create_signal(self, source_message, kind: SignalKind, *, direction="SENT"):
        signal = self.signal_factory.create(transaction=self.transaction, source_message=source_message, kind=kind,
                                            to=source_message.header.reply_to.address,
                                            reply_to=source_message.header.to)
        record = self.transaction.message_history[-1]
        self.record_metadata[record.message_id.serialize()] = {
            "direction": direction, "signal_kind": kind.value,
        }
        self.transaction.state = self.runtime.state_machine.receive_signal(self.transaction, kind)
        return signal

    def historical_application_message(self, message_id: str):
        """Rebuild the minimal validated Header context needed by core signal/fault factories."""
        record = next(item for item in self.transaction.message_history
                      if item.message_id.serialize() == message_id and item.message_kind is MessageKind.APPLICATION)
        metadata = self.record_metadata.get(message_id, {})
        message_code = metadata.get("message_code") or record.action.message_code
        initiating = message_code == self.definition.initiating_message
        header = SoapHeader(
            to=self._address(initiating), reply_to=EndpointReference(self._address(not initiating)),
            action=record.action, message_id=record.message_id,
            procedure_id=self.transaction.procedure_instance.procedure_id,
            conversation_id=self.transaction.conversation_id,
            relates_to=RelatesTo(record.relates_to) if record.relates_to else None,
        )
        return SimpleNamespace(header=header)

    def create_fault(self, source_message, sender, fault, *, direction="SENT", wsa_fault=False):
        message = self.fault_factory.create(source_message=source_message, sender=sender, fault=fault, wsa_fault=wsa_fault)
        record = MessageRecord(message.header.message_id, message.header.action, datetime.now(timezone.utc),
            len(self.transaction.message_history) + 1, MessageKind.TECHNICAL_FAULT,
            message.header.relates_to.message_id)
        self.transaction.message_history.append(record)
        self.record_metadata[record.message_id.serialize()] = {
            "direction": direction, "fault_kind": message.header.action.serialize(),
            "relates_action": message.header.relates_to.relates_action,
        }
        self.runtime.receive_fault(self.transaction)
        return message

    def _address(self, destination):
        participant_code = self.definition.responding_participant if destination else self.definition.initiating_participant
        if not participant_code:
            raise ProcessPackageError(code="TRANSACTION_PARTICIPANT_UNDEFINED", message=f"Для {self.definition.transaction_code} не заданы участники адресации.")
        participant = self.engine.participants[participant_code]
        segment = participant.fixed_segment if participant.segment_policy == "FIXED" else participant.test_segment
        if not segment:
            raise ProcessPackageError(code="PARTICIPANT_SEGMENT_UNRESOLVED", message=f"Для {participant_code} не задан сегмент адресации.")
        return LogicalAddressBuilder().build_common_process(
            segment=segment, process_code=self.process_code, participant_code=participant.participant_code,
        )

    def _metadata(self, message_code, envelope=None):
        message = self.engine.get_message(message_code); active = self.engine.package.profile.structures[message.structure_id].active_version
        try:resolution=self.engine.resolve_structure(message.structure_id,mode=GenerationMode.TEST)
        except ProcessPackageError:resolution=None
        data = {"process": self.process_code, "procedure": self.definition.procedure_code,
                "transaction": self.definition.transaction_code, "message": message_code,
                "structure": message.structure_id, "structure_version": active,
                "uses_version_placeholders":bool(resolution and resolution.uses_version_placeholders),
                "unresolved_structures":(message.structure_id,) if resolution and resolution.uses_version_placeholders else (),
                "placeholder_versions":resolution.placeholder_versions if resolution else (),
                "placeholder_sources":tuple(self.application._source_ref_display(ref) for ref in resolution.definition.source_refs) if resolution and resolution.uses_version_placeholders else ()}
        if envelope:
            data.update(message_id=envelope.header.message_id.serialize(), procedure_id=envelope.header.procedure_id.serialize(),
                        conversation_id=envelope.header.conversation_id.serialize(), action=envelope.header.action.serialize(),
                        relates_to=envelope.header.relates_to.message_id.serialize() if envelope.header.relates_to else None)
        return data

    def _error(self, code, message, message_code=None):
        return GenerationResult(False, None, code, (IssueView(code, "", message, "ERROR"),), (),
                                self._metadata(message_code) if message_code else {})
