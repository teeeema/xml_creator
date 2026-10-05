import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.043"
APP = "ipcdo:TrademarkApplicationDetails"
FULL = {1, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36, 37}
EXTERNAL = {2, 3, 4, 5, 31}
AMBIGUOUS = {13}
ENGINE_UNSUPPORTED = set()
UNMAPPED = (EXTERNAL | AMBIGUOUS | ENGINE_UNSUPPORTED) - {16, 17, 18, 19, 20}


def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text())


def rules(code):
    prefix = f"{MESSAGE}.T61.REQ.{code}"
    return [
        rule for rule in raw()["structured_rules"]
        if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")
    ]


def test_inventory_and_classification_are_exact():
    audit = raw()["mapping_audit"]
    assert (audit["captured_row_count"], audit["expanded_requirement_count"]) == (14, 37)
    assert audit["summary"]["FULLY_MAPPABLE"] == sorted(FULL)
    assert audit["summary"]["SAFE_PARTIAL"] == []
    assert audit["summary"]["EXTERNAL"] == sorted(EXTERNAL)
    assert audit["summary"]["AMBIGUOUS"] == sorted(AMBIGUOUS)
    assert audit["summary"]["ENGINE_UNSUPPORTED"] == sorted(ENGINE_UNSUPPORTED)
    assert audit["summary"]["SOURCE_CONFLICT"] == []
    assert sum(audit["classification_counts"].values()) == 37
    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 31,
        "SAFE_PARTIAL": 0,
        "EXTERNAL": 5,
        "AMBIGUOUS": 1,
        "ENGINE_UNSUPPORTED": 0,
        "SOURCE_CONFLICT": 0,
    }


def test_only_approved_requirements_are_executable():
    assert len(raw()["structured_rules"]) == 38
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


def test_req6_application_receipt_date_scoped_to_status01():
    r6 = rules(6)[0]
    assert r6["kind"] == "for_each"
    assert r6["selector"] == {
        "collection": APP,
        "where": {
            "field": "ipcdo:IPEntityStatusDetails/csdo:StatusCode",
            "operator": "EQ",
            "value": "01",
        },
    }
    assert r6["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:ApplicationReceiptDate"}, "state": "REQUIRED"}
    ]


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


def test_req10_communication_channel_code_scoped_to_status01():
    r10 = rules(10)[0]
    assert r10["kind"] == "for_each"
    assert r10["assertions"][0]["kind"] == "comparison"
    assert r10["assertions"][0]["operator"] == "IN"
    assert r10["assertions"][0]["right_value"] == ["TE", "EM", "FX"]


def test_req26_condition_assertion():
    r26 = rules(26)[0]
    assert r26["kind"] == "for_each"
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


def test_req32_semantic_role_cardinalities_and_attribute():
    r32_attr = next(r for r in rules(32) if r["rule_id"].endswith(".ATTR"))
    assert r32_attr["kind"] == "for_each"
    assert r32_attr["selector"]["where"]["value"] == "02"
    assert r32_attr["assertions"][0]["state"] == "FORBIDDEN"

    r32_role01 = next(r for r in rules(32) if r["rule_id"].endswith(".ROLE01"))
    assert r32_role01["kind"] == "selection_cardinality"
    assert r32_role01["selector"]["where"]["value"] == "01"
    assert r32_role01["min_occurs"] == 1
    assert r32_role01["max_occurs"] == 1

    r32_role02 = next(r for r in rules(32) if r["rule_id"].endswith(".ROLE02"))
    assert r32_role02["kind"] == "selection_cardinality"
    assert r32_role02["selector"]["where"]["value"] == "02"
    assert r32_role02["min_occurs"] == 1
    assert r32_role02["max_occurs"] == 1


def test_validity_dates_rules_have_exact_resource_owner():
    # REQ 33: StartDateTime REQUIRED
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

    # REQ 34: EndDateTime FORBIDDEN
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


def test_signature_rules_have_exact_owners_and_structure():
    # REQ 35: PRESENCE + BRANCH
    r35 = rules(35)
    assert len(r35) == 2
    r35_pres = next(r for r in r35 if r["rule_id"].endswith(".PRESENCE"))
    r35_branch = next(r for r in r35 if r["rule_id"].endswith(".BRANCH"))
    assert r35_pres["kind"] == "selection_cardinality"
    assert r35_pres["selector"] == {"collection": f"{APP}/ipcdo:SignatureDetails"}
    assert r35_pres["min_occurs"] == 1
    assert r35_pres["max_occurs"] is None

    assert r35_branch["kind"] == "for_each"
    assert r35_branch["selector"] == {"collection": f"{APP}/ipcdo:SignatureDetails"}
    assert r35_branch["assertions"] == [
        {
            "kind": "conditional_presence",
            "condition": {
                "field": "ipcdo:OfficerDetails",
                "operator": "NE",
                "value": None,
            },
            "target": {"field": "ccdo:FullNameDetails"},
            "state": "FORBIDDEN",
        }
    ]

    # REQ 36: FullNameDetails => OfficerDetails FORBIDDEN
    r36 = rules(36)[0]
    assert r36["kind"] == "for_each"
    assert r36["selector"] == {"collection": f"{APP}/ipcdo:SignatureDetails"}
    assert r36["assertions"] == [
        {
            "kind": "conditional_presence",
            "condition": {
                "field": "ccdo:FullNameDetails",
                "operator": "NE",
                "value": None,
            },
            "target": {"field": "ipcdo:OfficerDetails"},
            "state": "FORBIDDEN",
        }
    ]

    # REQ 37: OfficerDetails required fields and forbidden communication
    r37 = rules(37)[0]
    assert r37["kind"] == "for_each"
    assert r37["selector"] == {
        "qname": "ipcdo:OfficerDetails",
        "under": f"{APP}/ipcdo:SignatureDetails",
    }
    targets = {a["target"]["field"]: a["state"] for a in r37["assertions"]}
    assert targets == {
        "ccdo:FullNameDetails/csdo:LastName": "REQUIRED",
        "ccdo:FullNameDetails/csdo:FirstName": "REQUIRED",
        "csdo:PositionName": "REQUIRED",
        "ccdo:CommunicationDetails": "FORBIDDEN",
    }


def test_new_mappings_preserve_sources_and_remaining_unmapped_requirements():
    data = raw()
    inventory = data['mapping_audit']['inventory']
    by_code = {item['requirement_code']: item for item in inventory}
    assert by_code['13']['classification'] == 'AMBIGUOUS'
    assert by_code['13']['mapping_status'] == 'UNMAPPED'
    assert by_code['13']['engine_gap'] is None
    for item in inventory:
        code = item['requirement_code']
        prefix = MESSAGE + '.T' + item['source_refs'][0]['table'] + '.REQ.' + code
        executable = [r for r in data['structured_rules'] if r['rule_id'] == prefix or r['rule_id'].startswith(prefix + '.')]
        if item['classification'] in ('EXTERNAL', 'AMBIGUOUS', 'ENGINE_UNSUPPORTED', 'SOURCE_CONFLICT'):
            assert not executable
        if code in ('16', '17', '18', '19', '20', '26'):
            assert item['classification'] == 'FULLY_MAPPABLE'
            assert item['mapping_status'] == 'EXECUTABLE'
            assert item['engine_gap'] is None
            assert executable
            assert all(r['source_refs'] == item['source_refs'] for r in executable)
            if code == '26':
                assert 'any' in executable[0]['assertions'][0]['condition']


def test_no_positional_or_index_based_roles_in_rules_or_audit():
    content = (PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text()
    forbidden_tokens = ["[0]", "[1]", "first application", "second application", "первый экземпляр", "второй экземпляр"]
    for token in forbidden_tokens:
        assert token not in content, f"Forbidden ordinal token '{token}' found in {MESSAGE}.yaml"
