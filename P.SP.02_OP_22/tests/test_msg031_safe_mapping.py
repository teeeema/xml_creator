import json
from pathlib import Path

from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.031"

T48_FULL = {5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 31, 33, 34, 35, 36}
T48_PARTIAL = {1, 3, 4}
T48_AMBIGUOUS = {13}
T48_ENGINE = {16, 17, 18, 19, 20, 26}
T48_CONFLICT = {2, 30, 32}
T49_FULL = {1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24}
T49_PARTIAL = {3, 4, 5}
T49_ENGINE = {18, 19}
INHERITED = set(range(6, 30))
APP = "ipcdo:TrademarkApplicationDetails"
R007 = "ipcdo:UnifiedRegisterRecordsDetails"


def _raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def _rules(table, code):
    rid = f"{MESSAGE}.T{table}.REQ.{code}"
    return [rule for rule in _raw()["structured_rules"] if rule["rule_id"] == rid]


def _inventory(table, code):
    return next(
        item
        for item in _raw()["mapping_audit"]["inventory"]
        if item["table"] == str(table) and item["requirement_code"] == str(code)
    )


def test_expanded_normative_inventory_has_exactly_61_distinct_table_branch_requirements():
    inventory = _raw()["mapping_audit"]["inventory"]
    identities = {(item["table"], item["branch"], item["requirement_code"]) for item in inventory}
    assert len(inventory) == len(identities) == 61
    assert _raw()["mapping_audit"]["expanded_requirement_count"] == 61
    assert {(item["table"], item["branch"]) for item in inventory} == {
        ("47", "R.010"),
        ("48", "R.IP.SP.02.002"),
        ("49", "R.IP.SP.02.007"),
    }


def test_mapping_classification_is_complete_and_non_approximating():
    assert _raw()["mapping_audit"]["summary"] == {
        "table47": {"FULLY_MAPPABLE": [1]},
        "table48": {
            "FULLY_MAPPABLE": sorted(T48_FULL),
            "SAFE_PARTIAL": sorted(T48_PARTIAL),
            "AMBIGUOUS": sorted(T48_AMBIGUOUS),
            "ENGINE_UNSUPPORTED": sorted(T48_ENGINE),
            "SOURCE_CONFLICT": sorted(T48_CONFLICT),
        },
        "table49": {
            "FULLY_MAPPABLE": sorted(T49_FULL),
            "SAFE_PARTIAL": sorted(T49_PARTIAL),
            "ENGINE_UNSUPPORTED": sorted(T49_ENGINE),
        },
    }
    mapped48 = {int(rule["rule_id"].rsplit(".", 1)[1]) for rule in _raw()["structured_rules"] if ".T48." in rule["rule_id"]}
    mapped49 = {int(rule["rule_id"].rsplit(".", 1)[1]) for rule in _raw()["structured_rules"] if ".T49." in rule["rule_id"]}
    assert mapped48 == T48_FULL | T48_PARTIAL
    assert mapped49 == T49_FULL | T49_PARTIAL
    assert not mapped48.intersection(T48_AMBIGUOUS | T48_ENGINE | T48_CONFLICT)
    assert not mapped49.intersection(T49_ENGINE)


def test_table47_uses_existing_one_of_infrastructure_instead_of_fake_flattened_rule():
    messages = json.loads((PACKAGE / "messages.yaml").read_text(encoding="utf-8"))["messages"]
    definition = next(item for item in messages if item["message_code"] == MESSAGE)
    assert definition["structure_id"] == "R.010"
    assert definition["embedded_structures"] == {
        "selection": "ONE_OF",
        "structures": ["R.IP.SP.02.002", "R.IP.SP.02.007"],
    }
    item = _inventory(47, 1)
    assert item["classification"] == "FULLY_MAPPABLE"
    assert item["mapping_status"] == "INFRASTRUCTURE_EXECUTABLE"
    assert not any(".T47." in rule["rule_id"] for rule in _raw()["structured_rules"])


def test_every_structured_rule_is_message_and_branch_scoped():
    rules = _raw()["structured_rules"]
    assert len(rules) == 54
    assert all(rule["rule_id"].startswith(MESSAGE + ".") for rule in rules)
    assert {
        rule["applies_to_structure"] for rule in rules
    } == {"R.IP.SP.02.002", "R.IP.SP.02.007"}
    assert all(
        (".T48." in rule["rule_id"]) == (rule["applies_to_structure"] == "R.IP.SP.02.002")
        for rule in rules
    )
    assert all(
        (".T49." in rule["rule_id"]) == (rule["applies_to_structure"] == "R.IP.SP.02.007")
        for rule in rules
    )


def test_table48_inherited_requirements_have_dual_current_and_original_provenance():
    for item in _raw()["mapping_audit"]["inventory"]:
        if item["table"] != "48" or int(item["requirement_code"]) not in INHERITED:
            continue
        current, original = item["source_refs"]
        assert (current["table"], current["page"], current["item"]) == ("48", 734, "6-29")
        assert current["source_id"] == "22OP-RULE-P.SP.02.MSG.031-T48-6-29"
        assert original["table"] == "44"
        assert original["item"] == item["requirement_code"]
        assert original["source_id"].endswith(f"-T44-{item['requirement_code']}")


def test_table48_req2_req30_req32_are_exact_source_conflicts_and_unmapped():
    conflicts = {
        int(item["requirement_code"]): item
        for item in _raw()["mapping_audit"]["source_conflicts"]
    }
    assert set(conflicts) == {2, 30, 32}
    assert "GoodsBaseDetails/ipsdo:TrademarkId" in conflicts[2]["structure_path"]
    assert conflicts[30]["structure_path"] == "ipcdo:TrademarkApplicationDetails/ipsdo:InconsistencyText"
    assert conflicts[32]["structure_path"].endswith("(missing)")
    for code in conflicts:
        assert not _rules(48, code)
        item = _inventory(48, code)
        assert item["classification"] == "SOURCE_CONFLICT"
        assert item["mapping_status"] == "UNMAPPED"


def test_table48_req26_remains_unmapped_with_normative_or_not_strengthened_to_and():
    assert not _rules(48, 26)
    item = _inventory(48, 26)
    assert item["classification"] == "ENGINE_UNSUPPORTED"
    assert " OR " in item["reason"]
    assert "AND" in item["reason"]
    assert [ref["table"] for ref in item["source_refs"]] == ["48", "44"]


def test_table48_req27_keeps_same_trademark_code_or_name_condition():
    rule, = _rules(48, 27)
    assert rule["selector"] == {"collection": f"{APP}/ipcdo:TrademarkDetails"}
    assert {a["target"]["field"] for a in rule["assertions"]} == {
        "ipsdo:TrademarkPicture",
        "ipsdo:TrademarkColourName",
    }
    for assertion in rule["assertions"]:
        condition = assertion["condition"]
        assert set(condition) == {"any"}
        assert {part["field"] for part in condition["any"]} == {
            "ipsdo:TrademarkKindCode",
            "ipsdo:TrademarkKindName",
        }


def test_table48_req31_req33_and_signature_rules_use_exact_owners():
    req31, = _rules(48, 31)
    assert req31["selector"] == {"collection": "ipcdo:RefusalDetails"}
    assert (req31["min_occurs"], req31["max_occurs"]) == (1, 1)

    req33, = _rules(48, 33)
    assert req33["selector"] == {"collection": "ccdo:ResourceItemStatusDetails"}
    assert req33["assertions"][0]["target"]["field"] == "ccdo:ValidityPeriodDetails/csdo:EndDateTime"

    sig = f"{APP}/ipcdo:SignatureDetails"
    assert any(rule["kind"] == "selection_cardinality" and rule["selector"] == {"collection": sig} for rule in _rules(48, 34))
    req36, = _rules(48, 36)
    assert req36["selector"] == {"qname": "ipcdo:OfficerDetails", "under": sig}


def test_table49_req5_is_partial_without_inventing_two_literal_conditional_comparison():
    rule, = _rules(49, 5)
    assert rule["kind"] == "conditional_presence"
    assert rule["mapping_status"] == "PARTIAL"
    assert rule["scope"] == {"collection": R007}
    assert rule["condition"] == {"field": "ipsdo:IPDocKindCode", "operator": "EQ", "value": None}
    assert rule["target"] == {"field": "ipsdo:IPDocKindName"}
    assert rule["state"] == "REQUIRED"
    item = _inventory(49, 5)
    assert item["classification"] == "SAFE_PARTIAL"
    assert "conditional membership in the two exact normative fallback names" in item["unmapped_remainder"]
    assert item["engine_gap"] == "conditional IN comparison is unavailable"


def test_table49_req16_is_full_and_uses_exact_ipsdo_goods_class_code():
    rules = _rules(49, 16)
    assert len(rules) == 2
    cardinality = next(rule for rule in rules if rule["kind"] == "selection_cardinality")
    body = next(rule for rule in rules if rule["kind"] == "for_each")
    goods = f"{R007}/ipcdo:GoodsBaseDetails"
    assert cardinality["selector"] == {"collection": goods}
    assert (cardinality["min_occurs"], cardinality["max_occurs"]) == (1, None)
    assert {a["target"]["field"] for a in body["assertions"]} == {
        "ipsdo:GoodsClassCode",
        "ipsdo:GoodsClassName",
        "ipsdo:GoodsName",
        "ipsdo:TrademarkDecisionIndicator",
        "ipsdo:TrademarkApplicationId",
    }
    assert _inventory(49, 16)["classification"] == "FULLY_MAPPABLE"


def test_table49_req18_req19_are_engine_unsupported_without_cross_collection_approximation():
    for code in (18, 19):
        assert not _rules(49, code)
        item = _inventory(49, code)
        assert item["classification"] == "ENGINE_UNSUPPORTED"
        assert item["mapping_status"] == "UNMAPPED"
        assert item["engine_gap"]


def test_table49_signature_rules_keep_same_signature_and_officer_context():
    sig = f"{R007}/ipcdo:SignatureDetails"
    req22 = _rules(49, 22)
    assert any(rule["kind"] == "selection_cardinality" and rule["selector"] == {"collection": sig} for rule in req22)
    mutual = next(rule for rule in req22 if rule["kind"] == "for_each")
    assert mutual["assertions"][0]["condition"]["field"] == "ipcdo:OfficerDetails"
    assert mutual["assertions"][0]["target"]["field"] == "ccdo:FullNameDetails"

    req23, = _rules(49, 23)
    assert req23["selector"] == {"collection": sig}
    assert req23["assertions"][0]["condition"]["field"] == "ccdo:FullNameDetails"
    assert req23["assertions"][0]["target"]["field"] == "ipcdo:OfficerDetails"

    req24, = _rules(49, 24)
    assert req24["selector"] == {"qname": "ipcdo:OfficerDetails", "under": sig}


def test_message_rule_identity_is_disjoint_from_neighboring_messages():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    codes = ("P.SP.02.MSG.029", "P.SP.02.MSG.030", "P.SP.02.MSG.031", "P.SP.02.MSG.032")
    by_message = {code: {rule["rule_id"] for rule in engine.rules[code].structured_rules} for code in codes}
    assert by_message[MESSAGE]
    for code, ids in by_message.items():
        assert all(rule_id.startswith(code + ".") for rule_id in ids)
    assert by_message[MESSAGE].isdisjoint(by_message["P.SP.02.MSG.029"])
    assert by_message[MESSAGE].isdisjoint(by_message["P.SP.02.MSG.030"])
    assert by_message[MESSAGE].isdisjoint(by_message["P.SP.02.MSG.032"])
