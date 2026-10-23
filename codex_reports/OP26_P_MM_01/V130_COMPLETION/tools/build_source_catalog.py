"""Import official Word tables as a blocked, source-only OP26 edition.

Does not infer executable predicates, XML paths, model versions or datasets.
Table indexes address the archived official DOCX XML, not printed table numbers.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import csv
import hashlib
import io
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[4]
REPORT = ROOT / 'codex_reports/OP26_P_MM_01/V130_COMPLETION'
SOURCES = REPORT / 'sources'
PACKAGE = ROOT / 'P.MM.01_OP_26/versions/1.3.0'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
URLS = {'140': 'https://docs.eaeunion.org/documents/446/10427/',
        '77': 'https://docs.eaeunion.org/documents/463/10765/'}


def normalize(text):
    return ''.join(c for c in text if c.isalnum()).lower()


PDF_PAGES = {}
for number in URLS:
    parts = re.split(r'--- PDF PAGE (\d+) ---', (SOURCES / f'decision_{number}.txt').read_text())
    PDF_PAGES[number] = [(int(parts[i]), normalize(parts[i + 1])) for i in range(1, len(parts), 2)]


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def extract(number):
    archive = zipfile.ZipFile(SOURCES / f'decision_{number}_word.zip')
    name = max(archive.namelist(), key=lambda n: archive.getinfo(n).file_size)
    doc = zipfile.ZipFile(io.BytesIO(archive.read(name)))
    body = ET.fromstring(doc.read('word/document.xml')).find('w:body', NS)
    def text(element):
        return ' '.join(''.join(t.text or '' for t in element.findall('.//w:t', NS)).split())
    tables, paragraphs, all_paragraphs = [], [], []
    for element in body:
        if element.tag.endswith('}p'):
            paragraphs.append(text(element))
            all_paragraphs.append(text(element))
        elif element.tag.endswith('}tbl'):
            tables.append({'table_index': len(tables), 'preceding_paragraphs': paragraphs[-12:],
                           'rows': [[text(c) for c in r.findall('w:tc', NS)]
                                    for r in element.findall('w:tr', NS)]})
            paragraphs = []
    save(SOURCES / f'decision_{number}_tables.json', tables)
    save(SOURCES / f'decision_{number}_paragraphs.json', all_paragraphs)
    return tables


def ref(table, number='140', item=None):
    headings = table['preceding_paragraphs']
    label = next((p for p in reversed(headings) if re.search(r'Таблица\s+\d+', p)), '')
    printed = re.search(r'Таблица\s+(\d+)', label)
    caption = next((p for p in reversed(headings) if p.strip() and not re.fullmatch(r'[«\s]*Таблица\s+\d+', p)), '')
    needle = normalize(caption)
    matches = [page for page, text in PDF_PAGES[number] if needle and needle in text]
    return {'source_id': f'SRC-PMM01-{number}', 'document': URLS[number],
            'location': f"Official Word attachment, table_index={table['table_index']}; " + ' / '.join(headings[-3:]),
            'status': 'CONFIRMED', 'table': printed.group(1) if printed else None,
            'page': matches[0] if len(matches) == 1 else None,
            'section': 'page uses absolute PDF page number; Word table_index is authoritative locator within attachment',
            'item': item, 'version_context': 'P.MM.01 1.3.0; amendments 140/2025 and 77/2026'}


def codes(text, kind):
    return re.findall(r'P\.MM\.01\.' + kind + r'\.\d{3}', text)


def one(text, kind):
    found = list(dict.fromkeys(codes(text, kind)))
    if len(found) != 1:
        raise ValueError((kind, text))
    return found[0]


def build():
    a, b = extract('140'), extract('77')
    assert len(a) == 231 and len(b) == 14
    collections = {}
    participants = []
    for row in a[2]['rows'][2:]:
        participants.append({'participant_code': row[0], 'name': row[1], 'description': row[2],
                             'segment_policy': 'NEEDS_VERIFICATION',
                             'status': 'NEEDS_VERIFICATION', 'source_refs': [ref(a[2], item=row[0])]})
    collections['participants'] = participants
    procedures = []
    for t in a[3:11]:
        for row in t['rows'][2:]:
            procedures.append({'procedure_code': row[0], 'name': row[1], 'description': row[2],
                               'status': 'SOURCE_TEXT_IMPORTED', 'source_refs': [ref(t, item=row[0])]})
    collections['procedures'] = procedures
    operations = []
    for t in a[13:125]:
        rows = t['rows']
        if len(rows) != 9 or rows[2][1] != 'Кодовое обозначение':
            continue
        code = one(rows[2][2], 'OPR')
        operations.append({'operation_code': code, 'name': rows[3][2],
                           'participant_role': rows[4][2], 'normative_rows': rows[4:],
                           'status': 'SOURCE_TEXT_IMPORTED', 'source_refs': [ref(t, item=code)]})
    # 77/2026 1(c,d,f): retain both original and amendment references.
    for op in operations:
        if op['operation_code'].endswith('.073'):
            op['name'] = op['name'].replace('полученных ', '')
            op['source_refs'].append(ref(b[2], '77', '1(c,d)'))
        if op['operation_code'].endswith('.078'):
            op['name'] = op['name'].replace('обработка сведений', 'обработка сведений для исключения')
            op['source_refs'].append(ref(b[2], '77', '1(e,f)'))
    collections['operations'] = operations
    links = {}
    for index in (127, 128, 129, 179, 180, 181, 182):
        current = None
        for row in a[index]['rows'][2:]:
            if len(row) == 2:
                current = one(row[1], 'PRC')
            elif len(row) == 6:
                code = one(row[5], 'TRN')
                links[code] = {'procedure_code': current,
                               'initiating_operation': codes(row[1], 'OPR')[0],
                               'responding_operation': one(row[3], 'OPR'),
                               'source_refs': [ref(a[index], item=row[0])], 'normative_rows': [row]}
    transactions = []
    for index in list(range(131, 150)) + list(range(184, 193)):
        t = a[index]
        data = {r[1]: r[2] for r in t['rows'][2:]}
        code = one(data['Кодовое обозначение'], 'TRN')
        transaction = {'transaction_code': code, 'name': data['Наименование транзакции общего процесса'],
                       **links[code], 'source_pattern': data['Шаблон транзакции общего процесса'],
                       'initiating_role': data['Инициирующая роль'], 'responding_role': data['Реагирующая роль'],
                       'initiating_message': one(data['инициирующее сообщение'], 'MSG'),
                       'response_messages': codes(data['ответное сообщение'], 'MSG'),
                       'normative_rows': t['rows'][2:], 'status': 'SOURCE_TEXT_IMPORTED'}
        # Keep timing/auth/signature in exact source text until interpretation is verified.
        transaction['source_refs'] += [ref(t, item=code)]
        transactions.append(transaction)
    collections['transactions'] = transactions
    messages = {}
    for index in (130, 183):
        t = a[index]
        for row in t['rows'][2:]:
            code = one(row[0], 'MSG')
            structures = re.findall(r'R\.(?:HC\.MM\.01\.)?\d{3}', row[2])
            assert len(structures) == 1, row
            if code in messages:
                assert messages[code]['structure_id'] == structures[0], row
                messages[code]['source_refs'].append(ref(t, item=code))
                continue
            messages[code] = {'message_code': code, 'name': row[1], 'structure_id': structures[0],
                              'structure_version': None if structures[0] in ('R.006', 'R.007') else '1.3.0',
                              'status': 'SOURCE_TEXT_IMPORTED', 'message_rules_status': 'NEEDS_VERIFICATION',
                              'source_refs': [ref(t, item=code)]}
    collections['messages'] = [messages[c] for c in sorted(messages)]
    # Requirements remain scoped by regulation: repeated MSG tables must not overwrite each other.
    rule_tables = {i: a[i] for i in list(range(151, 177)) + list(range(194, 206))}
    rule_numbers = {i: '140' for i in rule_tables}
    for old, new in ((171, 4), (172, 5), (173, 6), (196, 9), (197, 10), (201, 11)):
        rule_tables[old] = b[new]
        rule_numbers[old] = '77'
    rules = {}
    for index, t in rule_tables.items():
        number = rule_numbers[index]
        code = one(' '.join(t['preceding_paragraphs'][-3:]), 'MSG')
        for row in t['rows'][1:]:
            cells = row[1:3] if number == '77' else row
            assert len(cells) == 2, (index, row)
            item, requirement = cells
            if index == 151 and item == '2':
                paragraph = next(p for p in b[2]['preceding_paragraphs'] if 'в позиции 2 графу вторую' in p)
                requirement = paragraph.split('следующей редакции: «', 1)[1].rsplit('»;', 1)[0]
                number_for_row = '77'
                row_ref = ref(b[2], '77', '2(a), row 2')
            elif index == 152 and re.fullmatch(r'3\s*[-–]\s*82', item):
                item = '3-87'
                requirement = re.sub(r'3\s*[-–]\s*85', '3-87', requirement).replace('таблицы 20', 'таблицы 26')
                number_for_row = '77'
                row_ref = ref(b[3], '77', '2(b)')
            else:
                number_for_row = number
                row_ref = ref(t, number, item)
            rules.setdefault(code, []).append({'source_requirement_code': item,
                                               'source_regulation_table_index': index,
                                               'requirement': requirement, 'field_paths': [],
                                               'interpretation_status': 'NOT_EXECUTABLE_SOURCE_TEXT',
                                               'source_refs': [row_ref]})
    for index, code in ((2, 'P.MM.01.MSG.001'), (3, 'P.MM.01.MSG.014')):
        row = b[index]['rows'][0]
        rules[code].append({'source_requirement_code': row[1], 'source_regulation_table_index': 151 if index == 2 else 159,
                            'requirement': row[2], 'field_paths': [],
                            'interpretation_status': 'NOT_EXECUTABLE_SOURCE_TEXT',
                            'source_refs': [ref(b[index], '77', row[1])]})
    for code, rows in rules.items():
        # Local IDs explicitly identify a source row, not a fabricated normative REQ identifier.
        for n, row in enumerate(rows, 1): row['rule_id'] = f'{code}.SOURCE_ROW.{n}'
        save(PACKAGE / 'message_rules' / f'{code}.yaml', {'message_code': code,
             'structure_id': messages[code]['structure_id'], 'business_rules': rows,
             'source_refs': [r for r in messages[code]['source_refs']], 'structured_rules': []})
    for code, message in messages.items():
        message['message_rules_source_refs'] = message['source_refs']
    classifiers = []
    for row in a[12]['rows'][2:]:
        if row[0] in ('P.MM.01.CLS.009', 'P.MM.01.CLS.010'): continue
        classifiers.append({'classifier_code': row[0], 'name': row[1], 'kind': row[2], 'description': row[3],
                            'dataset_status': 'SOURCE_BLOCKED', 'source_refs': [ref(a[12], item=row[0])]})
    for row in b[1]['rows']:
        classifiers.append({'classifier_code': row[1], 'name': row[2], 'kind': row[3], 'description': row[4],
                            'dataset_status': 'SOURCE_BLOCKED', 'source_refs': [ref(b[1], '77', row[1])]})
    save(PACKAGE / 'classifier_references.yaml', {'classifiers': classifiers, 'datasets_available': False})
    structures = []
    for definition, imports, fields in ((208, 209, 210), (211, 212, 213), (214, 215, 216),
                                         (217, 218, 219), (220, 221, 222), (223, 224, 225), (226, 227, 228)):
        values = {r[1]: r[2] for r in a[definition]['rows'][2:]}
        field_table = b[12] if fields == 216 else b[13] if fields == 225 else a[fields]
        number = '77' if fields in (216, 225) else '140'
        structures.append({'structure_id': values['Идентификатор'], 'declared_version': values['Версия'],
                           'namespace': values['Идентификатор пространства имен'],
                           'root_element': values['Корневой элемент XML-документа'],
                           'schema_filename': values['Имя файла XML-схемы'],
                           'imports_source_rows': a[imports]['rows'][2:],
                           'fields_source_rows': field_table['rows'][1:],
                           'source_refs': [ref(a[definition]), ref(a[imports]), ref(field_table, number)],
                           'runtime_status': 'SOURCE_BLOCKED_MODEL_VERSIONS_AND_XSD'})
    save(PACKAGE / 'structures/source_inventory.json', {'structures': structures,
         'note': 'Source rows only. No inferred executable XML paths, QName namespaces, facets or official XSD validation.'})
    field_inventory = []
    for structure in structures:
        for index, row in enumerate(structure['fields_source_rows'], 1):
            cells = row[:]
            while cells and not cells[0]: cells.pop(0)
            assert len(cells) == 5, (structure['structure_id'], index, row)
            name, description, identifier, datatype, cardinality = cells
            match = re.fullmatch(r'(\d+)(?:\.\.(\d+|\*))?', cardinality)
            assert match, cardinality
            field_inventory.append({'structure_id': structure['structure_id'], 'source_row_index': index,
                'source_field_name': name, 'source_identifier': identifier,
                'source_datatype': datatype, 'description': description,
                'source_cardinality': cardinality, 'min_occurs': int(match[1]),
                'max_occurs': None if match[2] == '*' else int(match[2] or match[1]),
                'expanded_qname': None, 'xml_path': None,
                'status': 'SOURCE_BLOCKED_MODEL_VERSIONS;NOT_TESTED_PATH_INTERPRETATION',
                'source_refs': structure['source_refs'][-1:]})
    save(REPORT / 'field_inventory.json', field_inventory)
    with (REPORT / 'field_inventory.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(k for k in field_inventory[0] if k != 'source_refs'))
        writer.writeheader()
        writer.writerows({k: row[k] for k in writer.fieldnames} for row in field_inventory)
    for name, items in collections.items(): save(PACKAGE / f'{name}.yaml', {name: items})
    process = json.loads((PACKAGE / 'process.yaml').read_text())
    process['source_refs'] = [{'source_id': 'SRC-PMM01-140', 'document': URLS['140'],
        'location': 'Приложение, пункт 1; Правила информационного взаимодействия, пункт 6',
        'status': 'CONFIRMED', 'page': 7, 'item': '6',
        'version_context': 'P.MM.01 1.3.0; page is absolute PDF page'}]
    save(PACKAGE / 'process.yaml', process)
    save(PACKAGE / 'message_rules_audit.yaml', {'messages': {c: {'status': 'NEEDS_VERIFICATION',
         'source_refs': messages[c]['source_refs']} for c in sorted(messages)}})
    save(PACKAGE / 'version_profiles/current.yaml', {'process_version': '1.3.0',
         'models': {'base': None, 'healthcare': None},
         'structures': {s['structure_id']: {'active_version': None if s['declared_version'] == 'Y.Y.Y' else s['declared_version'],
                                          'source': 'local'} for s in structures},
         'draft': True, 'readiness': 'NOT_READY',
         'notes': 'Model X.X.X/Z.Z.Z and R.006/R.007 Y.Y.Y are literal unresolved source parameters; production is blocked.'})
    summary = {name: len(items) for name, items in collections.items()}
    summary.update(structures=len(structures), classifiers=len(classifiers),
                   scoped_requirement_rows=sum(len(r) for r in rules.values()),
                   messages_with_requirement_tables=len(rules),
                   atomic_requirements='UNKNOWN_NOT_DECOMPOSED',
                   executable_structured_rules=0,
                   field_source_rows=sum(len(s['fields_source_rows']) for s in structures))
    save(REPORT / 'inventory.json', summary)
    delta = []
    for name, key in (('participants', 'participant_code'), ('procedures', 'procedure_code'),
                      ('operations', 'operation_code'), ('transactions', 'transaction_code'), ('messages', 'message_code')):
        legacy = json.loads((ROOT / 'P.MM.01_OP_26' / f'{name}.yaml').read_text())[name]
        old, new = {x[key]: x for x in legacy}, {x[key]: x for x in collections[name]}
        for code in sorted(old.keys() | new.keys()):
            change = 'ADDED' if code not in old else 'EXCLUDED' if code not in new else 'REQUIRES_CONFIRMATION'
            delta.append({'entity': name, 'code': code, 'change': change,
                          'legacy_name': old.get(code, {}).get('name'), 'new_name': new.get(code, {}).get('name'),
                          'explanation': 'Membership confirmed by full source lists; retained semantic equivalence is not inferred from equal IDs.',
                          'source_refs': new.get(code, {}).get('source_refs', []),
                          'evidence_for_exclusion': URLS['140'] if code not in new else None})
    save(REPORT / 'delta.json', delta)
    with (REPORT / 'delta.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=('entity', 'code', 'change', 'legacy_name', 'new_name'))
        writer.writeheader(); writer.writerows({k: r[k] for k in writer.fieldnames} for r in delta)
    save(REPORT / 'sources/sha256.json', {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
         for p in sorted(SOURCES.iterdir()) if p.suffix in ('.pdf', '.zip')})
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__': build()
