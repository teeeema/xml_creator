import json, csv, os, sys, re
from pathlib import Path
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator, RuleStatus

BASE_DIR = Path("/Users/tema/Documents/Work/xml_creator")
engine = EaeuXmlEngine.load_process(BASE_DIR / "P.MM.01_OP_26")

with open(BASE_DIR / "codex_reports/OP26_P_MM_01/OP26_SAFE_IMPLEMENTATION_BATCH_MAP.csv") as f:
    batch_rows = list(csv.DictReader(f))

yaml_data = {}
for ypath in sorted((BASE_DIR / "P.MM.01_OP_26/message_rules").glob("P.MM.01.MSG.*.yaml")):
    with open(ypath) as f:
        d = json.load(f)
        yaml_data[d["message_code"]] = d

print(f"Loaded {len(batch_rows)} batch rows across {len(yaml_data)} YAML messages.")

# Inspect each batch row
for r in batch_rows:
    msg = r["MSG"]
    prule = r["production_rule"]
    cid = r["canonical_requirement_id"]
    batch = r["safe_batch"]
    d = yaml_data[msg]
    br = next(b for b in d["business_rules"] if b["rule_id"] == prule)
    r["_br"] = br
    r["_struct_id"] = d["structure_id"]

print("Done linking business_rules.")

b1_rows = [r for r in batch_rows if r["safe_batch"] == "B1_SIMPLE_PRESENCE_AND_COMPARISON"]
print(f"\nAnalyzing B1: {len(b1_rows)} rows")

for r in b1_rows:
    br = r["_br"]
    req = br["requirement"]
    paths = br.get("field_paths", [])
    path = r["xml_path"]
    
    # Analyze requirement text:
    # 1. required vs forbidden vs allowed values
    print(f"[{r['MSG']}] {r['production_rule']} | path: {path} | req: {req[:60]}...")
