from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

pytest.importorskip("PySide6")

from eaeu_xml.gui_qt.view_model import GuiViewModel


ROOT = Path(__file__).resolve().parents[2]
START_PATH = "DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/StartDateTime"


def _model():
    model = GuiViewModel(ROOT)
    model.selectProcess("P.MM.01")
    model.selectTransaction("P.MM.01.TRN.001")
    model.selectMessage("P.MM.01.MSG.001")
    model.applyTestData()
    model.generateXml()
    return model


def _replace_start_datetime(xml_text, value):
    envelope = ET.fromstring(xml_text)
    start = next(element for element in envelope.iter() if element.tag.endswith("}StartDateTime"))
    start.text = value
    return ET.tostring(envelope, encoding="unicode")


def test_manual_invalid_xml_edit_invalidates_old_pass_and_validates_current_snapshot(tmp_path):
    model = _model()
    baseline = model.xml
    model.validate()
    assert model.validationSummary == "Проверка пройдена"

    model.setXml(_replace_start_datetime(baseline, None))
    assert model.validationSummary == "Проверка ещё не выполнялась."
    assert model.controller.validation is None

    path = tmp_path / "edited.xml"
    model.saveXml(str(path))
    assert path.read_text(encoding="utf-8") == model.xml
    assert model.validationSummary != "Проверка пройдена"

    model.validate()
    assert model.validationSummary != "Проверка пройдена"
    assert not model.controller.validation.is_valid
    assert model.controller.get_values()[START_PATH] is None
    assert any(
        item["severity"] == "ERROR" and item["code"] == "STRUCTURED_RULE_FAILED"
        for item in model.validationItems
    )


def test_manual_valid_xml_edit_can_pass_after_values_are_resynced():
    model = _model()
    edited_value = "2026-10-07T12:34:56+03:00"
    model.setXml(_replace_start_datetime(model.xml, edited_value))

    model.validate()

    assert model.validationSummary == "Проверка пройдена"
    assert model.controller.get_values()[START_PATH] == edited_value
