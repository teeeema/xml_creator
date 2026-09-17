"""Headless-testable presentation state for the wx frontend."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import time
from typing import Any
from eaeu_xml.application.input_helpers import datetime_value, time_value, today_value

from eaeu_xml.application import (
    DraftLoadResult, EaeuXmlApplication, FieldView, FieldVisibilityFilter,
    FormDisplayMode, GenerationResult, SessionRestoreStatus, ValidationView,
)


BLOCKED_STATUSES = {"UNRESOLVED_STRUCTURE_VERSION", "NORMATIVE_CONFLICT"}


@dataclass(frozen=True)
class ControlModel:
    path: str
    label: str
    control_kind: str
    required: bool
    read_only: bool
    repeatable: bool
    is_attribute: bool
    visibility: str
    tooltip: str = ""
    example_value: Any = None
    children: tuple["ControlModel", ...] = ()
    supports_file_picker: bool = False


@dataclass(frozen=True)
class GuiSettings:
    processes_root: Path
    mode: str = "TEST"
    seed: int = 12345
    autosave_enabled: bool = True
    autosave_delay_seconds: int = 3
    drafts_directory: Path | None = None
    default_timezone: str = "System"
    last_used_timezone: str | None = None


@dataclass(frozen=True)
class StatusPresentation:
    status: str
    severity: str
    title: str
    description: str
    suggested_action: str | None
    can_generate: bool
    details: tuple[str, ...] = ()


class SessionMode(str,Enum):
    NEW="NEW"
    RESTORED="RESTORED"


@dataclass(frozen=True)
class SessionPresentation:
    status: SessionRestoreStatus
    title: str
    description: str
    details: tuple[str,...]
    continue_ready: bool


class GuiController:
    def __init__(self, application: EaeuXmlApplication, *, test_seed: int = 12345) -> None:
        self.application = application
        self.test_seed = test_seed
        self.processes = application.list_processes()
        self.transactions = ()
        self.messages = ()
        self.process_issues = ()
        self.form = None
        self.process_code = self.transaction_code = self.message_code = None
        self.values: dict[str, object] = {}
        self.validation: ValidationView | None = None
        self.generation: GenerationResult | None = None
        self.session = None
        self.session_mode=SessionMode.NEW;self.session_open_result=None
        self.active_tab = "DATA"
        self.display_mode = FormDisplayMode.ALL
        self.search_query = ""
        self.revealed_paths: set[str] = set()
        self.visibility_filter = FieldVisibilityFilter()
        self.conditional_rules=();self.condition_dependency_index={};self.condition_results={}
        self.settings = GuiSettings(application.processes_root,"TEST",test_seed,True,3,application.drafts.drafts_root)
        self.dirty=False; self.current_draft_path: Path | None=None; self.current_draft_document=None
        self.last_draft_load: DraftLoadResult | None=None; self.autosave_due_at: float | None=None; self.autosave_document=None
        if self.processes:
            self.select_process(self.processes[0].process_code)

    @property
    def current_message(self):
        return next((item for item in self.messages if item.message_code == self.message_code), None)

    @property
    def generation_enabled(self) -> bool:
        if not self.current_message:return False
        if self.current_message.generation_status in BLOCKED_STATUSES:return False
        if self.settings.mode=="STRICT" and self.current_message.generation_status=="VERSION_PLACEHOLDER_TEST":return False
        return True

    @property
    def save_enabled(self) -> bool:
        return bool(self.generation and self.generation.success and self.generation.xml)

    @property
    def status_notice(self) -> str:
        presentation=self.message_presentation()
        return presentation.description if presentation else "Сообщение не выбрано."

    def message_presentation(self) -> StatusPresentation | None:
        message=self.current_message
        if not message:return None
        related=[issue for issue in self.process_issues if message.message_code in issue.affected_messages]
        if message.generation_status in {"UNRESOLVED_STRUCTURE_VERSION","VERSION_PLACEHOLDER_TEST"}:
            issue=next((item for item in related if item.category=="UNRESOLVED_VERSION"),None)
            strict=self.settings.mode=="STRICT" or message.generation_status=="UNRESOLVED_STRUCTURE_VERSION"
            description=(f"STRICT generation недоступна: для структуры {message.structure_id} не задана active_version." if strict else
                "Конкретная версия структуры не определена. В тестовом XML будут сохранены нормативные обозначения Y.Y.Y / X.X.X; такой XML не является production-ready.")
            return StatusPresentation(message.generation_status,"BLOCKED" if strict else "WARNING",
                "Не задана версия структуры" if strict else "Версия не указана — тестовый XML",description,
                issue.suggested_action if issue else "Перед production-использованием указать подтверждённую active_version.",not strict,
                tuple(filter(None,(f"Структура: {message.structure_id}",f"active_version: {message.active_version or 'не задана'}"))))
        if message.generation_status=="NORMATIVE_CONFLICT":
            conflicts=[item for item in related if item.category=="NORMATIVE_CONFLICT"]
            details=[]
            for issue in conflicts:
                details.extend((f"Конфликт: {issue.code}",f"Сообщение: {message.message_code}"))
                if issue.referenced_fields:details.append("Реквизит: "+", ".join(issue.referenced_fields))
                details.extend(f"Источник: {source}" for source in issue.source_display)
            description="Автоматическое формирование сообщения заблокировано, потому что нормативное правило ссылается на реквизит, отсутствующий в заявленной структуре."
            action=(conflicts[0].suggested_action if conflicts else "Требуется уточнение нормативного источника. Программа намеренно не подменяет реквизит похожим полем.")
            return StatusPresentation(message.generation_status,"BLOCKED","Конфликт нормативного источника",description,action,False,tuple(details))
        if message.generation_status=="TEST_ONLY":
            return StatusPresentation(message.generation_status,"WARNING","Только тестовый режим",
                "XML может быть сформирован только в тестовом режиме: не выполнена полная проверка по внешним классификаторам. Структура XML и внутренние правила при этом могут быть корректны.",
                "Подключить подтверждённые внешние классификаторы для полной проверки.",True,
                (f"Сообщение: {message.message_code}",f"Структура: {message.structure_id}"))
        return StatusPresentation(message.generation_status,"SUCCESS","Сообщение готово к формированию",
            "XML можно сформировать. Проверка пользовательского ввода выполняется отдельно.",None,True,
            (f"Сообщение: {message.message_code}",f"Структура: {message.structure_id}"))

    def filtered_process_issues(self, filter_name="ALL"):
        blocks=lambda issue:issue.blocks_strict_generation if self.settings.mode=="STRICT" else issue.blocks_test_generation
        if filter_name=="BLOCKING":return tuple(issue for issue in self.process_issues if blocks(issue))
        if filter_name=="WARNINGS":return tuple(issue for issue in self.process_issues if not blocks(issue))
        return tuple(self.process_issues)

    @staticmethod
    def message_marker(status):
        return {"VERIFIED_SOAP":"[OK]","TEST_ONLY":"[TEST]","VERSION_PLACEHOLDER_TEST":"","UNRESOLVED_STRUCTURE_VERSION":"[BLOCKED]","NORMATIVE_CONFLICT":"[BLOCKED]"}.get(status,"[INFO]")

    def select_process(self, process_code: str) -> None:
        self.process_code = process_code
        self.process_issues = self.application.list_process_issues(process_code)
        self.transactions = self.application.list_transactions(process_code)
        self.transaction_code = self.message_code = None
        self.messages = (); self.form = None; self._clear_result(); self.session = None;self.session_mode=SessionMode.NEW;self.session_open_result=None
        if self.transactions: self.select_transaction(self.transactions[0].transaction_code)

    def select_transaction(self, transaction_code: str) -> None:
        self.transaction_code = transaction_code
        self.messages = self.application.list_messages(self.process_code, transaction_code)
        self.message_code = None; self.form = None; self._clear_result(); self.session = None;self.session_mode=SessionMode.NEW;self.session_open_result=None
        if self.messages: self.select_message(self.messages[0].message_code)

    def select_message(self, message_code: str) -> None:
        self.message_code = message_code
        self.form = self.application.get_form(self.process_code, self.transaction_code, message_code)
        self.conditional_rules=self.application.get_conditional_rules(self.process_code,message_code)
        self.condition_dependency_index=self.application.condition_evaluator.dependency_index(self.conditional_rules)
        self.search_query = ""; self.revealed_paths.clear()
        self.clear(mark_dirty=False)

    def guide_context(self, field_path: str | None = None):
        return self.process_code, self.message_code, field_path

    def control_models(self) -> tuple[ControlModel, ...]:
        return tuple(self._control(field) for field in (self.form.fields if self.form else ()))

    def visible_control_models(self) -> tuple[ControlModel, ...]:
        presentation = self.form_presentation
        return tuple(self._control(field) for field in (presentation.fields if presentation else ()))

    @property
    def form_presentation(self):
        if not self.form:
            return None
        issues = () if not self.validation else (*self.validation.errors, *self.validation.warnings)
        return self.visibility_filter.apply(
            self.form, mode=self.display_mode, query=self.search_query,
            issues=issues, values=self.values, reveal_paths=self.revealed_paths,
            conditional_rules=self.conditional_rules,condition_evaluator=self.application.condition_evaluator,
            condition_results=self.condition_results,
        )

    @property
    def message_input_summary(self):
        if not self.form:
            return None
        return self.application.get_message_input_summary(
            self.process_code, self.transaction_code, self.message_code,self.values)

    def set_display_mode(self, mode: FormDisplayMode | str):
        self.display_mode = FormDisplayMode(mode); self.revealed_paths.clear()
        return self.form_presentation

    def set_search_query(self, query: str):
        self.search_query = query; self.revealed_paths.clear()
        return self.form_presentation

    def reveal_error_field(self, path: str):
        if not self.find_field(path):
            return False
        self.revealed_paths.add(path); self.active_tab = "DATA"
        return True

    def update_visible_values(self, visible_values) -> None:
        """Merge visible controls into the complete BodyValues state."""
        presentation = self.form_presentation
        if not presentation:
            return
        merged = dict(self.values)
        visible_values = dict(visible_values)

        def instance_count(path, source):
            value = source.get(path)
            if isinstance(value, list):
                return len(value)
            if path in source or any(item.startswith(path + "/") for item in source):
                return 1
            return 0

        def unwrap_singletons(value):
            while isinstance(value, list) and len(value) == 1:
                value = value[0]
            return value

        def has_descendant_value(path):
            return any(
                key.startswith(path + "/")
                and unwrap_singletons(value) not in (None, "", (), [], {})
                for key, value in visible_values.items()
            )

        for path in presentation.visible_paths:
            field = self.find_field(path)
            if field and not field.children:
                merged.pop(path, None)
            elif field and field.repeatable:
                old_count = instance_count(path, merged)
                new_count = instance_count(path, visible_values)
                if new_count != old_count:
                    should_keep_group = new_count and (
                        old_count or has_descendant_value(path)
                    )
                    if should_keep_group:
                        merged[path] = visible_values.get(path, [None] * new_count)
                    else:
                        merged.pop(path, None)

        for path, new_value in visible_values.items():
            field = self.find_field(path)
            if field and not field.children:
                old_value = merged.get(path)
                if isinstance(old_value, list):
                    normalized_value = new_value
                else:
                    normalized_value = unwrap_singletons(new_value)

                same_value = (
                    path in merged
                    and unwrap_singletons(old_value) == unwrap_singletons(new_value)
                )
                if same_value:
                    merged[path] = old_value
                else:
                    merged[path] = normalized_value

        changed = merged != self.values
        self.values = merged
        self._clear_result()
        if changed:
            self._mark_dirty()

    def _control(self, field: FieldView) -> ControlModel:
        datatype = (field.datatype or "").lower()
        if field.supports_file_picker:
            kind = "FILE"
        elif field.ui_input_policy == "GROUP":
            kind = "GROUP"
        elif field.ui_input_policy == "USER_SELECT":
            kind = "SELECT"
        elif "indicator" in datatype or "boolean" in datatype:
            kind = "BOOLEAN"
        else:
            kind = "TEXT"
        label = ("@" if field.is_attribute else "") + field.display_name + (" *" if field.required else "")
        return ControlModel(field.path, label, kind, field.required, not field.editable,
                            field.repeatable, field.is_attribute, field.visibility, self.field_help(field), field.example_value,
                            tuple(self._control(child) for child in field.children),field.supports_file_picker)

    @staticmethod
    def short_text(code: str, name: str | None, *, limit: int = 72, normative_document_number: int | None = None) -> str:
        prefix = code.rsplit(".", 1)[-1] if ".TRN." in code or ".MSG." in code else code
        prefix = f"№ {normative_document_number} ОП — {prefix}" if normative_document_number is not None else prefix
        text = f"{prefix} — {name}" if name else prefix
        return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"

    @staticmethod
    def field_help(field: FieldView) -> str:
        lines=[field.help_text] if field.help_text else []
        def add(label,value):
            if value not in (None,"",(),[]): lines.append(f"{label}: {value}")
        add("Название",field.official_name or field.display_name)
        add("Что вводить",field.description)
        add("XML",field.xml_qname)
        add("XML path",field.path)
        add("Вид","XML-атрибут" if field.is_attribute else "XML-элемент")
        add("Тип",field.datatype)
        add("Обязательность","обязательно" if field.required else "необязательно")
        add("Кардинальность",field.cardinality_display)
        add("Пример",field.example_value)
        add("Допустимые значения",", ".join(map(str,field.allowed_values)) if field.allowed_values else None)
        if "indicator" in (field.datatype or "").lower() or "boolean" in (field.datatype or "").lower():
            add("Варианты в интерфейсе", "Да / Нет (в XML: true / false)")
        add("Fixed value",field.fixed_value)
        add("Classifier",field.classifier)
        add("Normative input policy",field.normative_input_policy)
        add("Normative value source",field.value_source)
        add("UI input policy",field.ui_input_policy)
        add("UI policy origin",field.ui_policy_origin)
        add("Способ заполнения в программе",("можно ввести вручную или сформировать автоматически" if field.show_identifier_generator else
            "можно ввести вручную или использовать текущую дату/время" if field.show_now_button or field.show_today_button else None))
        add("Условие",field.condition_description)
        if field.normative_input_policy=="CONDITIONAL":add("Автоматическая проверка условия","доступна" if field.conditional_machine_evaluable else "недоступна в текущей модели")
        add("Condition ref",field.condition_ref)
        add("Source",", ".join(field.source_refs) if field.source_refs else None)
        return "\n".join(lines)

    @staticmethod
    def field_tooltip(field: FieldView) -> str:
        action={"USER_INPUT":"Заполняется пользователем.","USER_SELECT":"Выбирается пользователем из списка.",
                "AUTO":"Формируется автоматически.","READ_ONLY":"Формируется программой.",
                "EXTERNAL_SYSTEM":"Поступает из внешней информационной системы.","CONDITIONAL":"Зависит от условия.",
                "GROUP":"Структурный блок.","HIDDEN":"Служебный реквизит.",
                "UNRESOLVED_UI_POLICY":"Способ заполнения не определён."}[field.ui_input_policy]
        parts=[field.description or field.display_name,action]
        if field.show_now_button:
            parts.append("Формат: ISO 8601. Можно ввести вручную или использовать кнопку «Сейчас».")
        elif field.show_today_button:
            parts.append("Формат: YYYY-MM-DD. Можно ввести вручную, выбрать дату или использовать кнопку «Сегодня».")
        if field.show_identifier_generator:
            parts.append("Можно ввести вручную или использовать кнопку «Сгенерировать».")
        if field.normative_input_policy=="CONDITIONAL":
            parts.append("Автоматическая проверка условия доступна." if field.conditional_machine_evaluable else
                         "Реквизит заполняется при выполнении условия. Автоматическая проверка этого условия в текущей модели недоступна.")
        if field.example_value is not None:parts.append(f"Пример: {field.example_value}")
        return "\n".join(parts)

    def find_field(self, path: str):
        def walk(fields):
            for field in fields:
                if field.path == path: return field
                found=walk(field.children)
                if found:return found
        return walk(self.form.fields) if self.form else None

    def apply_test_data(self) -> dict[str, object]:
        self.values = self.application.generate_test_data(self.process_code, self.transaction_code,
                                                          self.message_code, seed=self.test_seed)
        self._clear_result()
        self._reevaluate_all_conditions()
        self._mark_dirty()
        return dict(self.values)

    def set_values(self, values) -> None:
        changed=dict(values)!=self.values
        self.values = dict(values); self._clear_result();self._reevaluate_all_conditions()
        if changed:self._mark_dirty()

    def assisted_value(self, action: str, *, timezone_name: str | None = None, temporal_kind: str = "DATETIME") -> str:
        if action == "GENERATE_IDENTIFIER":
            return self.application.generate_identifier_value()
        if action == "TODAY":
            return today_value()
        if action == "NOW":
            selected = timezone_name or self.settings.last_used_timezone or self.settings.default_timezone
            self.settings = GuiSettings(self.settings.processes_root,self.settings.mode,self.settings.seed,
                self.settings.autosave_enabled,self.settings.autosave_delay_seconds,self.settings.drafts_directory,
                self.settings.default_timezone,selected)
            return time_value(selected) if temporal_kind == "TIME" else datetime_value(selected)
        raise ValueError(f"Unknown assisted input action: {action}")

    def reevaluate_condition_sources(self,paths):
        for path in paths:
            self.condition_results.update(self.application.condition_evaluator.evaluate_affected(
                path,self.condition_dependency_index,self.values))

    def _reevaluate_all_conditions(self):
        self.condition_results={rule:self.application.condition_evaluator.evaluate(rule,self.values) for rule in self.conditional_rules}

    def get_values(self) -> dict[str, object]:
        return dict(self.values)

    def clear(self, *, mark_dirty=True) -> None:
        self.values = {}
        if self.form:
            def fixed(fields):
                for field in fields:
                    if field.fixed_value is not None: self.values[field.path] = field.fixed_value
                    fixed(field.children)
            fixed(self.form.fields)
        self._clear_result()
        self._reevaluate_all_conditions()
        if mark_dirty:self._mark_dirty()

    @property
    def requires_dirty_confirmation(self): return self.dirty

    def _mark_dirty(self):
        self.dirty=True
        if self.settings.autosave_enabled:self.autosave_due_at=time.monotonic()+self.settings.autosave_delay_seconds

    def _session_metadata(self):
        if not self.session:return {}
        transaction=self.session.transaction
        return {"conversation_id":transaction.conversation_id.serialize(),"procedure_id":transaction.procedure_instance.procedure_id.serialize(),"session_restorable":False}

    def save_draft(self, path: Path | None = None):
        if path is None:path=self.current_draft_path
        if path is None:raise ValueError("Draft path is required for the first manual save.")
        document=self.application.save_draft(path,process_code=self.process_code,transaction_code=self.transaction_code,
            message_code=self.message_code,values=self.values,generation_mode=self.settings.mode,
            session_metadata=self._session_metadata(),previous_document=self.current_draft_document)
        self.current_draft_path=Path(path); self.current_draft_document=document; self.dirty=False; self.autosave_due_at=None
        self.application.drafts.clear_autosave(); return document

    def load_draft(self,path: Path):
        result=self.application.load_draft(path)
        self.select_process(result.document.process_code); self.select_transaction(result.document.transaction_code); self.select_message(result.document.message_code)
        self.values=dict(result.compatible_values); self.settings=GuiSettings(self.settings.processes_root,result.document.generation_mode,self.settings.seed,
            self.settings.autosave_enabled,self.settings.autosave_delay_seconds,self.settings.drafts_directory,
            self.settings.default_timezone,self.settings.last_used_timezone)
        self.validation=result.validation; self.generation=None; self.session=None;self.session_mode=SessionMode.NEW;self.session_open_result=None; self.current_draft_path=Path(path); self.current_draft_document=result.document
        self.last_draft_load=result; self.dirty=False; self.autosave_due_at=None
        self._reevaluate_all_conditions()
        return result

    def autosave_if_due(self, *, now=None):
        current=time.monotonic() if now is None else now
        if not self.dirty or not self.settings.autosave_enabled or self.autosave_due_at is None or current<self.autosave_due_at:return None
        path,document=self.application.autosave_draft(process_code=self.process_code,transaction_code=self.transaction_code,
            message_code=self.message_code,values=self.values,generation_mode=self.settings.mode,
            session_metadata=self._session_metadata(),previous_document=self.autosave_document)
        self.autosave_document=document; self.autosave_due_at=None; return path

    @property
    def has_autosave_recovery(self):return self.application.drafts.has_recoverable_autosave()
    def recover_autosave(self):
        result=self.load_draft(self.application.drafts.autosave_path)
        # Recovery is an unsaved working copy, not a manual draft file.
        self.current_draft_path=None; self.dirty=True; self._mark_dirty()
        return result
    def discard_autosave(self):self.application.drafts.clear_autosave()
    def mark_clean_close(self, *, discard=False):
        if discard:self.application.drafts.clear_autosave(); self.dirty=False
        if not self.dirty:self.application.drafts.clear_autosave()
        self.application.drafts.mark_clean_shutdown()

    def validate(self) -> ValidationView:
        self.validation = self.application.validate(self.process_code, self.transaction_code,
                                                    self.message_code, self.values, mode=self.settings.mode)
        return self.validation

    def start_session(self):
        self.session = self.application.start_transaction(self.process_code, self.transaction_code,
                                                          seed=self.test_seed)
        self.session_mode=SessionMode.NEW;self.session_open_result=None
        return self.session

    @property
    def session_continue_enabled(self):
        return bool(self.session_open_result and self.session_open_result.continue_ready)

    @property
    def session_save_enabled(self):return self.session is not None

    def open_session_snapshot(self,path:Path):
        self.session_open_result=self.application.open_transaction_session(path,seed=self.test_seed)
        return self.session_open_result

    def session_presentation(self):
        opened=self.session_open_result
        if not opened:return None
        status=opened.status
        descriptions={
            SessionRestoreStatus.RESTORABLE:("Сессию можно продолжить","Проверка application layer завершена успешно."),
            SessionRestoreStatus.PROCESS_VERSION_MISMATCH:("Другая версия процесса","Продолжение существующей SOAP-сессии запрещено для текущей версии процесса."),
            SessionRestoreStatus.TIMING_REVALIDATION_REQUIRED:("Требуется повторная проверка времени","Временные условия требуют отдельного решения; автоматическое продолжение запрещено."),
            SessionRestoreStatus.CORRELATION_INVALID:("Нарушена корреляция сессии","Application layer отклонил историю корреляции."),
            SessionRestoreStatus.STATE_INVALID:("Некорректное состояние сессии","Application layer не подтвердил сохранённое состояние."),
            SessionRestoreStatus.SNAPSHOT_INVALID:("Файл сессии недействителен","Файл повреждён, имеет неверную схему или не прошёл строгую проверку."),
            SessionRestoreStatus.PROCESS_NOT_FOUND:("Процесс не найден","Текущий каталог не содержит процесс из файла сессии."),
            SessionRestoreStatus.TRANSACTION_NOT_FOUND:("Транзакция не найдена","Текущий пакет не содержит транзакцию из файла сессии."),
            SessionRestoreStatus.TRANSACTION_DEFINITION_MISMATCH:("Описание транзакции изменилось","Сохранённая сессия несовместима с текущим описанием транзакции."),
            SessionRestoreStatus.MESSAGE_DEFINITION_MISMATCH:("Описание сообщения изменилось","История содержит сообщение, несовместимое с текущим пакетом."),
            SessionRestoreStatus.ACTION_INVALID:("Некорректный Action","Application layer отклонил Action в истории."),
            SessionRestoreStatus.DIRECTION_INVALID:("Неподдерживаемое направление события","RECEIVED history нельзя восстановить без actor/transport ingestion model."),
            SessionRestoreStatus.RETRY_INVALID:("Некорректная история повторов","Application layer отклонил retry history."),
            SessionRestoreStatus.SIGNAL_INVALID:("Некорректная история сигналов","Application layer отклонил signal history."),
            SessionRestoreStatus.FAULT_INVALID:("Некорректная история ошибок","Application layer отклонил fault history."),
        }
        title,description=descriptions[status];snapshot=opened.snapshot;details=[]
        if snapshot:
            details.extend((f"Процесс: {snapshot.process_code}",f"Версия: {snapshot.process_version}",
                f"Транзакция: {snapshot.transaction_code}",f"ProcedureID: {snapshot.procedure_id}",
                f"ConversationID: {snapshot.conversation_id}",f"Состояние: {snapshot.current_state}",
                f"Событий истории: {len(snapshot.history)}",f"Попыток повтора: {snapshot.retry_attempts}"))
        details.extend(opened.restore.issues)
        return SessionPresentation(status,title,description,tuple(details),opened.continue_ready)

    def continue_session(self):
        opened=self.session_open_result
        if not opened or not opened.continue_ready:raise ValueError("Session is not RESTORABLE/continue_ready.")
        restored=opened.restore.session;snapshot=opened.snapshot
        self.select_process(snapshot.process_code);self.select_transaction(snapshot.transaction_code)
        if restored.transaction.message_history and restored.definition.response_messages:
            self.select_message(restored.definition.response_messages[0])
        self.session=restored;self.session_mode=SessionMode.RESTORED;self.session_open_result=opened
        return restored

    def open_draft_as_new(self,path:Path):
        loaded=self.load_draft(path);session=self.start_session()
        return loaded,session

    def save_session(self,path:Path):
        if not self.session:raise ValueError("Active TransactionSession is required.")
        return self.application.save_transaction_session(self.session,path)

    def generate_xml(self) -> GenerationResult:
        self.active_tab = "DATA"
        if not self.generation_enabled:
            status = "UNRESOLVED_STRUCTURE_VERSION" if self.settings.mode=="STRICT" and self.current_message.generation_status=="VERSION_PLACEHOLDER_TEST" else self.current_message.generation_status
            self.generation = GenerationResult(False, None, status)
            return self.generation
        if self.settings.mode == "STRICT":
            validation=self.validate()
            if not validation.is_valid:
                self.generation=GenerationResult(False,None,validation.status,validation.errors,validation.warnings)
                return self.generation
        direction = self.current_message.direction
        if direction == "initiating":
            if self.session is not None and self.session.transaction.message_history and self.session_mode is SessionMode.RESTORED:
                self.generation=GenerationResult(False,None,"INITIAL_ALREADY_GENERATED")
                return self.generation
            if self.session is None or self.session.transaction.message_history:
                self.start_session()
            self.generation = self.session.generate_initial_message(self.values)
        else:
            if self.session is None or not self.session.transaction.message_history:
                self.generation = GenerationResult(False, None, "INITIAL_MESSAGE_REQUIRED")
            else:
                self.generation = self.session.generate_response(self.message_code, self.values)
        if self.generation.success: self.active_tab = "XML"
        return self.generation

    def apply_settings(self, settings: GuiSettings) -> None:
        root_changed = settings.processes_root != self.settings.processes_root
        drafts_changed=settings.drafts_directory!=self.settings.drafts_directory
        self.settings = settings; self.test_seed = settings.seed
        if root_changed or drafts_changed:
            self.application = EaeuXmlApplication(settings.processes_root,drafts_root=settings.drafts_directory)
            self.processes = self.application.list_processes()
            self.transactions=(); self.messages=(); self.form=None; self.process_code=self.transaction_code=self.message_code=None
            self.process_issues=()
            if self.processes:self.select_process(self.processes[0].process_code)

    def _clear_result(self):
        self.validation = None; self.generation = None
