from pathlib import Path

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.presentation.field_info import build_field_details
from eaeu_xml.presentation.text_sanitizer import has_presentation_garbage


PROJECT_ROOT = Path(__file__).parents[2]
PROCESS_CODE = "P.SP.02"
EXPECTED_STRUCTURES = {
    "R.006",
    "R.010",
    "R.IP.SP.02.002",
    "R.IP.SP.02.007",
    "R.IP.SP.02.008",
    "R.IP.SP.03.003",
}
UUID_PATTERN = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"


def _message_transactions(engine):
    mapping = {}
    for transaction in engine.transactions.values():
        for message_code in (transaction.initiating_message, *transaction.response_messages):
            if message_code and message_code not in mapping:
                mapping[message_code] = transaction.transaction_code
    return mapping


def _flatten(fields):
    for field in fields:
        yield field
        yield from _flatten(field.children)


def _rendered_text(details):
    return "\n".join(
        [
            str(details.get("name") or ""),
            str(details.get("description") or ""),
            str(details.get("datatype") or ""),
            str(details.get("multiplicity") or ""),
            "\n".join(f"{item['label']}: {item['value']}" for item in details.get("constraints") or []),
            str(details.get("policy") or ""),
        ]
    )


def test_all_op22_messages_and_fields_render_without_presentation_garbage():
    app = EaeuXmlApplication(PROJECT_ROOT)
    engine = app._engine(PROCESS_CODE)
    message_transactions = _message_transactions(engine)

    assert len(engine.procedures) == 37
    assert len(engine.transactions) == 54
    assert len(engine.messages) == 61
    assert {message.structure_id for message in engine.messages.values()} == EXPECTED_STRUCTURES
    assert set(message_transactions) == set(engine.messages)

    for message_code, message in sorted(engine.messages.items()):
        structure = app._structure_for_form(engine, message_code)
        form = app.get_form(PROCESS_CODE, message_transactions[message_code], message_code)
        field_views = {field.path: field for field in _flatten(form.fields)}
        assert len(field_views) == len(structure.presentation_fields), message_code

        for definition in structure.presentation_fields:
            details = build_field_details(
                definition,
                field_views.get(definition.path),
                normalize_op22_regex=True,
            )
            rendered = _rendered_text(details)
            assert not has_presentation_garbage(rendered), (message_code, definition.path)
            assert "<PARSED TEXT FOR PAGE" not in rendered.upper(), (message_code, definition.path)
            assert details["name"], (message_code, definition.path, "name")
            if definition.description:
                assert details["description"], (message_code, definition.path, "description")
            if definition.datatype or definition.datatype_text:
                assert details["datatype"], (message_code, definition.path, "datatype")
            if definition.min_occurs is not None or definition.max_occurs is not None:
                assert details["multiplicity"], (message_code, definition.path, "multiplicity")
            if definition.constraints:
                assert details["constraints"], (message_code, definition.path, "constraints")


def test_op22_uuid_and_russian_hyphen_are_rendered_from_dirty_source_cleanly():
    app = EaeuXmlApplication(PROJECT_ROOT)
    engine = app._engine(PROCESS_CODE)
    transaction = _message_transactions(engine)["P.SP.02.MSG.001"]
    form = app.get_form(PROCESS_CODE, transaction, "P.SP.02.MSG.001")
    field_views = {field.path: field for field in _flatten(form.fields)}
    structure = app._structure_for_form(engine, "P.SP.02.MSG.001")
    definitions = {field.path: field for field in structure.presentation_fields}

    uuid_path = "ccdo:EDocHeader/csdo:EDocId"
    uuid_details = build_field_details(definitions[uuid_path], field_views[uuid_path], normalize_op22_regex=True)
    assert {item["label"]: item["value"] for item in uuid_details["constraints"]}["Шаблон"] == UUID_PATTERN

    district_path = next(path for path in definitions if path.endswith("/csdo:DistrictName"))
    assert "\ufffe" in (definitions[district_path].description or "")
    district_details = build_field_details(
        definitions[district_path], field_views[district_path], normalize_op22_regex=True
    )
    assert "административно-территориального" in district_details["description"]
    assert "\ufffe" not in district_details["description"]


def test_all_required_op22_structure_shapes_have_meaningful_field_cards():
    app = EaeuXmlApplication(PROJECT_ROOT)
    engine = app._engine(PROCESS_CODE)
    message_transactions = _message_transactions(engine)
    messages_by_structure = {}
    for message in engine.messages.values():
        messages_by_structure.setdefault(message.structure_id, message.message_code)

    saw_group = False
    saw_repeatable = False
    saw_long_description = False
    saw_no_constraints = False
    for structure_id in EXPECTED_STRUCTURES:
        message_code = messages_by_structure[structure_id]
        structure = app._structure_for_form(engine, message_code)
        form = app.get_form(PROCESS_CODE, message_transactions[message_code], message_code)
        field_views = {field.path: field for field in _flatten(form.fields)}
        for definition in structure.presentation_fields:
            details = build_field_details(
                definition, field_views.get(definition.path), normalize_op22_regex=True
            )
            if definition.kind == "GROUP" or any(
                child.parent == definition.field_id for child in structure.presentation_fields
            ):
                saw_group = True
                assert details["name"] and details["datatype"] and details["multiplicity"]
            if definition.max_occurs in (None, "*") or (
                isinstance(definition.max_occurs, int) and definition.max_occurs > 1
            ):
                saw_repeatable = True
                assert "*" in details["multiplicity"] or ".." in details["multiplicity"]
            if definition.description and len(definition.description) >= 180:
                saw_long_description = True
                assert len(details["description"]) >= 150
            if not definition.constraints:
                saw_no_constraints = True
                assert details["constraints"] == []

    assert saw_group
    assert saw_repeatable
    assert saw_long_description
    assert saw_no_constraints
