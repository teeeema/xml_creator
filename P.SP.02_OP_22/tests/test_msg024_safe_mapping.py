import json
from pathlib import Path

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
RULE_FILE = PACKAGE / "message_rules" / "P.SP.02.MSG.024.yaml"
MESSAGE = "P.SP.02.MSG.024"
STRUCTURE = "R.IP.SP.02.008"


def _data():
    return json.loads(RULE_FILE.read_text())


def _rules(requirement):
    rule_id = f"P.SP.02.MSG.024.T56.REQ.{requirement}"
    return [rule for rule in _data()["structured_rules"] if rule["rule_id"] == rule_id]


def test_msg024_exact_structure_root_and_country_owner():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    assert structure.structure_id == STRUCTURE
    assert (
        f"{{{structure.namespace}}}{structure.root_element}"
        == "{urn:EEC:R:IP:SP:02:TrademarkRegisterRequestDetails:v1.0.0}TrademarkRegisterRequestDetails"
    )
    fields = {field.path: field for field in structure.fields}
    country = fields["csdo:UnifiedCountryCode"]
    code_list = fields["csdo:UnifiedCountryCode/@codeListId"]
    assert country.parent is None
    assert country.min_occurs == 0
    assert country.max_occurs is None
    assert code_list.parent == country.field_id
    assert code_list.min_occurs == 1
    assert code_list.max_occurs == 1


def test_msg024_req1_is_full_required_update_datetime():
    rule, = _rules(1)
    assert rule["kind"] == "presence"
    assert rule["target"] == "csdo:UpdateDateTime"
    assert rule["state"] == "REQUIRED"
    assert rule["applies_to_structure"] == STRUCTURE
    assert rule["source_refs"] == [_data()["business_rules"][0]["source_refs"][0]]


def test_msg024_req2_source_conflict_has_no_executable_approximation():
    assert not _rules(2)
    encoded = json.dumps(_data()["structured_rules"], ensure_ascii=False)
    assert "AccompanyingDocumentsDetails" not in encoded
    assert "ApellationOfOriginApplicationId" not in encoded

    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    assert "ipcdo:AccompanyingDocumentsDetails" in {field.path for field in structure.fields}
    assert not any("ApellationOfOriginApplicationId" in field.path for field in structure.fields)


def test_msg024_req3_is_full_exact_top_level_country_attribute_rule():
    rule, = _rules(3)
    assert rule["kind"] == "for_each"
    assert rule["selector"] == {"collection": "csdo:UnifiedCountryCode"}
    assert rule["assertions"] == [
        {"kind": "fixed_value", "target": {"field": "@codeListId"}, "value": "ВОИС ST.3"}
    ]
    assert rule["applies_to_structure"] == STRUCTURE
    assert rule["source_refs"] == [_data()["business_rules"][2]["source_refs"][0]]


def test_msg024_does_not_create_rules_for_response_messages_without_tables():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    assert "P.SP.02.MSG.023" not in engine.rules
    assert "P.SP.02.MSG.025" not in engine.rules
    assert "P.SP.02.MSG.026" not in engine.rules
