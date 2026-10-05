from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.036"
APP = "ipcdo:TrademarkApplicationDetails"
DOCS = f"{APP}/ipcdo:AccompanyingDocumentsDetails"


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _q(structure, prefix, local):
    return f"{{{structure.imported_namespaces[prefix]}}}{local}"


def _child(parent, structure, prefix, local, text=None, namespace=None):
    ns = namespace if namespace is not None else structure.imported_namespaces[prefix]
    result = ET.SubElement(parent, ET.QName(ns, local))
    result.text = text
    return result


def _rules(engine, code):
    prefix = f"{MESSAGE}.T54.REQ.{code}"
    return [rule for rule in engine.rules[MESSAGE].structured_rules if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")]


def _base_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000036",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        APP: [None], DOCS: [None],
        f"{DOCS}/ipsdo:IPDocKindCode": "00036",
        f"{DOCS}/csdo:DocId": "DOC-036",
        f"{DOCS}/csdo:DocCreationDate": "2026-09-30",
        f"{DOCS}/csdo:DescriptionText": "Документ согласия",
        f"{DOCS}/csdo:PageQuantity": "1",
        f"{DOCS}/csdo:DocBinaryText": "QUJD",
    }


def _parsed():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    root = engine.body_provider._serialize(structure, engine.body_provider._flatten(_base_values()))
    return engine, structure, ET.fromstring(ET.tostring(root, encoding="utf-8"))


def _values(engine, structure, root):
    values, issues = engine.body_provider._values_from_element(structure, ET.fromstring(ET.tostring(root, encoding="utf-8")))
    assert not issues
    return values


def _add_doc(app, structure, missing=None):
    doc = _child(app, structure, "ipcdo", "AccompanyingDocumentsDetails")
    for prefix, local, value in (("ipsdo", "IPDocKindCode", "00036"), ("csdo", "DocId", "DOC-SECOND"), ("csdo", "DocCreationDate", "2026-09-30"), ("csdo", "DescriptionText", "Второй документ"), ("csdo", "PageQuantity", "1"), ("csdo", "DocBinaryText", "REVG")):
        if local != missing:
            _child(doc, structure, prefix, local, value)


@pytest.mark.parametrize("missing_index", [None, 0, 1])
def test_req4_direct_repeated_documents_preserve_per_parent_alignment(missing_index):
    engine, structure, root = _parsed()
    app = root.find(_q(structure, "ipcdo", "TrademarkApplicationDetails"))
    first = app.find(_q(structure, "ipcdo", "AccompanyingDocumentsDetails"))
    _add_doc(app, structure)
    if missing_index == 0:
        first.remove(first.find(_q(structure, "csdo", "DocBinaryText")))
    elif missing_index == 1:
        app.findall(_q(structure, "ipcdo", "AccompanyingDocumentsDetails"))[1].remove(app.findall(_q(structure, "ipcdo", "AccompanyingDocumentsDetails"))[1].find(_q(structure, "csdo", "DocBinaryText")))
    values = _values(engine, structure, root)
    assert values[f"{DOCS}/csdo:DocBinaryText"] == (["QUJD", "REVG"] if missing_index is None else ([None, "REVG"] if missing_index == 0 else ["QUJD", None]))
    statuses = [StructuredRuleEvaluator().evaluate(rule, values).status for rule in _rules(engine, 4)]
    assert (RuleStatus.PASS in statuses) if missing_index is None else (RuleStatus.FAIL in statuses)


def test_req4_qname_and_owner_do_not_select_nested_or_wrong_namespace_document():
    engine, structure, root = _parsed()
    app = root.find(_q(structure, "ipcdo", "TrademarkApplicationDetails"))
    bogus = _child(app, structure, "ipcdo", "AccompanyingDocumentsDetails", namespace="urn:wrong")
    _child(bogus, structure, "csdo", "DocBinaryText", "WRONG")
    values = _values(engine, structure, root)
    selected = StructuredRuleEvaluator().select(_rules(engine, 4)[1]["selector"], values)
    assert len(selected) == 1
    assert selected[0]["csdo:DocBinaryText"] == "QUJD"
