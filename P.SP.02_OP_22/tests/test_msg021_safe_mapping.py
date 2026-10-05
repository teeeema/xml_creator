import json
from pathlib import Path

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
RULE_FILE = PACKAGE / "message_rules" / "P.SP.02.MSG.021.yaml"
MESSAGE = "P.SP.02.MSG.021"
STRUCTURE = "R.IP.SP.02.007"
P = "ipcdo:UnifiedRegisterRecordsDetails"
FALLBACK = "Заявление о продлении срока действия исключительного права на товарный знак, знак обслуживания Евразийского экономического союза"


def _data():
    return json.loads(RULE_FILE.read_text())


def _rules():
    return _data()["structured_rules"]


def _direct(requirement):
    rule_id = f"P.SP.02.MSG.021.T54.REQ.{requirement}"
    return [rule for rule in _rules() if rule["rule_id"] == rule_id]


def _inherited(item):
    return [
        rule
        for rule in _rules()
        if rule["rule_id"] == "P.SP.02.MSG.021.T54.REQ.6_19"
        and len(rule.get("source_refs", [])) == 2
        and rule["source_refs"][1].get("item") == str(item)
    ]


def test_msg021_exact_structure_root_and_inventory():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    assert structure.structure_id == STRUCTURE
    assert f"{{{structure.namespace}}}{structure.root_element}" == "{urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0}TrademarkRegisterDetails"

    assert len(_rules()) == 19
    assert {r["requirement_code"] for r in _data()["business_rules"]} == {"1", "2", "3", "4", "5", "6-19", "20", "21", "22", "23"}


def test_req1_is_only_local_trademark_id_presence():
    rules = _direct(1)
    assert len(rules) == 1
    rule = rules[0]
    assert rule["mapping_status"] == "PARTIAL"
    assert rule["selector"] == {"collection": P}
    assert rule["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:TrademarkId"}, "state": "REQUIRED"}
    ]
    encoded = json.dumps(rule, ensure_ascii=False).lower()
    assert "lookup" not in encoded
    assert "external" not in encoded


def test_req2_exactly_one_outer_record():
    rule, = _direct(2)
    assert rule["kind"] == "selection_cardinality"
    assert rule["selector"] == {"collection": P}
    assert rule["min_occurs"] == 1
    assert rule["max_occurs"] == 1


def test_req3_forbids_only_normative_end_datetime_path():
    rule, = _direct(3)
    assert rule["selector"] == {"collection": P}
    assert rule["assertions"] == [{
        "kind": "presence",
        "target": {"field": "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime"},
        "state": "FORBIDDEN",
    }]


def test_req4_5_use_direct_document_kind_fields_and_exact_fallback():
    req4, = _direct(4)
    req5, = _direct(5)
    assert req4["mapping_status"] == req5["mapping_status"] == "PARTIAL"
    assert req4["scope"] == req5["scope"] == {"collection": P}
    assert req4["condition"] == {"field": "ipsdo:IPDocKindCode", "operator": "NE", "value": None}
    assert req4["target"] == {"field": "ipsdo:IPDocKindName"}
    assert req4["state"] == "FORBIDDEN"
    assert req5["condition"] == {"field": "ipsdo:IPDocKindCode", "operator": "EQ", "value": None}
    assert req5["target"] == {"field": "ipsdo:IPDocKindName"}
    assert req5["value"] == FALLBACK


def test_inherited_executable_core_has_double_provenance():
    expected = {"6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "17"}
    found = set()
    for rule in _rules():
        refs = rule.get("source_refs", [])
        if rule["rule_id"] != "P.SP.02.MSG.021.T54.REQ.6_19":
            continue
        assert len(refs) == 2
        current, original = refs
        assert current["source_id"] == "22OP-RULE-P.SP.02.MSG.021-T54-6-19"
        assert current["table"] == "54"
        assert current["item"] == "6-19"
        assert original["source_id"] == f"22OP-RULE-P.SP.02.MSG.003-T37-{original['item']}"
        assert original["table"] == "37"
        found.add(str(original["item"]))
    assert found == expected


def test_req11_is_exactly_one_rh_for_single_outer_record():
    rule, = _inherited(11)
    assert rule["mapping_status"] == "INHERITED"
    assert rule["kind"] == "selection_cardinality"
    assert rule["selector"] == {
        "collection": f"{P}/ipcdo:IPPartyDetails",
        "where": {"field": "ipsdo:IPPartyKindCode", "operator": "EQ", "value": "RH"},
    }
    assert rule["min_occurs"] == 1
    assert rule["max_occurs"] == 1


def test_req16_18_19_are_not_executable_and_goods_class_conflict_is_preserved():
    assert not _inherited(16)
    assert not _inherited(18)
    assert not _inherited(19)
    encoded = json.dumps(_rules(), ensure_ascii=False)
    assert "GoodsClassCode" not in encoded
    assert "IPPartyKindCode\", \"operator\": \"EQ\", \"value\": \"UE" not in encoded


def test_req20_status_rule_is_exact():
    rule, = _direct(20)
    assert rule["selector"] == {"collection": f"{P}/ipcdo:IPEntityStatusDetails"}
    assert rule["assertions"] == [
        {"kind": "presence", "target": {"field": "csdo:EventDate"}, "state": "REQUIRED"},
        {"kind": "fixed_value", "target": {"field": "csdo:StatusCode"}, "value": "03"},
        {"kind": "presence", "target": {"field": "csdo:StatusCode/@codeListId"}, "state": "FORBIDDEN"},
    ]


def test_req21_counts_only_direct_doc_validity_date_and_is_partial():
    rule, = _direct(21)
    assert rule["kind"] == "selection_cardinality"
    assert rule["mapping_status"] == "PARTIAL"
    assert rule["selector"] == {"collection": f"{P}/csdo:DocValidityDate"}
    assert rule["min_occurs"] == 1
    assert "max_occurs" not in rule


def test_req22_23_have_no_executable_approximation():
    assert not _direct(22)
    assert not _direct(23)
    encoded = json.dumps(_rules(), ensure_ascii=False).lower()
    assert "greater" not in encoded
    assert "ordering" not in encoded
