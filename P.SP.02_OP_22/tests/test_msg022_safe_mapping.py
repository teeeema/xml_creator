import json
from pathlib import Path

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
RULE_FILE = PACKAGE / "message_rules" / "P.SP.02.MSG.022.yaml"
MESSAGE = "P.SP.02.MSG.022"
STRUCTURE = "R.IP.SP.02.008"


def _data():
    return json.loads(RULE_FILE.read_text())


def test_msg022_exact_structure_root_and_top_level_inventory():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    assert structure.structure_id == STRUCTURE
    assert (
        f"{{{structure.namespace}}}{structure.root_element}"
        == "{urn:EEC:R:IP:SP:02:TrademarkRegisterRequestDetails:v1.0.0}TrademarkRegisterRequestDetails"
    )
    assert {field.path for field in structure.fields if field.parent is None} == {
        "ccdo:EDocHeader",
        "csdo:UpdateDateTime",
        "csdo:UnifiedCountryCode",
        "ipsdo:TrademarkId",
        "ipsdo:TrademarkApplicationId",
        "ipcdo:AccompanyingDocumentsDetails",
    }


def test_msg022_req1_is_fully_executable_with_exact_paths():
    rules = _data()["structured_rules"]
    assert len(rules) == 6
    assert {rule["rule_id"] for rule in rules} == {"P.SP.02.MSG.022.T55.REQ.1"}
    header, *forbidden = rules
    assert header == {
        "kind": "cardinality",
        "target": "ccdo:EDocHeader",
        "min_occurs": 1,
        "max_occurs": 1,
        "rule_id": "P.SP.02.MSG.022.T55.REQ.1",
        "applies_to_structure": STRUCTURE,
        "source_refs": header["source_refs"],
    }
    assert {(rule["target"], rule["state"]) for rule in forbidden} == {
        ("csdo:UpdateDateTime", "FORBIDDEN"),
        ("csdo:UnifiedCountryCode", "FORBIDDEN"),
        ("ipsdo:TrademarkId", "FORBIDDEN"),
        ("ipsdo:TrademarkApplicationId", "FORBIDDEN"),
        ("ipcdo:AccompanyingDocumentsDetails", "FORBIDDEN"),
    }
    for rule in rules:
        assert rule["applies_to_structure"] == STRUCTURE
        assert rule["source_refs"] == [_data()["business_rules"][0]["source_refs"][0]]
        assert "qname" not in rule


def test_msg022_does_not_create_rules_for_messages_without_rule_tables():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    assert "P.SP.02.MSG.023" not in engine.rules
    assert "P.SP.02.MSG.025" not in engine.rules
    assert "P.SP.02.MSG.026" not in engine.rules
