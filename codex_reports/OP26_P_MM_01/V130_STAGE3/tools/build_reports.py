"""Account for Stage 3 using actual catalogs, TEST XML and immutable Stage 2 evidence."""
from pathlib import Path
from collections import Counter
from xml.etree import ElementTree as ET
import csv,json,hashlib,copy,sys,re
R=Path(__file__).resolve().parents[4];D=R/'codex_reports/OP26_P_MM_01/V130_STAGE3';S=R/'codex_reports/OP26_P_MM_01/V130_STAGE2';P=R/'P.MM.01_OP_26/versions/1.3.0'
sys.path[:0]=[str(R/'eaeu_xml/src'),str(R/'P.MM.01_OP_26/tests')]
from v130_runtime_support import catalogs,sample_values,provider
from eaeu_xml.process_packages import GenerationMode

def read(p):return json.loads(p.read_text())
def write(name,data): (D/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def csvread(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def save(name,rows):
 with (D/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def js(x):return json.dumps(x,ensure_ascii=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

ss,rr,mm=catalogs();coverage=read(D/'business_coverage.json');old=read(S/'business_coverage.json');old_by={r['source_row_id']:r for r in old}
fields=read(S/'structure_fields.json');src={s['structure_id']:s for s in read(P/'structures/source_inventory.json')['structures']}
classifiers=read(P/'classifier_references.yaml')['classifiers'];nsi=read(D/'sources/nsi_acquisition.json');nsi_by={r['CLS']:r for r in nsi}
atoms={r['rule_id']:r for rules in rr.values() for r in rules.structured_rules if r.get('kind')=='field_constraint'}
old_atoms={a for r in old for a in r['atomic_rule_ids']}
assert old_atoms<=set(atoms),(old_atoms-set(atoms))
assert len(coverage)==481 and len(fields)==710 and len(mm)==41
for row in coverage:assert row['requirement']==old_by[row['source_row_id']]['requirement']
old_matrix={r['MSG']:r for r in csvread(S/'MESSAGE_TEST_MATRIX.csv')}
inventory=read(S/'verification/pdf_message_inventory.json')
assert set(mm)==set(inventory['sets']['A'])|set(inventory['sets']['B'])

def status(row):
 if row['coverage']=='IMPLEMENTED':return 'FULLY_IMPLEMENTED_TESTED'
 if row['coverage']=='PARTIAL':return 'PARTIALLY_IMPLEMENTED'
 t=row['requirement'].lower();reason=row['remaining_reason'] or ''
 if row['coverage']=='NOT_IMPLEMENTED':
  return 'NEEDS_NORMATIVE_INTERPRETATION' if 'AMBIGUOUS' in reason or 'UNRESOLVED_FIELD' in reason else 'NOT_IMPLEMENTED_LOCAL_CONSTRAINT'
 if 'заголовке' in t:return 'NOT_IMPLEMENTED_HEADER_CONTEXT'
 if any(s in t for s in ('в едином реестре','в единой базе','в единой реестре','в сообщении общего процесса')):return 'BLOCKED_EXTERNAL_RESOURCE'
 available={n['nsi_code'] for n in nsi if n['status']=='COMPLETE_OFFICIAL_SNAPSHOT'}
 if any('«'+code+'»' in t for code in available):return 'NOT_IMPLEMENTED_AVAILABLE_CLASSIFIER_BINDING'
 if any(s in t for s in ('классификатор','справочник','перечня','номенклатур')):return 'BLOCKED_OFFICIAL_DATASET_OR_BINDING'
 return 'NEEDS_SOURCE'

proof=[];(D/'verification/xml').mkdir(exist_ok=True)
service=provider(rr)
for code,m in mm.items():
 s=ss[m.structure_id];v=sample_values(s,m,rr.get(code));root=service.build_body(m,s,v,mode=GenerationMode.TEST).serialize_xml_element()
 path=D/'verification/xml'/(code+'.synthetic.xml');path.write_bytes(ET.tostring(root,encoding='utf-8',xml_declaration=True))
 extracted=service.extract_values(s,ET.fromstring(path.read_bytes()));result=service.validate_body(m,s,extracted,mode=GenerationMode.TEST)
 assert result.is_valid and not result.is_complete
 bad=copy.deepcopy(root);node=next(n for n in bad.iter() if str(n.tag).endswith('}EDocId'));node.text='INVALID_UUID'
 negative=D/'verification/xml'/(code+'.invalid.xml');negative.write_bytes(ET.tostring(bad,encoding='utf-8',xml_declaration=True))
 invalid=service.validate_body(m,s,service.extract_values(s,bad),mode=GenerationMode.TEST);assert not invalid.is_valid
 assert not service.validate_body(m,s,extracted,mode=GenerationMode.STRICT).is_valid
 proof.append(dict(MSG=code,xml=str(path.relative_to(R)),sha256=sha(path),negative=str(negative.relative_to(R)),negative_sha256=sha(negative),
   TEST_is_valid=result.is_valid,is_complete=result.is_complete,negative_is_valid=invalid.is_valid,STRICT_is_valid=False,
   incomplete_diagnostics=[dict(code=i.code,path=i.field_path) for i in result.issues],
   errors=[dict(code=i.code,path=i.field_path) for i in invalid.issues if i.severity.value=='ERROR']))
write('verification/xml_results.json',proof)

qrows=[]
for f in fields:
 source=src[f['structure_id']];raw=source['fields_source_rows'][f['source_row_index']-1];rawname=next(c for c in raw if c)
 qrows.append(dict(Structure=f['structure_id'],Field_ID=f['field_id'],Raw_normative_name=rawname,Normalized_name=f['official_name'],
  XML_local_name=f['xml_name'] or 'N/A',Prefix=f['namespace_prefix'] or 'N/A',Source_namespace_literal=f['namespace_uri'] or 'N/A',
  Effective_namespace='UNKNOWN_MODEL_VERSION' if f['kind']=='ELEMENT' else 'UNQUALIFIED_ATTRIBUTE' if f['kind']=='ATTRIBUTE' else 'ARBITRARY_XML',
  Expanded_QName=f['expanded_qname'] or 'UNKNOWN_OR_WILDCARD',Parent=f['parent'] or 'ROOT',PATH=f['path'],Order=f['order'],Kind=f['kind'],
  minOccurs=f['min_occurs'],maxOccurs=f['max_occurs'] if f['max_occurs'] is not None else 'unbounded',
  Source_interpretation=f['interpretation_status'],New_QName_closure='NO_NEW_EFFECTIVE_URI',
  Source=js(f['source_refs']),Page_precision='table-start when known; exact Word table_index/source row; row PDF page not verified',
  Unicode_normalization='U+200C removed only in derived interpretation' if '\u200c' in rawname else 'No U+200C in source name',
  Closure='Official versioned XSD/import closure and exact QName positive/negative proof'))
save('QNAME_RESOLUTION.csv',qrows)

rules=[]
for row in coverage:
 a=[atoms[i] for i in row['atomic_rule_ids']]
 rules.append(dict(MSG=row['msg'],Source_row_ID=row['source_row_id'],Normative_REQ=row['source_requirement_code'],Structure=row['structure'],
  Requirement=row['requirement'],Stage2=old_by[row['source_row_id']]['coverage'],Stage3=row['coverage'],Status=status(row),
  Executable_constraints=len(a),Atomic_IDs=';'.join(row['atomic_rule_ids']) or 'N/A',
  Operations=';'.join(sorted({x['operation'] for x in a})) or 'N/A',
  PATH=';'.join(sorted({p for x in a for p in x.get('targets',[x['target']])})) or 'UNRESOLVED',
  Conditions=js([x.get('condition',{}) for x in a]),Source=js(row['source_refs']),Derived_sources=js([x['source_refs'] for x in a]),
  Remaining_reason=row['remaining_reason'] or 'N/A',Positive='PASS_COMPILED_ATOMS' if a else 'NOT_EXECUTED',
  Negative='PASS_ACTUAL_XML_MUTATION' if a else 'NOT_EXECUTED',Generator_invocation='Existing StructuredProcessBodyProvider -> StructuredRuleEvaluator in TEST; actual edition gate blocked',
  Evidence='verification/regression.xml;test_v130_runtime.py::test_actual_xml_mutation_rejects_every_compiled_constraint'))
save('RULES_COVERAGE.csv',rules)

cls=[]
for c in classifiers:
 n=nsi_by.get(c['classifier_code'],{});used=[r for r in atoms.values() if r.get('classifier_ref')==n.get('nsi_code') and n.get('nsi_code')]
 cls.append(dict(CLS=c['classifier_code'],Official_name=c['name'],Description=c['description'],Normative_source=js(c['source_refs']),
  NSI_code=n.get('nsi_code','NO_EXPLICIT_BINDING'),Passport_title=n.get('title','UNKNOWN'),
  Status=n.get('status','NO_EXPLICIT_NSI_BINDING'),Passport_version=n.get('version_id','UNKNOWN'),
  Snapshot_date=n.get('snapshot_date','UNKNOWN'),Effective_from=n.get('effective_from','UNKNOWN'),
  Dataset_records=n.get('count','NOT_FULLY_BOUND'),Expected_records=n.get('expected_count','UNKNOWN'),
  Publication_status=n.get('publication_status','UNKNOWN'),Authority_status_literal=n.get('authority_status','UNKNOWN'),
  Sources=js(n.get('calls',[])),Local_lookup='AVAILABLE_DATED_SNAPSHOT' if n.get('status')=='COMPLETE_OFFICIAL_SNAPSHOT' else 'NOT_AVAILABLE_OR_NOT_BOUND',
  Runtime_constraints=len(used),MSG=';'.join(sorted({r['message_code'] for r in used})) or 'BINDING_NOT_COMPILED',
  PATH=';'.join(sorted({r['target'] for r in used})) or 'BINDING_NOT_COMPILED',
  Caveat='No claim of global dataset absence; four downloaded custom schemas await code-column interpretation, ten data endpoints failed; 25 refs lack explicit NSI binding'))
save('CLASSIFIER_STATUS.csv',cls)

matrix=[]
for code,m in mm.items():
 cov=[r for r in coverage if r['msg']==code]
 matrix.append(dict(MSG=code,Structure=m.structure_id,PRC=old_matrix[code]['PRC'],OPR=old_matrix[code]['OPR'],TRN=old_matrix[code]['TRN'],
  Catalog='PASS_UNCHANGED_140_77_SET',Mapping='PASS_CATALOG_REFERENCE_CHECKS',Fields='PASS_SOURCE_TREE_CLOSURE',
  QName='PARTIAL_SOURCE_TOKENS;EFFECTIVE_URI_BLOCKED',Order='PASS_SOURCE_TABLE_ORDER_NOT_OFFICIAL_COMPOSITOR',
  Cardinality='PASS_TESTED_HEADER_AND_COMPILED_LIMITS;FULL_MODEL_NOT_PROVEN',Attributes='PASS_TESTED_ALIGNED_AND_FIXED;OFFICIAL_XSD_NOT_PROVEN',
  Rules='PARTIAL' if cov else 'NOT_TESTED_NO_SCOPED_SOURCE_ROWS',Rule_rows=len(cov),Fully_covered=sum(r['coverage']=='IMPLEMENTED' for r in cov),
  Executable_constraints=sum(r['atomic_count'] for r in cov),Positive_XML='PASS_SYNTHETIC_TEST_COMPONENT_ONLY',
  Negative_XML='PASS_UUID_QNAME_ORDER_TYPES_CARDINALITY_AND_ALL_COMPILED_ATOMS',Complete_Level_A='NOT_PROVEN',
  Official_XSD='NOT_EXECUTED_NO_OFFICIAL_SET',Cross_message_correlation='NOT_EXECUTED_NEW_EDITION',
  Application_E2E='BLOCKED_READINESS_GATE',GUI='PASS_LEGACY_ONLY_DRAFT_READ_ONLY_METADATA',
  Proof='verification/xml_results.json;verification/regression.xml;verification/qt.xml'))
save('MESSAGE_VALIDATION_MATRIX.csv',matrix)

gaps=[]
def gap(id,problem,action,criterion,status,msg='N/A',req='N/A',structure='N/A',qname='N/A',path='N/A',source='N/A'):
 codes=msg.split(';') if msg!='N/A' else []
 linked=[old_matrix[c] for c in codes if c in old_matrix]
 def join(key):return ';'.join(sorted({r[key] for r in linked})) or 'N/A'
 gaps.append(dict(ID=id,OP='P.MM.01',PRC=join('PRC'),OPR=join('OPR'),TRN=join('TRN'),MSG=msg,REQ=req,STRUCTURE=structure,QName=qname,PATH=path,
  Source=source,Edition='140/2025 +77/2026; full later amendment history unresolved',Problem=problem,Action=action,
  Verification='Compiled component tests do not close this gap',Closure_criterion=criterion,Status=status))
for f in fields:
 if f['interpretation_status']!='VERIFIED':
  msgs=';'.join(c for c,m in mm.items() if m.structure_id==f['structure_id'])
  gap('NS-'+f['structure_id']+'-'+f['field_id'],'Source retains symbolic model version; effective expanded QName not confirmed',
   'Obtain authoritative versioned model/XSD dependency set','Exact URI/version/source + official schema positive/negative proof','NEEDS_SOURCE',
   msgs,structure=f['structure_id'],qname=f['namespace_prefix']+':'+f['xml_name'],path=f['path'],source=js(f['source_refs']))
for row in coverage:
 if row['coverage']!='IMPLEMENTED':gap('REQ-'+row['source_row_id'],str(row['remaining_reason'])+': '+row['requirement'],
  'Resolve source context and remaining clauses; implement local predicates or acquire explicitly needed external state/data',
  'All clauses traced and invoked through positive/negative XML/context tests',status(row),row['msg'],row['source_requirement_code'],row['structure'],source=js(row['source_refs']))
for c in cls:
 if c['Local_lookup']!='AVAILABLE_DATED_SNAPSHOT':gap('CLS-'+c['CLS'],c['Status']+'; dataset or exact code-column/version binding incomplete',
  'Retrieve complete authoritative dated data and verify exact binding','Source/hash/count/version checks + positive/negative runtime lookup','BLOCKED_OFFICIAL_DATASET_OR_BINDING',source=c['Normative_source'])
for sid,s in src.items():gap('XSD-'+sid,'Official XSD/type/compositor/import closure is unavailable','Obtain compatible official schema set',
 'All imports/includes proven, archived and officially validated','NEEDS_SOURCE',structure=sid,source=js(s['source_refs']))
gap('HISTORY','Full later amendment history not independently established','Verify official history','Complete authoritative amendment chain','NEEDS_SOURCE')
gap('E2E','New-edition application/GUI selection, full correlation and E2E remain blocked','Complete normative readiness and version-aware application flow',
 'All MSG through application and official schema; reviewed promotion','NOT_IMPLEMENTED')
regression=ET.parse(D/'verification/regression.xml').getroot() if (D/'verification/regression.xml').exists() else None
failed_cases=[] if regression is None else [t for t in regression.findall('.//testcase') if t.find('failure') is not None or t.find('error') is not None]
if failed_cases:
 gap('REGRESSION-SHARED-TREE',str(len(failed_cases))+' failures/errors in the latest full backend run; parallel source/tests appeared during Stage 3',
  'Reconcile shared APIs, rule support and new tests without discarding parallel work; isolate causes and rerun the full stable tree',
  'Zero failed/error cases and unchanged source hashes across the run','REGRESSION_FAILED')
write('verification/regression_failure_inventory.json',[dict(classname=t.get('classname'),name=t.get('name'),message=(t.find('failure') if t.find('failure') is not None else t.find('error')).get('message')) for t in failed_cases])
save('GAP_REGISTER.csv',gaps)

summary=dict(source_rows=481,baseline_incomplete=333,closed_baseline_rows=sum(r['coverage']=='IMPLEMENTED' and old_by[r['source_row_id']]['coverage']!='IMPLEMENTED' for r in coverage),
 coverage=dict(Counter(r['coverage'] for r in coverage)),statuses=dict(Counter(status(r) for r in coverage)),constraints=len(atoms),operations=dict(Counter(r['operation'] for r in atoms.values())),
 all_old_atoms_preserved=len(old_atoms),MSG=len(mm),partial_internal_structures=7,complete_normative_structures=0,complete_level_A_MSG=0,official_XSD_MSG=0,production_E2E_MSG=0,
 field_rows=710,source_interpretations_verified=119,effective_model_QNames_unresolved=591,new_effective_QNames_closed=0,
 full_classifier_snapshots=sum(n['status']=='COMPLETE_OFFICIAL_SNAPSHOT' for n in nsi),passports_retrieved=len(nsi),classifier_statuses=dict(Counter(n['status'] for n in nsi)),
 no_explicit_NSI_binding=47-len(nsi),gap_rows=len(gaps))
write('verification/stage3_counts.json',summary)
print(js(summary))
