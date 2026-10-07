import json, csv
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

for b in ["B1_SIMPLE_PRESENCE_AND_COMPARISON", "B2_REPEATED_AND_CONDITIONAL", "B3_POSITIONAL_AND_CARDINALITY", "B4_CROSS_INSTANCE_DATE_AGGREGATE"]:
    print(f"\n=================== {b} ({len([x for x in batch_rows if x['safe_batch'] == b])}) ===================")
    for r in [x for x in batch_rows if x["safe_batch"] == b]:
        print(f"[{r['MSG']}] {r['production_rule']} ({r['xml_path']}):")
        print(f"   REQ: {r['_br']['requirement']}")
        if r['_br'].get('condition'):
            print(f"   COND: {r['_br']['condition']}")
