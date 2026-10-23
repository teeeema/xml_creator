import csv
import json
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import BodyValidationResult, GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parent
MESSAGE = "P.SP.02.MSG.001"
APP = "ipcdo:TrademarkApplicationDetails"
DOC_KIND_CODE = f"{APP}/ipsdo:IPDocKindCode"
DOC_KIND_NAME = f"{APP}/ipsdo:IPDocKindName"
CLASSIFIER_PATH = PACKAGE / "normative_classifier_data" / "P.CLS.027.yaml"
USAGE_REPORT = ROOT / "codex_reports" / "OP22_P_SP_02" / "P_CLS_027" / "OP22_P_CLS_027_USAGE.csv"


def _classifier_entries() -> dict[str, dict[str, object]]:
    data = json.loads(CLASSIFIER_PATH.read_text(encoding="utf-8"))
    assert data["classifier"] == "P.CLS.027"
    return {entry["code"]: entry for entry in data["entries"]}


def test_pcls027_07220_is_source_exact_and_current_revision() -> None:
    entry = _classifier_entries()["07220"]

    assert entry["name"] == (
        "заявка на регистрацию товарного знака, знака обслуживания "
        "Евразийского экономического союза"
    )
    assert entry["member_states"] == ["AM", "BY", "KZ", "KG", "RU"]
    assert entry["source_document"] == "Решение Коллегии ЕЭК от 27.07.2021 №92"
    assert entry["source_page"] == 10
    assert "Решения №148" in entry["effective_revision"]


def test_pcls027_07245_and_07250_preserve_transformation_direction() -> None:
    entries = _classifier_entries()

    assert entries["07245"]["name"] == (
        "ходатайство о преобразовании коллективного знака Евразийского экономического союза "
        "в товарный знак, знак обслуживания Евразийского экономического союза"
    )
    assert entries["07250"]["name"] == (
        "ходатайство о преобразовании товарного знака, знака обслуживания Евразийского экономического союза "
        "в коллективный знак Евразийского экономического союза"
    )
    assert entries["07245"]["source_page"] == 11
    assert entries["07250"]["source_page"] == 11


def test_every_exact_usage_code_exists_in_op22_classifier_dataset() -> None:
    entries = _classifier_entries()
    with USAGE_REPORT.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    exact_rows = [row for row in rows if row["match_status"] == "EXACT_MATCH"]
    assert exact_rows
    for row in exact_rows:
        codes = [code.strip() for code in row["classifier_code"].split("|") if code.strip()]
        assert len(codes) == 1, row["canonical_requirement_id"]
        assert codes[0] in entries, row["canonical_requirement_id"]


def test_msg001_raw_validation_enforces_07220_and_forbids_name() -> None:
    engine = EaeuXmlEngine.load_process(PACKAGE)

    correct = engine.validate_body(MESSAGE, {DOC_KIND_CODE: "07220"}, mode=GenerationMode.TEST)
    assert not any(
        issue.code in {"FIXED_VALUE_MISMATCH", "FORBIDDEN_FIELD"}
        and issue.field_path in {DOC_KIND_CODE, DOC_KIND_NAME}
        for issue in correct.issues
    )

    wrong = engine.validate_body(MESSAGE, {DOC_KIND_CODE: "99999"}, mode=GenerationMode.TEST)
    assert any(issue.code == "FIXED_VALUE_MISMATCH" and issue.field_path == DOC_KIND_CODE for issue in wrong.issues)

    name_only = engine.validate_body(MESSAGE, {DOC_KIND_NAME: "legacy name"}, mode=GenerationMode.TEST)
    assert any(issue.code == "FORBIDDEN_FIELD" and issue.field_path == DOC_KIND_NAME for issue in name_only.issues)

    both = engine.validate_body(
        MESSAGE,
        {DOC_KIND_CODE: "07220", DOC_KIND_NAME: "legacy name"},
        mode=GenerationMode.TEST,
    )
    assert any(issue.code == "FORBIDDEN_FIELD" and issue.field_path == DOC_KIND_NAME for issue in both.issues)


def test_msg001_builder_materializes_07220_and_omits_name() -> None:
    engine = EaeuXmlEngine.load_process(PACKAGE)

    # Isolate serialization/defaulting from unrelated MSG.001 required-field
    # constraints; raw validation behavior is covered separately above.
    with patch.object(engine.body_provider, "validate_body", return_value=BodyValidationResult(())):
        body = engine.build_body(MESSAGE, {}, mode=GenerationMode.TEST)

    xml = ET.tostring(body.serialize_xml_element(), encoding="unicode")
    assert "IPDocKindCode" in xml
    assert ">07220<" in xml
    assert "IPDocKindName" not in xml


def test_pcls027_07360_is_present_in_current_decision_92_revision() -> None:
    entry = _classifier_entries()["07360"]

    assert entry["name"] == (
        "доводы заявителя в связи с обращением заинтересованного лица о наличии "
        "оснований для отказа в регистрации товарного знака, знака обслуживания "
        "Евразийского экономического союза, предусмотренных статьей 8 Договора "
        "о товарных знаках, знаках обслуживания и наименованиях мест происхождения "
        "товаров Евразийского экономического союза от 3 февраля 2020 года"
    )
    assert entry["member_states"] == ["AM", "BY", "KZ", "KG", "RU"]
    assert entry["source_document"] == "Решение Коллегии ЕЭК от 27.07.2021 №92"
    assert entry["source_page"] == 14
    assert entry["effective_revision"] == "Решение №92 в редакции Решения №148 от 23.12.2024"
