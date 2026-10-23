from collections import Counter
from pathlib import Path

import pytest

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


ROOT = Path(__file__).resolve().parents[2]
PROCESS = "P.SP.02"
TRANSACTION = "P.SP.02.TRN.001"
MESSAGE = "P.SP.02.MSG.001"
OTHER_MESSAGE = "P.SP.02.MSG.002"
APP = "ipcdo:TrademarkApplicationDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails/csdo:StatusCode"
STATUS_CODELIST = f"{STATUS}/@codeListId"
APPLICATION_ID = f"{APP}/ipsdo:TrademarkApplicationId"
RECEIPT_DATE = f"{APP}/ipsdo:ApplicationReceiptDate"
DOC_KIND_CODE = f"{APP}/ipsdo:IPDocKindCode"
DOC_KIND_NAME = f"{APP}/ipsdo:IPDocKindName"
CONSENT = f"{APP}/ipsdo:ConsentToDataProcessingIndicator"
PATENT_COUNTRY = f"{APP}/ipcdo:PatentAuthorityDetails/csdo:UnifiedCountryCode"
PATENT_COUNTRY_CODELIST = f"{PATENT_COUNTRY}/@codeListId"


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


def _policies(app: EaeuXmlApplication):
    engine = app._engine(PROCESS)
    structure = app._structure_for_form(engine, MESSAGE)
    definition = engine.package.message_field_policies[MESSAGE]
    return structure, app.message_field_policy_resolver.resolve_all(structure, definition)


def test_status_and_primary_required_fields_have_effective_form_policy(app: EaeuXmlApplication) -> None:
    fields = _flatten(app.get_form(PROCESS, TRANSACTION, MESSAGE).fields)

    status = fields[STATUS]
    assert status.effective_message_policy == "FIXED"
    assert status.fixed_value == "01"
    assert status.required is True
    assert status.editable is False
    assert status.visibility == "VISIBLE"

    code_list = fields[STATUS_CODELIST]
    assert code_list.effective_message_policy == "FORBIDDEN"
    assert code_list.visibility == "HIDDEN"
    assert code_list.editable is False

    for path in (APPLICATION_ID, RECEIPT_DATE):
        field = fields[path]
        assert field.effective_message_policy == "REQUIRED"
        assert field.required is True
        assert field.visibility == "VISIBLE"


def test_fixed_and_forbidden_values_are_enforced_at_non_gui_boundary(app: EaeuXmlApplication) -> None:
    sanitized = app._sanitize_message_values(
        PROCESS,
        MESSAGE,
        {
            STATUS: "99",
            STATUS_CODELIST: "STALE-LIST",
            CONSENT: "0",
        },
    )

    assert sanitized[STATUS] == "01"
    assert STATUS_CODELIST not in sanitized
    assert sanitized[CONSENT] == 1


def test_country_codelist_is_fixed_only_when_country_is_present(app: EaeuXmlApplication) -> None:
    fields = _flatten(app.get_form(PROCESS, TRANSACTION, MESSAGE).fields)
    code_list = fields[PATENT_COUNTRY_CODELIST]
    assert code_list.effective_message_policy == "FIXED"
    assert code_list.fixed_value == "ВОИС ST.3"
    assert code_list.editable is False
    assert code_list.message_policy_materialize_when_parent_present is True

    present = app._sanitize_message_values(
        PROCESS,
        MESSAGE,
        {PATENT_COUNTRY: "RU", PATENT_COUNTRY_CODELIST: "WRONG"},
    )
    assert present[PATENT_COUNTRY_CODELIST] == "ВОИС ST.3"

    absent = app._sanitize_message_values(
        PROCESS,
        MESSAGE,
        {PATENT_COUNTRY_CODELIST: "STALE"},
    )
    assert PATENT_COUNTRY_CODELIST not in absent


def test_document_kind_branch_resolves_to_confirmed_classifier_code(app: EaeuXmlApplication) -> None:
    fields = _flatten(app.get_form(PROCESS, TRANSACTION, MESSAGE).fields)

    code = fields[DOC_KIND_CODE]
    assert code.effective_message_policy == "FIXED"
    assert code.fixed_value == "07220"
    assert code.required is True
    assert code.editable is False
    assert code.visibility == "VISIBLE"
    assert "07220" in (code.message_policy_condition or "")
    assert "Решению №92" in (code.message_policy_condition or "")

    name = fields[DOC_KIND_NAME]
    assert name.effective_message_policy == "FORBIDDEN"
    assert name.fixed_value is None
    assert name.required is False
    assert name.editable is False
    assert name.visibility == "HIDDEN"

    required_values = app.generate_required_data(PROCESS, TRANSACTION, MESSAGE, seed=17)
    test_values = app.generate_test_data(PROCESS, TRANSACTION, MESSAGE, seed=17)
    for values in (required_values, test_values):
        assert values[DOC_KIND_CODE] == "07220"
        assert DOC_KIND_NAME not in values

    policy_text = (ROOT / "P.SP.02_OP_22" / "message_field_policies" / f"{MESSAGE}.yaml").read_text(encoding="utf-8")
    assert "CONDITIONAL_UNRESOLVED" not in policy_text
    assert "missing payload" not in policy_text.lower()


def test_document_kind_policy_sanitizes_stale_or_wrong_values(app: EaeuXmlApplication) -> None:
    sanitized = app._sanitize_message_values(
        PROCESS,
        MESSAGE,
        {
            DOC_KIND_CODE: "99999",
            DOC_KIND_NAME: "Устаревшее наименование",
        },
    )

    assert sanitized[DOC_KIND_CODE] == "07220"
    assert DOC_KIND_NAME not in sanitized


def test_document_kind_engine_validation_rejects_unsanitized_invalid_branch(app: EaeuXmlApplication) -> None:
    engine = app._engine(PROCESS)

    valid = engine.validate_body(MESSAGE, {DOC_KIND_CODE: "07220"}, mode=GenerationMode.TEST)
    valid_codes = {(issue.code, issue.field_path) for issue in valid.issues}
    assert ("FIXED_VALUE_MISMATCH", DOC_KIND_CODE) not in valid_codes
    assert ("FORBIDDEN_FIELD", DOC_KIND_NAME) not in valid_codes

    invalid = engine.validate_body(
        MESSAGE,
        {DOC_KIND_CODE: "99999", DOC_KIND_NAME: "Устаревшее наименование"},
        mode=GenerationMode.TEST,
    )
    invalid_codes = {(issue.code, issue.field_path) for issue in invalid.issues}
    assert ("FIXED_VALUE_MISMATCH", DOC_KIND_CODE) in invalid_codes
    assert ("FORBIDDEN_FIELD", DOC_KIND_NAME) in invalid_codes


def test_document_kind_round_trips_through_structure_serializer(app: EaeuXmlApplication) -> None:
    engine = app._engine(PROCESS)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    provider = engine.body_provider

    root = provider._serialize(structure, {DOC_KIND_CODE: "07220"})
    extracted, issues = provider._values_from_element(structure, root)

    assert issues == []
    assert extracted[DOC_KIND_CODE] == "07220"
    assert DOC_KIND_NAME not in extracted


def test_forbidden_values_are_removed_from_stale_draft_and_test_data(app: EaeuXmlApplication, tmp_path: Path) -> None:
    engine = app._engine(PROCESS)
    message = engine.get_message(MESSAGE)
    profile = engine.package.profile
    active = profile.structures[message.structure_id].active_version
    stale = app.drafts.new_document(
        process_code=PROCESS,
        process_version=profile.process_version,
        transaction_code=TRANSACTION,
        message_code=MESSAGE,
        structure_id=message.structure_id,
        structure_version=active,
        generation_mode="TEST",
        values={STATUS: "99", STATUS_CODELIST: "STALE-LIST"},
    )
    path = tmp_path / "stale.eaeudraft.json"
    app.drafts.save_draft(stale, path)

    loaded = app.load_draft(path)
    assert STATUS_CODELIST in loaded.document.values
    assert STATUS_CODELIST not in loaded.compatible_values
    assert loaded.compatible_values[STATUS] == "01"
    assert any(item.startswith("MESSAGE_POLICY_DROPPED_FIELDS:") for item in loaded.warnings)

    generated = app.generate_test_data(PROCESS, TRANSACTION, MESSAGE, seed=23)
    _, policies = _policies(app)
    forbidden_paths = {path for path, policy in policies.items() if policy.policy == "FORBIDDEN"}
    assert forbidden_paths.isdisjoint(generated)
    assert generated[STATUS] == "01"


def test_required_policy_adds_validation_errors_for_missing_leaf_fields(app: EaeuXmlApplication) -> None:
    validation = app.validate(PROCESS, TRANSACTION, MESSAGE, {})
    required_errors = {
        issue.field_path
        for issue in validation.errors
        if issue.code == "MESSAGE_POLICY_REQUIRED"
    }
    assert APPLICATION_ID in required_errors
    assert RECEIPT_DATE in required_errors


def test_group_policy_and_existing_cardinality_rule_remain_active(app: EaeuXmlApplication) -> None:
    fields = _flatten(app.get_form(PROCESS, TRANSACTION, MESSAGE).fields)
    assert fields[APP].effective_message_policy == "REQUIRED"

    engine = app._engine(PROCESS)
    rule = next(
        item
        for item in engine.rules[MESSAGE].structured_rules
        if item["rule_id"] == "P.SP.02.MSG.001.REQ.001"
    )
    evaluator = StructuredRuleEvaluator()
    assert evaluator.evaluate(rule, {APP: [None]}).status is RuleStatus.PASS
    assert evaluator.evaluate(rule, {APP: [None, None]}).status is RuleStatus.FAIL


def test_all_404_structure_fields_receive_exactly_one_effective_policy(app: EaeuXmlApplication) -> None:
    structure, policies = _policies(app)

    assert len(structure.presentation_fields) == 404
    assert len(policies) == 404
    assert set(policies) == {field.path for field in structure.presentation_fields}
    assert Counter(policy.policy for policy in policies.values()) == Counter(
        {"FORBIDDEN": 148, "OPTIONAL": 145, "CONDITIONAL": 74, "REQUIRED": 20, "FIXED": 17}
    )


def test_msg002_has_no_message_specific_policy_and_sanitizer_is_identity(app: EaeuXmlApplication) -> None:
    engine = app._engine(PROCESS)
    assert engine.package.message_field_policies.get(OTHER_MESSAGE) is None

    values = {"legacy:path": "legacy-value"}
    assert app._sanitize_message_values(PROCESS, OTHER_MESSAGE, values) == values

    transaction = engine.get_transaction(TRANSACTION)
    assert OTHER_MESSAGE in transaction.response_messages
    fields = _flatten(app.get_form(PROCESS, TRANSACTION, OTHER_MESSAGE).fields)
    assert fields
    assert all(field.effective_message_policy is None for field in fields.values())
