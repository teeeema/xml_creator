#!/usr/bin/env python3
"""Generate the final OP22 visual-field audit from canonical package metadata."""

from __future__ import annotations

import csv
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.presentation.field_info import build_field_details
from eaeu_xml.presentation.text_sanitizer import (
    has_presentation_garbage,
    is_unicode_noncharacter,
    normalize_extracted_regex,
    sanitize_presentation_text,
)


PROCESS_CODE = "P.SP.02"
REPORT_SUBDIR = Path("codex_reports/OP22_P_SP_02/VISUAL_ENGINE_FINAL")
PARSER_MARKER = "<PARSED TEXT FOR PAGE"
INVISIBLE_EXTRACTION_ARTIFACTS = {"\u00ad", "\u200b", "\u2060", "\ufeff"}


def _flatten(fields):
    for field in fields:
        yield field
        yield from _flatten(field.children)


def _bool(value: bool) -> str:
    return "1" if value else "0"


def _rendered_text(details: dict[str, object]) -> str:
    constraints = details.get("constraints") or []
    constraint_text = "\n".join(
        f"{item['label']}: {item['value']}" for item in constraints
    )
    return "\n".join(
        str(value)
        for value in (
            details.get("name") or "",
            details.get("description") or "",
            details.get("datatype") or "",
            details.get("multiplicity") or "",
            constraint_text,
            details.get("policy") or "",
        )
        if value
    )


def _source_fragments(definition, field) -> dict[str, str]:
    policy_parts = []
    if field is not None:
        policy_parts.extend(
            value
            for value in (
                field.fixed_value,
                field.message_policy_condition,
                field.message_policy_external_dependency,
            )
            if value is not None
        )
    return {
        "name": str(definition.official_name or (field.display_name if field else definition.path) or ""),
        "description": str(definition.description or ""),
        "datatype": "\n".join(
            str(value) for value in (definition.datatype, definition.datatype_text) if value
        ),
        "constraints": str(definition.constraints or ""),
        "policy": "\n".join(str(value) for value in policy_parts),
    }


def _artifact_codes(text: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if PARSER_MARKER in text.upper():
        found.append(("", "PARSER_MARKER_REMOVED"))
    for character in text:
        codepoint = ord(character)
        code = f"U+{codepoint:04X}"
        if is_unicode_noncharacter(character):
            found.append((code, "UNICODE_NONCHARACTER_NORMALIZED"))
        elif character == "\ufffd":
            found.append((code, "REPLACEMENT_CHARACTER_NORMALIZED"))
        elif character in INVISIBLE_EXTRACTION_ARTIFACTS:
            found.append((code, "INVISIBLE_EXTRACTION_ARTIFACT_REMOVED"))
        else:
            category = unicodedata.category(character)
            if category == "Cc" and character not in {"\n", "\r", "\t"}:
                found.append((code, "CONTROL_CHARACTER_NORMALIZED"))
            elif category in {"Zl", "Zp"}:
                found.append((code, "SEPARATOR_NORMALIZED"))
    return list(dict.fromkeys(found))


def _pattern_from_constraints(value: str) -> str:
    clean = sanitize_presentation_text(value)
    match = re.search(
        r"Шаблон:\s*(.*?)(?=\s+(?:Мин\. длина|Макс\. длина|Длина):|$)",
        clean,
    )
    return match.group(1).strip() if match else ""


def _truncate(value: str, limit: int = 220) -> str:
    text = value.replace("\n", " ").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def collect(project_root: Path):
    app = EaeuXmlApplication(project_root)
    engine = app._engine(PROCESS_CODE)

    message_links: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for transaction in engine.transactions.values():
        message_codes = tuple(
            code
            for code in (transaction.initiating_message, *transaction.response_messages)
            if code
        )
        for message_code in message_codes:
            message_links[message_code].append(
                (transaction.transaction_code, transaction.procedure_code)
            )

    coverage_rows: list[dict[str, str]] = []
    sanitization_rows: list[dict[str, str]] = []
    per_message: dict[str, dict[str, object]] = {}

    for message_code in sorted(engine.messages):
        message = engine.messages[message_code]
        links = sorted(set(message_links.get(message_code, ())))
        transactions = [item[0] for item in links]
        procedures = [item[1] for item in links]
        structure = app._structure_for_form(engine, message_code)
        field_views = {}
        if transactions:
            form = app.get_form(PROCESS_CODE, transactions[0], message_code)
            field_views = {field.path: field for field in _flatten(form.fields)}

        message_pass = True
        message_field_count = 0
        for definition in structure.presentation_fields:
            message_field_count += 1
            field = field_views.get(definition.path)
            details = build_field_details(definition, field, normalize_op22_regex=True)
            rendered = _rendered_text(details)
            fragments = _source_fragments(definition, field)

            raw_values = tuple(fragments.values())
            unicode_before = any(has_presentation_garbage(value) for value in raw_values)
            unicode_after = has_presentation_garbage(rendered)
            parser_after = PARSER_MARKER in rendered.upper()

            name_source = sanitize_presentation_text(fragments["name"])
            description_source = sanitize_presentation_text(fragments["description"])
            datatype_source = sanitize_presentation_text(fragments["datatype"])
            constraints_source = sanitize_presentation_text(fragments["constraints"])
            multiplicity_source = definition.min_occurs is not None or definition.max_occurs is not None

            empty_when_source = any(
                (
                    bool(name_source) and not bool(details["name"]),
                    bool(description_source) and not bool(details["description"]),
                    bool(datatype_source) and not bool(details["datatype"]),
                    multiplicity_source and not bool(details["multiplicity"]),
                    bool(constraints_source) and not bool(details["constraints"]),
                )
            )

            sanitization_applied = False
            for component, source_text in fragments.items():
                if not source_text:
                    continue
                artifact_codes = _artifact_codes(source_text)
                if artifact_codes:
                    sanitization_applied = True
                    rendered_fragment = {
                        "name": str(details["name"]),
                        "description": str(details["description"]),
                        "datatype": str(details["datatype"]),
                        "constraints": " | ".join(
                            f"{item['label']}: {item['value']}" for item in details["constraints"]
                        ),
                        "policy": str(details["policy"]),
                    }[component]
                    for codepoint, fix_type in artifact_codes:
                        sanitization_rows.append(
                            {
                                "message": message_code,
                                "field": definition.path,
                                "source_text_fragment": _truncate(source_text),
                                "rendered_text_fragment": _truncate(rendered_fragment),
                                "unicode_codepoint": codepoint,
                                "fix_type": fix_type,
                            }
                        )

            raw_pattern = _pattern_from_constraints(fragments["constraints"])
            if raw_pattern:
                clean_pattern = normalize_extracted_regex(raw_pattern)
                just_sanitized_pattern = sanitize_presentation_text(raw_pattern)
                if clean_pattern != just_sanitized_pattern:
                    sanitization_applied = True
                    sanitization_rows.append(
                        {
                            "message": message_code,
                            "field": definition.path,
                            "source_text_fragment": _truncate(raw_pattern),
                            "rendered_text_fragment": _truncate(clean_pattern),
                            "unicode_codepoint": "",
                            "fix_type": "REGEX_EXTRACTION_WHITESPACE_NORMALIZED",
                        }
                    )

            gui_pass = not unicode_after and not parser_after and not empty_when_source
            message_pass = message_pass and gui_pass
            coverage_rows.append(
                {
                    "message": message_code,
                    "transaction": "|".join(transactions),
                    "procedure": "|".join(procedures),
                    "structure": structure.structure_id,
                    "field_path": definition.path,
                    "field_kind": definition.kind,
                    "has_name": _bool(bool(details["name"])),
                    "has_description": _bool(bool(details["description"])),
                    "has_datatype": _bool(bool(details["datatype"])),
                    "has_multiplicity": _bool(bool(details["multiplicity"])),
                    "has_constraints": _bool(bool(details["constraints"])),
                    "sanitization_applied": _bool(sanitization_applied),
                    "unicode_garbage_before": _bool(unicode_before),
                    "unicode_garbage_after": _bool(unicode_after),
                    "parser_marker_found": _bool(parser_after),
                    "empty_info_when_source_present": _bool(empty_when_source),
                    "gui_status": "PASS" if gui_pass else "FAIL",
                }
            )

        per_message[message_code] = {
            "transactions": transactions,
            "procedures": procedures,
            "structure": structure.structure_id,
            "fields": message_field_count,
            "status": "PASS" if message_pass else "FAIL",
        }

    return engine, coverage_rows, sanitization_rows, per_message


def build_stats(engine, coverage_rows, sanitization_rows, per_message):
    return {
        "OP22_PROCEDURES_TOTAL": len(engine.procedures),
        "OP22_TRANSACTIONS_TOTAL": len(engine.transactions),
        "OP22_MESSAGES_TOTAL": len(engine.messages),
        "OP22_MESSAGES_WITH_FIELD_INFO": sum(
            1 for item in per_message.values() if item["fields"] and item["status"] == "PASS"
        ),
        "OP22_FIELDS_TOTAL": len(coverage_rows),
        "OP22_FIELDS_WITH_INFO": sum(
            1
            for row in coverage_rows
            if any(row[key] == "1" for key in ("has_name", "has_description", "has_datatype", "has_multiplicity", "has_constraints"))
        ),
        "OP22_FIELDS_WITH_DESCRIPTION": sum(row["has_description"] == "1" for row in coverage_rows),
        "OP22_FIELDS_WITH_DATATYPE": sum(row["has_datatype"] == "1" for row in coverage_rows),
        "OP22_FIELDS_WITH_MULTIPLICITY": sum(row["has_multiplicity"] == "1" for row in coverage_rows),
        "OP22_FIELDS_WITH_CONSTRAINTS": sum(row["has_constraints"] == "1" for row in coverage_rows),
        "OP22_FIELDS_WITH_SANITIZATION_CHANGES": sum(row["sanitization_applied"] == "1" for row in coverage_rows),
        "OP22_FIELDS_WITH_UNICODE_GARBAGE": sum(row["unicode_garbage_after"] == "1" for row in coverage_rows),
        "OP22_FIELDS_WITH_PARSER_MARKERS": sum(row["parser_marker_found"] == "1" for row in coverage_rows),
        "OP22_FIELDS_EMPTY_WHEN_SOURCE_PRESENT": sum(row["empty_info_when_source_present"] == "1" for row in coverage_rows),
        "FIELDS_WITH_COMPLETE_INFO": sum(row["gui_status"] == "PASS" for row in coverage_rows),
        "SANITIZATION_CASES_FIXED": len(sanitization_rows),
    }


def write_reports(project_root: Path, engine, coverage_rows, sanitization_rows, per_message, stats):
    report_dir = project_root / REPORT_SUBDIR
    report_dir.mkdir(parents=True, exist_ok=True)

    coverage_path = report_dir / "OP22_VISUAL_FIELD_COVERAGE.csv"
    coverage_fields = [
        "message", "transaction", "procedure", "structure", "field_path", "field_kind",
        "has_name", "has_description", "has_datatype", "has_multiplicity", "has_constraints",
        "sanitization_applied", "unicode_garbage_before", "unicode_garbage_after",
        "parser_marker_found", "empty_info_when_source_present", "gui_status",
    ]
    with coverage_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=coverage_fields)
        writer.writeheader()
        writer.writerows(coverage_rows)

    sanitization_path = report_dir / "OP22_VISUAL_SANITIZATION_CASES.csv"
    sanitization_fields = [
        "message", "field", "source_text_fragment", "rendered_text_fragment",
        "unicode_codepoint", "fix_type",
    ]
    with sanitization_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=sanitization_fields)
        writer.writeheader()
        writer.writerows(sanitization_rows)

    structures = sorted({message.structure_id for message in engine.messages.values() if message.structure_id})
    final_status = "COMPLETE" if (
        stats["OP22_MESSAGES_WITH_FIELD_INFO"] == stats["OP22_MESSAGES_TOTAL"]
        and stats["OP22_FIELDS_WITH_UNICODE_GARBAGE"] == 0
        and stats["OP22_FIELDS_WITH_PARSER_MARKERS"] == 0
        and stats["OP22_FIELDS_EMPTY_WHEN_SOURCE_PRESENT"] == 0
    ) else "PARTIAL"

    audit_path = report_dir / "OP22_VISUAL_ENGINE_FINAL_AUDIT.md"
    with audit_path.open("w", encoding="utf-8") as handle:
        handle.write("# OP22 / P.SP.02 — visual engine final audit\n\n")
        handle.write("Primary readable source for field information: `оп_22 обновление свединий.rtf`.\n\n")
        handle.write("Control normative source: `ОП_22.pdf`. Source files are read-only.\n\n")
        handle.write("## Coverage\n\n")
        for key, value in stats.items():
            handle.write(f"- {key}: {value}\n")
        handle.write(f"- OP22_STRUCTURES: {', '.join(structures)}\n")
        handle.write(f"- OP22_VISUAL_ENGINE: {final_status}\n\n")
        handle.write("## Message → transaction → procedure coverage\n\n")
        handle.write("| Message | Transaction | Procedure | Structure | Fields | Status |\n")
        handle.write("|---|---|---|---|---:|---|\n")
        for message_code, item in sorted(per_message.items()):
            handle.write(
                f"| {message_code} | {'; '.join(item['transactions'])} | {'; '.join(item['procedures'])} | "
                f"{item['structure']} | {item['fields']} | {item['status']} |\n"
            )
        failures = [row for row in coverage_rows if row["gui_status"] != "PASS"]
        handle.write("\n## Remaining blockers\n\n")
        if not failures:
            handle.write("None.\n")
        else:
            for row in failures:
                handle.write(
                    f"- {row['message']} / {row['field_path']}: "
                    f"unicode_after={row['unicode_garbage_after']}, "
                    f"parser_marker={row['parser_marker_found']}, "
                    f"empty_info={row['empty_info_when_source_present']}\n"
                )

    return audit_path, coverage_path, sanitization_path


def main() -> int:
    project_root = Path(__file__).resolve().parents[2]
    engine, coverage_rows, sanitization_rows, per_message = collect(project_root)
    stats = build_stats(engine, coverage_rows, sanitization_rows, per_message)
    paths = write_reports(project_root, engine, coverage_rows, sanitization_rows, per_message, stats)
    for key, value in stats.items():
        print(f"{key}={value}")
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
