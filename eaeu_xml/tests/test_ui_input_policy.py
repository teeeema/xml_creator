import unittest

from eaeu_xml.process_packages.input_policy import ResolvedFieldInputPolicy
from eaeu_xml.process_packages.models import SourceReference, UiInputPolicyDefinition
from eaeu_xml.process_packages.ui_input_policy import UiInputPolicyResolver


class UiInputPolicyResolverTests(unittest.TestCase):
    def setUp(self): self.resolver = UiInputPolicyResolver()

    def normative(self, policy):
        return ResolvedFieldInputPolicy(policy, "UNKNOWN", False, True)

    def resolve(self, policy, **kwargs):
        return self.resolver.resolve(normative=self.normative(policy), explicit=kwargs.get("explicit"),
                                     forbidden=kwargs.get("forbidden", False),
                                     classifier_dataset_available=kwargs.get("classifier", False))

    def test_normative_unresolved_uses_project_ui_default(self):
        result = self.resolve("UNRESOLVED_INPUT_POLICY")
        self.assertEqual((result.ui_input_policy, result.policy_origin, result.editable),
                         ("USER_INPUT", "PROJECT_UI_DEFAULT", True))
        self.assertEqual(self.normative("UNRESOLVED_INPUT_POLICY").input_policy, "UNRESOLVED_INPUT_POLICY")

    def test_classifier_with_dataset_is_select(self):
        self.assertEqual(self.resolve("CLASSIFIER", classifier=True).ui_input_policy, "USER_SELECT")

    def test_classifier_without_dataset_uses_test_input_fallback(self):
        self.assertEqual(self.resolve("CLASSIFIER").ui_input_policy, "USER_INPUT")

    def test_automatic_sources_are_read_only(self):
        for policy in ("AUTO_FIXED", "AUTO_GENERATED", "AUTO_DATETIME", "CORRELATION"):
            with self.subTest(policy=policy): self.assertEqual(self.resolve(policy).ui_input_policy, "READ_ONLY")

    def test_container_is_group(self):
        self.assertEqual(self.resolve("STRUCTURAL_CONTAINER").ui_input_policy, "GROUP")

    def test_external_system_is_not_editable(self):
        result = self.resolve("EXTERNAL_SYSTEM")
        self.assertEqual((result.ui_input_policy, result.editable), ("EXTERNAL_SYSTEM", False))

    def test_conditional_is_not_blindly_user_input(self):
        self.assertEqual(self.resolve("CONDITIONAL").ui_input_policy, "UNRESOLVED_UI_POLICY")

    def test_explicit_override_wins(self):
        source = SourceReference("TEST", "TEST_FIXTURE_ONLY", "ui", "TEST_ONLY")
        override = UiInputPolicyDefinition("P.T.MSG.1", "Value", "HIDDEN", "MANUAL_OVERRIDE", "fixture", (source,))
        result = self.resolve("UNRESOLVED_INPUT_POLICY", explicit=override)
        self.assertEqual((result.ui_input_policy, result.policy_origin), ("HIDDEN", "MANUAL_OVERRIDE"))

    def test_forbidden_is_hidden(self):
        self.assertEqual(self.resolve("UNRESOLVED_INPUT_POLICY", forbidden=True).ui_input_policy, "HIDDEN")


if __name__ == "__main__": unittest.main()
