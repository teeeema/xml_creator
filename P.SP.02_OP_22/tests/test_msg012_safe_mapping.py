import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.012"
APP = "ipcdo:TrademarkApplicationDetails"

FULL = {16, 17, 18, 19, 20,
    1, 6, 7, 8, 9, 10, 11, 12, 14, 15,
    21, 22, 23, 24, 25, 26, 27, 28, 29,
    30, 31, 33, 34,
}
EXTERNAL = {2, 3, 4, 5, 32}
AMBIGUOUS = {13}
ENGINE_UNSUPPORTED = set()
UNMAPPED = EXTERNAL | AMBIGUOUS | ENGINE_UNSUPPORTED


def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def rules(code):
    prefix = f"{MESSAGE}.T45.REQ.{code}"
    return [
        rule for rule in raw()["structured_rules"]
        if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")
    ]


def test_inventory_and_classification_are_exact():
    audit = raw()["mapping_audit"]
    assert (audit["captured_row_count"], audit["expanded_requirement_count"]) == (11, 34)
    assert audit["summary"]["FULLY_MAPPABLE"] == sorted(FULL)
    assert audit["summary"]["SAFE_PARTIAL"] == []
    assert audit["summary"]["EXTERNAL"] == sorted(EXTERNAL)
    assert audit["summary"]["AMBIGUOUS"] == sorted(AMBIGUOUS)
    assert audit["summary"]["ENGINE_UNSUPPORTED"] == sorted(ENGINE_UNSUPPORTED)
    assert audit["summary"]["SOURCE_CONFLICT"] == []
    assert sum(audit["classification_counts"].values()) == 34
    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 28,
        "SAFE_PARTIAL": 0,
        "EXTERNAL": 5,
        "AMBIGUOUS": 1,
        "ENGINE_UNSUPPORTED": 0,
        "SOURCE_CONFLICT": 0,
    }


def test_only_approved_requirements_are_executable():
    assert len(raw()["structured_rules"]) == 34
    executable_codes = {
        int(rule["rule_id"].split(".REQ.")[1].split(".")[0])
        for rule in raw()["structured_rules"]
    }
    assert executable_codes == FULL

    for code in UNMAPPED:
        assert not rules(code), f"Requirement {code} must not have executable rules"


def test_req1_exact_two_applications_cardinality():
    r1 = rules(1)[0]
    assert r1["kind"] == "selection_cardinality"
    assert r1["selector"] == {"collection": APP}
    assert r1["min_occurs"] == 2
    assert r1["max_occurs"] == 2


def test_req26_inclusive_or_condition_assertion():
    r26 = rules(26)[0]
    assert r26["kind"] == "for_each"
    assert "parent" in r26["selector"]
    assert r26["selector"]["parent"]["where"]["value"] == "01"
    assertion = r26["assertions"][0]
    assert assertion["kind"] == "condition"
    assert "any" in assertion["condition"]
    fields = [cond["field"] for cond in assertion["condition"]["any"]]
    assert fields == ["ipsdo:TrademarkKindCode", "ipsdo:TrademarkKindName"]


def test_req30_cross_instance_comparison():
    r30 = rules(30)[0]
    assert r30["kind"] == "cross_instance_comparison"
    assert r30["operator"] == "EQ"
    assert r30["left"]["field"] == "ipsdo:SourceTrademarkApplicationId"
    assert r30["left"]["selector"]["where"]["value"] == "01"
    assert r30["right"]["field"] == "ipsdo:TrademarkApplicationId"
    assert r30["right"]["selector"]["where"]["value"] == "02"


def test_req31_semantic_role_cardinalities_and_attribute():
    r31_attr = next(r for r in rules(31) if r["rule_id"].endswith(".ATTR"))
    assert r31_attr["kind"] == "for_each"
    assert r31_attr["selector"]["where"]["value"] == "02"
    assert r31_attr["assertions"][0]["state"] == "FORBIDDEN"

    r31_role01 = next(r for r in rules(31) if r["rule_id"].endswith(".ROLE01"))
    assert r31_role01["kind"] == "selection_cardinality"
    assert r31_role01["selector"]["where"]["value"] == "01"
    assert r31_role01["min_occurs"] == 1
    assert r31_role01["max_occurs"] == 1

    r31_role02 = next(r for r in rules(31) if r["rule_id"].endswith(".ROLE02"))
    assert r31_role02["kind"] == "selection_cardinality"
    assert r31_role02["selector"]["where"]["value"] == "02"
    assert r31_role02["min_occurs"] == 1
    assert r31_role02["max_occurs"] == 1


def test_inherited_child_collections_have_role_parent_selector():
    inherited_child_codes = [7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    for code in inherited_child_codes:
        for r in rules(code):
            selector = r.get("selector", {})
            assert "parent" in selector, f"Rule {r['rule_id']} must have parent-scoped selector"
            assert selector["parent"]["collection"] == APP
            assert selector["parent"]["where"] == {
                "field": "ipcdo:IPEntityStatusDetails/csdo:StatusCode",
                "operator": "EQ",
                "value": "01",
            }


def test_validity_dates_rules_have_exact_resource_owner():
    r33 = rules(33)[0]
    assert r33["kind"] == "for_each"
    assert r33["selector"] == {"collection": "ccdo:ResourceItemStatusDetails"}
    assert r33["assertions"] == [
        {
            "kind": "presence",
            "target": {"field": "ccdo:ValidityPeriodDetails/csdo:StartDateTime"},
            "state": "REQUIRED",
        }
    ]

    r34 = rules(34)[0]
    assert r34["kind"] == "for_each"
    assert r34["selector"] == {"collection": "ccdo:ResourceItemStatusDetails"}
    assert r34["assertions"] == [
        {
            "kind": "presence",
            "target": {"field": "ccdo:ValidityPeriodDetails/csdo:EndDateTime"},
            "state": "FORBIDDEN",
        }
    ]
