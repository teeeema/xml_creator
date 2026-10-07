import json, csv, re
from pathlib import Path

BASE_DIR = Path("/Users/tema/Documents/Work/xml_creator")

with open(BASE_DIR / "codex_reports/OP26_P_MM_01/OP26_SAFE_IMPLEMENTATION_BATCH_MAP.csv") as f:
    batch_rows = list(csv.DictReader(f))

yaml_data = {}
for ypath in sorted((BASE_DIR / "P.MM.01_OP_26/message_rules").glob("P.MM.01.MSG.*.yaml")):
    with open(ypath) as f:
        d = json.load(f)
        yaml_data[d["message_code"]] = d

for r in batch_rows:
    m = r["MSG"]
    prule = r["production_rule"]
    br = next(b for b in yaml_data[m]["business_rules"] if b["rule_id"] == prule)
    r["_br"] = br
    r["_struct_id"] = yaml_data[m]["structure_id"]

print(f"Loaded {len(batch_rows)} rows.")
