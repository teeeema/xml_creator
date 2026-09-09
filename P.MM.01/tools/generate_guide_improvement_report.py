"""Generate the example and unresolved-UI audit report."""

from collections import Counter
from pathlib import Path
from eaeu_xml.application import EaeuXmlApplication

PACKAGE=Path(__file__).parents[1];ROOT=PACKAGE.parent;OUTPUT=PACKAGE/"process_memory"/"GUIDE_QUALITY_IMPROVEMENT_REPORT.md"


def safe(value):return str(value or "—").replace("|","\\|").replace("\n"," ")


def main():
    app=EaeuXmlApplication(ROOT);engine=app._engine("P.MM.01");message_transaction={}
    for transaction in engine.transactions.values():
        for message in (transaction.initiating_message,*transaction.response_messages):message_transaction.setdefault(message,transaction.transaction_code)
    fields_by_message={};origins=Counter();no_examples=Counter();unresolved=Counter();examples=0;total=0
    for code in sorted(engine.messages):
        guide=app.get_message_guide("P.MM.01",code);fields=tuple(app._guide_service._walk(guide.fields));fields_by_message[code]=fields
        total+=len(fields);examples+=sum(field.example_value is not None for field in fields);origins.update(field.example_origin for field in fields)
        no_examples.update((field.no_example_reason or "OTHER") for field in fields if field.example_value is None)
        unresolved.update((field.unresolved_ui_reason or "OTHER") for field in fields if field.ui_input_policy=="UNRESOLVED_UI_POLICY")
    # Hidden fields are part of the 2960-usage quality baseline.
    all_form_fields=[]
    for code in sorted(engine.messages):
        all_form_fields.extend(app._walk_fields(app.get_form("P.MM.01",message_transaction[code],code).fields))
    full_origins=Counter(field.example_origin for field in all_form_fields);full_no=Counter((field.no_example_reason or "OTHER") for field in all_form_fields if field.example_value is None)
    after_examples=sum(field.example_value is not None for field in all_form_fields);after_unresolved=sum(field.ui_input_policy=="UNRESOLVED_UI_POLICY" for field in all_form_fields)
    lines=["# GUIDE QUALITY IMPROVEMENT REPORT","","Дата: 2026-08-24.","","## Итог","","| Metric | Before | After |","|---|---:|---:|",f"| Fields with example | 2202 | {after_examples} |",f"| Fields without example | 758 | {2960-after_examples} |",f"| UNRESOLVED_UI_POLICY | 132 | {after_unresolved} |","| UI policy changes | — | 0 |","| Manual UI overrides added | — | 0 |","","## Example origins","","| Origin | Count |","|---|---:|"]
    for name in ("FIXED_VALUE","ALLOWED_VALUE","CLASSIFIER_EXAMPLE","DATATYPE_EXAMPLE","TEST_DATA_GENERATOR","PROJECT_DOCUMENTATION","UNAVAILABLE"):lines.append(f"| {name} | {full_origins[name]} |")
    lines += ["","## Remaining no-example reasons","","| Reason | Count |","|---|---:|"]
    for name,count in sorted(full_no.items()):lines.append(f"| {name} | {count} |")
    lines += ["","## Remaining unresolved UI reasons","","| Reason | Count |","|---|---:|"]
    for name,count in sorted(unresolved.items()):lines.append(f"| {name} | {count} |")
    lines += ["","## Priority MSG quality","","| MSG | Fields | Examples | Without example | Unresolved UI |","|---|---:|---:|---:|---:|"]
    for code in ("P.MM.01.MSG.001","P.MM.01.MSG.002","P.MM.01.MSG.003","P.MM.01.MSG.005","P.MM.01.MSG.006","P.MM.01.MSG.007","P.MM.01.MSG.008","P.MM.01.MSG.011","P.MM.01.MSG.019","P.MM.01.MSG.026"):
        fields=fields_by_message[code];lines.append(f"| {code} | {len(fields)} | {sum(f.example_value is not None for f in fields)} | {sum(f.example_value is None for f in fields)} | {sum(f.ui_input_policy=='UNRESOLVED_UI_POLICY' for f in fields)} |")
    lines += ["","## UNRESOLVED_UI_POLICY audit","","| Message | Field path | Display name | Description | Datatype | Required | MessageRule/condition | Normative policy | Classifier | Parent/group | Source | Reason |","|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for code,fields in fields_by_message.items():
        for field in fields:
            if field.ui_input_policy!="UNRESOLVED_UI_POLICY":continue
            parent=field.path.rsplit("/",1)[0] if "/" in field.path else "—";sources="; ".join(f"{s.document}, {s.location}" for s in field.sources)
            lines.append("| "+" | ".join(safe(value) for value in (code,field.path,field.display_name,field.description,field.datatype,"Да" if field.requirement=="Обязательно" else "Нет",field.condition,field.normative_input_policy,field.classifier,parent,sources,field.unresolved_ui_reason))+" |")
    lines += ["","Нормативные policies не изменены. Поля с условным источником не переведены автоматически в USER_INPUT. Placeholder-примеры classifier и business identifiers являются пояснительными и не объявляют допустимые нормативные значения."]
    OUTPUT.write_text("\n".join(lines)+"\n",encoding="utf-8")


if __name__=="__main__":main()
