"""Independent accounting checks; no normative facts inferred from green tests."""
from pathlib import Path
import csv,json,hashlib,subprocess
from collections import Counter
R=Path(__file__).resolve().parents[4];D=R/'codex_reports/OP26_P_MM_01/V130_STAGE2';P=R/'P.MM.01_OP_26/versions/1.3.0'
def load(p):return json.loads(p.read_text())
def out(name,x):(D/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def rows(name):
 with (D/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def git(*args):return subprocess.run(['git',*args],cwd=R,text=True,capture_output=True,check=True).stdout
fields=load(D/'structure_fields.json');coverage=load(D/'business_coverage.json')
trees={s['structure_id']:s for f in (P/'structures').glob('*/*.yaml') if (s:=load(f))}
assert len(fields)==710 and len(coverage)==481 and len(trees)==7
source_ids={r['source_row_id'] for r in coverage};atom_ids=[];markers=0
for file in (P/'message_rules').glob('*.yaml'):
 doc=load(file);paths={f['path'] for f in trees[doc['structure_id']]['fields']}
 assert all(r['rule_id'] in source_ids for r in doc['business_rules'])
 for rule in doc['structured_rules']:
  assert rule['source_row_id'] in source_ids
  assert rule['source_refs']
  if rule.get('kind')=='field_constraint':
   atom_ids.append(rule['rule_id']);assert rule['target'] in paths
   assert all(path in paths for path in rule.get('targets',[])+rule.get('ancestors',[]))
   if rule.get('condition'):assert rule['condition']['target'] in paths
  else:markers+=1
assert len(atom_ids)==len(set(atom_ids))==167
assert markers==333
expected={'STRUCTURE_FIELD_AUDIT.csv':710,'QNAME_NAMESPACE_AUDIT.csv':710,'BUSINESS_RULES_COVERAGE.csv':481,'CLASSIFIER_DEPENDENCIES.csv':47,'MESSAGE_TEST_MATRIX.csv':41,'GAP_REGISTER.csv':980}
for name,count in expected.items():assert len(rows(name))==count,(name,count)
assert Counter(r['Interpretation'] for r in rows('STRUCTURE_FIELD_AUDIT.csv'))==Counter(VERIFIED=119,NEEDS_EXTERNAL_SOURCE=591)
proof=load(D/'verification/xml_results.json')
assert len(proof)==41
assert all(r['TEST_is_valid'] and not r['is_complete'] and not r['STRICT_is_valid'] and not r['negative_is_valid'] for r in proof)
for r in proof:
 for path,hashkey in [('synthetic_xml','sha256'),('negative_xml','negative_sha256')]:
  assert hashlib.sha256((R/r[path]).read_bytes()).hexdigest()==r[hashkey]
passport=load(P/'migration_status.json');assert passport['state']=='DRAFT_NOT_READY' and passport['promotion_allowed'] is False and passport['active_in_application'] is False
original=load(D/'verification/preserved_hashes.json')
assert all(hashlib.sha256((R/path).read_bytes()).hexdigest()==sha for path,sha in original.items())
required=['MSG_INVENTORY_VERIFICATION.md','STRUCTURE_FIELD_AUDIT.csv','QNAME_NAMESPACE_AUDIT.csv','BUSINESS_RULES_COVERAGE.csv','CLASSIFIER_DEPENDENCIES.csv','XSD_SOURCE_AUDIT.md','MESSAGE_TEST_MATRIX.csv','GAP_REGISTER.csv','REGRESSION_RESULTS.md','FINAL_REPORT.md']
assert all((D/name).is_file() for name in required)
out('verification/final_audit.json',dict(result='PASS_ACCOUNTING_ONLY',csv_rows=expected,source_rows=481,compiled_predicates=167,deferred_markers=markers,preserved_files=len(original),
 production_ready=False,official_xsd='NOT_EXECUTED',complete_level_A='NOT_PROVEN',
 known_limits=['119 VERIFIED means source interpretation only','591 effective QName unresolved','333 requirement rows incomplete','amendment history completeness unknown']))
status=git('status','--short','--untracked-files=all');(D/'verification/git_status.txt').write_text(status)
refs=git('ls-remote','--heads','origin','main','backup/op26-v1.1.0-baseline','feature/op26-v1.3.0')
state=dict(branch=git('branch','--show-current').strip(),HEAD=git('rev-parse','HEAD').strip(),remote_refs=refs,
           dirty=True,commit_performed=False,push_performed=False,destructive_git_performed=False)
assert state['branch']=='feature/op26-v1.3.0' and state['HEAD']=='da0af7459edae6aa8da6b56de585afb8c658002e'
assert '0c9b8c03cbf9f03cfc6be5c53e043e571d124038\trefs/heads/main' in refs
assert '0c9b8c03cbf9f03cfc6be5c53e043e571d124038\trefs/heads/backup/op26-v1.1.0-baseline' in refs
out('verification/final_git_state.json',state)
print('PASS accounting:',expected,'predicates',len(atom_ids),'deferred',markers,'preserved',len(original))
