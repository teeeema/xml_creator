import unittest
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator
from eaeu_xml.process_packages.body import BodyValidationResult
from eaeu_xml.process_packages.rules_engine import RuleEvaluation

class StructuredRuleTests(unittest.TestCase):
    def setUp(self):
        self.e=StructuredRuleEvaluator(); self.p='Groups'
        self.v={'Groups':[None,None], 'Groups/Flag':[True,False], 'Groups/Amount':['1.20','0.80'], 'Groups/Country':['AA',None]}
    def test_selector_eq_ne_and_cardinality(self):
        daily={'collection':self.p,'where':{'field':'Flag','operator':'EQ','value':True}}
        monthly={'collection':self.p,'where':{'field':'Flag','operator':'NE','value':True}}
        self.assertEqual(len(self.e.select(daily,self.v)),1); self.assertEqual(len(self.e.select(monthly,self.v)),1)
        self.assertEqual(self.e.evaluate({'kind':'selection_cardinality','selector':daily,'min_occurs':1,'max_occurs':1},self.v).status,RuleStatus.PASS)
        self.assertEqual(self.e.evaluate({'kind':'selection_cardinality','selector':daily,'min_occurs':0,'max_occurs':0},self.v).status,RuleStatus.FAIL)
    def test_conditional_and_aggregate(self):
        rule={'kind':'conditional_presence','scope':{'collection':self.p},'condition':{'field':'Flag','operator':'EQ','value':True},'target':{'field':'Country'},'state':'FORBIDDEN'}
        self.assertEqual(self.e.evaluate(rule,self.v).status,RuleStatus.FAIL)
        total={'collection':self.p,'where':{'field':'Flag','operator':'EQ','value':True}}
        parts={'collection':self.p,'where':{'field':'Flag','operator':'EQ','value':False}}
        rule={'kind':'aggregate_comparison','left':{'selector':total,'value_field':'Amount','aggregation':'VALUE'},'operator':'EQ','right':{'selector':parts,'value_field':'Amount','aggregation':'SUM'}}
        self.assertEqual(self.e.evaluate(rule,self.v).status,RuleStatus.FAIL)
    def test_external_and_unsupported_are_not_pass(self):
        self.assertEqual(self.e.evaluate({'evaluation_status':'EXTERNAL_CONTEXT_REQUIRED'},{}).status,RuleStatus.NOT_EVALUATED_EXTERNAL_CONTEXT)
        self.assertEqual(self.e.evaluate({'kind':'unknown'},{}).status,RuleStatus.UNSUPPORTED_RULE)

    def test_selection_many_zero_and_conditional_required(self):
        selector={'collection':self.p,'where':{'field':'Flag','operator':'EQ','value':True}}
        self.assertEqual(self.e.evaluate({'kind':'selection_cardinality','selector':selector,'min_occurs':2,'max_occurs':2},self.v).status,RuleStatus.FAIL)
        empty={'collection':self.p,'where':{'field':'Flag','operator':'EQ','value':'missing'}}
        self.assertEqual(self.e.evaluate({'kind':'selection_cardinality','selector':empty,'min_occurs':0,'max_occurs':0},self.v).status,RuleStatus.PASS)
        r={'kind':'conditional_presence','scope':{'collection':self.p},'condition':{'field':'Flag','operator':'EQ','value':False},'target':{'field':'Country'},'state':'REQUIRED'}
        self.assertEqual(self.e.evaluate(r,self.v).status,RuleStatus.FAIL)

    def test_completeness_statuses(self):
        self.assertTrue(BodyValidationResult((),(RuleEvaluation('x',RuleStatus.PASS,'x'),)).is_complete)
        self.assertFalse(BodyValidationResult((),(RuleEvaluation('x',RuleStatus.NOT_EVALUATED_EXTERNAL_CONTEXT,'x'),)).is_complete)
        self.assertFalse(BodyValidationResult((),(RuleEvaluation('x',RuleStatus.UNSUPPORTED_RULE,'x'),)).is_complete)

if __name__=='__main__': unittest.main()
