"""Reproducible CASE09/10 OP49 normative/runtime evidence; no product changes."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.process_packages.body import GenerationMode


ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
PROCESS, TRANSACTION, MESSAGE = "P.DS.01", "P.DS.01.TRN.001", "P.DS.01.MSG.001"
RULE_IDS = (f"{MESSAGE}.R002", f"{MESSAGE}.R003")
PDF = Path("/Users/tema/Documents/Work/Документы_xml/49_ОП.pdf")


def rules_from(result):
    return {
        item.rule_id: {"status": item.status.value, "message": item.message,
                       "source_refs": list(item.source_refs)}
        for item in result.rule_evaluations if item.rule_id in RULE_IDS
    }


def case_result(result):
    return {
        "valid": result.is_valid,
        "complete": result.is_complete,
        "issue_codes": [item.code for item in result.issues],
        "rule_results": rules_from(result),
    }


def find_form_fields(form):
    def walk(fields):
        for field in fields:
            if field.xml_name in ("DailyInfoIndicator", "ChargedDistributedDutyDetails"):
                yield {
                    "path": field.path,
                    "xml_qname": field.xml_qname,
                    "structural_required": field.required,
                    "effective_message_policy": field.effective_message_policy,
                    "message_policy_req_ids": list(field.message_policy_req_ids),
                    "min_occurs": field.min_occurs,
                    "max_occurs": field.max_occurs,
                    "editable": field.editable,
                    "input_policy": field.input_policy,
                }
            yield from walk(field.children)

    return list(walk(form.fields))


def main():
    app = EaeuXmlApplication(ROOT)
    engine = app._engine(PROCESS)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    form = app.get_form(PROCESS, TRANSACTION, MESSAGE)
    policies = app._effective_message_field_policies(engine, MESSAGE) or {}
    package_rules = engine.rules[MESSAGE].structured_rules

    spec = importlib.util.spec_from_file_location(
        "op49_test_fixture", ROOT / "P.DS.01_OP_49/tests/test_msg001_full_message.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    values = module.msg001_values(engine)
    indicator = next(f.path for f in structure.fields if f.xml_name == "DailyInfoIndicator")
    entry_path = next(f.path for f in structure.fields if f.xml_name == "ChargedDistributedDutyDetails")
    baseline = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    negative_values = {}
    for name, new_indicators in [
        ("two_true", [True, True]),
        ("true_plus_false", [True, False]),
        ("only_false", [False]),
        ("no_indicators", []),
    ]:
        changed = dict(values)
        changed[indicator] = new_indicators
        # Repeated child values must retain the same owner count as the parent.
        changed[entry_path] = [None] * len(new_indicators)
        negative_values[name] = case_result(engine.validate_body(MESSAGE, changed, mode=GenerationMode.TEST))

    body = engine.build_body(MESSAGE, values, mode=GenerationMode.TEST)
    root = body.serialize_xml_element()
    namespaces = structure.imported_namespaces
    report_qname = "{" + namespaces["ds01cdo"] + "}ChargedDistributedDutyReportDetails"
    entry_qname = "{" + namespaces["ds01cdo"] + "}ChargedDistributedDutyDetails"
    indicator_qname = "{" + namespaces["ds01sdo"] + "}DailyInfoIndicator"

    def xml_probe(label, node):
        xml_path = OUT / f"op49_case09_{label}.xml"
        xml_path.write_bytes(ET.tostring(node, encoding="utf-8", xml_declaration=True))
        reparsed = ET.parse(xml_path).getroot()
        extracted, issues = engine.body_provider._values_from_element(structure, reparsed)
        result = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
        # Diagnostic-only transformation: demonstrates the type mismatch without
        # changing the production extraction or evaluator implementations.
        def bool_cast(value):
            if isinstance(value, list):
                return [bool_cast(item) for item in value]
            if isinstance(value, str):
                return {"true": True, "false": False, "1": True, "0": False}.get(value, value)
            return value

        diagnostic = dict(extracted)
        for field in structure.fields:
            if "indicatortype" in (field.datatype or "").lower() and field.path in diagnostic:
                diagnostic[field.path] = bool_cast(diagnostic[field.path])
        diagnosis = engine.validate_body(MESSAGE, diagnostic, mode=GenerationMode.TEST)
        return {
            "xml_file": str(xml_path),
            "root_qname": reparsed.tag,
            "entry_count": len(list(reparsed.iter(entry_qname))),
            "indicator_lexical_values": [e.text for e in reparsed.iter(indicator_qname)],
            "extracted_indicator_value": extracted.get(indicator),
            "extract_issue_codes": [x.code for x in issues],
            "validation": case_result(result),
            "diagnostic_indicator_type_conversion_only": case_result(diagnosis),
        }

    xml_results = {"generated_positive": xml_probe("generated_positive", root)}
    original_report = next(root.iter(report_qname))
    original_entry = next(root.iter(entry_qname))
    clone = copy.deepcopy(root)
    clone_report = next(clone.iter(report_qname))
    clone_report.append(copy.deepcopy(next(clone.iter(entry_qname))))
    xml_results["duplicate_true"] = xml_probe("duplicate_true", clone)
    clone = copy.deepcopy(root)
    clone_report = next(clone.iter(report_qname))
    false_entry = copy.deepcopy(next(clone.iter(entry_qname)))
    next(false_entry.iter(indicator_qname)).text = "false"
    clone_report.append(false_entry)
    xml_results["add_forbidden_false"] = xml_probe("add_forbidden_false", clone)
    clone = copy.deepcopy(root)
    next(clone.iter(indicator_qname)).text = "false"
    xml_results["replace_daily_with_false"] = xml_probe("replace_daily_with_false", clone)

    report = {
        "case_ids": [9, 10],
        "process": PROCESS,
        "transaction": TRANSACTION,
        "message": MESSAGE,
        "requirements": list(RULE_IDS),
        "normative_source": {
            "file": str(PDF),
            "sha256": hashlib.sha256(PDF.read_bytes()).hexdigest(),
            "pdf_page_1_based": 79,
            "table": 10,
            "R002": "one DailyInfoIndicator=1 entry in ChargedDistributedDutyDetails",
            "R003": "zero DailyInfoIndicator=0 entries in ChargedDistributedDutyDetails",
        },
        "get_form": {
            "executed": True,
            "message": form.message_code,
            "generation_status": form.generation_status,
            "field_evidence": find_form_fields(form),
        },
        "effective_resolver": {
            "executed": True,
            "policy_count": len(policies),
            "all_resolved_paths": list(policies),
            "rule_scope": [r for r in package_rules if r.get("rule_id") in RULE_IDS],
            "indicator_static_policy": (policies.get(indicator).policy if indicator in policies else None),
        },
        "validator": {
            "direct_positive": case_result(baseline),
            "direct_negative": negative_values,
        },
        "xml_proof": xml_results,
        "observation": (
            "XML extraction preserves lexical 'true'/'false' strings. "
            "StructuredRuleEvaluator._compare now interprets XML boolean lexicals "
            "when the compared rule literal is a Python bool. R002/R003 select "
            "the expected instances after actual XML serialization and extraction."
        ),
        "previous_defect": (
            "Before the shared evaluator fix, generated positive XML failed R002 "
            "and a forbidden false entry incorrectly passed R003."
        ),
        "focused_test_command": (
            "PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q "
            "P.DS.01_OP_49/tests/test_msg001_full_message.py "
            "P.DS.01_OP_49/tests/test_pds01_catalog.py -k msg001"
        ),
        "focused_test_result": "101 passed, 7 subtests passed in 0.58s (observed on 2026-10-21; includes new XML roundtrip tests)",
        "scope": "Shared evaluator typed-boolean comparison fix with serialized XML regression tests",
    }
    output = OUT / "op49_case09_case10_evidence.json"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print(json.dumps({"evidence": str(output),
                      "form_fields": report["get_form"]["field_evidence"],
                      "policy": report["effective_resolver"]["indicator_static_policy"],
                      "positive": report["validator"]["direct_positive"],
                      "negative": {k: v["rule_results"] for k,v in negative_values.items()},
                      "xml": {k: {"indicators": v["indicator_lexical_values"],
                                   "rules": v["validation"]["rule_results"],
                                   "valid": v["validation"]["valid"]} for k,v in xml_results.items()}
                      }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
