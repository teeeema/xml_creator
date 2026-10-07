from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.process_packages.body import GenerationMode


REPOSITORY = Path(__file__).resolve().parents[2]
PROCESS = "P.SP.02"
CASES = (
    ("P.SP.02.TRN.002", "P.SP.02.MSG.003"),
    ("P.SP.02.TRN.026", "P.SP.02.MSG.031"),
    ("P.SP.02.TRN.051", "P.SP.02.MSG.059"),
)


@pytest.mark.parametrize(("transaction", "message"), CASES)
@pytest.mark.parametrize("data_mode", ["test", "required"])
def test_embedded_one_of_form_generation_is_valid_in_both_data_modes(transaction, message, data_mode):
    app = EaeuXmlApplication(REPOSITORY)
    engine = app._engine(PROCESS)
    values = (
        app.generate_test_data(PROCESS, transaction, message)
        if data_mode == "test"
        else app.generate_required_data(PROCESS, transaction, message)
    )

    payload = values["*"]
    assert isinstance(payload, ET.Element)

    definition = engine.get_message(message)
    allowed_tags = {
        f"{{{embedded.namespace}}}{embedded.root_element}"
        for structure_id in definition.embedded_structures.structures
        for embedded in (engine.resolve_structure(structure_id, mode=GenerationMode.TEST).definition,)
    }
    assert payload.tag in allowed_tags

    validation = app.validate(PROCESS, transaction, message, values, mode=GenerationMode.TEST)
    assert validation.is_valid, [(item.code, item.rule_id, item.field_path) for item in validation.errors]
    assert "DATATYPE_INVALID" not in {item.code for item in validation.errors}
    assert "EMBEDDED_STRUCTURE_CARDINALITY" not in {item.code for item in validation.errors}

    body = engine.build_body(message, values, mode=GenerationMode.TEST)
    serialized = ET.tostring(body.serialize_xml_element(), encoding="utf-8")
    parsed = ET.fromstring(serialized)
    container = engine.get_structure(message, mode=GenerationMode.TEST)
    assert parsed.tag == f"{{{container.namespace}}}{container.root_element}"
    embedded_roots = [element for element in parsed.iter() if element.tag in allowed_tags]
    assert len(embedded_roots) == 1

