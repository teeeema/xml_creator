from pathlib import Path

import pytest

from eaeu_xml.application import EaeuXmlApplication


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


def test_op22_msg004_projects_static_required_fixed_and_forbidden_rules(app: EaeuXmlApplication) -> None:
    base = "ipcdo:TrademarkApplicationDetails/ipcdo:IPEntityStatusDetails"
    event_date = f"{base}/csdo:EventDate"
    status_code = f"{base}/csdo:StatusCode"
    status_codelist = f"{status_code}/@codeListId"
    fields = _flatten(app.get_form("P.SP.02", "P.SP.02.TRN.003", "P.SP.02.MSG.004").fields)

    assert fields[event_date].effective_message_policy == "REQUIRED"
    assert fields[event_date].required is True

    assert fields[status_code].effective_message_policy == "FIXED"
    assert fields[status_code].fixed_value == "02"
    assert fields[status_code].editable is False
    assert fields[status_code].ui_input_policy == "READ_ONLY"

    assert fields[status_codelist].effective_message_policy == "FORBIDDEN"
    assert fields[status_codelist].visibility == "HIDDEN"
    assert fields[status_codelist].editable is False

    values = {status_code: "99", status_codelist: "STALE"}
    assert app._sanitize_message_values("P.SP.02", "P.SP.02.MSG.004", values) == {
        **values,
        "ipcdo:TrademarkApplicationDetails/ipsdo:IPDocKindCode": "07320",
    }


def test_op22_msg005_projects_message_specific_signature_and_claim_rules(app: EaeuXmlApplication) -> None:
    signature = "ipcdo:TrademarkApplicationDetails/ipcdo:SignatureDetails"
    request_id = "ipcdo:TrademarkApplicationDetails/ipcdo:TrademarkClaimDetails/ipsdo:RequestId"
    fields = _flatten(app.get_form("P.SP.02", "P.SP.02.TRN.004", "P.SP.02.MSG.005").fields)

    assert fields[signature].effective_message_policy == "FORBIDDEN"
    assert fields[signature].visibility == "HIDDEN"
    assert fields[signature].editable is False

    assert fields[request_id].effective_message_policy == "REQUIRED"
    assert fields[request_id].required is True


def test_op22_msg056_keeps_same_qname_rules_scoped_to_for_each_parent(app: EaeuXmlApplication) -> None:
    root_doc_id = "csdo:DocId"
    attached_doc_id = "ipcdo:IPPaymentDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId"
    fields = _flatten(app.get_form("P.SP.02", "P.SP.02.TRN.050", "P.SP.02.MSG.056").fields)

    assert fields[root_doc_id].effective_message_policy == "FORBIDDEN"
    assert fields[root_doc_id].visibility == "HIDDEN"
    assert fields[root_doc_id].editable is False

    assert fields[attached_doc_id].effective_message_policy == "REQUIRED"
    assert fields[attached_doc_id].required is True


@pytest.mark.parametrize(
    ("process", "transaction", "message", "path"),
    (
        ("P.SP.02", "P.SP.02.TRN.049", "P.SP.02.MSG.055", "ipsdo:TrademarkApplicationId"),
        ("P.SP.03", "P.SP.03.TRN.018", "P.SP.03.MSG.023", "ipsdo:ApellationOfOriginApplicationId"),
        ("P.MM.01", "P.MM.01.TRN.018", "P.MM.01.MSG.027", "RegistrationNumberId"),
    ),
)
def test_top_level_string_target_presence_rules_project_into_form_policy(
    app: EaeuXmlApplication,
    process: str,
    transaction: str,
    message: str,
    path: str,
) -> None:
    fields = _flatten(app.get_form(process, transaction, message).fields)

    assert fields[path].effective_message_policy == "REQUIRED"
    assert fields[path].required is True


def test_op22_msg054_forbids_only_the_confirmed_root_fields(app: EaeuXmlApplication) -> None:
    fields = _flatten(app.get_form("P.SP.02", "P.SP.02.TRN.049", "P.SP.02.MSG.054").fields)

    for path in (
        "ipsdo:ApellationOfOriginApplicationId",
        "csdo:DocId",
        "ipcdo:IPPaymentDetails",
        "ipsdo:DutyPaymentIndicator",
        "csdo:PaymentAmount",
    ):
        assert fields[path].effective_message_policy == "FORBIDDEN"
        assert fields[path].visibility == "HIDDEN"

    nested_doc_ids = [
        field for path, field in fields.items()
        if path != "csdo:DocId" and path.endswith("/csdo:DocId")
    ]
    assert nested_doc_ids
    assert all(field.effective_message_policy != "FORBIDDEN" for field in nested_doc_ids)


def test_op23_msg001_projects_static_authority_requirement(app: EaeuXmlApplication) -> None:
    authority_name = (
        "ipcdo:ApellationOfOriginApplicationDetails/ipcdo:PatentAuthorityDetails/csdo:AuthorityName"
    )
    fields = _flatten(app.get_form("P.SP.03", "P.SP.03.TRN.001", "P.SP.03.MSG.001").fields)

    assert fields[authority_name].effective_message_policy == "REQUIRED"
    assert fields[authority_name].required is True


def test_op26_msg001_projects_static_classifier_id_as_read_only_fixed_value(app: EaeuXmlApplication) -> None:
    code_list_id = "DrugRegistrationDetails/DrugCountryRegistrationDetails/UnifiedCountryCode/@codeListId"
    fields = _flatten(app.get_form("P.MM.01", "P.MM.01.TRN.001", "P.MM.01.MSG.001").fields)

    field = fields[code_list_id]
    assert field.effective_message_policy == "FIXED"
    assert field.fixed_value == "P.CLS.019"
    assert field.editable is False
    assert field.ui_input_policy == "READ_ONLY"
    assert field.message_policy_materialize_when_parent_present is True

    values = {code_list_id: "WRONG"}
    assert app._sanitize_message_values("P.MM.01", "P.MM.01.MSG.001", values) == values


def test_op49_where_scoped_cardinality_is_not_flattened_into_static_policy(app: EaeuXmlApplication) -> None:
    contextual_path = (
        "ChargedDistributedReport/ds01cdo:ChargedDistributedDutyReportDetails/"
        "ds01cdo:ChargedDistributedDutyDetails"
    )
    engine = app._engine("P.DS.01")
    policies = app._effective_message_field_policies(engine, "P.DS.01.MSG.001") or {}

    assert contextual_path not in policies

