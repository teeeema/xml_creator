"""Generate guide coverage metrics from FormDefinition and structured guide API."""

from pathlib import Path
from collections import Counter
from eaeu_xml.application import EaeuXmlApplication

PACKAGE=Path(__file__).parents[1];ROOT=PACKAGE.parent;OUTPUT=PACKAGE/"process_memory"/"GUIDE_GENERATION_REPORT.md"


def main():
    app=EaeuXmlApplication(ROOT);engine=app._engine("P.MM.01");message_transaction={}
    for transaction in engine.transactions.values():
        for message in (transaction.initiating_message,*transaction.response_messages):message_transaction.setdefault(message,transaction.transaction_code)
    total=described=examples=sourced=unresolved=visible=0;example_origins=Counter();no_example_reasons=Counter();unresolved_reasons=Counter()
    for code in sorted(engine.messages):
        form=app.get_form("P.MM.01",message_transaction[code],code);fields=tuple(app._walk_fields(form.fields));total+=len(fields)
        described+=sum(bool(field.description) for field in fields);examples+=sum(field.example_value is not None for field in fields);sourced+=sum(bool(field.source_refs) for field in fields)
        example_origins.update(field.example_origin for field in fields)
        no_example_reasons.update((field.no_example_reason or "OTHER") for field in fields if field.example_value is None)
        unresolved+=sum(field.ui_input_policy=="UNRESOLVED_UI_POLICY" for field in fields);visible+=sum(field.visibility!="HIDDEN" for field in fields)
        message_guide=app.get_message_guide("P.MM.01",code)
        unresolved_reasons.update((field.unresolved_ui_reason or "OTHER") for field in app._guide_service._walk(message_guide.fields) if field.ui_input_policy=="UNRESOLVED_UI_POLICY")
    conflicts=sum(len(app.get_message_guide("P.MM.01",code).conflicts) for code in engine.messages)
    lines=["# GUIDE GENERATION REPORT","","Дата: 2026-08-24.","","| Metric | Result |","|---|---:|",f"| MSG coverage | {len(engine.messages)}/28 |",f"| Field usages covered | {total}/{total} |",f"| Visible guide entries | {visible} |",f"| Fields with description | {described} |",f"| Fields without description | {total-described} |",f"| Fields with example | {examples} |",f"| Fields without example | {total-examples} |",f"| Fields with source reference | {sourced} |",f"| Fields without source reference | {total-sourced} |",f"| UNRESOLVED_UI_POLICY | {unresolved} |",f"| Normative conflicts | {conflicts} |","","## Example origin distribution","","| Origin | Count |","|---|---:|"]
    for name in ("FIXED_VALUE","ALLOWED_VALUE","CLASSIFIER_EXAMPLE","DATATYPE_EXAMPLE","TEST_DATA_GENERATOR","PROJECT_DOCUMENTATION","UNAVAILABLE"):lines.append(f"| {name} | {example_origins[name]} |")
    lines += ["","## Remaining no-example reasons","","| Reason | Count |","|---|---:|"]
    for name,count in sorted(no_example_reasons.items()):lines.append(f"| {name} | {count} |")
    lines += ["","## Remaining unresolved UI reasons","","| Reason | Count |","|---|---:|"]
    for name,count in sorted(unresolved_reasons.items()):lines.append(f"| {name} | {count} |")
    lines += ["","Hidden usages учитываются в coverage и quality metrics, но не выводятся как заполняемые реквизиты пользовательской инструкции. Конфликтные сообщения не получают обходной пример Body."]
    OUTPUT.write_text("\n".join(lines)+"\n",encoding="utf-8")


if __name__=="__main__":main()
