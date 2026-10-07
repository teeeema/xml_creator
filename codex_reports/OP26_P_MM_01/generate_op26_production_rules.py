import json, csv, re
from pathlib import Path

BASE_DIR = Path("/Users/tema/Documents/Work/xml_creator")

with open(BASE_DIR / "codex_reports/OP26_P_MM_01/OP26_SAFE_IMPLEMENTATION_BATCH_MAP.csv") as f:
    batch_rows = list(csv.DictReader(f))

# Map message to yaml file
msg_yaml = {}
for ypath in sorted((BASE_DIR / "P.MM.01_OP_26/message_rules").glob("P.MM.01.MSG.*.yaml")):
    with open(ypath) as f:
        d = json.load(f)
        msg_yaml[d["message_code"]] = (ypath, d)

# We will build structured_rules for each message
structured_by_msg = {msg: [] for msg in msg_yaml}

# Helper to build structured rule dictionary
def make_rule(cid, kind, source_refs, **kwargs):
    rule = {
        "rule_id": cid,
        "kind": kind,
        "source_refs": source_refs,
    }
    rule.update(kwargs)
    return rule

print(f"Total safe rows to map: {len(batch_rows)}")
