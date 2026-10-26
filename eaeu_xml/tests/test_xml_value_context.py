"""Shared XML context invariants; synthetic schema, no OP-specific semantics."""
from types import SimpleNamespace
import unittest
from xml.etree import ElementTree as ET
from eaeu_xml.process_packages.body import StructuredProcessBodyProvider, GenerationMode
from eaeu_xml.process_packages.models import StructureDefinition, StructureFieldDefinition
from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator, RuleStatus


def schema():
    specifications=[('G',None,'Groups',0,None),('N','G','Groups/Name',0,1),
                    ('P','G','Groups/Parts',0,None),('V','P','Groups/Parts/Value',1,1),
                    ('A','G','Groups/@code',0,1)]
    fields=[]
    for index,(identifier,parent,path,minimum,maximum) in enumerate(specifications):
        fields.append(StructureFieldDefinition(field_id=identifier,order=index,depth=path.count('/'),parent=parent,
            path=path,official_name=path,xml_name=path.split('/')[-1].lstrip('@'),namespace_prefix=None if '/@' in path else 't',
            kind='ATTRIBUTE' if '/@' in path else 'ELEMENT',datatype='t:StringType',datatype_text='synthetic',
            min_occurs=minimum,max_occurs=maximum))
    return StructureDefinition('R.TEST.CONTEXT','1.0.0','urn:test:root','Root',None,imported_namespaces={'t':'urn:test:fields'},fields=tuple(fields))


class XmlContextTests(unittest.TestCase):
    def setUp(self):
        self.schema=schema();self.provider=StructuredProcessBodyProvider(SimpleNamespace(rules={}))
        self.message=SimpleNamespace(message_code='P.TEST.MSG.001')

    def test_flatten_preserves_missing_first_and_later_children(self):
        for first,second in (({}, {'Name':'B'}),({'Name':'A'},{})):
            with self.subTest(first=first):
                flat=self.provider._flatten({'Groups':[first,second]})
                self.assertEqual(flat['Groups/Name'],[first.get('Name'),second.get('Name')])

    def test_nested_repeatables_roundtrip_keep_every_parent_axis(self):
        values={'Groups':[{'Name':'A','Parts':[{'Value':'one'},{'Value':'two'}],'@code':'first'},
                          {'Parts':[{'Value':'three'}]}]}
        root=self.provider.build_body(self.message,self.schema,values,mode=GenerationMode.TEST).serialize_xml_element()
        groups=list(root)
        self.assertEqual([n.text for n in groups[0].findall('{urn:test:fields}Parts/{urn:test:fields}Value')],['one','two'])
        self.assertEqual([n.text for n in groups[1].findall('{urn:test:fields}Parts/{urn:test:fields}Value')],['three'])
        self.assertIsNone(groups[1].find('{urn:test:fields}Name'))
        self.assertEqual(groups[0].get('code'),'first');self.assertIsNone(groups[1].get('code'))
        flat=self.provider.extract_values(self.schema,ET.fromstring(ET.tostring(root)))
        self.assertEqual(flat['Groups/Name'],['A',None])
        self.assertEqual(flat['Groups/Parts/Value'],[['one','two'],['three']])
        self.assertTrue(self.provider.validate_body(self.message,self.schema,flat,mode=GenerationMode.TEST).is_valid)

    def test_missing_required_nested_child_is_not_borrowed(self):
        for parts in (([{'Value':'ok'}],[{}]),([{}],[{'Value':'ok'}])):
            with self.subTest(parts=parts):
                result=self.provider.validate_body(self.message,self.schema,{'Groups':[{'Parts':parts[0]},{'Parts':parts[1]}]},mode=GenerationMode.TEST)
                self.assertTrue(any(i.code=='MIN_OCCURS' and i.field_path.endswith('/Value') for i in result.issues))

    def test_explicit_empty_container_survives_and_absent_container_does_not_appear(self):
        root=self.provider.build_body(self.message,self.schema,{'Groups':[{}, {'Name':'B'}]},mode=GenerationMode.TEST).serialize_xml_element()
        self.assertEqual(len(root),2)
        self.assertEqual(len(root[0]),0)
        self.assertIsNone(root[0].find('{urn:test:fields}Parts'))

    def test_scalar_broadcast_into_repeated_parents_is_rejected(self):
        result=self.provider.validate_body(self.message,self.schema,{'Groups':[{},{}],'Groups/Name':'leak'},mode=GenerationMode.TEST)
        self.assertTrue(any(i.code=='VALUE_CONTEXT_ALIGNMENT' for i in result.issues))

    def test_required_rejects_blank_and_conditional_parent_alignment(self):
        rule={'kind':'field_constraint','operation':'REQUIRED','target':'Groups/Name','ancestors':['Groups']}
        for value in ('','  ',None):
            with self.subTest(value=value):
                self.assertEqual(StructuredRuleEvaluator().evaluate(rule,{'Groups':[{},{}],'Groups/Name':['ok',value]}).status,RuleStatus.FAIL)

    def test_forbidden_rejects_explicit_empty_element_but_preserves_missing_slot(self):
        rule={'kind':'field_constraint','operation':'FORBIDDEN','target':'Groups/Name','ancestors':['Groups']}
        evaluator=StructuredRuleEvaluator()
        for value in (None, '', 'value'):
            with self.subTest(value=value):
                values={'Groups':{},'Groups/Name':value}
                root=self.provider.build_body(self.message,self.schema,values,mode=GenerationMode.TEST).serialize_xml_element()
                self.assertIsNotNone(root[0].find('{urn:test:fields}Name'))
                self.assertEqual(evaluator.evaluate(rule,self.provider._flatten(values)).status,RuleStatus.FAIL)
        self.assertEqual(evaluator.evaluate(rule,{'Groups':[{},{}],'Groups/Name':[None,None]}).status,RuleStatus.PASS)

    def test_cardinality_counts_only_emitted_nodes_and_empty_lists_are_absent(self):
        from dataclasses import replace
        required=replace(self.schema,fields=(replace(self.schema.fields[0],min_occurs=1),*self.schema.fields[1:]))
        for value in ([],[None]):
            with self.subTest(value=value):
                values={'Groups':value}
                self.assertTrue(any(i.code=='MIN_OCCURS' for i in self.provider.validate_body(self.message,required,values).issues))
                rule={'kind':'field_constraint','operation':'CARDINALITY','target':'Groups','ancestors':[],'container':True,'min_occurs':1}
                self.assertEqual(StructuredRuleEvaluator().evaluate(rule,values).status,RuleStatus.FAIL)
                rule['operation']='FORBIDDEN'
                self.assertEqual(StructuredRuleEvaluator().evaluate(rule,values).status,RuleStatus.PASS)


if __name__=='__main__':unittest.main()
