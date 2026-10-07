import json, csv, os, sys
from pathlib import Path
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator, RuleStatus

BASE_DIR = Path("/Users/tema/Documents/Work/xml_creator")

with open(BASE_DIR / "codex_reports/OP26_P_MM_01/OP26_SAFE_IMPLEMENTATION_BATCH_MAP.csv") as f:
    batch_rows = list(csv.DictReader(f))

yaml_data = {}
for ypath in sorted((BASE_DIR / "P.MM.01_OP_26/message_rules").glob("P.MM.01.MSG.*.yaml")):
    with open(ypath) as f:
        d = json.load(f)
        yaml_data[d["message_code"]] = (ypath, d)

# Map (MSG, prule) to canonical_id and batch info
row_by_prule = {}
for r in batch_rows:
    row_by_prule[(r["MSG"], r["production_rule"])] = r

def get_source_refs(msg, prule):
    d = yaml_data[msg][1]
    br = next(b for b in d["business_rules"] if b["rule_id"] == prule)
    return br.get("source_refs", [])

# Let's map each of the 159 rules cleanly!
structured_rules_by_msg = {msg: [] for msg in yaml_data}

# Helper to register rule
def add_rule(msg, prule, rule_def):
    cid = row_by_prule[(msg, prule)]["canonical_requirement_id"]
    rule_def["rule_id"] = cid
    rule_def["production_rule_id"] = prule
    rule_def["source_refs"] = get_source_refs(msg, prule)
    structured_rules_by_msg[msg].append(rule_def)

print("Mapping started...")
