"""Bind only an explicit subset of source statements; account for every other row.

This is an offline migration tool, not a natural-language validation engine.
Unrecognized/ambiguous statements remain visible as non-PASS evaluations.
"""
from pathlib import Path
import copy
import json
import re
import hashlib
from compile_structures import clean, dump, PACKAGE, REPORT

QNAME=re.compile(r'\(([a-z]+):\s*([A-Za-z0-9_]+)\)')


def ancestry(field, by_id):
    paths=[]
    parent=by_id.get(field['parent'])
    while parent:
        paths.insert(0,parent['path']);parent=by_id.get(parent['parent'])
    return paths


def bind(row, structure):
    text=clean(row['requirement']).strip().rstrip('.')
    qnames=QNAME.findall(text)
    if not qnames:return [],'UNRESOLVED_FIELD_BINDING'
    by_id={f['field_id']:f for f in structure['fields']}
    noun=r'реквизит «[^»]+»\s*\([a-z]+:\s*[A-Za-z0-9_]+\)'
    def unique(q):
        matches=[f for f in structure['fields'] if (f['namespace_prefix'],f['xml_name'])==q]
        return matches[0] if len(matches)==1 else None
    def atom(f, operation, **extra):
        return {'kind':'field_constraint','operation':operation,'target':f['path'],
                'ancestors':ancestry(f,by_id),'container':any(g['parent']==f['field_id'] and g['kind']!='ATTRIBUTE' for g in structure['fields']),**extra}
    if len(qnames)==2 and re.fullmatch(r'должен быть заполнен '+noun+r' или '+noun,text):
        first,second=map(unique,qnames)
        if first and second and first['parent']==second['parent']:
            return [atom(first,'AT_LEAST_ONE',targets=[first['path'],second['path']])],None
    conditional_attr=re.fullmatch(r'если заполнен '+noun+r', то атрибут «[^»]+» \(атрибут (\w+)\) в его составе должен содержать значение «([^»]+)»',text)
    if conditional_attr and len(qnames)==1:
        parent=unique(qnames[0])
        if parent:
            attributes=[f for f in structure['fields'] if f['parent']==parent['field_id'] and f['kind']=='ATTRIBUTE' and f['xml_name']==conditional_attr[1]]
            if len(attributes)==1:return [atom(attributes[0],'FIXED',value=conditional_attr[2])],None
    universal=re.fullmatch(r'если '+noun+r' в составе любых сложных реквизитов заполнен, то '+noun+r' в его составе заполняется обязательно',text)
    if universal and len(qnames)==2:
        parents=[f for f in structure['fields'] if (f['namespace_prefix'],f['xml_name'])==qnames[0]]
        output=[]
        for parent in parents:
            matches=[f for f in structure['fields'] if f['parent']==parent['field_id'] and (f['namespace_prefix'],f['xml_name'])==qnames[1]]
            if len(matches)!=1:return [],'MISSING_FIELD_IN_UNIVERSAL_PARENT'
            output.append(atom(matches[0],'REQUIRED',conditional_on_parent=True))
        if output:return output,None
    conditional=re.fullmatch(r'если '+noun+r' соответствует значению «([^»]+)», то '+noun+r' (не заполняется|должен быть заполнен|заполняется обязательно)',text)
    if conditional and len(qnames)==2:
        condition,target=map(unique,qnames)
        if condition and target and condition['parent']==target['parent']:
            literal=re.split(r'\s+[–-]\s+',conditional[1])[0]
            return [atom(target,'FORBIDDEN' if conditional[2]=='не заполняется' else 'REQUIRED',condition={'target':condition['path'],'allowed_values':[literal]})],None
    prefix,local=qnames[0]
    candidates=[f for f in structure['fields'] if f['xml_name']==local and f['namespace_prefix']==prefix]
    if len(qnames)>1:
        # Parent qualification in a simple sentence, never positional broadcasting.
        parents={q[1] for q in qnames[1:]}
        candidates=[f for f in candidates if parents <= set(f['path'].split('/')[:-1])]
    if len(candidates)!=1:return [],'AMBIGUOUS_OR_MISSING_QNAME_CONTEXT'
    field=candidates[0]
    target=field['path']
    if any(token in text.lower() for token in ('если',' при ', 'кажд', ' или ', ' и ', 'кроме', 'этим же','должна содержаться','в едином','в единой','заголовке','в сообщении общего процесса')):
        return [],'CONTEXTUAL_OR_COMPOUND_REQUIREMENT'
    operation=None;extra={}
    # Anchored lexical patterns: do not drop conditions or surrounding clauses.
    qualifier=r'(?: в составе (?:сложного )?'+noun+r')?'
    if re.fullmatch(r'(?:должен быть заполнен '+noun+qualifier+'|'+noun+' должен быть заполнен|'+noun+' заполняется обязательно)',text):operation='REQUIRED'
    elif re.fullmatch(r'(?:не заполняется '+noun+qualifier+'|'+noun+' не заполня(?:ется|ются))',text):operation='FORBIDDEN'
    elif re.fullmatch(r'(?:в электронном сообщении должен передаваться 1 экземпляр |должен быть заполнен (?:только )?(?:1|один) экземпляр |должен присутствовать ровно один экземпляр )'+noun,text):
        operation='CARDINALITY';extra={'min_occurs':1,'max_occurs':1}
    elif re.fullmatch(noun+r' должен (?:иметь|содержать) значение «[^»]+»',text):
        operation='FIXED';literal=re.search(r'значение «([^»]+)»',text)[1];extra={'value':re.split(r'\s+[–-]\s+',literal)[0]}
    elif re.fullmatch(noun+r' должен соответствовать значению «[^»]+»',text):
        operation='FIXED';literal=re.search(r'значению «([^»]+)»',text)[1];extra={'value':re.split(r'\s+[–-]\s+',literal)[0]}
    elif re.fullmatch(noun+r' должен соответствовать одному из значений:.+',text):
        values=re.findall(r'(?:значений:|;)\s*(\d+)\s*[–-]',text)
        if values:operation='ENUM';extra={'allowed_values':values}
    if not operation:return [],'NOT_IMPLEMENTED_SOURCE_INTERPRETATION'
    by_id={f['field_id']:f for f in structure['fields']}
    container=any(f['parent']==field['field_id'] and f['kind']!='ATTRIBUTE' for f in structure['fields'])
    return [{'kind':'field_constraint','operation':operation,'target':target,
             'ancestors':ancestry(field,by_id),'container':container,**extra}],None


def compile_all():
    structures={p.parent.name:json.loads(p.read_text()) for p in (PACKAGE/'structures').glob('*/*.yaml')}
    catalogs={p.stem:json.loads(p.read_text()) for p in (PACKAGE/'message_rules').glob('*.yaml')}
    coverage=[]
    def atoms_for(row, structure, trail=()):
        text=clean(row['requirement'])
        inherited=re.fullmatch(r'соответствуют требованиям (\d+)\s*[-–]\s*(\d+) таблицы (\d+) настоящего Регламента',text)
        if inherited:
            scope='A' if row['source_regulation_table_index']<177 else 'B'
            # Printed table numbers in 140: A table 26 -> index151; A47 ->172.
            table_index=int(inherited[3])+125 if scope=='A' else int(inherited[3])+177
            candidates=[r for d in catalogs.values() for r in d['business_rules'] if r['source_regulation_table_index']==table_index and r['source_requirement_code'].isdigit() and int(inherited[1])<=int(r['source_requirement_code'])<=int(inherited[2])]
            if not candidates or row['rule_id'] in trail:return [],'UNRESOLVED_INHERITED_RANGE'
            output=[];unresolved=[]
            for source in candidates:
                atoms,reason=atoms_for(source,structure,(*trail,row['rule_id']))
                for atom in atoms:
                    atom['source_refs']=row['source_refs']+atom['source_refs']
                    atom['inherited_source_row']=source['rule_id'];output.append(atom)
                if reason:unresolved.append(source['rule_id'])
            return output,('INHERITED_RANGE_PARTIAL:'+','.join(unresolved)) if unresolved else None
        atoms,reason=bind(row,structure)
        for atom in atoms:atom['source_refs']=row['source_refs']
        return atoms,reason
    executable=0
    for code,data in sorted(catalogs.items()):
        structure=structures[data['structure_id']]
        structured=[]
        for row in data['business_rules']:
            atoms,reason=atoms_for(row,structure)
            ids=[]
            for n,atom in enumerate(atoms,1):
                identity={key:atom.get(key) for key in ('operation','target','targets','condition','inherited_source_row')}
                identifier=row['rule_id']+'.A'+hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()[:12]
                atom.update(rule_id=identifier,source_row_id=row['rule_id'],message_code=code,
                            diagnostic=f"{code}: {atom['operation']} {atom['target']}",error_code='NORMATIVE_FIELD_CONSTRAINT')
                structured.append(atom);ids.append(identifier);executable+=1
            if reason:
                external=any(t in row['requirement'].lower() for t in ('классификатор','справочник','в едином реестре','в единой базе','заголовке','в сообщении общего процесса'))
                marker={'rule_id':row['rule_id']+'.DEFERRED','source_row_id':row['rule_id'],
                    'kind':'unresolved_normative_requirement','source_refs':row['source_refs'],'diagnostic':reason}
                if external:marker['evaluation_status']='EXTERNAL_CONTEXT_REQUIRED'
                structured.append(marker)
            coverage.append({'source_row_id':row['rule_id'],'msg':code,'structure':data['structure_id'],
                'source_requirement_code':row['source_requirement_code'],
                'requirement':row['requirement'],'atomic_rule_ids':ids,'atomic_count':len(ids),
                'coverage':'PARTIAL' if ids and reason else 'IMPLEMENTED' if ids else 'SOURCE_BLOCKED' if external else 'NOT_IMPLEMENTED',
                'remaining_reason':reason,'source_refs':row['source_refs']})
        data['structured_rules']=structured
        dump(PACKAGE/'message_rules'/(code+'.yaml'),data)
    dump(REPORT/'business_coverage.json',coverage)
    print('Source rows:',len(coverage),'executable constraints:',executable,'coverage:',
          {s:sum(r['coverage']==s for r in coverage) for s in set(r['coverage'] for r in coverage)})


if __name__=='__main__':compile_all()
