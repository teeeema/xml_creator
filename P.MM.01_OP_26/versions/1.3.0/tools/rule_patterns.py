"""Closed source grammar for additional local predicates, not runtime NLP.

Quoted labels are replaced with their literal QName token before grammar checks:
conjunctions in an official field name are never interpreted as rule operators.
Ambiguous bindings and unrecognized clauses stay deferred.
"""
import re
import json
from pathlib import Path

AVAILABLE_CLASSIFIERS={p.stem for p in (Path(__file__).resolve().parents[1]/"classifiers").glob("*.json")}
from compile_structures import clean

REFERENCE=re.compile(r'(?:реквизит(?:а|ов|ы)?\s*)?«[^»]+»\s*\(([a-z]+):\s*([A-Za-z0-9_]+)\)')


def bind_local(row, structure):
    names=[]
    def token(m):
        names.append((m[1],m[2]));return 'Q'+str(len(names)-1)
    text=REFERENCE.sub(token,clean(row['requirement']))
    text=re.sub(r'\s+',' ',text).strip().rstrip('.')
    fields=structure['fields'];by_id={f['field_id']:f for f in fields}
    def matches(index, parent=None):
        q=names[int(index)]
        return [f for f in fields if (f['namespace_prefix'],f['xml_name'])==q and (parent is None or f['path'].startswith(parent['path']+'/'))]
    def one(index,parent=None):
        found=matches(index,parent)
        if parent is not None:
            direct=[f for f in found if f['parent']==parent['field_id']]
            if direct: found=direct
        return found[0] if len(found)==1 else None
    def ancestors(f):
        result=[];p=by_id.get(f['parent'])
        while p:result.insert(0,p['path']);p=by_id.get(p['parent'])
        return result
    def atom(f,operation,**extra):
        return dict(kind='field_constraint',operation=operation,target=f['path'],ancestors=ancestors(f),
                    container=any(g['parent']==f['field_id'] and g['kind']!='ATTRIBUTE' for g in fields),**extra)
    def make(index,op,parent=None,**extra):
        f=one(index,parent);return [atom(f,op,**extra)] if f else []
    def literal(s):return re.split(r'\s+[–-]\s+',s)[0]
    def enum_values(s):return re.findall(r'(?:^|;)\s*«?(\d+)\s*[–-]',s)
    # Complete unary sentences, with an explicit parent qualifier where supplied.
    m=re.fullmatch(r'(должен быть заполнен|не заполняется|не должен быть заполнен) Q(\d+)(?: в составе (?:сложного )?Q(\d+))?',text)
    if m:
        parent=one(m[3]) if m[3] else None
        if m[3] and parent is None:return [],'AMBIGUOUS_PARENT_BINDING'
        result=make(m[2],'REQUIRED' if m[1]=='должен быть заполнен' else 'FORBIDDEN',parent)
        if result:return result,None
    m=re.fullmatch(r'(?:в составе (?:сложного )?Q(\d+)|в каждом экземпляре Q(\d+)) Q(\d+) должен быть заполнен',text)
    if m:
        parent=one(m[1] or m[2]);result=make(m[3],'REQUIRED',parent) if parent else []
        if result:return result,None
    m=re.fullmatch(r'(?:в электронном сообщении должен передаваться 1 экземпляр|должен быть заполнен (?:только )?(?:1|один) экземпляр|должен присутствовать ровно один экземпляр) Q(\d+)',text)
    if m:
        result=make(m[1],'CARDINALITY',min_occurs=1,max_occurs=1)
        if result:return result,None
    # Universal child requirement: source explicitly says "any complex fields".
    m=re.fullmatch(r'если Q(\d+) в составе любых сложных реквизитов заполнен, то в его составе Q(\d+) должен быть заполнен',text)
    if m:
        output=[]
        for parent in matches(m[1]):
            target=one(m[2],parent)
            if target is None:return [],'UNRESOLVED_UNIVERSAL_CHILD'
            output.append(atom(target,'REQUIRED'))
        if output:return output,None
    # Local child presence and binary alternatives under the same source parent.
    m=re.fullmatch(r'если Q(\d+)\s*заполнен, то в его составе должен быть заполнен Q(\d+)(?: (?:или|и \(или\)) Q(\d+))?',text)
    if m:
        parent=one(m[1]);first=one(m[2],parent) if parent else None
        second=one(m[3],parent) if parent and m[3] else None
        if first and not m[3]:return [atom(first,'REQUIRED')],None
        if first and second and first['parent']==second['parent']:
            return [atom(first,'AT_LEAST_ONE',targets=[first['path'],second['path']])],None
    # Parent-qualified presence: the verb may precede the child reference.
    m=re.fullmatch(r'в составе (?:сложного |заполненного )?Q(\d+) должен быть заполнен Q(\d+)(?: (?:или|и \(или\)) Q(\d+))?',text)
    if m:
        parent=one(m[1]);first=one(m[2],parent) if parent else None
        second=one(m[3],parent) if parent and m[3] else None
        if first and not m[3]:return [atom(first,'REQUIRED')],None
        if first and second and first['parent']==second['parent']:
            return [atom(first,'AT_LEAST_ONE',targets=[first['path'],second['path']])],None
    m=re.fullmatch(r'должен быть заполнен Q(\d+) либо Q(\d+)',text)
    if m:
        first,second=one(m[1]),one(m[2])
        if first and second and first['parent']==second['parent']:
            return [atom(first,'AT_LEAST_ONE',targets=[first['path'],second['path']])],None
    m=re.fullmatch(r'если Q(\d+) в составе любых сложных реквизитов заполнен, то в его составе (.+)',text)
    if m:
        unary=re.fullmatch(r'Q(\d+) заполняется обязательно',m[2])
        binary=re.fullmatch(r'должен быть заполнен Q(\d+) или Q(\d+)',m[2])
        output=[]
        for parent in matches(m[1]):
            if unary:
                first=one(unary[1],parent)
                if first is None:return [],'UNRESOLVED_UNIVERSAL_CHILD'
                output.append(atom(first,'REQUIRED'))
            elif binary:
                first,second=one(binary[1],parent),one(binary[2],parent)
                if first is None or second is None or first['parent']!=second['parent']:return [],'UNRESOLVED_UNIVERSAL_CHILD'
                output.append(atom(first,'AT_LEAST_ONE',targets=[first['path'],second['path']]))
        if output:return output,None
    m=re.fullmatch(r'Q(\d+) не заполняется',text)
    if m:
        result=make(m[1],'FORBIDDEN')
        if result:return result,None
    m=re.fullmatch(r'должно быть заполнено не более одного экземпляра Q(\d+)',text)
    if m:
        result=make(m[1],'CARDINALITY',min_occurs=0,max_occurs=1)
        if result:return result,None
    m=re.fullmatch(r'(?:должен быть заполнен Q(\d+)|Q(\d+) должен быть заполнен), а атрибут «[^»]+» \(атрибут (\w+)\) в его составе должен содержать значение «([^»]+)»',text)
    if m:
        parent=one(m[1] or m[2])
        attrs=[f for f in fields if parent and f['parent']==parent['field_id'] and f['kind']=='ATTRIBUTE' and f['xml_name']==m[3]]
        if parent and len(attrs)==1:return [atom(parent,'REQUIRED'),atom(attrs[0],'FIXED',value=m[4])],None
    m=re.fullmatch(r'Q(\d+) должен быть заполнен и должен содержать информацию о текущем этапе',text)
    if m:
        result=make(m[1],'REQUIRED')
        if result:return result,'CURRENT_STAGE_SEMANTICS_NOT_IMPLEMENTED'
    m=re.fullmatch(r'Q(\d+) может принимать следующие значения:(.+)',text)
    if m:
        values=enum_values(m[2]);result=make(m[1],'ENUM',allowed_values=values) if values else []
        if result:return result,None
    # Enumerations explicitly printed in a requirement, never invented datasets.
    m=re.fullmatch(r'если Q(\d+) заполнен\s*, то (?:он должен соответствовать|его значение должно соответствовать|соответствует) одному из (?:следующих )?значений:(.+)',text)
    if m:
        values=enum_values(m[2]);result=make(m[1],'ENUM',allowed_values=values) if values else []
        if result:return result,None
    m=re.fullmatch(r'Q(\d+) должен быть заполнен и должен соответствовать (?:1 из|одному из следующих|одному из) значений:(.+)',text)
    if m:
        values=enum_values(m[2]);f=one(m[1])
        if values and f:return [atom(f,'REQUIRED'),atom(f,'ENUM',allowed_values=values)],None
    m=re.fullmatch(r'Q(\d+) должен соответствовать одному из следующих значений:(.+)',text)
    if m:
        values=enum_values(m[2]);result=make(m[1],'ENUM',allowed_values=values) if values else []
        if result:return result,None
    # Conditional local predicates. Never broadcast a deeper condition upwards.
    m=re.fullmatch(r'если (?:значение )?Q(\d+) соответствует значению «([^»]+)», то (.+)',text)
    if m:
        condition=one(m[1]);tail=m[3]
        single=re.fullmatch(r'(?:должен быть заполнен )?Q(\d+)(?: (не заполняется|должен быть заполнен|заполняется обязательно))?',tail)
        alternative=re.fullmatch(r'должен быть заполнен Q(\d+) и \(или\) Q(\d+)',tail)
        forbidden=re.fullmatch(r'не должны быть заполнены реквизиты:(Q\d+(?:;Q\d+)*)',tail)
        targets=[];operation=None
        if single and (tail.startswith('должен быть заполнен ') or single[2]):
            target=one(single[1]);targets=[target] if target else [];operation='FORBIDDEN' if single[2]=='не заполняется' else 'REQUIRED'
        elif alternative:
            targets=[one(alternative[1]),one(alternative[2])];operation='AT_LEAST_ONE'
        elif forbidden:
            targets=[one(i) for i in re.findall(r'Q(\d+)',forbidden[1])];operation='FORBIDDEN'
        if condition and targets and all(targets):
            if all(condition['parent']==t['parent'] or (by_id.get(condition['parent']) and by_id[condition['parent']]['path'] in ancestors(t)) for t in targets):
                clause={'target':condition['path'],'allowed_values':[literal(m[2])]}
                if operation=='AT_LEAST_ONE' and len({t['parent'] for t in targets})==1:
                    return [atom(targets[0],operation,targets=[t['path'] for t in targets],condition=clause)],None
                if operation!='AT_LEAST_ONE':return [atom(t,operation,condition=clause) for t in targets],None
    # Explicit uniqueness inside a repeated source parent.
    m=re.fullmatch(r'значения Q(\d+) не могут повторяться среди экземпляров Q(\d+)',text)
    if m:
        parent=one(m[2]);target=one(m[1],parent) if parent else None
        if target:
            rule=atom(target,'UNIQUE');rule['ancestors']=ancestors(parent)
            return [rule],None
    # Every participating country has a source-defined role by its position.
    m=re.fullmatch(r'(?:должны присутствовать|должны быть заполнены) один или несколько экземпляров Q(\d+), из которых первый экземпляр должен содержать Q(\d+), соответствующий значению «([^»]+)», а в других экземплярах этот реквизит должен соответствовать значению «([^»]+)»',text)
    if m:
        parent=one(m[1]);target=one(m[2],parent) if parent else None
        if target:
            position=atom(target,'POSITIONAL_VALUES',first_value=literal(m[3]),other_value=literal(m[4]))
            position['ancestors']=ancestors(parent)
            return [atom(parent,'CARDINALITY',min_occurs=1,max_occurs=None),position],None
    # Extract the independent fixed classifier attribute, leaving lookup deferred.
    m=re.fullmatch(r'если Q(\d+)(?: в составе любых сложных реквизитов)? заполнен, то его значение должно соответствовать коду .+(?:классификатор|справочник).+а атрибут «[^»]+» \(атрибут (\w+)\) в его составе должен содержать значение «([^»]+)»',text)
    if m and len(names)==1:
        parents=matches(m[1]) if 'в составе любых сложных реквизитов' in text else ([one(m[1])] if one(m[1]) else [])
        output=[]
        for parent in parents:
            attrs=[f for f in fields if f['parent']==parent['field_id'] and f['kind']=='ATTRIBUTE' and f['xml_name']==m[2]]
            if len(attrs)!=1:return [],'UNRESOLVED_CLASSIFIER_ATTRIBUTE'
            output.append(atom(attrs[0],'FIXED',value=m[3]))
            if m[3] in AVAILABLE_CLASSIFIERS:
                output.append(atom(parent,'CLASSIFIER',classifier_ref=m[3]))
        if output:return output,None if m[3] in AVAILABLE_CLASSIFIERS else 'EXTERNAL_CLASSIFIER_LOOKUP'
    return [],'NEEDS_NORMATIVE_INTERPRETATION'
