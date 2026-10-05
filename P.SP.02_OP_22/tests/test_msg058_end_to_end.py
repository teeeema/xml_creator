from pathlib import Path
from xml.etree import ElementTree as ET
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine

P = Path(__file__).resolve().parents[1]; M = "P.SP.02.MSG.058"; D = "ipcdo:AccompanyingDocumentsDetails"


def test_valid_fixture_builds_extracts_and_validates():
    e = EaeuXmlEngine.load_process(P); s = e.get_structure(M, mode=GenerationMode.TEST)
    v = {"ccdo:EDocHeader":[None], "ccdo:EDocHeader/csdo:InfEnvelopeCode":M, "ccdo:EDocHeader/csdo:EDocCode":"R.IP.SP.02.008", "ccdo:EDocHeader/csdo:EDocId":"00000000-0000-0000-0000-000000000058", "ccdo:EDocHeader/csdo:EDocDateTime":"2026-09-30T14:00:00+03:00", D:[None], f"{D}/ipsdo:IPDocKindCode":"07015", f"{D}/csdo:DocName":"Материал", f"{D}/csdo:DocId":"DOC-058", f"{D}/csdo:DocCreationDate":"2026-09-30"}
    x = ET.fromstring(ET.tostring(e.build_body(M, v, mode=GenerationMode.TEST).serialize_xml_element()))
    extracted, issues = e.body_provider._values_from_element(s, x)
    assert not issues
    assert e.validate_body(M, extracted, mode=GenerationMode.TEST).is_valid
    assert all(r["rule_id"].startswith(M) for r in e.rules[M].structured_rules)
