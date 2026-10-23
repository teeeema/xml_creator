"""Requirement-specific runtime proof for OP49 implementation Wave 2."""

from pathlib import Path

import pytest

from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.rules_engine import RuleStatus


PACKAGE = Path(__file__).parents[1]

CALENDAR_RULE = ("P.DS.01.MSG.002", "P.DS.01.MSG.002.R006")
AGGREGATE_RULES = (
    ("P.DS.01.MSG.005", "P.DS.01.MSG.005.R023", "3.5.9", "DistributableDutyAmount"),
    ("P.DS.01.MSG.005", "P.DS.01.MSG.005.R029", "3.5.10", "TransferDistributedDutyAmount"),
    ("P.DS.01.MSG.005", "P.DS.01.MSG.005.R036", "3.5.12", "StopTransferDistributedDutyAmount"),
    ("P.DS.01.MSG.006", "P.DS.01.MSG.006.R019", "3.5.9", "DistributableDutyAmount"),
    ("P.DS.01.MSG.006", "P.DS.01.MSG.006.R025", "3.5.10", "TransferDistributedDutyAmount"),
    ("P.DS.01.MSG.006", "P.DS.01.MSG.006.R032", "3.5.12", "StopTransferDistributedDutyAmount"),
)


def _base_values(engine: EaeuXmlEngine, message_code: str) -> tuple[dict[str, object], dict[str, str]]:
    structure = engine.get_structure(message_code, mode=GenerationMode.TEST)
    values: dict[str, object] = {}
    for field in structure.fields:
        if field.kind == "ATTRIBUTE":
            values[field.path] = (
                "AAA" if field.xml_name == "currencyCode"
                else "0" if field.xml_name == "scaleNumber"
                else "ID"
            )
        elif field.min_occurs:
            datatype = field.datatype or ""
            values[field.path] = (
                "2024-01-03T00:00:00" if "DateTime" in datatype
                else "2024-01-03" if "DateType" in datatype
                else True if "Indicator" in datatype
                else "0.00" if "PaymentAmount" in datatype
                else "AA" if "CountryCode" in datatype
                else "x"
            )

    by_id = {field.field_id: field.path for field in structure.fields}
    values.update(
        {
            by_id["3"]: [None],
            by_id["3.1"]: "2024-01-15",
            by_id["3.2"]: "2024-01-20",
            by_id["3.3"]: "2023-12-31",
            by_id["3.5"]: [None],
            by_id["3.5.1"]: [True],
        }
    )

    for field_id, amount_name in (
        ("3.5.9", "DistributableDutyAmount"),
        ("3.5.10", "TransferDistributedDutyAmount"),
        ("3.5.12", "StopTransferDistributedDutyAmount"),
    ):
        collection = by_id[field_id]
        values.update(
            {
                collection: [None, None, None],
                collection + "/ds01sdo:TotalAmountIndicator": [True, False, False],
                collection + "/csdo:UnifiedCountryCode": [None, "AA", "BB"],
                collection + "/ds01sdo:" + amount_name: ["10.00", "4.00", "6.00"],
            }
        )

    if message_code == "P.DS.01.MSG.005":
        values[by_id["3.4"]] = "2024-01-21T00:00:00"
    return values, by_id


def _evaluation(engine: EaeuXmlEngine, message_code: str, rule_id: str, values: dict[str, object]):
    result = engine.validate_body(message_code, values, mode=GenerationMode.TEST)
    return result, {item.rule_id: item for item in result.rule_evaluations}[rule_id]


def _local_name(tag: object) -> str:
    return str(tag).rsplit("}", 1)[-1]


def test_wave2_calendar_month_rule_passes_and_serializes_real_xml() -> None:
    engine = EaeuXmlEngine.load_process(PACKAGE)
    message_code, rule_id = CALENDAR_RULE
    values, _ = _base_values(engine, message_code)

    result, evaluation = _evaluation(engine, message_code, rule_id, values)
    body = engine.build_body(message_code, values, mode=GenerationMode.TEST)
    xml_root = body.serialize_xml_element()

    assert result.is_valid
    assert evaluation.status is RuleStatus.PASS
    assert any(_local_name(element.tag) == "EventDate" and element.text == "2024-01-15" for element in xml_root.iter())
    assert any(_local_name(element.tag) == "PreviousReportDate" and element.text == "2023-12-31" for element in xml_root.iter())


def test_wave2_calendar_month_rule_rejects_same_month() -> None:
    engine = EaeuXmlEngine.load_process(PACKAGE)
    message_code, rule_id = CALENDAR_RULE
    values, by_id = _base_values(engine, message_code)
    values[by_id["3.3"]] = "2024-01-01"

    result, evaluation = _evaluation(engine, message_code, rule_id, values)

    assert evaluation.status is RuleStatus.FAIL
    assert any(issue.code == "STRUCTURED_RULE_FAILED" and issue.rule_id == rule_id for issue in result.issues)


@pytest.mark.parametrize(("message_code", "rule_id", "field_id", "amount_name"), AGGREGATE_RULES)
def test_wave2_aggregate_rules_pass_and_serialize_real_xml(
    message_code: str, rule_id: str, field_id: str, amount_name: str,
) -> None:
    engine = EaeuXmlEngine.load_process(PACKAGE)
    values, _ = _base_values(engine, message_code)

    result, evaluation = _evaluation(engine, message_code, rule_id, values)
    body = engine.build_body(message_code, values, mode=GenerationMode.TEST)
    xml_root = body.serialize_xml_element()

    assert result.is_valid
    assert evaluation.status is RuleStatus.PASS
    assert sum(_local_name(element.tag) == amount_name for element in xml_root.iter()) == 3


@pytest.mark.parametrize(("message_code", "rule_id", "field_id", "amount_name"), AGGREGATE_RULES)
def test_wave2_aggregate_rules_reject_wrong_total(
    message_code: str, rule_id: str, field_id: str, amount_name: str,
) -> None:
    engine = EaeuXmlEngine.load_process(PACKAGE)
    values, by_id = _base_values(engine, message_code)
    amount_path = by_id[field_id] + "/ds01sdo:" + amount_name
    values[amount_path] = ["9.00", "4.00", "6.00"]

    result, evaluation = _evaluation(engine, message_code, rule_id, values)

    assert evaluation.status is RuleStatus.FAIL
    assert any(issue.code == "STRUCTURED_RULE_FAILED" and issue.rule_id == rule_id for issue in result.issues)
