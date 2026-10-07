import json, csv, os, sys
from pathlib import Path

BASE_DIR = Path("/Users/tema/Documents/Work/xml_creator")

with open(BASE_DIR / "codex_reports/OP26_P_MM_01/OP26_SAFE_IMPLEMENTATION_BATCH_MAP.csv") as f:
    batch_rows = list(csv.DictReader(f))

msg_yaml = {}
for ypath in sorted((BASE_DIR / "P.MM.01_OP_26/message_rules").glob("P.MM.01.MSG.*.yaml")):
    with open(ypath) as f:
        d = json.load(f)
        msg_yaml[d["message_code"]] = (ypath, d)

b2_rows = [r for r in batch_rows if r["safe_batch"] == "B2_REPEATED_AND_CONDITIONAL"]
for r in b2_rows:
    m = r["MSG"]
    prule = r["production_rule"]
    br = next(b for b in msg_yaml[m][1]["business_rules"] if b["rule_id"] == prule)
    print(f"[{m}] {prule} ({r['xml_path']}):")
    print(f"   COND: {br.get('condition')}")
    print(f"   REQ:  {br.get('requirement')}")
