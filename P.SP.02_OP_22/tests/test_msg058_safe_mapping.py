import json
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "message_rules/P.SP.02.MSG.058.yaml"


def test_msg058_inventory_and_executable_boundary():
    data = json.loads(P.read_text())
    audit = data["mapping_audit"]
    assert (audit["captured_row_count"], audit["expanded_requirement_count"]) == (7, 7)
    assert audit["counts"] == {"FULLY_MAPPABLE": 7, "SAFE_PARTIAL": 0, "EXTERNAL": 0, "AMBIGUOUS": 0, "ENGINE_UNSUPPORTED": 0, "SOURCE_CONFLICT": 0}
    assert {x["requirement_code"] for x in audit["requirements"]} == {str(x) for x in range(1, 8)}
    assert len(data["structured_rules"]) == 7
    assert {r["rule_id"].split(".REQ.")[1] for r in data["structured_rules"]} == {str(x) for x in range(1, 8)}
    assert all(r["source_refs"][0]["table"] == "76" for r in data["structured_rules"])
