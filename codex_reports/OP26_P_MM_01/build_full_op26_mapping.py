import json, csv, os, sys
from pathlib import Path
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator, RuleStatus

BASE_DIR = Path("/Users/tema/Documents/Work/xml_creator")

with open(BASE_DIR / "codex_reports/OP26_P_MM_01/OP26_SAFE_IMPLEMENTATION_BATCH_MAP.csv") as f:
    batch_rows = list(csv.DictReader(f))

msg_yaml = {}
for ypath in sorted((BASE_DIR / "P.MM.01_OP_26/message_rules").glob("P.MM.01.MSG.*.yaml")):
    with open(ypath) as f:
        d = json.load(f)
        msg_yaml[d["message_code"]] = (ypath, d)

# Map (MSG, prule) to canonical_id and batch info
row_by_prule = {}
for r in batch_rows:
    row_by_prule[(r["MSG"], r["production_rule"])] = r

print(f"Loaded {len(row_by_prule)} rules from batch map.")
