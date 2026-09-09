from xml.etree import ElementTree as ET

from eaeu_xml.application.models import (
    ConflictGuide, FieldGuide, GuideSearchHit, GuideSourceView, MessageGuide,
    MessageUsageGuide, ProcessGuide, TransactionGuide,
)
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.services.logical_address_builder import LogicalAddressBuilder


class GuideService:
    """Builds user-facing guides exclusively from loaded package/application data."""

    def __init__(self, application):
        self.application = application

    def get_process_guide(self, process_code: str) -> ProcessGuide:
        engine = self.application._engine(process_code)
        messages = tuple(self.get_message_guide(process_code, code) for code in sorted(engine.messages))
        transactions = tuple(self._transaction_guide(engine,item)
                             for item in sorted(engine.transactions.values(), key=lambda value: value.transaction_code))
        return ProcessGuide(process_code, engine.process.name or process_code, engine.package.profile.process_version,
                            len(engine.procedures), len(engine.transactions), len(engine.messages), transactions, messages)

    @staticmethod
    def _transaction_guide(engine,item):
        def address(participant_code):
            if not participant_code:return None
            participant=engine.participants[participant_code]
            segment=participant.fixed_segment if participant.segment_policy=="FIXED" else participant.test_segment
            if not segment:return None
            return LogicalAddressBuilder().build_common_process(segment=segment,process_code=engine.process.process_code,
                                                                 participant_code=participant_code).serialize()
        initiating=address(item.initiating_participant);responding=address(item.responding_participant)
        action=engine.build_application_action(item.transaction_code,item.initiating_message).serialize() if item.initiating_message else None
        return TransactionGuide(item.transaction_code,item.procedure_code,item.pattern,item.initiating_message,
                                item.response_messages,item.initiating_participant,item.responding_participant,
                                responding,initiating,action,initiating,responding)

    def get_message_guide(self, process_code: str, message_code: str) -> MessageGuide:
        engine = self.application._engine(process_code)
        message = engine.get_message(message_code)
        usages = self._usages(engine, message_code)
        if not usages: raise KeyError(message_code)
        transaction_code = usages[0].transaction_code
        form = self.application.get_form(process_code, transaction_code, message_code)
        structure = self.application._structure_for_form(engine, message_code)
        definitions = {field.path: field for field in structure.fields}
        conflicts = self._conflicts(engine, message_code)
        condition_rules={rule.target_field_path:rule for rule in self.application.get_conditional_rules(process_code,message_code)}

        def convert(view):
            definition = definitions[view.path]
            condition_rule=condition_rules.get(view.path)
            requirement = "Не используется" if view.visibility == "HIDDEN" else (
                "Условно" if view.normative_input_policy == "CONDITIONAL" else
                "Обязательно" if view.required else "Необязательно")
            who = {"USER_INPUT":"Пользователь", "USER_SELECT":"Пользователь выбирает из списка",
                   "AUTO":"Программа", "READ_ONLY":"Программа", "EXTERNAL_SYSTEM":"Внешняя информационная система",
                   "CONDITIONAL":"Зависит от условия", "GROUP":"Структурный блок", "HIDDEN":"Служебный реквизит",
                   "UNRESOLVED_UI_POLICY":"Способ заполнения не определён"}[view.ui_input_policy]
            description = view.description or "Описание реквизита отсутствует в текущей нормативной модели."
            what = description
            if view.ui_input_policy == "USER_INPUT": what = "Укажите значение реквизита: " + description
            elif view.ui_input_policy == "USER_SELECT": what = "Выберите значение из доступного списка: " + description
            elif view.ui_input_policy in {"READ_ONLY","AUTO"}: what = "Значение формируется автоматически. " + description
            elif view.ui_input_policy == "EXTERNAL_SYSTEM": what = "Значение должно поступить из внешней информационной системы. " + description
            if view.input_policy == "CLASSIFIER": what = "Значение определяется по соответствующему классификатору. " + description
            if view.kind == "ARBITRARY_XML" or (view.datatype or "").upper() == "ANY_XML":
                what = "Реквизит допускает XML-содержимое, структура которого не определяется данной StructureDefinition."
            assistance = ("Можно ввести вручную или сформировать идентификатор автоматически."
                          if view.show_identifier_generator else
                          "Значение можно ввести вручную или заполнить текущей датой и временем с выбором часового пояса."
                          if view.show_now_button and view.show_timezone_picker else
                          "Значение можно ввести вручную или заполнить текущей датой."
                          if view.show_today_button else None)
            return FieldGuide(
                message_code, view.path, view.xml_name, view.display_name, description, view.datatype,
                "XML-атрибут" if view.is_attribute else "XML-элемент", requirement,
                view.cardinality_display or "—", view.repeatable, who, view.normative_input_policy,
                view.ui_input_policy, view.value_source, what, view.example_value,
                "Пример тестового значения" if view.normative_input_policy == "CLASSIFIER" else "Пример",
                example_origin=view.example_origin, no_example_reason=view.no_example_reason,
                unresolved_ui_reason=("NORMATIVE_CONFLICT" if conflicts and view.ui_input_policy == "UNRESOLVED_UI_POLICY" else view.unresolved_ui_reason),
                condition=view.condition_description, classifier=view.classifier,
                classifier_dataset_available=engine.package.classifiers_available,
                sources=self._sources(definition.source_refs), children=convert_list(view.children),
                automatic_condition_check=view.path in condition_rules,
                condition_source_field=condition_rule.source_field_path if condition_rule else None,
                condition_operator_description=({"EQUALS":"равно","NOT_EQUALS":"не равно","IN":"входит в перечень","NOT_IN":"не входит в перечень","PRESENT":"заполнено","ABSENT":"не заполнено","TRUE":"истина","FALSE":"ложь"}.get(condition_rule.operator) if condition_rule else None),
                condition_expected_value=(condition_rule.expected_value if condition_rule and condition_rule.operator in {"EQUALS","NOT_EQUALS"} else (condition_rule.values if condition_rule else None)),
                xml_qname=view.xml_qname,
                input_assistance=assistance,
            )
        def convert_list(views):
            result=[]
            for view in views:
                if view.visibility == "HIDDEN": result.extend(convert_list(view.children))
                else: result.append(convert(view))
            return tuple(result)
        fields = convert_list(form.fields)
        flat = tuple(self._walk(fields))
        summary = self.application.get_message_input_summary(process_code, transaction_code, message_code)
        body_example, body_status = self._body_example(process_code, transaction_code, message_code, conflicts)
        active = engine.package.profile.structures[message.structure_id].active_version
        version = active or structure.version
        version_description = (f"{version} — версия не установлена в текущем профиле. "
                               "Y.Y.Y обозначает номер версии структуры электронного документа (сведений), "
                               "определяемый с учётом версии базисной модели данных. X.X.X обозначает номер "
                               "версии базисной модели данных, использованной для импортируемых пространств имён."
                               if active is None else version)
        rules_status_labels = {
            "HAS_SEPARATE_RULE_TABLE": "Есть отдельная нормативная таблица правил",
            "NO_SEPARATE_RULE_TABLE": "Отдельная нормативная таблица правил отсутствует",
            "NEEDS_VERIFICATION": "Статус правил требует проверки",
            "NORMATIVE_CONFLICT": "Обнаружен нормативный конфликт правил",
        }
        return MessageGuide(
            message_code, message.name, message.purpose or message.name, message.structure_id, active,
            version_description, structure.root_element, usages, fields, len(flat), summary.user_input,
            summary.user_select, summary.automatic_fields,
            sum(field.normative_input_policy == "CLASSIFIER" for field in flat),
            sum(field.normative_input_policy == "CONDITIONAL" for field in flat), summary.external_system,
            summary.unresolved, body_example, body_status, conflicts, self._sources(message.source_refs),
            message_rules_status=message.message_rules_status,
            message_rules_status_display=rules_status_labels[message.message_rules_status],
            message_rules_sources=self._sources(message.message_rules_source_refs),
        )

    def get_field_guide(self, process_code: str, message_code: str, field_path: str) -> FieldGuide:
        guide = self.get_message_guide(process_code, message_code)
        try: return next(field for field in self._walk(guide.fields) if field.path == field_path)
        except StopIteration as error: raise KeyError(field_path) from error

    def search_guide(self, process_code: str, query: str) -> tuple[GuideSearchHit, ...]:
        needle = query.strip().casefold()
        if not needle: return ()
        hits = []
        for message in self.get_process_guide(process_code).messages:
            if needle in f"{message.message_code} {message.name} {message.purpose}".casefold():
                hits.append(GuideSearchHit(message.message_code, None, f"{message.message_code} — {message.name}", message.purpose))
            for field in self._walk(message.fields):
                haystack = " ".join(filter(None, (field.xml_name, field.path, field.display_name, field.description)))
                if needle in haystack.casefold():
                    hits.append(GuideSearchHit(message.message_code, field.path, field.display_name, field.description))
        return tuple(hits)

    def _body_example(self, process_code, transaction_code, message_code, conflicts):
        if conflicts: return None, "Недоступен: нормативное несоответствие не обходится."
        try:
            values = self.application.generate_test_data(process_code, transaction_code, message_code, seed=12345)
            body = self.application._engine(process_code).build_body(message_code, values, mode=GenerationMode.TEST)
            element = ET.fromstring(ET.tostring(body.serialize_xml_element()))
            ET.indent(element, space="  ")
            return ET.tostring(element, encoding="unicode"), "TEST example generated by Application Facade data."
        except Exception as error:
            return None, f"Пример Body недоступен: {getattr(error, 'code', type(error).__name__)}."

    @staticmethod
    def _walk(fields):
        for field in fields:
            yield field
            yield from GuideService._walk(field.children)

    @staticmethod
    def _sources(refs):
        values = []
        for ref in refs:
            view = GuideSourceView(ref.document, ref.section or ref.location, ref.table, ref.item, ref.page)
            if view not in values: values.append(view)
        return tuple(values)

    def _usages(self, engine, message_code):
        result = []
        for transaction in sorted(engine.transactions.values(), key=lambda value: value.transaction_code):
            if message_code == transaction.initiating_message:
                role = "Исходное сообщение"
            elif message_code in transaction.response_messages:
                role = "Ответное сообщение" if len(transaction.response_messages) == 1 else "Альтернативное ответное сообщение"
            else: continue
            result.append(MessageUsageGuide(transaction.transaction_code, transaction.procedure_code, role,
                                            transaction.initiating_participant, transaction.responding_participant))
        return tuple(result)

    def _conflicts(self, engine, message_code):
        rules = engine.rules.get(message_code)
        result = []
        for rule in rules.business_rules if rules else ():
            if rule.get("interpretation_status") != "INTERNAL_NORMATIVE_CONFLICT": continue
            refs = []
            for item in rule.get("source_refs") or ():
                refs.append(GuideSourceView(item.get("document", ""), item.get("section") or item.get("location", ""),
                                            item.get("table"), item.get("item"), item.get("page")))
            result.append(ConflictGuide(rule.get("conflict_id") or rule.get("rule_id", "NORMATIVE_CONFLICT"),
                                        tuple(rule.get("referenced_identifiers") or ()),
                                        rule.get("conflict_details") or "В нормативном источнике обнаружено внутреннее несоответствие.", tuple(refs)))
        return tuple(result)
