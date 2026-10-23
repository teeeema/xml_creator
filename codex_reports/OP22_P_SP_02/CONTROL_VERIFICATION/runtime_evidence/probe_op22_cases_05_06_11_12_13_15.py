"""Focused, executable control probes for OP22 XML and effective policies."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.process_packages.body import GenerationMode


ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
APP = EaeuXmlApplication(ROOT)
PROCESS = "P.SP.02"
DATA = {}


def load_fixture(message):
    module_path = ROOT / "P.SP.02_OP_22" / "tests" / f"test_msg{message[-3:]}_end_to_end.py"
    spec = importlib.util.spec_from_file_location(f"cv_fixture_{message[-3:]}", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_values()


def field_views(form):
    found = {}
    def walk(fields):
        for field in fields:
            found[field.path] = field
            walk(field.children)
    walk(form.fields)
    return found


def verify(message, transaction, prefix):
    engine = APP._engine(PROCESS)
    form = APP.get_form(PROCESS, transaction, message)
    policies = APP._effective_message_field_policies(engine, message)
    structure = engine.get_structure(message, mode=GenerationMode.TEST)
    fields = field_views(form)
    values = load_fixture(message)
    positive = engine.validate_body(message, values, mode=GenerationMode.TEST)
    body = engine.build_body(message, values, mode=GenerationMode.TEST)
    root = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    (OUT / f"{prefix}_positive.xml").write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))
    actual, extraction_issues = engine.body_provider._values_from_element(structure, root)
    roundtrip = engine.validate_body(message, actual, mode=GenerationMode.TEST)
    return {
        "engine": engine, "form": form, "fields": fields, "policies": policies,
        "structure": structure, "xml": root,
        "proof": {
            "message": message, "transaction": transaction,
            "get_form": True, "policy_count": len(policies),
            "positive_is_valid": positive.is_valid,
            "positive_issues": [(v.rule_id, v.message) for v in positive.issues],
            "roundtrip_is_valid": roundtrip.is_valid,
            "roundtrip_issues": [(v.rule_id, v.message) for v in roundtrip.issues],
            "extraction_issues": [str(v) for v in extraction_issues],
            "xml": f"{prefix}_positive.xml",
            "root_qname": root.tag,
        },
    }


def extract_check(ctx, mutated, filename):
    (OUT / filename).write_bytes(ET.tostring(mutated, encoding="utf-8", xml_declaration=True))
    actual, extraction_issues = ctx["engine"].body_provider._values_from_element(ctx["structure"], mutated)
    result = ctx["engine"].validate_body(ctx["proof"]["message"], actual, mode=GenerationMode.TEST)
    return {
        "xml": filename, "valid": result.is_valid,
        "issues": [(v.rule_id, v.message) for v in result.issues],
        "extraction_issues": [str(v) for v in extraction_issues],
        "extracted_DocId": {k: v for k, v in actual.items() if k.endswith("/csdo:DocId") or k == "csdo:DocId"},
    }


def meta(ctx, path):
    view = ctx["fields"].get(path)
    structure = next((x for x in ctx["structure"].fields if x.path == path), None)
    policy = ctx["policies"].get(path)
    return {
        "path": path,
        "structure_min_occurs": structure.min_occurs if structure else None,
        "structure_source_refs": [str(x) for x in structure.source_refs] if structure else [],
        "form_required": view.required if view else None,
        "form_editable": view.editable if view else None,
        "form_effective_policy": view.effective_message_policy if view else None,
        "effective_policy": policy.policy if policy else None,
        "policy_reqs": policy.affected_by_req if policy else [],
    }


def main():
    m54 = verify("P.SP.02.MSG.054", "P.SP.02.TRN.049", "cv05_msg054")
    m56 = verify("P.SP.02.MSG.056", "P.SP.02.TRN.050", "cv06_msg056")
    code_ns = m54["structure"].imported_namespaces["csdo"]
    root_doc_id = "csdo:DocId"
    nested_id = "ipcdo:IPPaymentDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId"

    # CASE 05: root-level DocId is explicitly prohibited in MSG054.
    root54 = copy.deepcopy(m54["xml"])
    ET.SubElement(root54, ET.QName(code_ns, "DocId")).text = "FORBIDDEN-054"
    DATA["05"] = {**m54["proof"], "normative": "ОП_22.pdf p.803 Table72 REQ.7", "field": meta(m54, root_doc_id),
                  "negative": extract_check(m54, root54, "cv05_msg054_forbidden_root.xml")}

    # CASE 06: an existing accompanying document must contain its own DocId.
    root56 = copy.deepcopy(m56["xml"])
    document_tag = ET.QName(m56["structure"].imported_namespaces["ipcdo"], "AccompanyingDocumentsDetails")
    doc = next(node for node in root56.iter() if node.tag == document_tag)
    doc_id = next(node for node in doc if node.tag == ET.QName(code_ns, "DocId"))
    doc.remove(doc_id)
    DATA["06"] = {**m56["proof"], "normative": "ОП_22.pdf p.807 Table74 REQ.18", "field": meta(m56, nested_id),
                  "negative": extract_check(m56, root56, "cv06_msg056_missing_nested_id.xml")}

    # CASE 11: MSG028 permits multiple documents; MSG056 normatively allows exactly one.
    spec = importlib.util.spec_from_file_location("cv_fixture_028", ROOT / "P.SP.02_OP_22/tests/test_msg028_end_to_end.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    e28, s28, repeated = module._build_valid_parsed()
    app28 = APP.get_form(PROCESS, "P.SP.02.TRN.023", "P.SP.02.MSG.028")
    p28 = APP._effective_message_field_policies(e28, "P.SP.02.MSG.028")
    ctx28 = {"engine": e28, "structure": s28, "fields": field_views(app28), "policies": p28,
             "proof": {"message": "P.SP.02.MSG.028"}}
    parent = module._required(repeated, s28, "ipcdo", "TrademarkApplicationDetails")
    for i in (1, 2):
        doc28 = module._add_document(parent, s28)
        module._required(doc28, s28, "csdo", "DocId").text = f"DOCUMENT-{i}"
    repeated_positive = extract_check(ctx28, repeated, "cv11_msg028_two_documents.xml")
    broken_repeated = copy.deepcopy(repeated)
    docs = [node for node in broken_repeated.iter() if node.tag == ET.QName(s28.imported_namespaces["ipcdo"], "AccompanyingDocumentsDetails")]
    last_id = next(node for node in docs[-1] if node.tag == ET.QName(code_ns, "DocId"))
    docs[-1].remove(last_id)
    repeated_negative = extract_check(ctx28, broken_repeated, "cv11_msg028_second_document_missing_id.xml")
    DATA["11"] = {"get_form": True, "transaction": "P.SP.02.TRN.023", "message": "P.SP.02.MSG.028",
                  "normative": "ОП_22.pdf p.722 Table44 REQ.33",
                  "field": meta(ctx28, "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId"),
                  "positive": repeated_positive, "negative": repeated_negative}

    # CASE 12: optional in structure, required by message rule.
    DATA["12"] = {"get_form": True, "normative": "ОП_22.pdf p.807 Table74 REQ.18; R.IP.SP.03.003 Table13 row 8.10.4",
                  "field": meta(m56, nested_id), "positive": m56["proof"], "negative": DATA["06"]["negative"]}

    # CASE 13: structurally allowed root DocId, explicitly prohibited by MSG054.
    DATA["13"] = {"get_form": True, "normative": "ОП_22.pdf p.803 Table72 REQ.7; R.IP.SP.03.003",
                  "field": meta(m54, root_doc_id), "positive": m54["proof"], "negative": DATA["05"]["negative"]}

    # CASE 15: a contextual rule from another OP than OP49, preserved dynamically.
    legal_name = "ipsdo:IPLegalActionKindName"
    legal_code = "ipsdo:IPLegalActionKindCode"
    bad54 = copy.deepcopy(m54["xml"])
    legal_name_tag = ET.QName(m54["structure"].imported_namespaces["ipsdo"], "IPLegalActionKindName")
    target = next(node for node in bad54.iter() if node.tag == legal_name_tag)
    target.text = "UNLISTED-LEGAL-ACTION"
    missing54 = copy.deepcopy(m54["xml"])
    missing_target = next(node for node in missing54.iter() if node.tag == legal_name_tag)
    missing_parent = next(node for node in missing54.iter() if missing_target in list(node))
    missing_parent.remove(missing_target)
    code_and_name54 = copy.deepcopy(m54["xml"])
    ET.SubElement(code_and_name54, ET.QName(m54["structure"].imported_namespaces["ipsdo"], "IPLegalActionKindCode")).text = "PLACEHOLDER"
    DATA["15"] = {"get_form": True, "normative": "ОП_22.pdf p.802 Table72 REQ.4/5",
                  "field": meta(m54, legal_name), "context_field": meta(m54, legal_code),
                  "context_rules": [r["rule_id"] for r in m54["engine"].rules["P.SP.02.MSG.054"].structured_rules if r["rule_id"].startswith("P.SP.02.MSG.054.T72.REQ.4") or r["rule_id"].startswith("P.SP.02.MSG.054.T72.REQ.5")],
                  "positive": m54["proof"], "negative": extract_check(m54, bad54, "cv15_msg054_bad_legal_action_name.xml"),
                  "negative_missing": extract_check(m54, missing54, "cv15_msg054_missing_legal_action_name.xml"),
                  "negative_code_and_name": extract_check(m54, code_and_name54, "cv15_msg054_code_and_name.xml")}

    # This script is an executable positive/negative regression probe, not just logging.
    for number in ("05", "06", "12", "13", "15"):
        assert DATA[number]["negative"]["valid"] is False, number
    assert m54["proof"]["roundtrip_is_valid"] and m56["proof"]["roundtrip_is_valid"]
    assert DATA["11"]["positive"]["valid"] is True
    assert DATA["11"]["negative"]["valid"] is False
    assert DATA["11"]["positive"]["extracted_DocId"]["ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId"] == ["DOCUMENT-1", "DOCUMENT-2"]
    assert DATA["11"]["negative"]["extracted_DocId"]["ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId"] == ["DOCUMENT-1", None]
    assert DATA["12"]["field"]["structure_min_occurs"] == 0 and DATA["12"]["field"]["effective_policy"] == "REQUIRED"
    assert DATA["13"]["field"]["structure_min_occurs"] == 0 and DATA["13"]["field"]["effective_policy"] == "FORBIDDEN"
    assert DATA["15"]["field"]["effective_policy"] is None  # Conditional rules remain dynamic.

    (OUT / "op22_cases_05_06_11_12_13_15.json").write_text(json.dumps(DATA, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    for number, evidence in DATA.items():
        negative = evidence.get("negative", {})
        print(f"CASE={number} positive={evidence.get('positive', evidence).get('roundtrip_is_valid', evidence.get('positive',{}).get('valid'))} negative_valid={negative.get('valid')} ids={[x[0] for x in negative.get('issues', [])]}")


if __name__ == "__main__":
    main()
