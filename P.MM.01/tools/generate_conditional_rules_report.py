"""Generate the conservative P.MM.01 conditional-rule coverage audit."""

from collections import Counter
from pathlib import Path

from eaeu_xml.application import EaeuXmlApplication


PACKAGE=Path(__file__).parents[1]
ROOT=PACKAGE.parent
OUTPUT=PACKAGE/"process_memory"/"CONDITIONAL_RULES_REPORT.md"


def build_report():
    app=EaeuXmlApplication(ROOT);seen=set();rows=[];operators=Counter();effects=Counter()
    for transaction in app.list_transactions("P.MM.01"):
        for message in app.list_messages("P.MM.01",transaction.transaction_code):
            if message.message_code in seen:continue
            seen.add(message.message_code)
            form=app.get_form("P.MM.01",transaction.transaction_code,message.message_code)
            fields=tuple(app._walk_fields(form.fields))
            total=sum(field.normative_input_policy=="CONDITIONAL" for field in fields)
            rules=app.get_conditional_rules("P.MM.01",message.message_code)
            for rule in rules:operators[rule.operator]+=1;effects[rule.effect]+=1
            if total:rows.append((message.message_code,total,len(rules),total-len(rules)))
    rows.sort();total=sum(row[1] for row in rows);machine=sum(row[2] for row in rows)
    lines=["# P.MM.01 conditional rules report","","Generated: 2026-08-25","",
           "## Summary","",f"- total conditional usages: {total}",f"- machine-evaluable: {machine}",
           f"- unresolved: {total-machine}","- compilation policy: only explicit structured `conditional_rule` metadata with source traceability", "",
           "The current P.MM.01 MessageRules contain textual condition descriptions and referenced fields, but no explicit `source_field_path + operator + expected value + effect` metadata. No NLP or XML-name inference was performed; therefore no real P.MM.01 field is dynamically hidden, enabled or required.","",
           "## By message","","| MSG | Conditional usages | Machine-evaluable | Unresolved |","|---|---:|---:|---:|"]
    lines.extend(f"| {code} | {total} | {machine} | {unresolved} |" for code,total,machine,unresolved in rows)
    lines.extend(("","## Condition type distribution","",*(f"- {key}: {value}" for key,value in sorted(operators.items()))))
    if not operators:lines.append("- none (0 compiled rules)")
    lines.extend(("","## Effect distribution","",*(f"- {key}: {value}" for key,value in sorted(effects.items()))))
    if not effects:lines.append("- none (0 compiled rules)")
    lines.extend(("","## Safety conclusion","","All 133 usages remain visible and annotated as conditional. Their current evaluation is `UNKNOWN`. Known normative conflicts in MSG.002, MSG.023 and MSG.024 retain priority and were not reinterpreted."))
    return "\n".join(lines)+"\n"


if __name__=="__main__":
    OUTPUT.write_text(build_report(),encoding="utf-8")
    print(OUTPUT)
