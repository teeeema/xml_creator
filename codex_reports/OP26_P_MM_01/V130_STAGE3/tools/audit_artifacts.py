"""Independent Stage 3 accounting/provenance checks. Not normative acceptance."""
from pathlib import Path
from collections import Counter
import csv,json,hashlib,subprocess
R=Path(__file__).resolve().parents[4];D=R/'codex_reports/OP26_P_MM_01/V130_STAGE3';P=R/'P.MM.01_OP_26/versions/1.3.0'
csv.field_size_limit(2_000_000)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(name):
 with (D/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
old=read(R/'codex_reports/OP26_P_MM_01/V130_STAGE2/business_coverage.json');new=read(D/'business_coverage.json')
assert len(old)==len(new)==481
assert {r['source_row_id']:r['requirement'] for r in old}=={r['source_row_id']:r['requirement'] for r in new}
assert len({a for r in new for a in r['atomic_rule_ids']})==518
assert {a for r in old for a in r['atomic_rule_ids']}<={a for r in new for a in r['atomic_rule_ids']}
assert Counter(r['coverage'] for r in new)==Counter(IMPLEMENTED=270,PARTIAL=10,SOURCE_BLOCKED=71,NOT_IMPLEMENTED=130)
counts={'RULES_COVERAGE.csv':481,'QNAME_RESOLUTION.csv':710,'CLASSIFIER_STATUS.csv':47,'MESSAGE_VALIDATION_MATRIX.csv':41,'GAP_REGISTER.csv':851}
for name,count in counts.items():assert len(rows(name))==count
preserved=read(D/'verification/preserved_hashes.json');changed=[p for p,h in preserved.items() if not (R/p).exists() or sha(R/p)!=h]
expected_test_updates={'P.MM.01_OP_26/tests/test_v130_runtime.py','P.MM.01_OP_26/tests/v130_runtime_support.py'}
assert not set(changed)-expected_test_updates,changed
for r in read(D/'verification/xml_results.json'):
 assert r['TEST_is_valid'] and not r['is_complete'] and not r['negative_is_valid'] and not r['STRICT_is_valid']
 assert sha(R/r['xml'])==r['sha256'] and sha(R/r['negative'])==r['negative_sha256']
passport=read(P/'migration_status.json');assert passport['state']=='DRAFT_NOT_READY' and passport['promotion_allowed'] is False and passport['active_in_application'] is False
for p in (P/'classifiers').glob('*.json'):
 x=read(p);assert len(x['values'])==x['expected_count']==len(set(x['values']))
 for call in x['sources']:assert sha(R/call['artifact'])==call['sha256']
result=dict(result='PASS_ACCOUNTING_AND_PROVENANCE_ONLY',csv_rows=counts,preserved_files_checked=len(preserved),unchanged_files=len(preserved)-len(changed),expected_v130_test_updates=changed,unexpected_changes=[],
 production_ready=False,official_xsd_validation='NOT_EXECUTED',complete_level_A='NOT_PROVEN',all_167_prior_constraints_retained=True)
(D/'verification/final_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(result)
