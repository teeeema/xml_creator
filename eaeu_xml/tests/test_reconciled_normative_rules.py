"""Source-backed form rules; XML proofs are runtime checks, not official XSD proof."""
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.application.message_field_policy import MessageFieldPolicyResolver
from eaeu_xml.application.xml_validation_service import XmlValidationService
from eaeu_xml.process_packages import ProcessPackageLoader
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

ROOT = Path(__file__).resolve().parents[2]
COUNTRY = "DrugRegistrationDetails/DrugCountryRegistrationDetails/UnifiedCountryCode"
AUTHORITY = "ipcdo:ApellationOfOriginApplicationDetails/ipcdo:PatentAuthorityDetails"
CASES = (
    ("P.SP.03", "P.SP.03.TRN.018", "P.SP.03.MSG.023",
     "ipsdo:ApellationOfOriginApplicationId", "P.SP.03.MSG.023.T27.REQ.6"),
    ("P.SP.03", "P.SP.03.TRN.001", "P.SP.03.MSG.001",
     AUTHORITY + "/csdo:AuthorityName", "P.SP.03.MSG.001.REQ.014"),
    ("P.MM.01", "P.MM.01.TRN.018", "P.MM.01.MSG.027",
     "RegistrationNumberId", "P.MM.01.MSG.027.T24.REQ.1"),
    ("P.MM.01", "P.MM.01.TRN.001", "P.MM.01.MSG.001",
     COUNTRY + "/@codeListId", "P.MM.01.MSG.001.R34"),
)


@pytest.fixture()
def app(tmp_path):
    return EaeuXmlApplication(ROOT, drafts_root=tmp_path / "drafts")


def evaluator(engine, message):
    structure = engine.get_structure(message, mode="TEST")
    parents = {f.parent for f in structure.fields if f.kind != "ATTRIBUTE"}
    return StructuredRuleEvaluator(complex_paths={f.path for f in structure.fields
                                                  if f.field_id in parents})


def failed_rule(result, identifier):
    return any(r.rule_id == identifier and r.status == RuleStatus.FAIL
               for r in result.rule_evaluations)


def xml_body(root):
    return root.find("{http://www.w3.org/2003/05/soap-envelope}Body")[0]


@pytest.mark.parametrize("process,transaction,message,path,rule_id", CASES)
def test_reconciled_rules_form_generation_and_xml_roundtrip(
    app, process, transaction, message, path, rule_id,
):
    fields = {f.path: f for f in app._walk_fields(app.get_form(process, transaction, message).fields)}
    field = fields[path]
    assert field.effective_message_policy == ("FIXED" if path.endswith("/@codeListId") else "REQUIRED")
    assert rule_id in field.message_policy_req_ids
    values = app.generate_test_data(process, transaction, message, seed=29)
    engine = app._engine(process)
    assert engine.validate_body(message, values, mode="TEST").is_valid
    generated = app.generate_test_xml(process, transaction, message, values)
    assert generated.success
    assert XmlValidationService().validate(generated.xml, engine=engine,
        transaction_code=transaction, message_code=message, mode="TEST").is_valid
    structure = engine.get_structure(message, mode="TEST")
    extracted = engine.body_provider.extract_values(structure, xml_body(ET.fromstring(generated.xml)))
    result = engine.validate_body(message, extracted, mode="TEST")
    assert result.is_valid
    assert any(r.rule_id == rule_id and r.status == RuleStatus.PASS for r in result.rule_evaluations)


@pytest.mark.parametrize("process,transaction,message,path,rule_id", CASES)
def test_actual_xml_mutation_is_rejected_by_body_rule(app, process, transaction, message, path, rule_id):
    generated = app.generate_test_xml(process, transaction, message,
        app.generate_test_data(process, transaction, message, seed=29))
    assert generated.success
    root = ET.fromstring(generated.xml)
    if path.endswith("/@codeListId"):
        nodes = [n for n in xml_body(root).iter() if n.tag.rsplit("}", 1)[-1] == "UnifiedCountryCode"]
        assert nodes and all(n.attrib["codeListId"] == "P.CLS.019" for n in nodes)
        nodes[0].attrib["codeListId"] = "2021"
    else:
        name = path.rsplit("/", 1)[-1].split(":")[-1]
        node = next(n for n in xml_body(root).iter() if n.tag.rsplit("}", 1)[-1] == name)
        node.text = "   "
    engine = app._engine(process)
    # Reparse the changed bytes, then extract actual body values. Testing the
    # old input dictionary would not prove that a changed XML is rejected.
    changed = ET.fromstring(ET.tostring(root, encoding="unicode"))
    values = engine.body_provider.extract_values(engine.get_structure(message, mode="TEST"), xml_body(changed))
    result = engine.validate_body(message, values, mode="TEST")
    assert not result.is_valid
    assert failed_rule(result, rule_id)


@pytest.mark.parametrize("case", CASES[:3])
@pytest.mark.parametrize("bad", [None, "", "   "])
def test_required_scalar_rejects_empty_values(app, case, bad):
    process, transaction, message, path, rule_id = case
    values = app.generate_test_data(process, transaction, message, seed=29)
    values[path] = bad
    result = app._engine(process).validate_body(message, values, mode="TEST")
    assert not result.is_valid
    assert failed_rule(result, rule_id)


def test_op23_authority_rule_preserves_instance_context_and_absent_parent(app):
    engine = app._engine("P.SP.03")
    rule = next(r for r in engine.rules["P.SP.03.MSG.001"].structured_rules
                if r["rule_id"] == "P.SP.03.MSG.001.REQ.014")
    evaluate = evaluator(engine, "P.SP.03.MSG.001")
    assert evaluate.evaluate(rule, {}).status == RuleStatus.PASS
    assert evaluate.evaluate(rule, {AUTHORITY: None}).status == RuleStatus.PASS
    values = {AUTHORITY: [None, None], AUTHORITY + "/csdo:UnifiedCountryCode": ["RU", "BY"],
              AUTHORITY + "/csdo:AuthorityName": ["Authority A", "Authority B"]}
    assert evaluate.evaluate(rule, values).status == RuleStatus.PASS
    for child in ("csdo:UnifiedCountryCode", "csdo:AuthorityName"):
        for index in (0, 1):
            wrong = deepcopy(values)
            wrong[AUTHORITY + "/" + child][index] = ""
            assert evaluate.evaluate(rule, wrong).status == RuleStatus.FAIL


def test_v110_country_only_scope_and_parent_slots(app):
    engine = app._engine("P.MM.01")
    assert engine.package.profile.process_version == "1.1.0"
    form = app.get_form("P.MM.01", "P.MM.01.TRN.001", "P.MM.01.MSG.001")
    fields = tuple(app._walk_fields(form.fields))
    countries = [f for f in fields if f.path.endswith("UnifiedCountryCode/@codeListId")]
    assert len(countries) == 11
    for field in countries:
        assert (field.effective_message_policy, field.fixed_value, field.ui_input_policy, field.editable) == (
            "FIXED", "P.CLS.019", "READ_ONLY", False)
        assert field.message_policy_materialize_when_parent_present
    other_ids = [f for f in fields if f.path.endswith("/@codeListId") and f not in countries]
    assert other_ids and all(f.fixed_value != "P.CLS.019" for f in other_ids)
    rule = next(r for r in engine.rules["P.MM.01.MSG.001"].structured_rules if r["rule_id"].endswith(".R34"))
    evaluate = evaluator(engine, "P.MM.01.MSG.001")
    assert evaluate.evaluate(rule, {}).status == RuleStatus.PASS
    assert evaluate.evaluate(rule, {COUNTRY: "RU"}).status == RuleStatus.FAIL
    assert evaluate.evaluate(rule, {COUNTRY: [None, "RU"],
        COUNTRY + "/@codeListId": [None, "P.CLS.019"]}).status == RuleStatus.PASS
    values = {COUNTRY: ["RU", "BY"], COUNTRY + "/@codeListId": ["P.CLS.019", "P.CLS.019"]}
    assert evaluate.evaluate(rule, values).status == RuleStatus.PASS
    values[COUNTRY + "/@codeListId"][1] = "2021"
    assert evaluate.evaluate(rule, values).status == RuleStatus.FAIL
    assert app._sanitize_message_values("P.MM.01", "P.MM.01.MSG.001", values)[COUNTRY + "/@codeListId"][1] == "2021"
    generated = app.generate_test_data("P.MM.01", "P.MM.01.TRN.001", "P.MM.01.MSG.001", seed=29)
    # An absent optional holder is not created merely to materialize its fixed id.
    optional = "DrugRegistrationDetails/RegistrationCertificateHolderDetails/UnifiedCountryCode"
    assert optional not in generated and optional + "/@codeListId" not in generated


def test_draft_2021_is_an_independent_component_and_stays_blocked(app):
    package = ROOT / "P.MM.01_OP_26/versions/1.3.0"
    structures = ProcessPackageLoader.load_structures(package / "structures")
    structure = next(s for s in structures.values() if s.structure_id == "R.HC.MM.01.001")
    rules = ProcessPackageLoader.load_rules(package / "message_rules")["P.MM.01.MSG.001"]
    policies = MessageFieldPolicyResolver().resolve_structured_rules(structure, rules.structured_rules)
    assert policies[COUNTRY + "/@codeListId"].fixed_value == "2021"
    assert policies[COUNTRY + "/@codeListId"].policy == "FIXED"
    rule = next(r for r in rules.structured_rules
                if r.get("target") == COUNTRY + "/@codeListId" and r.get("operation") == "FIXED")
    values = {COUNTRY: "RU", COUNTRY + "/@codeListId": "2021"}
    # Supply containing contexts explicitly; no production readiness gate bypass.
    for path in rule.get("ancestors", ()):
        values.setdefault(path, None)
    evaluate = StructuredRuleEvaluator()
    assert evaluate.evaluate(rule, values).status == RuleStatus.PASS
    values[COUNTRY + "/@codeListId"] = "P.CLS.019"
    assert evaluate.evaluate(rule, values).status == RuleStatus.FAIL
    editions = {e["version"]: e for e in app.describe_process_editions("P.MM.01")}
    assert editions["1.1.0"]["default"] is True
    assert editions["1.3.0"]["available"] is False
    assert editions["1.3.0"]["block_code"] == "PROCESS_VERSION_NOT_READY"


@pytest.mark.parametrize("bad", [None, "", "2021"])
def test_v110_present_country_cannot_omit_or_change_classifier_id(app, bad):
    engine = app._engine("P.MM.01")
    values = app.generate_test_data("P.MM.01", "P.MM.01.TRN.001", "P.MM.01.MSG.001", seed=29)
    values[COUNTRY + "/@codeListId"] = bad
    assert failed_rule(engine.validate_body("P.MM.01.MSG.001", values, mode="TEST"),
                       "P.MM.01.MSG.001.R34")


def test_legacy_relative_element_roundtrip_keeps_exact_qname_guard(app):
    from eaeu_xml.core.errors import BodyValidationError
    engine = app._engine("P.MM.01")
    generated = app.generate_test_xml("P.MM.01", "P.MM.01.TRN.001", "P.MM.01.MSG.001")
    assert generated.success
    body = xml_body(ET.fromstring(generated.xml))
    relative = next(n for n in body.iter() if n.tag.rsplit("}", 1)[-1] == "StartDateTime")
    # The serializer emitted this declared RELATIVE field; the extractor must
    # accept its declared QName and still reject the same local name elsewhere.
    assert engine.body_provider.extract_values(engine.get_structure("P.MM.01.MSG.001", mode="TEST"), body)
    relative.tag = "{urn:test:wrong}StartDateTime"
    with pytest.raises(BodyValidationError) as error:
        engine.body_provider.extract_values(engine.get_structure("P.MM.01.MSG.001", mode="TEST"), body)
    assert error.value.code == "UNKNOWN_XML_QNAME"
