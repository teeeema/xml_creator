from pathlib import Path
import tempfile
import unittest

from eaeu_xml.application import (
    ConditionEvaluator, ConditionResult, ConditionalFieldRule, ConditionalRuleCompiler,
    DraftService, FieldView, FieldVisibilityFilter, FormDefinition, FormDisplayMode,
)


def field(path, *, required=False, children=(), repeatable=False, policy="USER_INPUT"):
    return FieldView(path,path.rsplit("/",1)[-1],path.rsplit("/",1)[-1],f"Описание {path}","ELEMENT","StringType",
                     required,1 if required else 0,None if repeatable else 1,False,repeatable,
                     children=tuple(children),normative_input_policy="CONDITIONAL" if path.endswith("Target") else policy,
                     ui_input_policy="USER_INPUT")


class ConditionEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.evaluator=ConditionEvaluator()
        self.target=field("Group/Target")
        self.source=field("Group/Source")
        self.group=field("Group",children=(self.source,self.target),policy="GROUP")
        self.form=FormDefinition("P","T","M","R","1", "OK",None,(self.group,))

    def rule(self,operator="EQUALS",expected="yes",effect="SHOW",values=()):
        return ConditionalFieldRule("Group/Target",operator,"Group/Source",operator,expected,tuple(values),effect,
                                    ("SRC-TEST",),original_description="Structured test condition",rule_id="C-1")

    def test_equals_true_false_and_unknown(self):
        rule=self.rule()
        self.assertEqual(self.evaluator.evaluate(rule,{"Group/Source":"yes"}),ConditionResult.TRUE)
        self.assertEqual(self.evaluator.evaluate(rule,{"Group/Source":"no"}),ConditionResult.FALSE)
        self.assertEqual(self.evaluator.evaluate(rule,{}),ConditionResult.UNKNOWN)

    def test_present_absent_true_false_in_and_not_in(self):
        cases=(("PRESENT",{"Group/Source":"x"},ConditionResult.TRUE),("ABSENT",{"Group/Source":None},ConditionResult.TRUE),
               ("TRUE",{"Group/Source":True},ConditionResult.TRUE),("FALSE",{"Group/Source":False},ConditionResult.TRUE),
               ("IN",{"Group/Source":"A"},ConditionResult.TRUE),("NOT_IN",{"Group/Source":"C"},ConditionResult.TRUE))
        for operator,values,result in cases:
            with self.subTest(operator=operator):
                self.assertEqual(self.evaluator.evaluate(self.rule(operator,values=("A","B")),values),result)

    def test_conditional_show_hide_enable_disable_and_required(self):
        hidden=self.evaluator.project(self.form.fields,(self.rule(effect="SHOW"),),{"Group/Source":"no"})
        self.assertNotIn("Group/Target",[item.path for item in self.evaluator.walk(hidden.fields)])
        shown=self.evaluator.project(self.form.fields,(self.rule(effect="SHOW"),),{"Group/Source":"yes"})
        target=next(item for item in self.evaluator.walk(shown.fields) if item.path=="Group/Target")
        self.assertTrue(target.conditional_machine_evaluable)
        required=self.evaluator.project(self.form.fields,(self.rule(effect="REQUIRE"),),{"Group/Source":"yes"})
        self.assertTrue(next(item for item in self.evaluator.walk(required.fields) if item.path=="Group/Target").required)
        disabled=self.evaluator.project(self.form.fields,(self.rule(effect="ENABLE"),),{"Group/Source":"no"})
        self.assertFalse(next(item for item in self.evaluator.walk(disabled.fields) if item.path=="Group/Target").editable)
        hidden_by_hide=self.evaluator.project(self.form.fields,(self.rule(effect="HIDE"),),{"Group/Source":"yes"})
        self.assertIn("Group/Target",hidden_by_hide.hidden_paths)

    def test_unknown_condition_remains_visible(self):
        result=self.evaluator.project(self.form.fields,(self.rule(),),{})
        self.assertIn("Group/Target",[item.path for item in self.evaluator.walk(result.fields)])

    def test_conditional_required_validation_uses_same_evaluator(self):
        rule=self.rule(effect="REQUIRE")
        self.assertEqual(self.evaluator.validation_issues((rule,),{"Group/Source":"yes"})[0].code,"CONDITIONAL_REQUIRED")
        self.assertFalse(self.evaluator.validation_issues((rule,),{"Group/Source":"no"}))

    def test_hidden_filled_and_repeatable_values_are_never_deleted(self):
        values={"Group/Source":"no","Group/Target":["one","two"]}
        repeatable_target=field("Group/Target",repeatable=True)
        form=FormDefinition("P","T","M","R","1","OK",None,(field("Group",children=(self.source,repeatable_target),policy="GROUP"),))
        self.evaluator.project(form.fields,(self.rule(),),values)
        self.assertEqual(values["Group/Target"],["one","two"])

    def test_filters_run_after_conditions_and_search_does_not_activate_hidden_field(self):
        service=FieldVisibilityFilter();rule=self.rule()
        result=service.apply(self.form,mode=FormDisplayMode.ALL,query="Target",values={"Group/Source":"no"},
                             conditional_rules=(rule,),condition_evaluator=self.evaluator)
        self.assertNotIn("Group/Target",result.visible_paths)
        self.assertEqual(result.conditionally_hidden_search_paths,("Group/Target",))

    def test_diagnostic_reveal_and_dependency_index(self):
        rule=self.rule();service=FieldVisibilityFilter()
        result=service.apply(self.form,values={"Group/Source":"no"},reveal_paths=("Group/Target",),
                             conditional_rules=(rule,),condition_evaluator=self.evaluator)
        self.assertIn("Group/Target",result.visible_paths)
        self.assertEqual(self.evaluator.dependency_index((rule,)),{"Group/Source":(rule,)})
        self.assertEqual(self.evaluator.evaluate_affected("Group/Source",{"Group/Source":(rule,)},{"Group/Source":"yes"}),{rule:ConditionResult.TRUE})

    def test_draft_roundtrip_preserves_hidden_conditional_value(self):
        with tempfile.TemporaryDirectory() as directory:
            service=DraftService(Path(directory));path=Path(directory)/"conditional.eaeudraft.json"
            values={"Group/Source":"no","Group/Target":"preserve me"}
            document=service.new_document(process_code="P",process_version="1",transaction_code="T",message_code="M",
                structure_id="R",structure_version="1",generation_mode="TEST",values=values)
            service.save_draft(document,path)
            self.assertEqual(service.load_draft(path).values,values)


class ConditionalCompilerTests(unittest.TestCase):
    def test_compiler_accepts_only_explicit_traced_structured_metadata(self):
        compiler=ConditionalRuleCompiler()
        text_only=({"rule_id":"TEXT","condition":"если X, заполнить Y"},)
        self.assertFalse(compiler.compile(text_only,fallback_source_refs=("SRC",)))
        structured=({"rule_id":"C-1","condition":"Structured condition","conditional_rule":{
            "target_field_path":"Target","source_field_path":"Source","operator":"EQUALS",
            "expected_value":"A","effect":"REQUIRE"}},)
        rule=compiler.compile(structured,fallback_source_refs=("SRC",))[0]
        self.assertEqual((rule.target_field_path,rule.operator,rule.effect),("Target","EQUALS","REQUIRE"))
        self.assertEqual(rule.source_refs,("SRC",))
        self.assertFalse(compiler.compile(structured))


if __name__=="__main__":unittest.main()
