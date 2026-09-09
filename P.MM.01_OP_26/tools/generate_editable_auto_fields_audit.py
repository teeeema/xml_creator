"""Generate UI-only assisted-input and READ_ONLY audit from public DTOs."""

from collections import Counter
from pathlib import Path

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.application.input_helpers import datatype_category


PACKAGE=Path(__file__).parents[1];ROOT=PACKAGE.parent;OUTPUT=PACKAGE/"process_memory/EDITABLE_AUTO_FIELDS_AUDIT.md"


def walk(fields):
    for field in fields:
        yield field;yield from walk(field.children)


def generate():
    app=EaeuXmlApplication(ROOT);seen=set();read_only=[];date_rows=[];counts=Counter()
    for transaction in app.list_transactions("P.MM.01"):
        for message in app.list_messages("P.MM.01",transaction.transaction_code):
            if message.message_code in seen:continue
            seen.add(message.message_code)
            form=app.get_form("P.MM.01",transaction.transaction_code,message.message_code)
            for field in walk(form.fields):
                key=(message.message_code,field.path)
                if field.ui_input_policy=="READ_ONLY":
                    category=("AUTO_ONLY" if field.normative_input_policy=="AUTO_FIXED" else
                              "CORRELATION_ONLY" if field.normative_input_policy=="CORRELATION" else "OTHER")
                    counts[category]+=1;read_only.append((key,field,category))
                if field.show_identifier_generator:counts["AUTO_ASSISTED_EDITABLE"]+=1
                if field.ui_input_policy=="EXTERNAL_SYSTEM":counts["EXTERNAL_SYSTEM"]+=1
                category=datatype_category(field.datatype)
                if category:
                    date_rows.append((message.message_code,field,category))
    lines=["# Аудит READ_ONLY и вспомогательного ввода","",
           "Этот отчёт описывает только presentation behaviour. Normative FieldInputPolicy и value source не изменены.","",
           f"- AUTO_ONLY: {counts['AUTO_ONLY']}",f"- AUTO_ASSISTED_EDITABLE: {counts['AUTO_ASSISTED_EDITABLE']}",
           f"- CORRELATION_ONLY: {counts['CORRELATION_ONLY']}",f"- EXTERNAL_SYSTEM: {counts['EXTERNAL_SYSTEM']}",
           f"- OTHER READ_ONLY: {counts['OTHER']}",f"- DATE/TIME/DATETIME usages: {len(date_rows)}","",
           "## READ_ONLY usages","","| MSG | Field | Normative policy | UI policy | Origin | Classification | Reason |",
           "|---|---|---|---|---|---|---|"]
    for (message,path),field,category in read_only:
        lines.append(f"| {message} | `{path}` | {field.normative_input_policy} | {field.ui_input_policy} | {field.ui_policy_origin} | {category} | {field.ui_policy_reason or 'derived from model'} |")
    lines += ["","## Assisted identifiers","","| MSG | Field | Normative policy | UI policy | Manual | Generator | Reason |","|---|---|---|---|---:|---:|---|"]
    for transaction in app.list_transactions("P.MM.01"):
        for message in app.list_messages("P.MM.01",transaction.transaction_code):
            if message.message_code not in seen:continue
            form=app.get_form("P.MM.01",transaction.transaction_code,message.message_code)
            for field in walk(form.fields):
                if field.show_identifier_generator:
                    lines.append(f"| {message.message_code} | `{field.path}` | {field.normative_input_policy} | {field.ui_input_policy} | да | да | {field.ui_policy_reason} |")
            seen.remove(message.message_code)
    lines += ["","## DATE/TIME/DATETIME usages","","| MSG | Field | Datatype | UI policy | Value source | Manual | Today | Now | Timezone | Reason |","|---|---|---|---|---|---:|---:|---:|---:|---|"]
    for message,field,category in date_rows:
        lines.append(f"| {message} | `{field.path}` | {field.datatype} ({category}) | {field.ui_input_policy} | {field.value_source} | {'да' if field.manual_edit_allowed else 'нет'} | {'да' if field.show_today_button else 'нет'} | {'да' if field.show_now_button else 'нет'} | {'да' if field.show_timezone_picker else 'нет'} | {field.ui_policy_reason or 'capabilities derived from datatype and UI/value-source policy'} |")
    return "\n".join(lines)+"\n"


if __name__=="__main__":OUTPUT.write_text(generate(),encoding="utf-8");print(OUTPUT)
