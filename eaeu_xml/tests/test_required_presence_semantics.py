from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


def _presence(state="REQUIRED", target="Root/Value"):
    return {
        "rule_id": "TEST.REQUIRED",
        "kind": "presence",
        "target": target,
        "state": state,
    }


def test_required_presence_rejects_none_empty_and_whitespace_values():
    evaluator = StructuredRuleEvaluator(complex_paths=set())

    for value in (None, "", "   \t\n", [""], ["   "]):
        result = evaluator.evaluate(_presence(), {"Root/Value": value})
        assert result.status is RuleStatus.FAIL

    assert evaluator.evaluate(_presence(), {"Root/Value": "filled"}).status is RuleStatus.PASS


def test_required_complex_group_uses_structural_presence_but_scalar_attributes_do_not_fill_text():
    evaluator = StructuredRuleEvaluator(complex_paths={"Root/Group"})

    complex_values = {
        "Root/Group": "",
    }
    assert evaluator.evaluate(_presence(target="Root/Group"), complex_values).status is RuleStatus.PASS

    scalar_evaluator = StructuredRuleEvaluator(complex_paths=set())
    scalar_with_attribute_only = {
        "Root/Value": None,
        "Root/Value/@codeListId": "LIST",
    }
    assert scalar_evaluator.evaluate(_presence(), scalar_with_attribute_only).status is RuleStatus.FAIL


def test_forbidden_presence_keeps_structural_semantics_for_empty_value():
    evaluator = StructuredRuleEvaluator()
    result = evaluator.evaluate(_presence(state="FORBIDDEN"), {"Root/Value": None})
    assert result.status is RuleStatus.FAIL
