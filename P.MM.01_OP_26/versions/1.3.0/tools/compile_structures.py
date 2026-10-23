"""Compile preserved official table rows, retaining unresolved namespace parameters.

Fnnnn are local row IDs, not invented normative identifiers. Grid indentation
in the archived official Word tables owns hierarchy, including wildcard numbers.
No official XSD or production model version is synthesized.
"""
from pathlib import Path
import copy
import json
import re
import unicodedata

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[2]
REPORT = ROOT / 'codex_reports/OP26_P_MM_01/V130_STAGE2'


def clean(text):
    return ''.join(c for c in text if unicodedata.category(c) != 'Cf')


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def facets(text):
    out = {}
    for label, key in ((r'Мин\. длина:', 'min_length'), (r'Макс\. длина:', 'max_length'),
                       (r'Общее количество цифр:', 'total_digits'), (r'Количество дробных цифр:', 'fraction_digits')):
        match = re.search(label+r'\s*(\d+)', text)
        if match: out[key] = int(match[1])
    length = re.search(r'(?:^|[.\s])Длина:\s*(\d+)', text)
    if length: out.update(min_length=int(length[1]), max_length=int(length[1]))
    pattern = re.search(r'Шаблон:\s*(.+)$', text)
    if pattern:
        re.compile(pattern[1])
        out['pattern'] = pattern[1]
    return out


def compile_all():
    inventory = json.loads((PACKAGE / 'structures/source_inventory.json').read_text())['structures']
    audit = []
    for source in inventory:
        imports = {r[2]: clean(r[1]) for r in source['imports_source_rows']}
        fields, stack = [], {}
        for index, raw in enumerate(source['fields_source_rows'], 1):
            depth = next(i for i,c in enumerate(raw) if c)
            assert len(raw[depth:]) == 5
            name, description, identifier, dtype, occurs = map(clean, raw[depth:])
            assert depth == 0 or depth-1 in stack, (source['structure_id'], index, depth)
            parent = stack.get(depth-1) if depth else None
            assert parent is None or parent['kind'] == 'ELEMENT', (index, parent)
            attribute = re.search(r'\(атрибут\s+(\w+)\)', name)
            qname = re.search(r'\(([a-z]+):([A-Za-z_][A-Za-z0-9_]*)\)', name)
            if attribute:
                kind, prefix, local = 'ATTRIBUTE', None, attribute[1]
                part = '@'+local
            elif qname:
                kind, prefix, local = 'ELEMENT', qname[1], qname[2]
                assert prefix in imports, (source['structure_id'], index, prefix)
                part = local
            elif 'XML-документ' in name:
                # The source calls for arbitrary XML, not an invented wrapper QName.
                kind, prefix, local, part = 'ARBITRARY_XML', None, None, '*'
            else:
                raise ValueError(('UNRESOLVED_LOCAL_NAME', source['structure_id'], index, name))
            path = (parent['path']+'/' if parent else '')+part
            min_max = re.fullmatch(r'(\d+)(?:\.\.(\d+|\*))?', occurs)
            assert min_max, occurs
            datatype = 'ANY_XML' if kind == 'ARBITRARY_XML' else re.match(r'[a-z]+:[A-Za-z0-9_]+', dtype)
            if kind != 'ARBITRARY_XML': datatype = datatype[0] if datatype else None
            refs = copy.deepcopy(source['source_refs'][-1:])
            for ref in refs:
                ref['item'] = f'row {index}: {name.split(" ",1)[0]}'
            facet = facets(dtype)
            if kind == 'ATTRIBUTE':
                fixed = re.search(r'Значение\s*«([^»]+)»', dtype)
                if fixed: facet.update(enum=[fixed[1]], default_value=fixed[1])
            interpretation = 'VERIFIED' if kind in ('ATTRIBUTE','ARBITRARY_XML') else 'NEEDS_EXTERNAL_SOURCE'
            field = {'field_id':f'F{index:04d}', 'order':index, 'depth':depth,
                'parent':parent['field_id'] if parent else None, 'path':path, 'official_name':name,
                'xml_name':local, 'namespace_prefix':prefix, 'kind':kind, 'datatype':datatype,
                'datatype_text':dtype, 'min_occurs':int(min_max[1]),
                'max_occurs':None if min_max[2]=='*' else int(min_max[2] or min_max[1]),
                'description':description, 'identifier':identifier, 'constraints':dtype,
                'facets':facet or None, 'source_refs':refs, 'status':'CONFIRMED',
                'interpretation_status':interpretation,
                'reason_code':None if interpretation=='VERIFIED' else 'MODEL_NAMESPACE_VERSION_UNRESOLVED'}
            fields.append(field)
            stack = {k:v for k,v in stack.items() if k<depth}
            stack[depth] = field
            audit.append({'structure_id':source['structure_id'], **field,
                'source_row_index':index, 'source_grid_depth':depth,
                'namespace_uri':None if kind=='ATTRIBUTE' else imports.get(prefix),
                'expanded_qname':local if kind=='ATTRIBUTE' else None,
                'qname_status':'UNQUALIFIED_ATTRIBUTE' if kind=='ATTRIBUTE' else 'WILDCARD' if kind=='ARBITRARY_XML' else 'UNRESOLVED_MODEL_VERSION',
                'schema_order':'SOURCE_TABLE_ORDER;XSD_COMPOSITOR_NOT_CONFIRMED'})
        paths = [f['path'] for f in fields]
        assert len(paths)==len(set(paths)), (source['structure_id'],'DUPLICATE_PATH')
        by_id={f['field_id']:f for f in fields}
        for field in fields:
            if field['kind']=='ATTRIBUTE' and field.get('facets',{}):
                fixed=field['facets'].get('default_value')
                if fixed and field['xml_name']=='codeListId':
                    by_id[field['parent']]['classifier_ref']=fixed
        # Copy classifier binding into the audit rows after reading child attributes.
        for row in audit:
            if row['structure_id']==source['structure_id']:
                row['classifier_ref']=by_id[row['field_id']].get('classifier_ref')
        definition={'structure_id':source['structure_id'], 'version':source['declared_version'],
            'namespace':source['namespace'], 'root_element':source['root_element'],
            'xsd_file':source['schema_filename'], 'official_name':source['root_element'],
            'imported_namespaces':imports, 'fields':fields, 'expected_normative_rows':len(fields),
            'imported_normative_rows':len(fields), 'excluded_rows':[], 'source_refs':source['source_refs'],
            'status':'DRAFT_MODEL_NAMESPACE_UNRESOLVED',
            'field_table_reference':{'status':'SOURCE_TREE_COMPILED;OFFICIAL_XSD_NOT_VERIFIED'}}
        dump(PACKAGE/'structures'/source['structure_id']/(source['declared_version']+'.yaml'),definition)
    dump(REPORT/'structure_fields.json',audit)
    print('Compiled:',len(inventory),'source trees;',len(audit),'rows; statuses:',
          {s:sum(f['interpretation_status']==s for f in audit) for s in set(f['interpretation_status'] for f in audit)})


if __name__=='__main__': compile_all()
