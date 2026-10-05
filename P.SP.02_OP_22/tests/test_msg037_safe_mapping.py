import json
from pathlib import Path

from eaeu_xml.process_packages.engine import EaeuXmlEngine

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.037"
APP = "ipcdo:TrademarkApplicationDetails"
FULL = {1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31}
PARTIAL = {4}
EXTERNAL = {2, 3}
AMBIGUOUS = {13}
ENGINE = {16, 17, 18, 19, 20, 26}
UNMAPPED = EXTERNAL | AMBIGUOUS | ENGINE
INHERITED = set(range(6, 30))


def _raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def _rules(code):
    base = f"{MESSAGE}.T55.REQ.{code}"
    return [r for r in _raw()["structured_rules"] if r["rule_id"] == base or r["rule_id"].startswith(base + ".")]


def _inventory(code):
    return next(x for x in _raw()["mapping_audit"]["inventory"] if x["requirement_code"] == str(code))


def test_inventory_and_classification_are_exact():
    audit = _raw()["mapping_audit"]
    assert audit["captured_row_count"] == 8
    assert audit["expanded_requirement_count"] == 31
    assert len(audit["inventory"]) == 31
    assert audit["summary"] == {
        "FULLY_MAPPABLE": sorted(FULL),
        "SAFE_PARTIAL": sorted(PARTIAL),
        "EXTERNAL": sorted(EXTERNAL),
        "AMBIGUOUS": sorted(AMBIGUOUS),
        "ENGINE_UNSUPPORTED": sorted(ENGINE),
        "SOURCE_CONFLICT": [],
    }
    assert sum(audit["classification_counts"].values()) == 31
    assert {int(x["requirement_code"]) for x in audit["unmapped_requirements"]} == UNMAPPED


def test_only_msg037_rule_ids_and_exact_executable_requirement_set():
    rules = _raw()["structured_rules"]
    assert len(rules) == 25
    assert all(r["rule_id"].startswith(MESSAGE + ".") for r in rules)
    codes = {int(r["rule_id"].split(".REQ.", 1)[1].split(".", 1)[0]) for r in rules}
    assert codes == FULL | PARTIAL
    assert codes.isdisjoint(UNMAPPED)


def test_req1_req4_req5_direct_shapes():
    req1, = _rules(1)
    assert req1["kind"] == "selection_cardinality"
    assert req1["selector"] == {"collection": APP}
    assert (req1["min_occurs"], req1["max_occurs"]) == (1, 1)

    req4, = _rules(4)
    assert req4["mapping_status"] == "PARTIAL"
    assert req4["selector"] == {"collection": APP}
    assert req4["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:TrademarkApplicationId"}, "state": "REQUIRED"}
    ]
    assert _inventory(4)["classification"] == "SAFE_PARTIAL"
    assert len(_inventory(4)["unmapped_remainder"]) == 4

    req5 = _rules(5)
    assert len(req5) == 2
    cardinality = next(r for r in req5 if r["kind"] == "selection_cardinality")
    body = next(r for r in req5 if r["kind"] == "for_each")
    owner = f"{APP}/ipcdo:IPEntityStatusDetails"
    assert cardinality["selector"] == {"collection": owner}
    assert (cardinality["min_occurs"], cardinality["max_occurs"]) == (1, 1)
    assert body["selector"] == {"collection": owner}
    assert body["assertions"] == [
        {"kind": "fixed_value", "target": {"field": "csdo:StatusCode"}, "value": "31"},
        {"kind": "presence", "target": {"field": "csdo:StatusCode/@codeListId"}, "state": "FORBIDDEN"},
    ]


def test_external_and_unsupported_requirements_have_no_executable_rules():
    for code in UNMAPPED:
        assert not _rules(code)
    assert _inventory(2)["classification"] == "EXTERNAL"
    assert _inventory(3)["classification"] == "EXTERNAL"
    assert _inventory(13)["classification"] == "AMBIGUOUS"
    for code in (16, 17, 18, 19, 20, 26):
        assert _inventory(code)["classification"] == "ENGINE_UNSUPPORTED"
    assert " OR " in _inventory(26)["reason"]


def test_inherited_req6_29_keep_dual_table55_table44_provenance():
    for code in INHERITED:
        item = _inventory(code)
        assert item["provenance_kind"] == "INHERITED"
        assert len(item["source_refs"]) >= 2
        current, original = item["source_refs"][0], item["source_refs"][1]
        assert (current["table"], current["page"], current["item"]) == ("55", 753, "6-29")
        assert current["source_id"] == "22OP-RULE-P.SP.02.MSG.037-T55-6-29"
        assert original["table"] == "44"
        assert original["item"] == str(code)
    for code in {6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29}:
        assert _rules(code)


def test_req27_is_same_trademark_parent_conditional():
    req27, = _rules(27)
    assert req27["kind"] == "for_each"
    assert req27["selector"] == {"collection": f"{APP}/ipcdo:TrademarkDetails"}
    assert {a["target"]["field"] for a in req27["assertions"]} == {
        "ipsdo:TrademarkPicture", "ipsdo:TrademarkColourName"
    }
    for assertion in req27["assertions"]:
        assert set(assertion["condition"]) == {"any"}
        assert {x["field"] for x in assertion["condition"]["any"]} == {
            "ipsdo:TrademarkKindCode", "ipsdo:TrademarkKindName"
        }


def test_req30_req31_both_dates_required_under_root_resource_owner():
    for code, leaf in ((30, "StartDateTime"), (31, "EndDateTime")):
        rule, = _rules(code)
        assert rule["kind"] == "for_each"
        assert rule["selector"] == {"collection": "ccdo:ResourceItemStatusDetails"}
        assert rule["assertions"] == [{
            "kind": "presence",
            "target": {"field": f"ccdo:ValidityPeriodDetails/csdo:{leaf}"},
            "state": "REQUIRED",
        }]


def test_message_rule_identity_is_loaded_only_for_msg037():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    ids = {r["rule_id"] for r in engine.rules[MESSAGE].structured_rules}
    assert ids
    assert all(x.startswith(MESSAGE + ".") for x in ids)
