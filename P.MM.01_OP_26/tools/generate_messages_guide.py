"""Generate the standalone user guide from the same structured guide API as wx GUI."""

from pathlib import Path

from eaeu_xml.application import EaeuXmlApplication


PACKAGE=Path(__file__).parents[1]; ROOT=PACKAGE.parent
OUTPUT=PACKAGE/"process_memory"/"P_MM_01_MESSAGES_GUIDE.md"


def text(value): return str(value if value not in (None,"") else "—").replace("|","\\|").replace("\n"," ")


def tree_lines(fields,root):
    lines=[root]
    def add(items,prefix):
        for index,field in enumerate(items):
            last=index==len(items)-1; branch="└── " if last else "├── "; suffix=" (XML-атрибут)" if field.xml_kind=="XML-атрибут" else ""
            lines.append(prefix+branch+("@" if field.xml_kind=="XML-атрибут" else "")+(field.xml_name or field.display_name)+suffix)
            add(field.children,prefix+("    " if last else "│   "))
    add(fields,"");return lines


def field_table(fields):
    rows=[]
    def walk(items):
        for field in items:
            repeat=" Может быть указано несколько значений." if field.repeatable else ""
            classifier=" Набор значений классификатора не включён в текущий пакет." if field.normative_input_policy=="CLASSIFIER" and not field.classifier_dataset_available else ""
            condition=f" Условие: {field.condition}" if field.condition else ""
            assistance=(" "+field.input_assistance) if field.input_assistance else ""
            rows.append("| "+" | ".join(text(value) for value in (field.display_name,field.path,f"{field.requirement} ({field.cardinality})",field.who_fills,field.what_to_enter+assistance+repeat+classifier+condition,field.example_value,field.value_source))+" |")
            walk(field.children)
    walk(fields);return rows


def main():
    app=EaeuXmlApplication(ROOT);guide=app.get_process_guide("P.MM.01")
    lines=["# Сводка по заполнению сообщений общего процесса P.MM.01","","## Назначение документа","",
           "Инструкция предназначена для сотрудников, формирующих XML-сообщения общего процесса P.MM.01 в EAEU XML Creator. Она описывает сообщения MSG.001–MSG.028, состав и назначение реквизитов Body, обязательность, способ получения значения и примеры заполнения.","",
           "Служебный SOAP Header формируется программой. Пользователь преимущественно работает с реквизитами Body. Часть значений формируется автоматически, часть вводится пользователем, определяется по классификаторам, зависит от условий либо поступает из внешних информационных систем.","",
           "## Общий процесс P.MM.01","",f"- Код: `{guide.process_code}`",f"- Официальное название: {guide.name}",f"- Версия: {guide.version or 'Версия не установлена в текущем профиле.'}",f"- Процедур: {guide.procedure_count}",f"- Транзакций: {guide.transaction_count}",f"- Сообщений: {guide.message_count}","",
           "## Как формируется служебная часть XML","","Пользователь обычно не заполняет SOAP Header вручную. Программа формирует:","",
           "- `To` — адрес получателя согласно участникам транзакции;","- `ReplyTo` — адрес отправителя для ответа;","- `MessageID` — уникальный идентификатор SOAP-сообщения;","- `Action` — действие, составленное из процесса, версии, процедуры, транзакции и сообщения;","- `ProcedureID` — идентификатор экземпляра процедуры;","- `ConversationID` — идентификатор экземпляра транзакции;","- `RelatesTo` — связь ответного SOAP-сообщения с исходным сообщением.","",
           "Эти идентификаторы не заменяют Body-реквизиты `EDocId` и `EDocRefId`.","","## Транзакции","","| TRN | Procedure | Тип транзакции | Исходное MSG | Ответное MSG | Участник-инициатор | Участник-получатель |","|---|---|---|---|---|---|---|"]
    for item in guide.transactions:
        lines.append("| "+" | ".join(text(value) for value in (item.transaction_code,item.procedure_code,item.pattern,item.initiating_message,", ".join(item.response_messages),item.initiating_participant,item.responding_participant))+" |")
    trn004=next((item for item in guide.transactions if item.transaction_code.endswith(".TRN.004")),None)
    if trn004:
        lines += ["","### Пример формирования Header для TRN.004","",f"Для `{trn004.initiating_message}`:","",f"- `To`: `{trn004.initiating_to}`",f"- `ReplyTo`: `{trn004.initiating_reply_to}`",f"- `Action`: `{trn004.initiating_action}`","",f"Для ответного сообщения направление меняется: `To` = `{trn004.response_to}`, `ReplyTo` = `{trn004.response_reply_to}`."]
    for message in guide.messages:
        lines += ["",f"# {message.message_code}","",f"## Назначение сообщения","",message.purpose,"","## Где используется",""]
        for usage in message.usages:
            direction=(f"от {usage.initiating_participant} к {usage.responding_participant}" if usage.role=="Исходное сообщение" else f"от {usage.responding_participant} к {usage.initiating_participant}")
            lines.append(f"- {usage.transaction_code}, {usage.procedure_code}; {usage.role}; направление: {direction}.")
        if message.conflicts:
            lines += ["","> **В нормативном источнике обнаружено внутреннее несоответствие.**",">"]
            for conflict in message.conflicts:
                refs="; ".join(f"{s.document}, {s.location}"+(f", таблица {s.table}" if s.table else "")+(f", пункт/строка {s.item}" if s.item else "")+(f", страница {s.page}" if s.page is not None else "") for s in conflict.sources)
                lines.append(f"> {conflict.conflict_id}. Реквизит: {', '.join(conflict.referenced_fields) or 'не указан'}. {conflict.description} Источник: {refs or 'указан в модели сообщения'}. Подбирать похожий реквизит самостоятельно не следует.")
        lines += ["","## Структура электронного документа","",f"- Сообщение: `{message.message_code}`",f"- Структура: `{message.structure_id}`",f"- Версия: {message.version_description}",f"- Правила сообщения: {message.message_rules_status_display}",f"- Корневой XML-элемент: `{message.root_element or 'не указан'}`","",f"Всего реквизитов: {message.total_fields}. Пользователь заполняет: {message.user_input}; выбирает: {message.user_select}; автоматически: {message.automatic}; классификаторы: {message.classifier_fields}; условные: {message.conditional}; внешние источники: {message.external_system}; способ заполнения не определён: {message.unresolved}.",""]
        auto=[f for f in flatten(message.fields) if f.ui_input_policy in {"READ_ONLY","AUTO"}]
        if auto:
            lines += ["## Автоматически заполняемые реквизиты","","| Реквизит | XML path | Пояснение |","|---|---|---|"]
            for field in auto:lines.append(f"| {text(field.display_name)} | {text(field.path)} | {text(field.what_to_enter)} |")
            lines.append("")
        conditional=[f for f in flatten(message.fields) if f.normative_input_policy=="CONDITIONAL"]
        if conditional:
            lines += ["## Условные реквизиты","","| Реквизит | Обязательность | Условие | Автоматическая проверка |","|---|---|---|---|"]
            for field in conditional:lines.append(f"| {text(field.display_name)} | Условно | {text(field.condition)} | {'Да' if field.automatic_condition_check else 'Нет'} |")
            lines.append("")
        classifiers=[f for f in flatten(message.fields) if f.normative_input_policy=="CLASSIFIER"]
        if classifiers:
            lines += ["## Реквизиты классификаторов","","Значения определяются по соответствующим классификаторам. Если набор данных не включён в пакет, показанный пример является только тестовым и не подтверждает нормативную допустимость значения.",""]
        lines += ["## Структура XML Body","","```text",*tree_lines(message.fields,message.root_element or message.structure_id),"```","","## Полная таблица реквизитов","","| Реквизит | XML path | Обязательность | Кто заполняет | Что указывать | Пример | Источник значения |","|---|---|---|---|---|---|---|",*field_table(message.fields),"","## Пример заполнения Body",""]
        if message.body_example:lines += ["```xml",message.body_example,"```",""]
        else:lines += [message.body_example_status,""]
        lines += ["Полный TEST SOAP XML формируется существующей функцией создания XML в программе; отдельный генератор примеров в инструкции не используется.","","## Нормативный источник",""]
        for source in message.sources:
            lines.append(f"- {source.document}; {source.location}"+(f"; таблица {source.table}" if source.table else "")+(f"; пункт/строка {source.item}" if source.item else "")+(f"; страница {source.page}" if source.page is not None else "")+".")
    OUTPUT.write_text("\n".join(lines).rstrip()+"\n",encoding="utf-8")


def flatten(fields):
    for field in fields:
        yield field;yield from flatten(field.children)


if __name__=="__main__":main()
