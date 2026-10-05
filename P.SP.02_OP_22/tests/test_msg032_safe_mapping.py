import json
from pathlib import Path

from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.032"
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
DOCS = f"{APP}/ipcdo:AccompanyingDocumentsDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
FALLBACK = (
    "Жалоба на решение национального патентного ведомства в отношении регистрации товарного знака, "
    "знака обслуживания Евразийского экономического союза"
)

FULL = {1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32}
PARTIAL = {2, 3, 4}
AMBIGUOUS = {13}
ENGINE = {16, 17, 18, 19, 20, 26}
INHERITED = set(range(6, 30))


def _raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def _rules(code):
    rid = f"{MESSAGE}.T50.REQ.{code}"
    return [rule for rule in _raw()["structured_rules"] if rule["rule_id"] == rid]


def _inventory(code):
    return next(
        item for item in _raw()["mapping_audit"]["inventory"]
        if item["requirement_code"] == str(code)
    )


def test_expanded_normative_inventory_has_exactly_32_requirements():
    data = _raw()
    inventory = data["mapping_audit"]["inventory"]
    assert len(inventory) == 32
    assert data["mapping_audit"]["expanded_requirement_count"] == 32
    assert {int(item["requirement_code"]) for item in inventory} == set(range(1, 33))
    assert all(item["table"] == "50" for item in inventory)
    assert all(item["branch"] == "R.IP.SP.02.002" for item in inventory)


def test_mapping_classification_is_complete_and_non_approximating():
    summary = _raw()["mapping_audit"]["summary"]
    assert summary == {
        "FULLY_MAPPABLE": sorted(FULL),
        "SAFE_PARTIAL": sorted(PARTIAL),
        "AMBIGUOUS": sorted(AMBIGUOUS),
        "ENGINE_UNSUPPORTED": sorted(ENGINE),
        "EXTERNAL": [],
        "SOURCE_CONFLICT": [],
    }
    mapped = {int(rule["rule_id"].rsplit(".", 1)[1]) for rule in _raw()["structured_rules"]}
    assert mapped == FULL | PARTIAL
    assert not mapped.intersection(AMBIGUOUS | ENGINE)


def test_normative_context_is_msg032_trn027_prc006_and_r002():
    context = _raw()["mapping_audit"]["normative_context"]
    assert context["message_code"] == MESSAGE
    assert context["structure_id"] == "R.IP.SP.02.002"
    assert context["root_qname"] == (
        "{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails"
    )
    assert context["transaction"] == "P.SP.02.TRN.027"
    assert context["procedure"] == "P.SP.02.PRC.006"
    assert context["initiating_operation"] == "P.SP.02.OPR.022"
    assert context["responding_operation"] == "P.SP.02.OPR.023"
    assert context["initiating_participant"] == "P.SP.02.ACT.002"
    assert context["responding_participant"] == "P.SP.02.ACT.001"
    assert context["response_message"] == "P.SP.02.MSG.002"
    assert context["pages"] == [741, 742, 743]


def test_inherited_req6_29_have_dual_table50_and_original_table44_provenance():
    for code in INHERITED:
        item = _inventory(code)
        current, original = item["source_refs"]
        assert (current["table"], current["page"], current["item"]) == ("50", 742, "6-29")
        assert current["source_id"] == "22OP-RULE-P.SP.02.MSG.032-T50-6-29"
        assert original["table"] == "44"
        assert original["item"] == str(code)
        assert original["source_id"].endswith(f"-T44-{code}")

    for rule in _raw()["structured_rules"]:
        code = int(rule["rule_id"].rsplit(".", 1)[1])
        if code in INHERITED:
            current, original = rule["source_refs"]
            assert current["source_id"] == "22OP-RULE-P.SP.02.MSG.032-T50-6-29"
            assert original["table"] == "44"
            assert original["item"] == str(code)


def test_req1_application_cardinality_is_exactly_one():
    rule, = _rules(1)
    assert rule["kind"] == "selection_cardinality"
    assert rule["selector"] == {"collection": APP}
    assert (rule["min_occurs"], rule["max_occurs"]) == (1, 1)


def test_req2_req3_classifier_logic_is_only_safe_local_partial():
    req2, = _rules(2)
    assert req2["mapping_status"] == "PARTIAL"
    assert req2["kind"] == "conditional_presence"
    assert req2["scope"] == {"collection": APP}
    assert req2["condition"] == {"field": "ipsdo:IPDocKindCode", "operator": "NE", "value": None}
    assert req2["target"] == {"field": "ipsdo:IPDocKindName"}
    assert req2["state"] == "FORBIDDEN"
    assert _inventory(2)["classification"] == "SAFE_PARTIAL"
    assert _inventory(2)["external_dependency"] == "classifier of document/material kinds"

    req3, = _rules(3)
    assert req3["mapping_status"] == "PARTIAL"
    assert req3["kind"] == "conditional_fixed_value"
    assert req3["scope"] == {"collection": APP}
    assert req3["condition"] == {"field": "ipsdo:IPDocKindCode", "operator": "EQ", "value": None}
    assert req3["target"] == {"field": "ipsdo:IPDocKindName"}
    assert req3["value"] == FALLBACK
    assert _inventory(3)["classification"] == "SAFE_PARTIAL"


def test_req4_maps_only_independently_required_application_id():
    rule, = _rules(4)
    assert rule["mapping_status"] == "PARTIAL"
    assert rule["selector"] == {"collection": APP}
    assert rule["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:TrademarkApplicationId"}, "state": "REQUIRED"}
    ]
    item = _inventory(4)
    assert item["classification"] == "SAFE_PARTIAL"
    assert item["external_dependency"] == "filing-office information resource"
    assert len(item["unmapped_remainder"]) == 4


def test_req5_requires_exact_complaintdetails_owner():
    rule, = _rules(5)
    assert rule["selector"] == {"collection": APP}
    assert rule["assertions"] == [
        {"kind": "presence", "target": {"field": "ipcdo:ComplaintDetails"}, "state": "REQUIRED"}
    ]


def test_req13_is_ambiguous_and_unmapped():
    assert not _rules(13)
    item = _inventory(13)
    assert item["classification"] == "AMBIGUOUS"
    assert item["mapping_status"] == "UNMAPPED"
    assert "PA/RE" in item["reason"]


def test_req16_20_are_engine_unsupported_and_unmapped():
    for code in range(16, 21):
        assert not _rules(code)
        item = _inventory(code)
        assert item["classification"] == "ENGINE_UNSUPPORTED"
        assert item["mapping_status"] == "UNMAPPED"
        assert item["engine_gap"] == "missing exact nested repeated correlation/filter semantics"


def test_req26_normative_or_is_unmapped_without_strengthening_to_and():
    assert not _rules(26)
    item = _inventory(26)
    assert item["classification"] == "ENGINE_UNSUPPORTED"
    assert " OR " in item["reason"]
    assert "AND" in item["reason"]
    assert [ref["table"] for ref in item["source_refs"]] == ["50", "44"]


def test_req27_uses_same_trademark_code_or_name_condition():
    rule, = _rules(27)
    assert rule["selector"] == {"collection": TM}
    assert {item["target"]["field"] for item in rule["assertions"]} == {
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


def test_req30_is_optional_per_document_and_requires_exact_six_children():
    rule, = _rules(30)
    assert rule["kind"] == "for_each"
    assert rule["selector"] == {"collection": DOCS}
    assert {item["target"]["field"] for item in rule["assertions"]} == {
        "ipsdo:IPDocKindCode",
        "csdo:DocId",
        "csdo:DocCreationDate",
        "csdo:DescriptionText",
        "csdo:PageQuantity",
        "csdo:DocBinaryText",
    }


def test_req31_req32_use_exact_validity_period_paths():
    req31, = _rules(31)
    assert req31["selector"] == {"collection": RESOURCE}
    assert req31["assertions"] == [
        {
            "kind": "presence",
            "target": {"field": "ccdo:ValidityPeriodDetails/csdo:StartDateTime"},
            "state": "REQUIRED",
        }
    ]

    req32, = _rules(32)
    assert req32["selector"] == {"collection": RESOURCE}
    assert req32["assertions"] == [
        {
            "kind": "presence",
            "target": {"field": "ccdo:ValidityPeriodDetails/csdo:EndDateTime"},
            "state": "FORBIDDEN",
        }
    ]


def test_exact_structure_paths_exist_for_all_msg032_specific_targets():
    structure = json.loads(
        (PACKAGE / "structures" / "R.IP.SP.02.002" / "1.0.0.yaml").read_text(encoding="utf-8")
    )
    paths = {field["path"] for field in structure["fields"]}
    expected = {
        APP,
        f"{APP}/ipsdo:IPDocKindCode",
        f"{APP}/ipsdo:IPDocKindName",
        f"{APP}/ipsdo:TrademarkApplicationId",
        f"{APP}/ipcdo:ComplaintDetails",
        DOCS,
        f"{DOCS}/ipsdo:IPDocKindCode",
        f"{DOCS}/csdo:DocId",
        f"{DOCS}/csdo:DocCreationDate",
        f"{DOCS}/csdo:DescriptionText",
        f"{DOCS}/csdo:PageQuantity",
        f"{DOCS}/csdo:DocBinaryText",
        RESOURCE,
        f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:StartDateTime",
        f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:EndDateTime",
    }
    assert expected <= paths
    docs = next(field for field in structure["fields"] if field["path"] == DOCS)
    assert (docs["min_occurs"], docs["max_occurs"]) == (0, "*")


def test_rule_identity_is_disjoint_from_msg031_and_msg033():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    codes = ("P.SP.02.MSG.031", MESSAGE, "P.SP.02.MSG.033")
    by_message = {
        code: {rule["rule_id"] for rule in engine.rules[code].structured_rules}
        for code in codes
    }
    assert by_message["P.SP.02.MSG.031"]
    assert by_message[MESSAGE]
    assert all(rule_id.startswith(MESSAGE + ".") for rule_id in by_message[MESSAGE])
    assert by_message[MESSAGE].isdisjoint(by_message["P.SP.02.MSG.031"])
    assert by_message[MESSAGE].isdisjoint(by_message["P.SP.02.MSG.033"])
