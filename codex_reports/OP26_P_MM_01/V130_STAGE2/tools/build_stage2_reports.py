"""Rebuild Stage 2 evidence from preserved catalogs and the existing Body provider.

Synthetic XML is component proof in TEST mode, never an official normative sample.
No readiness bypass, network import, source mutation or production activation.
"""
from pathlib import Path
from collections import Counter
from xml.etree import ElementTree as ET
import copy
import csv
import hashlib
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[4]
REPORT=ROOT/'codex_reports/OP26_P_MM_01/V130_STAGE2'
PACKAGE=ROOT/'P.MM.01_OP_26/versions/1.3.0'
STAGE1=ROOT/'codex_reports/OP26_P_MM_01/V130_COMPLETION'
sys.path[:0]=[str(ROOT/'eaeu_xml/src'),str(ROOT/'P.MM.01_OP_26/tests')]
from v130_runtime_support import catalogs, sample_values, provider
from eaeu_xml.process_packages import GenerationMode


def read(path):return json.loads(path.read_text())
def write(name,text): (REPORT/name).write_text(text,encoding='utf-8')
def js(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def csv_out(name,rows):
    assert rows
    with (REPORT/name).open('w',newline='',encoding='utf-8-sig') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
def refs(items):return js(items)
def short(items,key):return ';'.join(sorted(set(i[key] for i in items))) or 'N/A'

fields=read(REPORT/'structure_fields.json');coverage=read(REPORT/'business_coverage.json')
messages=read(PACKAGE/'messages.yaml')['messages']
transactions=read(PACKAGE/'transactions.yaml')['transactions']
procedures=read(PACKAGE/'procedures.yaml')['procedures']
operations=read(PACKAGE/'operations.yaml')['operations']
classifiers=read(PACKAGE/'classifier_references.yaml')['classifiers']
source_structures=read(PACKAGE/'structures/source_inventory.json')['structures']
structure_meta={s['structure_id']:s for s in source_structures}
structures,rules,runtime_messages=catalogs()
operation_map={o['operation_code']:o for o in operations}
procedure_codes={p['procedure_code'] for p in procedures}
assert len(messages)==41 and len(transactions)==28 and len(procedures)==28 and len(operations)==84
links={}
for m in messages:
    code=m['message_code'];linked=[]
    for t in transactions:
        if code==t.get('initiating_message') or code in t.get('response_messages',[]):
            assert t['procedure_code'] in procedure_codes
            for op in (t['initiating_operation'],t['responding_operation']):assert op in operation_map
            sending=t['initiating_operation'] if code==t.get('initiating_message') else t['responding_operation']
            receiving=t['responding_operation'] if code==t.get('initiating_message') else t['initiating_operation']
            linked.append(dict(PRC=t['procedure_code'],TRN=t['transaction_code'],OPR=sending,
                               receiver_OPR=receiving,sender=operation_map[sending]['participant_role'],
                               recipient=operation_map[receiving]['participant_role']))
    assert linked,code
    links[code]=linked

# Independent PDF inventory: exact complete tables, separate regulation contexts.
import pymupdf
pdf=STAGE1/'sources/decision_140.pdf'
doc=pymupdf.open(pdf)
sets={label:set(re.findall(r'P\.MM\.01\.MSG\.\d{3}', ''.join(doc[p-1].get_text() for p in pages)))
      for label,pages in [('A',range(259,263)),('B',range(381,383))]}
assert (len(sets['A']),len(sets['B']),len(sets['A']&sets['B']),len(sets['A']|sets['B']))==(34,13,6,41)
assert sets['A']|sets['B']==set(runtime_messages)
write('verification/pdf_message_inventory.json',json.dumps(dict(pdf=str(pdf.relative_to(ROOT)),sha256=sha(pdf),
    pages={'A':'259-262 (table 5)','B':'381-382 (table 6)'},sets={k:sorted(v) for k,v in sets.items()},
    intersection=sorted(sets['A']&sets['B']),extra_B=sorted(sets['B']-sets['A'])),ensure_ascii=False,indent=2)+'\n')

# Emit reproducible Body XML, extracted diagnostics and an actual negative XML per MSG.
proof=[];xml_dir=REPORT/'verification/xml';xml_dir.mkdir(exist_ok=True)
service=provider(rules)
for code,m in runtime_messages.items():
    s=structures[m.structure_id];values=sample_values(s,m,rules.get(code))
    element=service.build_body(m,s,values,mode=GenerationMode.TEST).serialize_xml_element()
    payload=ET.tostring(element,encoding='utf-8',xml_declaration=True)
    positive=xml_dir/(code+'.synthetic.xml');positive.write_bytes(payload)
    restored=service.extract_values(s,ET.fromstring(payload))
    result=service.validate_body(m,s,restored,mode=GenerationMode.TEST)
    assert result.is_valid and not result.is_complete
    strict=service.validate_body(m,s,restored,mode=GenerationMode.STRICT)
    assert not strict.is_valid
    negative=copy.deepcopy(element)
    identifier=next(n for n in negative.iter() if str(n.tag).endswith('}EDocId'))
    identifier.text='INVALID_UUID'
    path=xml_dir/(code+'.invalid_uuid.xml');path.write_bytes(ET.tostring(negative,encoding='utf-8',xml_declaration=True))
    bad=service.validate_body(m,s,service.extract_values(s,ET.fromstring(path.read_bytes())),mode=GenerationMode.TEST)
    assert not bad.is_valid
    proof.append(dict(MSG=code,synthetic_xml=str(positive.relative_to(ROOT)),sha256=sha(positive),
        negative_xml=str(path.relative_to(ROOT)),negative_sha256=sha(path),
        TEST_is_valid=result.is_valid,is_complete=result.is_complete,STRICT_is_valid=strict.is_valid,
        negative_is_valid=bad.is_valid,issues=[dict(code=i.code,path=i.field_path,severity=i.severity.value) for i in result.issues],
        negative_errors=[dict(code=i.code,path=i.field_path) for i in bad.issues if i.severity.value=='ERROR']))
write('verification/xml_results.json',json.dumps(proof,ensure_ascii=False,indent=2)+'\n')

# Per-field source interpretation. A table-start page is not a row-specific page.
rows=[]
for f in fields:
    meta=structure_meta[f['structure_id']]
    rows.append(dict(Structure=f['structure_id'],FieldID=f['field_id'],Normative_identifier=f['identifier'],
        Official_name=f['official_name'],ParentID=f['parent'] or 'ROOT',Order=f['order'],Kind=f['kind'],
        XML_local_name=f['xml_name'] or 'N/A',Prefix=f['namespace_prefix'] or 'N/A',
        Source_namespace_literal=f['namespace_uri'] or 'N/A',Effective_namespace='UNRESOLVED' if f['kind']=='ELEMENT' else 'N/A',
        Expanded_QName=f['expanded_qname'] or ('ANY_XML' if f['kind']=='ARBITRARY_XML' else 'UNKNOWN'),
        Body_path='/'+meta['root_element']+'/'+f['path'],Engine_path=f['path'],Datatype=f['datatype'] or 'UNKNOWN',
        Datatype_source=f['datatype_text'],minOccurs=f['min_occurs'],maxOccurs='unbounded' if f['max_occurs'] is None else f['max_occurs'],
        Facets=js(f['facets']),Classifier=f.get('classifier_ref') or 'N/A',
        Value_formation='Explicit source facets/constants only; no classifier values synthesized',
        Required_condition='Base minOccurs; compiled MSG predicates tracked in BUSINESS_RULES_COVERAGE.csv; remaining rules unresolved',
        Source=refs(f['source_refs']),Source_row=f['source_row_index'],
        Page_precision='Table-start page when available; exact Word table_index and row; row-specific PDF page NOT_VERIFIED',
        Interpretation=f['interpretation_status'],Reason=f['reason_code'] or 'Source token/tree verified; official XSD semantics not established'))
csv_out('STRUCTURE_FIELD_AUDIT.csv',rows)
csv_out('QNAME_NAMESPACE_AUDIT.csv',[{k:r[k] for k in ('Structure','FieldID','XML_local_name','Prefix','Source_namespace_literal','Effective_namespace','Expanded_QName','Body_path','ParentID','Kind','Source','Interpretation')} for r in rows])

all_atoms={r['rule_id']:r for rule in rules.values() for r in rule.structured_rules if r.get('kind')=='field_constraint'}
rule_rows=[]
for row in coverage:
    atoms=[all_atoms[i] for i in row['atomic_rule_ids']]
    rule_rows.append(dict(Source_row_ID=row['source_row_id'],MSG=row['msg'],Structure=row['structure'],
        Normative_REQ=row['source_requirement_code'],Requirement=row['requirement'],
        Atomic_IDs=';'.join(row['atomic_rule_ids']) or 'N/A',Executable_constraints=row['atomic_count'],
        XML_paths=';'.join(sorted({p for a in atoms for p in a.get('targets',[a['target']])})) or 'UNRESOLVED',
        Operations=';'.join(sorted({a['operation'] for a in atoms})) or 'N/A',
        Conditions=js([a.get('condition',{'ancestors':a.get('ancestors',[])}) for a in atoms]),
        Error_code='NORMATIVE_FIELD_CONSTRAINT' if atoms else 'STRUCTURED_RULE_NOT_EVALUATED',
        Expected='Source predicate in each actual parent context; no external closure implied',
        Coverage=row['coverage'],Remaining_reason=row['remaining_reason'] or 'N/A',
        Source=refs(row['source_refs']),
        Compiled_source_refs=refs([a['source_refs'] for a in atoms]),
        Positive_test='PASS_LOCAL_PREDICATES' if atoms else 'NOT_EXECUTED',
        Negative_test='PASS_XML_MUTATION' if atoms else 'NOT_EXECUTED',
        Test_scenario='test_v130_runtime.py::test_every_compiled_atom_has_positive_and_negative_value_proof;test_actual_xml_mutation_rejects_every_compiled_constraint' if atoms else 'Deferred marker remains non-PASS'))
csv_out('BUSINESS_RULES_COVERAGE.csv',rule_rows)

classifier_rows=[]
for c in classifiers:
    # Only literal CLS references or an explicitly printed ES NSI code bind fields.
    nsi=re.findall(r'код (?:классификатора|справочника) в ЕС НСИ «([^»]+)»',c['description'])
    bindings=[f for f in fields if f.get('classifier_ref') in [c['classifier_code'],*nsi]]
    classifier_rows.append(dict(CLS=c['classifier_code'],Official_name=c['name'],Description=c['description'],
        Edition='140/2025 with 77/2026 amendments',Dataset_version='UNKNOWN',Dataset_date='UNKNOWN',
        ES_NSI_code=';'.join(nsi) or 'NOT_EXPLICIT',
        Structures=';'.join(sorted({f['structure_id'] for f in bindings})) or 'BINDING_NOT_RESOLVED',
        Fields=';'.join(f['structure_id']+':'+f['path'] for f in bindings) or 'BINDING_NOT_RESOLVED',
        Dataset_available=False,Local_lookup='SOURCE_BLOCKED',External_access='Required official snapshot or authoritative system; no connectivity assumed',Source=refs(c['source_refs'])))
assert len(classifier_rows)==47
assert {'P.MM.01.CLS.028','P.MM.01.CLS.029'} <= {c['CLS'] for c in classifier_rows}
assert not {'P.MM.01.CLS.009','P.MM.01.CLS.010'} & {c['CLS'] for c in classifier_rows}
csv_out('CLASSIFIER_DEPENDENCIES.csv',classifier_rows)

matrix=[]
for m in messages:
    code=m['message_code'];cov=[r for r in coverage if r['msg']==code];ls=links[code]
    matrix.append(dict(MSG=code,Name=m['name'],PRC=short(ls,'PRC'),OPR=short(ls,'OPR'),TRN=short(ls,'TRN'),
        Structure=m['structure_id'],Structure_version=m['structure_version'] or 'UNKNOWN',
        Catalog='PASS_140_77_SCOPE',Mapping='PASS_CATALOG_LINKS',Structure_mapping='PASS_SOURCE_TABLE',
        Fields='PASS_TREE_CLOSURE_710_ROWS',Namespace='SOURCE_BLOCKED_MODEL_VERSION',
        Cardinality='PARTIAL_HEADER_AND_GENERIC_REPEAT_TESTS',Rules='PARTIAL' if cov else 'NOT_TESTED_NO_SCOPED_SOURCE_ROWS',
        Source_rule_rows=len(cov),Fully_compiled_rows=sum(r['coverage']=='IMPLEMENTED' for r in cov),
        Executable_constraints=sum(r['atomic_count'] for r in cov),
        Positive_XML='PARTIAL_TEST_MODE_ONLY',Serialization_roundtrip='PASS_SYNTHETIC_COMPONENT',
        Negative_XML='PASS_SCOPED_UUID_DATETIME_CARDINALITY_QNAME_SEQUENCE_AND_COMPILED_RULES',
        XSD='NOT_TESTED_NO_OFFICIAL_XSD',Correlation='NOT_TESTED_NEW_EDITION_EXTERNAL_CONTEXT',
        End_to_end='BLOCKED_READINESS_GATE',Complete_internal_validation='NOT_PROVEN',
        Proof='verification/xml_results.json;verification/regression.xml',Source=refs(m['source_refs'])))
csv_out('MESSAGE_TEST_MATRIX.csv',matrix)

# Contextual source gaps; field and requirement counts intentionally non-additive.
gaps=[]
def gap(id,problem,action,criterion,status='OPEN',msg='N/A',req='N/A',structure='N/A',qname='N/A',path='N/A',source='N/A'):
    ls=links.get(msg,[])
    gaps.append(dict(ID=id,OP='P.MM.01',PRC=short(ls,'PRC'),OPR=short(ls,'OPR'),TRN=short(ls,'TRN'),MSG=msg,REQ=req,
        Structure=structure,QName=qname,path=path,Source=source,Problem=problem,Action=action,
        Verification='Current component tests do not close this gap',Closure_criterion=criterion,Status=status))
for f in fields:
    if f['interpretation_status']!='VERIFIED':gap('NS-'+f['structure_id']+'-'+f['field_id'],
        'Source uses a symbolic imported model version; effective expanded QName is unknown. Prefix/local and tree verified only. Risk: draft XML may have wrong effective namespace.',
        'Retrieve official matching model/XSD publication and resolve dependency graph',
        'Authoritative URI and model version linked to source; exact QName positive/negative proof; official XSD validation',
        'NEEDS_EXTERNAL_SOURCE',structure=f['structure_id'],qname=(f['namespace_prefix']+':'+f['xml_name']),path=f['path'],source=refs(f['source_refs']))
for r in coverage:
    if r['coverage']!='IMPLEMENTED':gap('REQ-'+r['source_row_id'],r['coverage']+': '+str(r['remaining_reason'])+'; source text: '+r['requirement'],
        'Resolve exact field/context semantics; implement remaining local predicates or obtain classifier/prior-message/registry evidence as applicable',
        'All atomic clauses traced to source and tested by positive and negative actual XML/context cases',
        r['coverage'],msg=r['msg'],req=r['source_requirement_code'],structure=r['structure'],source=refs(r['source_refs']))
for c in classifiers:gap('CLS-'+c['classifier_code'],'Official dataset/version not retrieved; local membership lookup unavailable',
    'Obtain authoritative versioned dataset and verify field bindings','Dataset provenance/hash/version and positive/negative lookup tests',
    'SOURCE_BLOCKED',source=refs(c['source_refs']))
for s in source_structures:
    gap('XSD-'+s['structure_id'],'Official schema/dependency/compositor set is unavailable; table tree is not proof of xs:sequence/choice/all/type closure',
        'Retrieve schema named by source with all dependencies; verify editions','Every import resolved, hash archived, official schema validates positive XML and rejects negative XML',
        'SOURCE_BLOCKED',structure=s['structure_id'],source=refs(s['source_refs']))
gap('EDITION-HISTORY','Independent full later-amendment history after 77/2026 not established from accessible official service',
    'Verify official decision-card amendment history','Accessible official history confirms all applicable amendments through audit date','NEEDS_EXTERNAL_SOURCE')
gap('APPLICATION-E2E','Full engine/GUI selection, new-edition correlation and complete normative policy remain blocked/incomplete',
    'Finish remaining requirements and policies, dependency proof, then validate readiness through existing engine/application',
    'End-to-end positive/negative generation and correlation for every applicable MSG; reviewed promotion passport','NOT_IMPLEMENTED')
csv_out('GAP_REGISTER.csv',gaps)

old=read(ROOT/'P.MM.01_OP_26/messages.yaml')['messages'];old_by={m['message_code']:m for m in old}
new_by={m['message_code']:m for m in messages}
text='''# MSG inventory verification — Stage 2, 2026-10-23\n\nВердикт: **Подтверждено в объёме редакции 140/2025 с изменениями 77/2026**. Полнота последующей истории изменений: **Недостаточно данных**.\n\nНезависимо прочитан PDF Решения 140: таблица 5 первого регламента, абсолютные страницы 259–262 — 34 MSG; таблица 6 второго регламента, страницы 381–382 — 13 MSG. Пересечение — 6; объединение — 41. Word table_index=130 и 183 дают те же множества. Это два регламента одного процесса, а не смешение версий. 77 меняет требования/структуры/CLS; оснований исключать второй регламент не обнаружено. Машинное доказательство и SHA-256: `verification/pdf_message_inventory.json`.\n\nДополнительные семь кодов второго регламента: MSG.012, .016, .017, .021, .022, .023, .024. Общие шесть: MSG.004, .009, .019, .020, .030, .031.\n\nКорневой каталог 1.1.0: 28 MSG. Сохраняются 27 кодов, исключён из новых полных перечней MSG.003, добавлены 14 кодов. Совпадение кода не подтверждает неизменность семантики. Исполняемые компоненты 1.3.0: 41 частичный тестовый Body; production engine: 0 активированных MSG. R.006/R.007 имеют неизвестную эффективную версию (в источнике Y.Y.Y), остальные пять структур — 1.3.0. Назначение ниже приведено официальным наименованием; роли взяты дословно у связанных операций, без выдумывания ACT.\n\n| MSG | OLD 1.1.0 | NORMATIVE 1.3.0 | IMPLEMENTED 1.3.0 | Наименование / назначение | Структура / версия | PRC/TRN/OPR, отправитель → получатель | Источник |\n|---|---|---|---|---|---|---|---|\n'''
for code in sorted(set(old_by)|set(new_by)):
    m=new_by.get(code)
    if not m:
        text+=f'| {code} | PRESENT | EXCLUDED_FROM_140_77_LISTS | NOT_IMPLEMENTED | {old_by[code]["name"]} | N/A | N/A | Full lists: 140 tables 5/6 |\n';continue
    ls=links[code]
    chain='<br>'.join(f'{x["PRC"]}/{x["TRN"]}/{x["OPR"]}: {x["sender"]} → {x["recipient"]}' for x in ls)
    sr='<br>'.join(r['location'] for r in m['source_refs'])
    text+=f'| {code} | {"PRESENT" if code in old_by else "ABSENT"} | PRESENT_140_77 | PARTIAL_COMPONENT | {m["name"]} | {m["structure_id"]}/{m["structure_version"] or "UNKNOWN (Y.Y.Y)"} | {chain} | {sr} |\n'
text+='\nОфициальные источники: [Решение 140](https://docs.eaeunion.org/documents/446/10427/), [Решение 77](https://docs.eaeunion.org/documents/463/10765/). Исходные архивы/извлечения этапа 1 сохранены. Полная семантическая эквивалентность старых/новых кодов и последующие изменения не объявляются подтверждёнными.\n'
write('MSG_INVENTORY_VERIFICATION.md',text)

xsd='''# XSD and model source audit — 2026-10-23\n\nВердикт: **Недостаточно данных** для официальной XSD-валидации. Уровень B: NOT_EXECUTED. Тайм-аут/TLS-ошибка не доказывают отсутствие публикации.\n\nСтратегия: повторно открыть официальные карточки решений 140/77 и искать точные имена схем/структур версии 1.3.0; проверить официальные реестры схем и моделей по HTTP/HTTPS; сверить сохранённые официальные приложения и явные imports. Сохранённые PDF/Word — нормативные таблицы, не XSD. Нового официального XSD, архива схем или набора модельных зависимостей не получено.\n\n| Адрес | Назначение | Фактический результат | Доказательство |\n|---|---|---|---|\n| https://docs.eaeunion.org/documents/446/10427/ | 140/2025 | Повторное web-открытие недоступно; сохранённый PDF/Word доступен локально | V130_COMPLETION/sources |\n| https://docs.eaeunion.org/documents/463/10765/ | 77/2026 | Повторное web-открытие недоступно; сохранённый PDF/Word доступен локально | V130_COMPLETION/sources |\n| https://rseds.eaeunion.org/ | Реестр электронных документов и сведений | curl SSL_ERROR_SYSCALL | verification/rseds_https.txt |\n| http://rseds.eaeunion.org/ | Альтернативный протокол реестра | curl Empty reply | verification/rseds_http.txt |\n| https://eomi.eaeunion.org/ | Модели данных | curl SSL_ERROR_SYSCALL | verification/eomi_https.txt |\n| http://eomi.eaeunion.org/ | Альтернативный протокол моделей | curl Empty reply | verification/eomi_http.txt |\n| https://eec.eaeunion.org/upload/iblock/aad/K_1026.pdf | Официальный документ архитектуры | Web-поиск указал официальные rseds/eomi; не является публикацией схем версии 1.3.0 | Primary-source discovery only |\n\nПоиск точных имён схем в официальных доменах не дал загруженного артефакта. Поисковая выдача/карточка без полезной нагрузки не считаются схемой. Хэш недоступного ресурса: N/A, а не выдуманное значение.\n\n## Имеющиеся нормативные артефакты\n\n| Файл | Происхождение/редакция | SHA-256 |\n|---|---|---|\n'''
for file in sorted((STAGE1/'sources').iterdir()):
    if file.suffix.lower() in {'.pdf','.zip'}:xsd+=f'| {file.name} | official attachment archived in Stage 1; 140/2025 or 77/2026 by filename | {sha(file)} |\n'
xsd+='\n## Структуры и зависимости\n\n| Структура | Версия источника | Root URI | Имя XSD из источника (не загруженный файл) | Imports |\n|---|---|---|---|---|\n'
for s in source_structures:xsd+=f'| {s["structure_id"]} | {s["declared_version"]} | {s["namespace"]} | {s["schema_filename"]} | '+'; '.join(r[1] for r in s['imports_source_rows'])+' |\n'
xsd+='''\nX.X.X/Z.Z.Z — буквальные параметры базисной/отраслевой модели; Y.Y.Y — версия R.006/R.007. Их нельзя подменять 1.3.0. Пять отраслевых root URI подтверждены источниками; 591 QName вложенных элементов не имеет подтверждённого effective URI. 117 атрибутов unqualified и 2 arbitrary XML имеют подтверждённую интерпретацию токена/дерева (119), без доказательства полноты типов/XSD. `xs:any` реализован как исходный произвольный XML без синтетической обёртки; processContents/namespace/compositor требуют официальной схемы.\n\nУровень A: семь деревьев, 710 строк, явные facets, кратность и 167 локальных предикатов исполняются через существующий Body provider. XML тестов содержит буквальные unresolved URI и не пригоден как production-образец. Уровень A целиком не закрыт: 333 исходные строки требований не завершены. Уровень B требует авторитетного совместимого набора XSD, import/include closure, версии, дат, происхождения и SHA-256 каждого файла.\n'''
write('XSD_SOURCE_AUDIT.md',xsd)

stats=dict(MSG=41,structures_partial=7,structures_complete=0,field_rows=len(fields),field_statuses=dict(Counter(f['interpretation_status'] for f in fields)),
 source_rows=len(coverage),coverage=dict(Counter(r['coverage'] for r in coverage)),constraints=len(all_atoms),operations=dict(Counter(a['operation'] for a in all_atoms.values())),
 classifiers=len(classifiers),component_roundtrips=len(proof),complete_internal_MSG=0,official_XSD_MSG=0,production_engine_E2E=0,gap_rows=len(gaps))
write('verification/stage2_counts.json',json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
print(js(stats))
