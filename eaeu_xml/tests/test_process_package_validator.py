import json
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest

from eaeu_xml.core.errors import ProcessPackageValidationError
from eaeu_xml.process_packages.loader import ProcessPackageLoader
from eaeu_xml.process_packages.validator import ProcessPackageValidator


FIXTURE = Path(__file__).parent / "fixtures/P.TEST.01"


def test_validator_accepts_for_each_with_parent_selector():
    validator = ProcessPackageValidator()
    rule = {
        "rule_id": "TEST.RULE.PARENT",
        "kind": "for_each",
        "selector": {
            "collection": "ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails",
            "parent": {
                "collection": "ipcdo:TrademarkApplicationDetails",
                "where": {
                    "field": "ipcdo:IPEntityStatusDetails/csdo:StatusCode",
                    "operator": "EQ",
                    "value": "01",
                },
            },
        },
        "assertions": [
            {
                "kind": "presence",
                "target": {"field": "csdo:PartyLegalStatus"},
                "state": "REQUIRED",
            }
        ],
    }
    # Must not raise
    validator._validate_structured_rule(rule, "TEST_MSG")


def test_validator_accepts_for_each_with_condition_assertion():
    validator = ProcessPackageValidator()
    rule = {
        "rule_id": "TEST.RULE.CONDITION",
        "kind": "for_each",
        "selector": {
            "collection": "ipcdo:TrademarkApplicationDetails",
        },
        "assertions": [
            {
                "kind": "condition",
                "condition": {
                    "any": [
                        {
                            "field": "ipcdo:ApplicantDetails/csdo:UnifiedCountryCode",
                            "operator": "IN",
                            "value": ["BY", "RU"],
                        },
                        {
                            "field": "ipcdo:PatentAgentDetails/csdo:UnifiedCountryCode",
                            "operator": "IN",
                            "value": ["BY", "RU"],
                        },
                    ]
                },
            }
        ],
    }
    # Must not raise
    validator._validate_structured_rule(rule, "TEST_MSG")


def test_validator_accepts_cross_instance_comparison():
    validator = ProcessPackageValidator()
    rule = {
        "rule_id": "TEST.RULE.CROSS_INSTANCE",
        "kind": "cross_instance_comparison",
        "operator": "EQ",
        "left": {
            "selector": {
                "collection": "ipcdo:TrademarkApplicationDetails",
                "where": {
                    "field": "ipcdo:IPEntityStatusDetails/csdo:StatusCode",
                    "operator": "EQ",
                    "value": "01",
                },
            },
            "field": "ipsdo:SourceTrademarkApplicationId",
        },
        "right": {
            "selector": {
                "collection": "ipcdo:TrademarkApplicationDetails",
                "where": {
                    "field": "ipcdo:IPEntityStatusDetails/csdo:StatusCode",
                    "operator": "EQ",
                    "value": "02",
                },
            },
            "field": "ipsdo:TrademarkApplicationId",
        },
    }
    # Must not raise
    validator._validate_structured_rule(rule, "TEST_MSG")


def test_validator_rejects_unknown_top_level_rule_kind():
    validator = ProcessPackageValidator()
    rule = {
        "rule_id": "TEST.RULE.UNKNOWN",
        "kind": "unknown_top_level_kind",
    }
    with pytest.raises(ProcessPackageValidationError) as exc:
        validator._validate_structured_rule(rule, "TEST_MSG")
    assert exc.value.code == "UNKNOWN_STRUCTURED_RULE_KIND"


def test_validator_rejects_unknown_for_each_assertion_kind():
    validator = ProcessPackageValidator()
    rule = {
        "rule_id": "TEST.RULE.FOR_EACH.UNKNOWN",
        "kind": "for_each",
        "selector": {"collection": "Items"},
        "assertions": [
            {
                "kind": "unknown_assertion_kind",
            }
        ],
    }
    with pytest.raises(ProcessPackageValidationError) as exc:
        validator._validate_structured_rule(rule, "TEST_MSG")
    assert exc.value.code == "UNKNOWN_STRUCTURED_RULE_KIND"


def test_validator_rejects_condition_at_top_level():
    validator = ProcessPackageValidator()
    rule = {
        "rule_id": "TEST.RULE.TOP_LEVEL_CONDITION",
        "kind": "condition",
        "condition": {"field": "StatusCode", "operator": "EQ", "value": "01"},
    }
    with pytest.raises(ProcessPackageValidationError) as exc:
        validator._validate_structured_rule(rule, "TEST_MSG", assertion=False)
    assert exc.value.code == "UNKNOWN_STRUCTURED_RULE_KIND"


def test_validator_rejects_cross_instance_inside_for_each():
    validator = ProcessPackageValidator()
    rule = {
        "rule_id": "TEST.RULE.FOR_EACH_CROSS_INSTANCE",
        "kind": "for_each",
        "selector": {"collection": "Items"},
        "assertions": [
            {
                "kind": "cross_instance_comparison",
                "operator": "EQ",
                "left": {"selector": {"collection": "A"}, "field": "f1"},
                "right": {"selector": {"collection": "B"}, "field": "f2"},
            }
        ],
    }
    with pytest.raises(ProcessPackageValidationError) as exc:
        validator._validate_structured_rule(rule, "TEST_MSG")
    assert exc.value.code == "UNKNOWN_STRUCTURED_RULE_KIND"


def test_validator_rejects_invalid_cross_instance_shape():
    validator = ProcessPackageValidator()
    # Missing left
    with pytest.raises(ProcessPackageValidationError) as exc:
        validator._validate_structured_rule({
            "rule_id": "R1",
            "kind": "cross_instance_comparison",
            "operator": "EQ",
            "right": {"selector": {"collection": "B"}, "field": "f2"},
        }, "TEST_MSG")
    assert exc.value.code == "INVALID_CROSS_INSTANCE_OPERAND"

    # Invalid operator
    with pytest.raises(ProcessPackageValidationError) as exc:
        validator._validate_structured_rule({
            "rule_id": "R2",
            "kind": "cross_instance_comparison",
            "operator": "INVALID_OP",
            "left": {"selector": {"collection": "A"}, "field": "f1"},
            "right": {"selector": {"collection": "B"}, "field": "f2"},
        }, "TEST_MSG")
    assert exc.value.code == "UNKNOWN_STRUCTURED_RULE_OPERATOR"

    # Missing field in operand
    with pytest.raises(ProcessPackageValidationError) as exc:
        validator._validate_structured_rule({
            "rule_id": "R3",
            "kind": "cross_instance_comparison",
            "operator": "EQ",
            "left": {"selector": {"collection": "A"}},
            "right": {"selector": {"collection": "B"}, "field": "f2"},
        }, "TEST_MSG")
    assert exc.value.code == "INVALID_CROSS_INSTANCE_FIELD"


def test_validator_rejects_invalid_condition_assertion():
    validator = ProcessPackageValidator()
    # Missing condition field
    with pytest.raises(ProcessPackageValidationError) as exc:
        validator._validate_structured_rule({
            "kind": "condition",
        }, "TEST_MSG", assertion=True)
    assert exc.value.code == "INVALID_STRUCTURED_RULE_CONDITION"

    # Non-mapping condition
    with pytest.raises(ProcessPackageValidationError) as exc:
        validator._validate_structured_rule({
            "kind": "condition",
            "condition": "not-a-mapping",
        }, "TEST_MSG", assertion=True)
    assert exc.value.code == "INVALID_STRUCTURED_RULE_CONDITION"


def test_loader_to_validator_path_with_approved_capabilities():
    """Verify that a process package loaded from disk via ProcessPackageLoader passes validation."""
    with TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "test_pkg"
        shutil.copytree(FIXTURE, target)
        rules_path = target / "message_rules/P.TS.01.MSG.001.yaml"
        rules_data = json.loads(rules_path.read_text(encoding="utf-8"))

        # Add approved capabilities to structured_rules
        rules_data["structured_rules"] = [
            {
                "rule_id": "P.TS.01.MSG.001.RULE.PARENT_SELECTOR",
                "applies_to_structure": "R.TEST.001",
                "kind": "for_each",
                "selector": {
                    "collection": "Items/ChildItems",
                    "parent": {
                        "collection": "Items",
                        "where": {
                            "field": "Name",
                            "operator": "EQ",
                            "value": "A",
                        },
                    },
                },
                "assertions": [
                    {
                        "kind": "presence",
                        "target": {"field": "Value"},
                        "state": "REQUIRED",
                    }
                ],
            },
            {
                "rule_id": "P.TS.01.MSG.001.RULE.CONDITION_ASSERTION",
                "applies_to_structure": "R.TEST.001",
                "kind": "for_each",
                "selector": {
                    "collection": "Items",
                },
                "assertions": [
                    {
                        "kind": "condition",
                        "condition": {
                            "any": [
                                {
                                    "field": "Name",
                                    "operator": "IN",
                                    "value": ["A", "B"],
                                },
                                {
                                    "field": "Code",
                                    "operator": "EQ",
                                    "value": "01",
                                },
                            ]
                        },
                    }
                ],
            },
            {
                "rule_id": "P.TS.01.MSG.001.RULE.CROSS_INSTANCE",
                "applies_to_structure": "R.TEST.001",
                "kind": "cross_instance_comparison",
                "operator": "EQ",
                "left": {
                    "selector": {
                        "collection": "Items",
                        "where": {
                            "field": "Code",
                            "operator": "EQ",
                            "value": "01",
                        },
                    },
                    "field": "SourceId",
                },
                "right": {
                    "selector": {
                        "collection": "Items",
                        "where": {
                            "field": "Code",
                            "operator": "EQ",
                            "value": "02",
                        },
                    },
                    "field": "TargetId",
                },
            },
        ]

        rules_path.write_text(json.dumps(rules_data, ensure_ascii=False), encoding="utf-8")

        # Load package through ProcessPackageLoader -> runs ProcessPackageValidator.validate(package)
        loaded = ProcessPackageLoader.load(target)
        assert loaded.process.process_code == "P.TS.01"
        assert len(loaded.rules["P.TS.01.MSG.001"].structured_rules) == 3
