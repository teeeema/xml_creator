from pathlib import Path
import unittest

from eaeu_xml.application import EaeuXmlApplication, FieldView, FormDefinition
from eaeu_xml.application.services import TestDataGenerator
from eaeu_xml.presentation import GuiController


def field(path, *, required=False, children=(), repeatable=False, conditional=False,
          fixed=None, datatype="StringType"):
    return FieldView(
        path, path.rsplit("/", 1)[-1], path.rsplit("/", 1)[-1],
        "Описание", "ELEMENT", datatype, required, 1 if required else 0,
        None if repeatable else 1, False, repeatable, fixed_value=fixed,
        children=tuple(children), ui_input_policy="GROUP" if children else "USER_INPUT",
        normative_input_policy="CONDITIONAL" if conditional else "USER_INPUT",
    )


class RequiredFormDataTests(unittest.TestCase):
    def test_conflicted_message_never_erases_existing_user_values(self):
        form = FormDefinition("P", "T", "M", "R", None, "NORMATIVE_CONFLICT", None,
                              (field("Required", required=True),))
        self.assertEqual(TestDataGenerator().generate(form, mode="required",
                                                      existing_values={"User": "keep"}), {"User": "keep"})

    def test_required_pattern_without_valid_example_is_not_fabricated(self):
        from dataclasses import replace
        constrained = replace(field("Code", required=True), pattern="[0-9]{8}", example_value=None)
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (constrained,))
        self.assertNotIn("Code", TestDataGenerator().generate(form, mode="required"))

    def test_unconditional_rule_cardinality_adds_only_minimum_instances(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Group", children=(field("Group/Child", required=True),)),
            field("Unrelated"),
        ))
        rule = {"kind": "cardinality", "target": "Group", "min_occurs": 1,
                "applies_to_structure": "R"}
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=(rule,))
        self.assertEqual(generated["Group"], [None])
        self.assertEqual(generated["Group/Child"], "TEST")
        self.assertNotIn("Unrelated", generated)
        self.assertEqual(TestDataGenerator().generate(form, mode="required", structured_rules=(rule,),
                                                      existing_values={"Group/Child": "USER"})["Group/Child"], "USER")

    def test_only_required_tree_preserves_values_and_is_idempotent(self):
        form = FormDefinition("P", "T", "P.TEST.MSG.001", "R.001", "1.0", "OK", None, (
            field("Required", required=True, repeatable=True, children=(
                field("Required/Child", required=True),
                field("Required/Optional"),
                field("Required/Conditional", required=True, conditional=True),
            )),
            field("OptionalParent", children=(field("OptionalParent/Child", required=True),)),
            field("OptionalFixed", fixed="FIXED"),
        ))
        generator = TestDataGenerator()
        values = generator.generate(form, mode="required")
        self.assertEqual(values["Required/Child"], "TEST")
        self.assertEqual(values["Required"], [None])
        self.assertNotIn("Required/Optional", values)
        self.assertNotIn("Required/Conditional", values)
        self.assertNotIn("OptionalParent/Child", values)
        self.assertNotIn("OptionalFixed", values)
        self.assertEqual(generator.generate(form, mode="required", existing_values=values), values)
        edited = generator.generate(form, mode="required", existing_values={"Required/Child": "USER"})
        self.assertEqual(edited["Required/Child"], "USER")

    def test_message_specific_codes_and_valid_xml(self):
        app = EaeuXmlApplication(Path(__file__).parents[2])
        controller = GuiController(app)
        controller.select_process("P.MM.01")
        message = "P.MM.01.MSG.005"
        transaction = next(item.transaction_code for item in controller.transactions
                           if any(m.message_code == message for m in app.list_messages("P.MM.01", item.transaction_code)))
        controller.select_transaction(transaction)
        controller.select_message(message)
        count = controller.apply_required_data()
        self.assertGreater(count, 0)
        self.assertEqual(controller.values["EDocHeader/InfEnvelopeCode"], message)
        self.assertEqual(controller.values["EDocHeader/EDocCode"], "R.007")
        self.assertNotIn("EDocHeader/EDocRefId", controller.values)
        self.assertEqual(controller.apply_required_data(), 0)
        self.assertTrue(controller.generate_xml().success)

    def test_existing_user_identifier_survives_button(self):
        app = EaeuXmlApplication(Path(__file__).parents[2])
        controller = GuiController(app)
        controller.select_process("P.MM.01")
        message = "P.MM.01.MSG.005"
        transaction = next(item.transaction_code for item in controller.transactions
                           if any(m.message_code == message for m in app.list_messages("P.MM.01", item.transaction_code)))
        controller.select_transaction(transaction)
        controller.select_message(message)
        controller.set_values({**controller.values, "EDocHeader/EDocId": "user-id"})
        controller.apply_required_data()
        self.assertEqual(controller.values["EDocHeader/EDocId"], "user-id")

    def test_required_subset_creates_xml_for_other_locally_complete_messages(self):
        app = EaeuXmlApplication(Path(__file__).parents[2])
        controller = GuiController(app)
        for process, message in (("P.SP.02", "P.SP.02.MSG.022"),
                                 ("P.SP.03", "P.SP.03.MSG.001")):
            with self.subTest(message=message):
                controller.select_process(process)
                transaction = next(item.transaction_code for item in controller.transactions
                                   if any(m.message_code == message for m in app.list_messages(process, item.transaction_code)))
                controller.select_transaction(transaction)
                controller.select_message(message)
                controller.apply_required_data()
                self.assertTrue(controller.generate_xml().success)


if __name__ == "__main__":
    unittest.main()
