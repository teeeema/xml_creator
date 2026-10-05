import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.049"
R007 = "ipcdo:UnifiedRegisterRecordsDetails"
REQ_LIST = set(range(1, 20)) | {21, 22, 23, 24, 25}
FULL = {2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,23,24,25}
SAFE_PARTIAL = {1,21,22}
ENGINE_UNSUPPORTED = {18,19}
EXECUTABLE = FULL | SAFE_PARTIAL
EXACT_DOC_NAME = "Заявление о внесении изменений в сведения Единого реестра товарных знаков, знаков обслуживания Евразийского экономического союза"

def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))

def rules(code):
    prefix=f"{MESSAGE}.T67.REQ.{code}"
    return [r for r in raw()["structured_rules"] if r["rule_id"] == prefix or r["rule_id"].startswith(prefix+".")]

def test_inventory_and_classification_are_exact():
    audit=raw()["mapping_audit"]
    inventory={int(x["requirement_code"]) for x in audit["inventory"]}
    assert inventory == REQ_LIST
    assert 20 not in inventory
    assert (audit["captured_row_count"], audit["expanded_requirement_count"]) == (11,24)
    assert audit["summary"]["FULLY_MAPPABLE"] == sorted(FULL)
    assert audit["summary"]["SAFE_PARTIAL"] == sorted(SAFE_PARTIAL)
    assert audit["summary"]["ENGINE_UNSUPPORTED"] == sorted(ENGINE_UNSUPPORTED)
    assert audit["classification_counts"] == {"FULLY_MAPPABLE":19,"SAFE_PARTIAL":3,"EXTERNAL":0,"AMBIGUOUS":0,"ENGINE_UNSUPPORTED":2,"SOURCE_CONFLICT":0}
    assert sum(audit["classification_counts"].values()) == 24

def test_executable_set_exact_and_req20_absent():
    executable={int(r["rule_id"].split(".REQ.")[1].split(".")[0]) for r in raw()["structured_rules"]}
    assert executable == EXECUTABLE
    assert len(executable) == 22
    assert not rules(18) and not rules(19) and not rules(20)
    assert not any(".REQ.20" in r["rule_id"] for r in raw()["structured_rules"])

def test_req1_partial_local_trademark_id_only():
    r=rules(1)[0]
    assert r["mapping_status"] == "PARTIAL"
    assert r["selector"] == {"collection":R007}
    assert r["assertions"] == [{"kind":"presence","target":{"field":"ipsdo:TrademarkId"},"state":"REQUIRED"}]
    inv=next(x for x in raw()["mapping_audit"]["inventory"] if x["requirement_code"]=="1")
    assert inv["classification"] == "SAFE_PARTIAL"
    assert inv["unmapped_remainder"]

def test_req2_exact_one_record():
    r=rules(2)[0]
    assert r["kind"]=="selection_cardinality"
    assert r["selector"]=={"collection":R007}
    assert (r["min_occurs"],r["max_occurs"])==(1,1)

def test_req3_start_required_and_req4_end_forbidden():
    r3=rules(3)[0]
    assert r3["selector"]=={"collection":f"{R007}/ccdo:ResourceItemStatusDetails"}
    assert r3["assertions"]==[{"kind":"presence","target":{"field":"ccdo:ValidityPeriodDetails/csdo:StartDateTime"},"state":"REQUIRED"}]
    r4=rules(4)[0]
    assert r4["selector"]=={"collection":f"{R007}/ccdo:ResourceItemStatusDetails"}
    assert r4["assertions"]==[{"kind":"presence","target":{"field":"ccdo:ValidityPeriodDetails/csdo:EndDateTime"},"state":"FORBIDDEN"}]

def test_req5_status_exact_03_event_date_and_no_codelist():
    r=rules(5)[0]
    assert r["selector"]=={"collection":f"{R007}/ipcdo:IPEntityStatusDetails"}
    targets={a["target"]["field"]:a for a in r["assertions"]}
    assert targets["csdo:StatusCode"]["value"]=="03"
    assert targets["csdo:EventDate"]["state"]=="REQUIRED"
    assert targets["csdo:StatusCode/@codeListId"]["state"]=="FORBIDDEN"

def test_req6_17_dual_table49_provenance_and_req18_19_unmapped():
    inv={int(x["requirement_code"]):x for x in raw()["mapping_audit"]["inventory"]}
    for code in range(6,18):
        refs=inv[code]["source_refs"]
        assert refs[0]["table"]=="67" and refs[0]["item"]=="6-19"
        assert refs[1]["table"]=="49" and refs[1]["item"]==str(code)
    for code in (18,19):
        assert inv[code]["classification"]=="ENGINE_UNSUPPORTED"
        assert inv[code]["mapping_status"]=="UNMAPPED"

def test_req21_22_partial_document_kind_branches():
    r21=rules(21)[0]
    assert r21["mapping_status"]=="PARTIAL"
    assert r21["scope"]=={"collection":R007}
    assert r21["condition"]=={"field":"ipsdo:IPDocKindCode","operator":"NE","value":None}
    assert r21["target"]=={"field":"ipsdo:IPDocKindName"} and r21["state"]=="FORBIDDEN"
    r22=rules(22)[0]
    assert r22["mapping_status"]=="PARTIAL"
    assert r22["condition"]=={"field":"ipsdo:IPDocKindCode","operator":"EQ","value":None}
    assert r22["target"]=={"field":"ipsdo:IPDocKindName"}
    assert r22["value"]==EXACT_DOC_NAME

def test_req23_25_signature_same_parent_shapes():
    r23=rules(23)
    assert len(r23)==2
    assert any(x["kind"]=="selection_cardinality" and x["selector"]=={"collection":f"{R007}/ipcdo:SignatureDetails"} for x in r23)
    branch=next(x for x in r23 if x["rule_id"].endswith(".BRANCH"))
    a=branch["assertions"][0]
    assert a["condition"]["field"]=="ipcdo:OfficerDetails" and a["target"]["field"]=="ccdo:FullNameDetails" and a["state"]=="FORBIDDEN"
    a24=rules(24)[0]["assertions"][0]
    assert a24["condition"]["field"]=="ccdo:FullNameDetails" and a24["target"]["field"]=="ipcdo:OfficerDetails"
    r25=rules(25)[0]
    assert r25["selector"]=={"qname":"ipcdo:OfficerDetails","under":f"{R007}/ipcdo:SignatureDetails"}
    targets={a["target"]["field"]:a["state"] for a in r25["assertions"]}
    assert targets=={"ccdo:FullNameDetails/csdo:LastName":"REQUIRED","ccdo:FullNameDetails/csdo:FirstName":"REQUIRED","csdo:PositionName":"REQUIRED","ccdo:CommunicationDetails":"FORBIDDEN"}
