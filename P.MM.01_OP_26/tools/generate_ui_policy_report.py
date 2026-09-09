"""Generate the auditable UI policy report from the public application facade."""

from collections import Counter
from pathlib import Path

from eaeu_xml.application import EaeuXmlApplication


PACKAGE = Path(__file__).parents[1]
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "process_memory" / "UI_INPUT_POLICY_REPORT.md"


def clean(value):
    return str(value or "—").replace("|", "\\|").replace("\n", " ")


def main():
    app = EaeuXmlApplication(ROOT)
    engine = app._engine("P.MM.01")
    message_transaction = {}
    for transaction in engine.transactions.values():
        for message in (transaction.initiating_message, *transaction.response_messages):
            message_transaction.setdefault(message, transaction.transaction_code)

    ui_counts = Counter()
    origin_counts = Counter()
    normative_counts = Counter()
    manual_paths = Counter()
    message_rows = []
    field_sections = []
    for message_code in sorted(engine.messages):
        form = app.get_form("P.MM.01", message_transaction[message_code], message_code)
        fields = tuple(app._walk_fields(form.fields))
        counts = Counter(field.ui_input_policy for field in fields)
        ui_counts.update(counts)
        origin_counts.update(field.ui_policy_origin for field in fields)
        normative_counts.update(field.normative_input_policy for field in fields)
        message_rows.append((message_code, len(fields), *(counts[name] for name in (
            "USER_INPUT", "USER_SELECT", "AUTO", "READ_ONLY", "CONDITIONAL",
            "EXTERNAL_SYSTEM", "GROUP", "HIDDEN", "UNRESOLVED_UI_POLICY"))))
        manual = [field for field in fields if field.ui_input_policy in {"USER_INPUT", "USER_SELECT"}]
        manual_paths.update(field.path for field in manual if field.ui_input_policy == "USER_INPUT")
        lines = [f"### {message_code}", "", "| Field | Display name | Required | Normative policy | UI policy | Policy origin | What to enter | Example |",
                 "|---|---|---:|---|---|---|---|---|"]
        for field in fields:
            lines.append("| " + " | ".join(clean(value) for value in (
                field.path, field.display_name, "yes" if field.required else "no",
                field.normative_input_policy, field.ui_input_policy, field.ui_policy_origin,
                field.description or field.ui_policy_reason, field.example_value,
            )) + " |")
        field_sections.extend(lines + [""])

    lines = ["# UI INPUT POLICY REPORT", "", "Дата: 2026-08-24. Отчёт сформирован из Application Facade; normative и UI policies подсчитаны раздельно.", "",
             "## Метрики UI", "", "| UI policy | Count |", "|---|---:|"]
    for name in ("USER_INPUT", "USER_SELECT", "AUTO", "READ_ONLY", "EXTERNAL_SYSTEM", "CONDITIONAL", "GROUP", "HIDDEN", "UNRESOLVED_UI_POLICY"):
        lines.append(f"| {name} | {ui_counts[name]} |")
    lines += [f"| **Total field usages** | **{sum(ui_counts.values())}** |", "",
              f"Normative `UNRESOLVED_INPUT_POLICY` остаётся **{normative_counts['UNRESOLVED_INPUT_POLICY']}**.", "",
              "## Policy origin", "", "| Origin | Count |", "|---|---:|"]
    for name in ("NORMATIVE", "DERIVED_FROM_MODEL", "PROJECT_UI_DEFAULT", "MANUAL_OVERRIDE"):
        lines.append(f"| {name} | {origin_counts[name]} |")
    lines += ["", "## По сообщениям", "", "| MSG | Total | User input | User select | Auto | Read-only | Conditional | External | Group | Hidden | Unresolved |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for row in message_rows: lines.append("| " + " | ".join(map(str, row)) + " |")
    lines += ["", "## TOP-20 USER_INPUT fields", "", "| Uses | Field path |", "|---:|---|"]
    lines.extend(f"| {count} | {clean(path)} |" for path, count in manual_paths.most_common(20))
    lines += ["", "## Все поля по MSG", "", *field_sections]
    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__": main()
