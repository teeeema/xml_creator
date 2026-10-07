from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.presentation.controller import GuiController
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "P.MM.01_OP_26"
MESSAGE = "P.MM.01.MSG.001"
DRUG_KIND = "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/DrugApplicationKindCode"
COUNTRY_KIND = "DrugRegistrationDetails/DrugCountryRegistrationDetails/CountryKindCode"
START_DATETIME = "DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/StartDateTime"
REQ003 = "OP26.P_MM_01.P.MM.01.MSG.001.REQ.003"
REQ005 = "OP26.P_MM_01.P.MM.01.MSG.001.REQ.005"
REQ008 = "OP26.P_MM_01.P.MM.01.MSG.001.REQ.008"


def _controller():
    controller = GuiController(EaeuXmlApplication(ROOT), test_seed=12345)
    controller.select_process("P.MM.01")
    controller.select_transaction("P.MM.01.TRN.001")
    controller.select_message(MESSAGE)
    controller.apply_test_data()
    return controller


def _status(result, rule_id):
    return next(item.status for item in result.rule_evaluations if item.rule_id == rule_id)


def test_test_data_uses_normative_allowed_values_and_remains_valid():
    controller = _controller()
    values = controller.get_values()

    assert values[DRUG_KIND] in {"01", "02", "03", "04", "99"}
    assert values[COUNTRY_KIND] in {"01", "02"}
    assert values[DRUG_KIND] != "TEST"
    assert values[COUNTRY_KIND] != "TEST"

    validation = controller.validate()
    assert validation.is_valid
    body_validation = EaeuXmlEngine.load_process(PACKAGE).validate_body(
        MESSAGE,
        values,
        mode=GenerationMode.TEST,
    )
    assert _status(body_validation, REQ005) is RuleStatus.PASS
    assert _status(body_validation, REQ008) is RuleStatus.PASS
    assert controller.generate_xml().success


@pytest.mark.parametrize(
    "path,rule_id",
    [
        (DRUG_KIND, REQ005),
        (COUNTRY_KIND, REQ008),
    ],
)
def test_test_placeholder_is_rejected_by_normative_code_rules(path, rule_id):
    controller = _controller()
    values = controller.get_values()
    values[path] = "TEST"
    result = EaeuXmlEngine.load_process(PACKAGE).validate_body(
        MESSAGE,
        values,
        mode=GenerationMode.TEST,
    )

    assert not result.is_valid
    assert _status(result, rule_id) is RuleStatus.FAIL


def test_required_start_datetime_rejects_empty_xml_element():
    controller = _controller()
    generated = controller.generate_xml()
    assert generated.success

    envelope = ET.fromstring(generated.xml)
    body = next(element for element in envelope if element.tag.endswith("}Body"))
    document = next(iter(body))
    start = next(element for element in document.iter() if element.tag.endswith("}StartDateTime"))
    start.text = None

    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    values, issues = engine.body_provider._values_from_element(structure, document)
    assert not issues
    assert values[START_DATETIME] is None

    result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert not result.is_valid
    assert _status(result, REQ003) is RuleStatus.FAIL
