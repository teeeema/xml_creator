"""Internal component proof only: no readiness flag changes or alternate generator."""
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree as ET
import json
import re

from eaeu_xml.process_packages import ProcessPackageLoader
from eaeu_xml.process_packages.models import MessageDefinition
from eaeu_xml.process_packages.body import StructuredProcessBodyProvider

PACKAGE = Path(__file__).resolve().parents[1] / 'versions/1.3.0'
CLASSIFIER_VALUES = ProcessPackageLoader.load_classifier_values(PACKAGE/'classifiers')


def catalogs():
    structures = {s.structure_id:s for s in ProcessPackageLoader.load_structures(PACKAGE/'structures').values()}
    rules = ProcessPackageLoader.load_rules(PACKAGE/'message_rules')
    messages = {m['message_code']:MessageDefinition(message_code=m['message_code'],name=m['name'],structure_id=m['structure_id'])
                for m in json.loads((PACKAGE/'messages.yaml').read_text())['messages']}
    return structures,rules,messages


def value_for(field, message, structure, classifier_ref=None):
    facets=field.facets
    if facets and facets.enum:return facets.enum[0]
    ref=classifier_ref or field.classifier_ref
    if ref in CLASSIFIER_VALUES:
        for code in sorted(CLASSIFIER_VALUES[ref]):
            if (not facets or ((not facets.pattern or re.fullmatch(facets.pattern,code)) and (facets.min_length is None or len(code)>=facets.min_length) and (facets.max_length is None or len(code)<=facets.max_length))):return code
        raise ValueError(('No classifier sample meeting explicit facets',field.path))
    if field.xml_name=='InfEnvelopeCode':return message.message_code
    if field.xml_name=='EDocCode':return structure.structure_id
    dtype=(field.datatype or '').lower()
    if 'universallyunique' in dtype:return '11111111-1111-4111-8111-111111111111'
    if 'datetime' in dtype:return '2026-10-23T12:00:00+03:00'
    if dtype.endswith('datetype'):return '2026-10-23'
    if 'indicator' in dtype:return True
    if field.kind=='ARBITRARY_XML':return ET.Element('{urn:example:untrusted}Sample')
    if 'quantity' in dtype or 'integer' in dtype:return 1
    if facets and facets.pattern:
        digits=re.fullmatch(r'\\d\{(\d+)\}',facets.pattern)
        if digits:return '1'*int(digits[1])
        for sample in ('A01AA01','RU','ru','123456789','1','01','001','11111111-1111-4111-8111-111111111111','A0A'):
            if re.fullmatch(facets.pattern,sample):return sample
        raise ValueError(('No test sample for pattern',field.path,facets.pattern))
    return 'X'*max(1,facets.min_length if facets and facets.min_length else 1)


def sample_values(structure, message, rules):
    """Synthetic test input, not classifier data or a normative example."""
    fields={f.path:f for f in structure.fields};values={}
    child_elements={f.parent for f in structure.fields if f.kind!='ATTRIBUTE'}
    forbidden={r['target'] for r in rules.structured_rules if r.get('kind')=='field_constraint' and r['operation']=='FORBIDDEN' and not r.get('condition')} if rules else set()
    requested={r['target'] for r in rules.structured_rules if r.get('kind')=='field_constraint' and r['operation'] in ('REQUIRED','CARDINALITY','FIXED')} if rules else set()
    if rules:
        requested.update(r['targets'][0] for r in rules.structured_rules if r.get('operation')=='AT_LEAST_ONE')
        requested.update(r['condition']['target'] for r in rules.structured_rules if r.get('condition') and r['operation']!='FORBIDDEN')
        requested.update(r['target'] for r in rules.structured_rules if r.get('operation')=='POSITIONAL_VALUES')
    def excluded(path):return any(path==p or path.startswith(p+'/') for p in forbidden)
    def include(path):
        if excluded(path):return
        parts=path.split('/')
        for i in range(1,len(parts)):
            parent='/'.join(parts[:i]);f=fields[parent]
            values.setdefault(parent,None if f.field_id in child_elements else value_for(f,message,structure))
        field=fields[path]
        values.setdefault(path,None if field.field_id in child_elements else value_for(field,message,structure))
    for f in structure.fields:
        if not f.parent and f.min_occurs:include(f.path)
    for path in requested:include(path)
    # Close required descendants only where an actual parent instance exists.
    for f in structure.fields:
        if f.min_occurs and (not f.parent or f.path.rsplit('/',1)[0] in values):include(f.path)
    if rules:
        for rule in rules.structured_rules:
            if rule.get('kind')!='field_constraint':continue
            if rule['operation']=='FIXED':values[rule['target']]=rule['value']
            if rule['operation']=='ENUM' and rule['target'] in values:values[rule['target']]=rule['allowed_values'][0]
            if rule.get('condition') and rule['operation']!='FORBIDDEN':values[rule['condition']['target']]=rule['condition']['allowed_values'][0]
            if rule['operation']=='CLASSIFIER' and rule['target'] in values:values[rule['target']]=value_for(fields[rule['target']],message,structure,rule['classifier_ref'])
            if rule['operation']=='POSITIONAL_VALUES':values[rule['target']]=rule['first_value']
    return values


def provider(rules):
    return StructuredProcessBodyProvider(SimpleNamespace(rules=rules,classifier_values=CLASSIFIER_VALUES))
