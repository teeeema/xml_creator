"""Export a reproducible audit of user-visible help for every process form."""

import csv
import json
from pathlib import Path
import re
import subprocess
import sys
import types

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.presentation.field_help import resolve_field_help


COLUMNS = (
    "structure", "field_path", "qname", "display_name", "required_type",
    "old_description", "new_purpose", "new_what_to_enter", "old_example",
    "new_example", "example_source", "pattern", "validation_status",
)


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    app = EaeuXmlApplication(root)
    previous_source = subprocess.run(
        ["git", "show", "HEAD:eaeu_xml/src/eaeu_xml/application/examples.py"],
        cwd=root, check=True, capture_output=True, text=True,
    ).stdout
    previous_module = types.ModuleType("previous_example_resolver")
    sys.modules[previous_module.__name__] = previous_module
    exec(compile(previous_source, "HEAD:examples.py", "exec"), previous_module.__dict__)
    previous_resolver = previous_module.ExampleValueResolver()
    output = root / "FIELD_HELP_AUDIT.csv"
    counts = {name: 0 for name in (
        "TOTAL_FIELDS", "FIELDS_WITH_PURPOSE", "FIELDS_WITH_INPUT_GUIDE",
        "FIELDS_WITH_EXAMPLE", "GENERIC_PLACEHOLDERS_LEFT", "INVALID_EXAMPLES", "MISSING_HELP",
    )}

    def rows(fields, structure, parent_required=True):
        for field in fields:
            if field.visibility == "HIDDEN":
                continue
            required = (parent_required and field.required
                        and field.normative_input_policy != "CONDITIONAL"
                        and not field.condition_description)
            info = resolve_field_help(field, unconditionally_required=required)
            example = field.example_value
            if field.example_origin in {"FIXED_VALUE", "ALLOWED_VALUE", "TEST_DATA_GENERATOR"}:
                previous_example = example
            else:
                previous_example = previous_resolver.resolve(
                    datatype=field.datatype if not field.children else None,
                    description=field.description, fixed_value=field.fixed_value,
                    allowed_values=field.allowed_values,
                    classifier=field.normative_input_policy == "CLASSIFIER",
                ).value
            valid = True
            if example is not None and field.pattern:
                try:
                    valid = re.fullmatch(field.pattern, str(example)) is not None
                except re.error:
                    valid = False
            if example is not None and field.allowed_values and field.example_origin == "ALLOWED_VALUE":
                valid = valid and example in field.allowed_values
            counts["TOTAL_FIELDS"] += 1
            counts["FIELDS_WITH_PURPOSE"] += bool(info.purpose.strip())
            counts["FIELDS_WITH_INPUT_GUIDE"] += bool(info.what_to_enter.strip())
            counts["FIELDS_WITH_EXAMPLE"] += example is not None
            counts["GENERIC_PLACEHOLDERS_LEFT"] += bool(re.match(r"^\[(?:идентификатор|значение|код|текст|дата|номер)(?:\]|\s)", str(example), re.I))
            counts["INVALID_EXAMPLES"] += not valid
            counts["MISSING_HELP"] += not (info.purpose and info.what_to_enter and info.example)
            yield {
                "structure": structure, "field_path": field.path,
                "qname": field.xml_qname or field.xml_name or "",
                "display_name": field.display_name,
                "required_type": info.required_type,
                "old_description": field.description or "",
                "new_purpose": info.purpose,
                "new_what_to_enter": info.what_to_enter,
                "old_example": "" if previous_example is None else str(previous_example),
                "new_example": info.example,
                "example_source": field.example_origin,
                "pattern": field.pattern or "",
                "validation_status": "PASS" if valid and example is not None else
                                     "NO_SOURCE_EXAMPLE" if valid else "INVALID",
            }
            yield from rows(field.children, structure, required)

    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        for process in app.list_processes():
            for transaction in app.list_transactions(process.process_code):
                for message in app.list_messages(process.process_code, transaction.transaction_code):
                    form = app.get_form(process.process_code, transaction.transaction_code, message.message_code)
                    writer.writerows(rows(form.fields, f"{form.structure_id} / {message.message_code}"))
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    print(output)


if __name__ == "__main__":
    main()
