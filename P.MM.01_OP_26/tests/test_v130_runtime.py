import copy
from pathlib import Path
import json
import unittest
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages import EaeuXmlEngine, GenerationMode
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator
from eaeu_xml.core.errors import BodyValidationError, ProcessPackageValidationError
from v130_runtime_support import PACKAGE, catalogs, sample_values, provider


class V130RuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.structures,cls.rules,cls.messages=catalogs()

    def test_source_trees_cover_all_rows_and_resolve_every_parent_without_duplicate_paths(self):
        self.assertEqual(len(self.structures),7)
        self.assertEqual(sum(len(s.fields) for s in self.structures.values()),710)
        for s in self.structures.values():
            with self.subTest(structure=s.structure_id):
                by_id={f.field_id:f for f in s.fields}
                self.assertEqual(len({f.path for f in s.fields}),len(s.fields))
                for f in s.fields:
                    if f.parent:
                        self.assertIn(f.parent,by_id)
                        self.assertTrue(f.path.startswith(by_id[f.parent].path+'/'))
                    if f.namespace_prefix:self.assertIn(f.namespace_prefix,s.imported_namespaces)

    def test_every_compiled_atom_has_positive_and_negative_value_proof(self):
        evaluator=StructuredRuleEvaluator()
        seen=0
        for rules in self.rules.values():
            for rule in rules.structured_rules:
                if rule.get('kind')!='field_constraint':continue
                with self.subTest(rule=rule['rule_id']):
                    values={p:None for p in rule['ancestors']}
                    if rule.get('condition'):
                        values[rule['condition']['target']]=rule['condition']['allowed_values'][0]
                    operation=rule['operation']
                    if operation=='REQUIRED':values[rule['target']]=None if rule['container'] else 'value'
                    elif operation=='CARDINALITY':values[rule['target']]=[None]
                    elif operation=='FIXED':values[rule['target']]=rule['value']
                    elif operation=='ENUM':values[rule['target']]=rule['allowed_values'][0]
                    elif operation=='AT_LEAST_ONE':values[rule['targets'][0]]='one alternative'
                    self.assertEqual(evaluator.evaluate(rule,values).status,RuleStatus.PASS)
                    bad=copy.deepcopy(values)
                    if operation=='FORBIDDEN':bad[rule['target']]=None if rule['container'] else 'forbidden'
                    elif operation in ('ENUM','FIXED'):bad[rule['target']]='INVALID_VALUE'
                    elif operation=='AT_LEAST_ONE':
                        for path in rule['targets']:bad.pop(path,None)
                    else:bad.pop(rule['target'])
                    self.assertEqual(evaluator.evaluate(rule,bad).status,RuleStatus.FAIL)
                    if rule.get('condition'):
                        inactive=copy.deepcopy(bad);inactive[rule['condition']['target']]='not the triggering value'
                        self.assertEqual(evaluator.evaluate(rule,inactive).status,RuleStatus.PASS)
                    self.assertTrue(rule['source_refs'])
                    seen+=1
        self.assertGreater(seen,0)

    def test_all_messages_serialize_synthetic_body_through_existing_provider_in_test_mode(self):
        for code,message in self.messages.items():
            with self.subTest(msg=code):
                structure=self.structures[message.structure_id]
                values=sample_values(structure,message,self.rules.get(code))
                service=provider(self.rules)
                validation=service.validate_body(message,structure,values,mode=GenerationMode.TEST)
                self.assertTrue(validation.is_valid,[(i.code,i.field_path) for i in validation.issues if i.severity.value=='ERROR'])
                body=service.build_body(message,structure,values,mode=GenerationMode.TEST).serialize_xml_element()
                xml=ET.tostring(body,encoding='unicode');parsed=ET.fromstring(xml)
                self.assertEqual(parsed.tag,f'{{{structure.namespace}}}{structure.root_element}')
                self.assertTrue(any(i.code=='UNRESOLVED_NAMESPACE_VERSION' for i in validation.issues))
                self.assertFalse(validation.is_complete)
                extracted=service.extract_values(structure,parsed)
                again=service.validate_body(message,structure,extracted,mode=GenerationMode.TEST)
                self.assertTrue(again.is_valid,[(i.code,i.field_path) for i in again.issues if i.severity.value=='ERROR'])

    def test_actual_xml_mutation_rejects_every_compiled_constraint(self):
        for code,rules in self.rules.items():
            message=self.messages[code];structure=self.structures[message.structure_id]
            service=provider(self.rules);fields={f.path:f for f in structure.fields}
            values=sample_values(structure,message,rules)
            base=ET.tostring(service.build_body(message,structure,values,mode=GenerationMode.TEST).serialize_xml_element())
            for rule in rules.structured_rules:
                if rule.get('kind')!='field_constraint':continue
                with self.subTest(rule=rule['rule_id']):
                    root=ET.fromstring(base);parent=root;parts=rule['target'].split('/')
                    if rule.get('condition'):
                        condition_path=rule['condition']['target'].split('/')
                        xpath='/'.join(f"{{{structure.imported_namespaces[fields['/'.join(condition_path[:i+1])].namespace_prefix]}}}{fields['/'.join(condition_path[:i+1])].xml_name}" for i in range(len(condition_path)))
                        node=root.find(xpath);self.assertIsNotNone(node)
                        node.text=rule['condition']['allowed_values'][0]
                    for i,part in enumerate(parts):
                        path='/'.join(parts[:i+1]);f=fields[path]
                        if f.kind=='ATTRIBUTE':
                            parent.set(f.xml_name,'INVALID_VALUE')
                            break
                        tag=f'{{{structure.imported_namespaces[f.namespace_prefix]}}}{f.xml_name}'
                        node=next((n for n in parent if n.tag==tag),None)
                        if i==len(parts)-1 and rule['operation'] in ('REQUIRED','CARDINALITY','AT_LEAST_ONE'):
                            for child in list(parent):
                                if child.tag==tag:parent.remove(child)
                                elif rule['operation']=='AT_LEAST_ONE':
                                    alternatives={f"{{{structure.imported_namespaces[fields[p].namespace_prefix]}}}{fields[p].xml_name}" for p in rule['targets']}
                                    if child.tag in alternatives:parent.remove(child)
                            break
                        if node is None:
                            node=ET.Element(tag)
                            siblings={g.xml_name:g.order for g in structure.fields if g.parent==f.parent}
                            position=next((j for j,n in enumerate(parent) if siblings.get(str(n.tag).split('}')[-1],10**9)>f.order),len(parent))
                            parent.insert(position,node)
                        if i==len(parts)-1:
                            node.text='INVALID_VALUE'
                        parent=node
                    extracted=service.extract_values(structure,root)
                    result=service.validate_body(message,structure,extracted,mode=GenerationMode.TEST)
                    evaluation=next(e for e in result.rule_evaluations if e.rule_id==rule['rule_id'])
                    self.assertEqual(evaluation.status,RuleStatus.FAIL)

    def test_exact_namespaces_and_sequence_are_checked_for_every_message(self):
        for code,message in self.messages.items():
            with self.subTest(msg=code):
                structure=self.structures[message.structure_id];service=provider(self.rules)
                root=ET.fromstring(ET.tostring(service.build_body(message,structure,sample_values(structure,message,self.rules.get(code)),mode=GenerationMode.TEST).serialize_xml_element()))
                bad=copy.deepcopy(root);list(list(bad)[0])[0].tag='{urn:wrong}InfEnvelopeCode'
                with self.assertRaises(BodyValidationError) as error:service.extract_values(structure,bad)
                self.assertEqual(error.exception.code,'UNKNOWN_XML_QNAME')
                bad=copy.deepcopy(root);header=list(bad)[0];header[:]=list(reversed(list(header)))
                with self.assertRaises(BodyValidationError) as error:service.extract_values(structure,bad)
                self.assertEqual(error.exception.code,'XML_SEQUENCE_ORDER')

    def test_every_message_rejects_missing_header_identifier(self):
        for code,message in self.messages.items():
            with self.subTest(msg=code):
                structure=self.structures[message.structure_id]
                values=sample_values(structure,message,self.rules.get(code));values.pop('EDocHeader/EDocId',None)
                result=provider(self.rules).validate_body(message,structure,values,mode=GenerationMode.TEST)
                self.assertTrue(any(i.code=='MIN_OCCURS' and i.field_path=='EDocHeader/EDocId' for i in result.issues))

    def test_every_message_rejects_invalid_uuid_datetime_and_header_cardinality(self):
        for code,message in self.messages.items():
            with self.subTest(msg=code):
                structure=self.structures[message.structure_id]
                original=sample_values(structure,message,self.rules.get(code))
                for path,value,expected in (('EDocHeader/EDocId','invalid','PATTERN'),
                                             ('EDocHeader/EDocDateTime','not-a-date','DATATYPE_INVALID'),
                                             ('EDocHeader/InfEnvelopeCode',[code,code],'MAX_OCCURS')):
                    values=dict(original);values[path]=value
                    result=provider(self.rules).validate_body(message,structure,values,mode=GenerationMode.TEST)
                    self.assertTrue(any(i.code==expected and i.field_path==path for i in result.issues))

    def test_arbitrary_xml_alternative_roundtrips_without_invented_wrapper(self):
        message=self.messages['P.MM.01.MSG.031'];structure=self.structures[message.structure_id]
        values=sample_values(structure,message,self.rules[message.message_code])
        for path in list(values):
            if '/DocCopyBinaryText' in path:values.pop(path)
        any_field=next(f for f in structure.fields if f.kind=='ARBITRARY_XML')
        values[any_field.path]=ET.fromstring('<e:Payload xmlns:e="urn:external:test" answer="42"><e:Child/></e:Payload>')
        values[any_field.path.rsplit('/',1)[0]]=None
        service=provider(self.rules)
        root=service.build_body(message,structure,values,mode=GenerationMode.TEST).serialize_xml_element()
        self.assertIsNotNone(root.find('.//{urn:external:test}Payload'))
        flat=service.extract_values(structure,ET.fromstring(ET.tostring(root)))
        self.assertTrue(service.validate_body(message,structure,flat,mode=GenerationMode.TEST).is_valid)

    def test_actual_process_version_stays_blocked(self):
        with self.assertRaises(ProcessPackageValidationError) as error:EaeuXmlEngine.load_process(PACKAGE)
        self.assertEqual(error.exception.code,'PROCESS_VERSION_NOT_READY')
        status=json.loads((PACKAGE/'migration_status.json').read_text())
        self.assertIs(status['promotion_allowed'],False)


if __name__=='__main__':unittest.main()
