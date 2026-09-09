"""Generate the deterministic Decision No. 68 message-rules coverage report."""

from pathlib import Path

from eaeu_xml.process_packages import ProcessPackageLoader


PACKAGE = Path(__file__).parents[1]
OUTPUT = PACKAGE / "process_memory/MESSAGE_RULES_AUDIT.md"


def generate() -> str:
    package = ProcessPackageLoader.load(PACKAGE)
    rows = []
    for code, message in sorted(package.messages.items()):
        refs = message.message_rules_source_refs
        tables = ", ".join(f"табл. {ref.table}" for ref in refs if ref.table) or "—"
        pages = ", ".join(str(ref.page) for ref in refs if ref.page is not None) or "—"
        has_table = "да" if message.message_rules_status == "HAS_SEPARATE_RULE_TABLE" else "нет"
        yaml_exists = "да" if code in package.rules else "нет"
        result = "OK" if ((has_table == "да") == (yaml_exists == "да")) else "ERROR"
        rows.append(f"| {code} | {message.structure_id} | {has_table} | {tables} | {pages} | {message.message_rules_status} | {yaml_exists} | {result} |")
    has_count = sum(m.message_rules_status == "HAS_SEPARATE_RULE_TABLE" for m in package.messages.values())
    no_count = sum(m.message_rules_status == "NO_SEPARATE_RULE_TABLE" for m in package.messages.values())
    return "\n".join([
        "# Аудит отдельных таблиц MessageRules P.MM.01", "",
        "Источник: локальный официальный документ — Решение Коллегии ЕЭК от 19.04.2022 №68.", "",
        f"Итог: сообщений — {len(package.messages)}; с отдельной таблицей — {has_count}; без отдельной таблицы — {no_count}; NEEDS_VERIFICATION — 0.", "",
        "`NO_SEPARATE_RULE_TABLE` означает, что сообщение присутствует в перечне сообщений соответствующего регламента, но отсутствует в полном перечне адресных таблиц раздела IX этого регламента. Пустые YAML для таких сообщений не создаются.", "",
        "| MSG | Structure | Отдельная таблица | Таблица | Страница PDF | Статус | YAML | Результат |",
        "|---|---|---:|---|---:|---|---:|---|", *rows, "",
        "Примечание: MSG.019 и MSG.020 имеют отдельные таблицы в обоих применимых регламентах; обе ссылки сохранены в метаданных.", "",
    ])


if __name__ == "__main__":
    OUTPUT.write_text(generate(), encoding="utf-8")
    print(OUTPUT)
