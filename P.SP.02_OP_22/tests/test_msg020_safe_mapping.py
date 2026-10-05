import json
from pathlib import Path

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.020"
STRUCTURE = "R.IP.SP.02.007"
P = "ipcdo:UnifiedRegisterRecordsDetails"
STATUS_CODE = "ipcdo:IPEntityStatusDetails/csdo:StatusCode"


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _rules():
    return _engine().rules[MESSAGE].structured_rules


def _inherited(item):
    return [
        rule
        for rule in _rules()
        if len(rule.get("source_refs", [])) == 2
        and rule["source_refs"][0].get("source_id") == "22OP-RULE-P.SP.02.MSG.020-T53-6-19"
        and rule["source_refs"][1].get("item") == str(item)
    ]


def test_structure_root_and_msg020_rule_inventory():
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE, mode=GenerationMode.TEST).definition
    assert structure.namespace == "urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0"
    assert structure.root_element == "TrademarkRegisterDetails"

    rules = _rules()
    assert len(rules) == 30
    ids = {rule["rule_id"] for rule in rules}
    assert "P.SP.02.MSG.020.T53.REQ.3" in ids
    assert "P.SP.02.MSG.020.T53.REQ.24" not in ids
    for requirement in ("1", "2", "4", "5", "20", "21", "22", "23", "25", "26", "27", "28"):
        assert f"P.SP.02.MSG.020.T53.REQ.{requirement}" in ids


def test_req3_is_executable_with_captured_source():
    engine = _engine()
    captured = {rule["rule_id"]: rule for rule in engine.rules[MESSAGE].business_rules}
    assert captured["P.SP.02.MSG.020.T53.REQ.3"]["source_refs"][0]["source_id"] == "22OP-RULE-P.SP.02.MSG.020-T53-3"
    assert next(rule for rule in _rules() if rule["rule_id"] == "P.SP.02.MSG.020.T53.REQ.3")["source_refs"] == captured["P.SP.02.MSG.020.T53.REQ.3"]["source_refs"]


def test_role_selectors_use_exact_status_04_and_01_only():
    role_rules = [
        rule
        for rule in _rules()
        if rule["rule_id"].split(".")[-1] in {"2", "4", "5", "20", "21", "22", "23", "25", "26", "27", "28"}
    ]
    assert role_rules
    seen = set()
    for rule in role_rules:
        selector = rule.get("selector", {})
        where = selector.get("where")
        if not where:
            continue
        assert selector["collection"] == P
        assert where["field"] == STATUS_CODE
        assert where["operator"] == "EQ"
        assert where["value"] in {"04", "01"}
        seen.add(where["value"])
    assert seen == {"04", "01"}


def test_inherited_req6_19_have_dual_provenance_and_expected_scope():
    for item in range(6, 20):
        rules = _inherited(item)
        assert rules, item
        for rule in rules:
            current, original = rule["source_refs"]
            assert current["source_id"] == "22OP-RULE-P.SP.02.MSG.020-T53-6-19"
            assert original["source_id"] == f"22OP-RULE-P.SP.02.MSG.003-T37-{item}"
            assert original["item"] == str(item)
            assert rule["applies_to_structure"] == STRUCTURE

    for item in (6, 7, 8, 9):
        for rule in _inherited(item):
            if "qname" in rule["selector"]:
                assert rule["selector"]["under"] == P


def test_req11_is_only_safe_global_necessary_condition():
    rules = _inherited(11)
    assert len(rules) == 1
    rule = rules[0]
    assert rule["mapping_status"] == "PARTIAL"
    assert rule["kind"] == "selection_cardinality"
    assert rule["min_occurs"] == 1
    assert rule["max_occurs"] == 2
    assert rule["selector"]["collection"] == f"{P}/ipcdo:IPPartyDetails"
    assert rule["selector"]["where"] == {
        "field": "ipsdo:IPPartyKindCode",
        "operator": "EQ",
        "value": "RH",
    }

    evaluator = StructuredRuleEvaluator()
    party = f"{P}/ipcdo:IPPartyDetails"
    assert evaluator.evaluate(rule, {party: [None], f"{party}/ipsdo:IPPartyKindCode": ["RH"]}).status is RuleStatus.PASS
    assert evaluator.evaluate(rule, {party: [None, None], f"{party}/ipsdo:IPPartyKindCode": ["RH", "RH"]}).status is RuleStatus.PASS
    assert evaluator.evaluate(rule, {party: [None, None, None], f"{party}/ipsdo:IPPartyKindCode": ["RH", "RH", "RH"]}).status is RuleStatus.FAIL


def test_req16_keeps_goods_class_code_source_conflict_unmapped():
    rules = _inherited(16)
    assert len(rules) == 2
    assert all(rule["mapping_status"] == "PARTIAL" for rule in rules)
    encoded = json.dumps(rules, ensure_ascii=False)
    assert "GoodsClassCode" not in encoded
    assert "ipsdo:GoodsClassName" in encoded
    assert "ipsdo:GoodsName" in encoded
    assert "ipsdo:TrademarkDecisionIndicator" in encoded
    assert "ipsdo:TrademarkApplicationId" in encoded


def test_req18_19_are_same_parent_presence_fragments_only():
    req18 = _inherited(18)
    req19 = _inherited(19)
    assert len(req18) == len(req19) == 1
    for rule in req18 + req19:
        assert rule["mapping_status"] == "PARTIAL"
        assert rule["selector"] == {"collection": P}
        assertion = rule["assertions"][0]
        assert assertion["kind"] == "conditional_presence"
        assert assertion["condition"] == {
            "field": "ipcdo:TrademarkDetails/ipsdo:CollectiveMarkIndicator",
            "operator": "EQ",
            "value": "1",
        }
    assert req18[0]["assertions"][0]["target"]["field"] == "ipcdo:IPPartyDetails"
    assert req19[0]["assertions"][0]["target"]["field"] == "ipcdo:AccompanyingDocumentsDetails"


def test_req20_and_req24_share_one_local_presence_fragment_with_both_sources():
    rules = [rule for rule in _rules() if rule["rule_id"] == "P.SP.02.MSG.020.T53.REQ.20"]
    assert len(rules) == 1
    rule = rules[0]
    assert rule["mapping_status"] == "PARTIAL"
    assert [ref["item"] for ref in rule["source_refs"]] == ["20", "24"]
    assert rule["selector"]["where"]["value"] == "01"
    assert rule["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:TrademarkId"}, "state": "REQUIRED"}
    ]


def test_req21_22_do_not_encode_time_comparisons():
    for requirement, leaf in (("21", "StartDateTime"), ("22", "EndDateTime")):
        rules = [rule for rule in _rules() if rule["rule_id"] == f"P.SP.02.MSG.020.T53.REQ.{requirement}"]
        assert len(rules) == 1
        rule = rules[0]
        assert rule["mapping_status"] == "PARTIAL"
        assert rule["selector"]["where"]["value"] == "04"
        assert rule["assertions"][0]["kind"] == "presence"
        assert rule["assertions"][0]["target"]["field"].endswith(f"/csdo:{leaf}")
        assert "comparison" not in json.dumps(rule)


def test_req25_28_are_role_local_and_use_exact_fallback_names():
    expected = {
        "25": ("04", "conditional_presence", None),
        "26": (
            "04",
            "conditional_fixed_value",
            "Решение об аннулировании регистрации товарного знака, знака обслуживания Евразийского экономического союза",
        ),
        "27": ("01", "conditional_presence", None),
        "28": (
            "01",
            "conditional_fixed_value",
            "Решение о регистрации товарного знака, знака обслуживания Евразийского экономического союза в отношении всех заявленных товаров и (или) услуг",
        ),
    }
    for requirement, (status, kind, value) in expected.items():
        rules = [rule for rule in _rules() if rule["rule_id"] == f"P.SP.02.MSG.020.T53.REQ.{requirement}"]
        assert len(rules) == 1
        rule = rules[0]
        assert rule["mapping_status"] == "PARTIAL"
        assert rule["selector"]["where"]["value"] == status
        assertion = rule["assertions"][0]
        assert assertion["kind"] == kind
        assert assertion["condition"]["field"] == "ipsdo:IPDocKindCode"
        assert assertion["target"]["field"] == "ipsdo:IPDocKindName"
        if value is not None:
            assert assertion["value"] == value
