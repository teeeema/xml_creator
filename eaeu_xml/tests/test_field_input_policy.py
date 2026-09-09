import unittest

from eaeu_xml.process_packages.input_policy import FieldInputPolicyResolver
from eaeu_xml.process_packages.models import FieldInputPolicyDefinition, MessageRules, SourceReference, StructureFieldDefinition


class FieldInputPolicyResolverTests(unittest.TestCase):
    def setUp(self):
        self.resolver = FieldInputPolicyResolver()
        self.source = SourceReference("TEST", "TEST_FIXTURE_ONLY", "field policy", "TEST_ONLY")

    def field(self, *, path="Value", kind="ELEMENT", classifier=None):
        return StructureFieldDefinition("F1", 1, 0, None, path, "Value", "Value", None, kind, "StringType", None, 0, 1,
                                        classifier_ref=classifier, source_refs=(self.source,))

    def resolve(self, field=None, rules=None, explicit=None, children=False):
        return self.resolver.resolve(message_code="P.T.MSG.001", field=field or self.field(), rules=rules,
                                     explicit=explicit, has_children=children)

    def explicit(self, policy, source, **kwargs):
        return FieldInputPolicyDefinition("P.T.MSG.001", "Value", policy, source, source_refs=(self.source,), **kwargs)

    def test_fixed_is_auto_fixed_and_can_be_required(self):
        rules = MessageRules("P.T.MSG.001", "R.T", {"Value": "X"}, {"Value": "REQUIRED"})
        result = self.resolve(rules=rules)
        self.assertEqual((result.input_policy, result.value_source, result.editable), ("AUTO_FIXED", "MESSAGE_METADATA", False))

    def test_classifier_is_classifier(self):
        self.assertEqual(self.resolve(field=self.field(classifier="TEST")).input_policy, "CLASSIFIER")

    def test_explicit_generated_uuid(self):
        result = self.resolve(explicit=self.explicit("AUTO_GENERATED", "GENERATED_UUID"))
        self.assertEqual((result.input_policy, result.editable), ("AUTO_GENERATED", False))

    def test_explicit_correlation(self):
        self.assertEqual(self.resolve(explicit=self.explicit("CORRELATION", "PREVIOUS_BODY")).input_policy, "CORRELATION")

    def test_explicit_conditional_keeps_condition(self):
        result = self.resolve(explicit=self.explicit("CONDITIONAL", "USER", condition_description="if X", condition_ref="R1"))
        self.assertEqual((result.input_policy, result.condition_ref), ("CONDITIONAL", "R1"))

    def test_optional_user_input_is_editable(self):
        result = self.resolve(explicit=self.explicit("USER_INPUT", "USER"))
        self.assertTrue(result.editable)

    def test_complex_container_is_not_editable(self):
        result = self.resolve(children=True)
        self.assertEqual((result.input_policy, result.editable), ("STRUCTURAL_CONTAINER", False))

    def test_attribute_uses_explicit_policy(self):
        result = self.resolve(field=self.field(kind="ATTRIBUTE"), explicit=self.explicit("USER_INPUT", "USER"))
        self.assertTrue(result.editable)

    def test_unknown_is_unresolved(self):
        result = self.resolve()
        self.assertEqual((result.input_policy, result.value_source, result.editable),
                         ("UNRESOLVED_INPUT_POLICY", "UNKNOWN", False))


if __name__ == "__main__":
    unittest.main()
