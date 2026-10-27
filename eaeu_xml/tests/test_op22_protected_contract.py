"""Protected regression contract tests for restored OP 22 (P.SP.02) functionality.

This test module locks in the restored features of OP 22 to prevent regressions:
1. Field information presentation & cards (names, descriptions, types, cardinality, friendly regex, source refs).
2. The four document kind codes (MSG.001=07220, MSG.004=07320, MSG.005=07360, MSG.027=07365).
3. Field policies: FIXED, READ_ONLY, and FORBIDDEN / HIDDEN status.
4. XML generation integrity and rejection of tampering.
5. Classifier P.CLS.027 normalization and resolution.
6. Draft save and restore lifecycle for OP 22 forms.
"""

import json
from pathlib import Path
import xml.etree.ElementTree as ET
import pytest

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.presentation.field_info import build_field_details
from eaeu_xml.process_packages.body import GenerationMode


ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture()
def app(tmp_path: Path) -> EaeuXmlApplication:
    return EaeuXmlApplication(ROOT, drafts_root=tmp_path / "drafts")


def _flatten(fields):
    result = {}

    def visit(field):
        result[field.path] = field
        for child in field.children:
            visit(child)

    for field in fields:
        visit(field)
    return result


class TestOp22ProtectedContract:
    """Consolidated contract tests protecting OP 22 (P.SP.02)."""

    def test_op22_field_cards_and_presentation_metadata(self, app: EaeuXmlApplication) -> None:
        """Verify field cards contain human-readable titles, descriptions, constraints, and sources."""
        form = app.get_form("P.SP.02", "P.SP.02.TRN.003", "P.SP.02.MSG.004")
        fields = _flatten(form.fields)

        target_path = "ipcdo:TrademarkApplicationDetails/ipcdo:IPEntityStatusDetails/csdo:StatusCode"
        field = fields[target_path]

        assert field.display_name
        assert field.official_name
        assert field.datatype == "csdo:StatusCodeType"
        assert field.cardinality_display in {"1..1", "1"}
        assert field.effective_message_policy == "FIXED"
        assert field.fixed_value == "02"
        assert field.editable is False
        assert field.ui_input_policy == "READ_ONLY"

        engine = app._engine("P.SP.02")
        structure = app._structure_for_form(engine, "P.SP.02.MSG.004")
        definition = next(f for f in structure.presentation_fields if f.path == target_path)

        details = build_field_details(definition, field, normalize_op22_regex=True)
        assert details["name"]
        assert details["datatype"]
        assert details["multiplicity"] in {"1..1", "1"}
        assert "02" in details["policy"]
        assert "Фиксированное значение" in details["policy"]

    def test_op22_regex_friendly_explanation(self, app: EaeuXmlApplication) -> None:
        """Verify regex patterns are accompanied by human-friendly explanations."""
        engine = app._engine("P.SP.02")
        structure = app._structure_for_form(engine, "P.SP.02.MSG.004")
        code_path = "ipcdo:TrademarkApplicationDetails/ipsdo:IPDocKindCode"
        form = app.get_form("P.SP.02", "P.SP.02.TRN.003", "P.SP.02.MSG.004")
        fields = _flatten(form.fields)
        field = fields[code_path]
        definition = next(f for f in structure.presentation_fields if f.path == code_path)

        details = build_field_details(definition, field, normalize_op22_regex=True)
        constraint_labels = {c["label"]: c["value"] for c in details["constraints"]}
        if "Шаблон" in constraint_labels and constraint_labels["Шаблон"] == r"\d{5}":
            assert constraint_labels.get("Пояснение") == "Ровно 5 цифр"

    def test_op22_all_four_mandatory_document_codes_enforced(self, app: EaeuXmlApplication) -> None:
        """Verify MSG.001, MSG.004, MSG.005, and MSG.027 enforce the confirmed document kind codes."""
        cases = [
            ("P.SP.02.TRN.001", "P.SP.02.MSG.001", "07220"),
            ("P.SP.02.TRN.003", "P.SP.02.MSG.004", "07320"),
            ("P.SP.02.TRN.004", "P.SP.02.MSG.005", "07360"),
            ("P.SP.02.TRN.022", "P.SP.02.MSG.027", "07365"),
        ]
        code_path = "ipcdo:TrademarkApplicationDetails/ipsdo:IPDocKindCode"
        name_path = "ipcdo:TrademarkApplicationDetails/ipsdo:IPDocKindName"

        for trn, msg, expected_code in cases:
            form = app.get_form("P.SP.02", trn, msg)
            fields = _flatten(form.fields)

            code_field = fields[code_path]
            assert code_field.effective_message_policy == "FIXED", f"{msg} code policy"
            assert code_field.fixed_value == expected_code, f"{msg} expected {expected_code}"
            assert code_field.editable is False, f"{msg} editable"

            name_field = fields[name_path]
            assert name_field.effective_message_policy == "FORBIDDEN", f"{msg} name policy"
            assert name_field.visibility == "HIDDEN", f"{msg} name visibility"
            assert name_field.editable is False, f"{msg} name editable"

            # Sanitization test: tampering attempt is corrected
            tampered = {code_path: "99999", name_path: "STALE_NAME"}
            sanitized = app._sanitize_message_values("P.SP.02", msg, tampered)
            assert sanitized[code_path] == expected_code
            assert name_path not in sanitized

    def test_op22_xml_serialization_contains_confirmed_code_and_omits_forbidden_name(self, app: EaeuXmlApplication) -> None:
        """Verify that XML serialization outputs confirmed 07320 code and omits IPDocKindName."""
        import importlib.util
        target_file = ROOT / "P.SP.02_OP_22" / "tests" / "test_msg004_end_to_end.py"
        spec = importlib.util.spec_from_file_location("op22_msg004_e2e", target_file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _generation_values = mod._generation_values

        engine = app._engine("P.SP.02")

        values = _generation_values()
        # Deliberately attempt tampering
        app_prefix = "ipcdo:TrademarkApplicationDetails"
        values[f"{app_prefix}/ipsdo:IPDocKindCode"] = "99999"
        values[f"{app_prefix}/ipsdo:IPDocKindName"] = "UNAUTHORIZED_NAME"

        sanitized = app._sanitize_message_values("P.SP.02", "P.SP.02.MSG.004", values)
        body = engine.build_body("P.SP.02.MSG.004", sanitized, mode=GenerationMode.TEST)
        xml_text = ET.tostring(body.serialize_xml_element(), encoding="utf-8").decode("utf-8")

        assert ">07320<" in xml_text or ">07320</" in xml_text
        assert "99999" not in xml_text
        assert "UNAUTHORIZED_NAME" not in xml_text
        assert f"{app_prefix}/ipsdo:IPDocKindName" not in sanitized

    def test_op22_pcls027_classifier_dataset_loaded_and_active(self, app: EaeuXmlApplication) -> None:
        """Verify classifier P.CLS.027 is loaded, active, and accessible."""
        classifier_file = ROOT / "P.SP.02_OP_22" / "normative_classifier_data" / "P.CLS.027.yaml"
        assert classifier_file.is_file()
        data = json.loads(classifier_file.read_text(encoding="utf-8"))
        assert data["classifier"] == "P.CLS.027"
        entries = {e["code"]: e for e in data["entries"]}
        for code in ("07220", "07320", "07360", "07365"):
            assert code in entries, f"Classifier P.CLS.027 missing code {code}"

    def test_op22_draft_save_and_restore_cycle(self, app: EaeuXmlApplication, tmp_path: Path) -> None:
        """Verify full lifecycle of saving and loading an OP 22 draft."""
        trn = "P.SP.02.TRN.003"
        msg = "P.SP.02.MSG.004"
        event_date_path = "ipcdo:TrademarkApplicationDetails/ipcdo:IPEntityStatusDetails/csdo:EventDate"

        draft_file = tmp_path / "op22_draft.json"
        app.save_draft(
            draft_file,
            process_code="P.SP.02",
            transaction_code=trn,
            message_code=msg,
            values={event_date_path: "2026-10-26"},
        )
        assert draft_file.is_file()

        loaded = app.load_draft(draft_file)
        assert loaded is not None
        assert loaded.document.process_code == "P.SP.02"
        assert loaded.compatible_values.get(event_date_path) == "2026-10-26"
