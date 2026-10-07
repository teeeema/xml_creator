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
    def test_for_each_can_extend_owner_already_selected_by_descendant_rule(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Root", required=True, children=(
                field("Root/Owner", children=(
                    field("Root/Owner/Status"),
                    field("Root/Owner/Needed"),
                )),
            )),
        ))
        rules = (
            {"kind": "presence", "target": "Root/Owner/Status", "state": "REQUIRED",
             "applies_to_structure": "R"},
            {"kind": "for_each", "selector": {"collection": "Root/Owner"},
             "assertions": [{"kind": "presence", "target": {"field": "Needed"},
                              "state": "REQUIRED"}],
             "applies_to_structure": "R"},
        )
        generated = TestDataGenerator().generate(form, structured_rules=rules)
        self.assertEqual(generated["Root/Owner/Status"], "TEST")
        self.assertEqual(generated["Root/Owner/Needed"], "TEST")

    def test_nested_for_each_runs_when_optional_ancestor_is_selected_by_descendant(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Root", children=(
                field("Root/Items", repeatable=True, children=(
                    field("Root/Items/Kind"),
                    field("Root/Items/RequiredByRule"),
                )),
            )),
        ))
        rules = (
            {"kind": "selection_cardinality", "selector": {"collection": "Root/Items", "where": {
                "field": "Kind", "operator": "IN", "value": ["A", "B"]}}, "min_occurs": 1},
            {"kind": "for_each", "selector": {"collection": "Root/Items"}, "assertions": (
                {"kind": "fixed_value", "target": {"field": "RequiredByRule"}, "value": "FIXED"},
            )},
        )
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=rules)
        self.assertEqual(generated["Root/Items/Kind"], ["A"])
        self.assertEqual(generated["Root/Items/RequiredByRule"], "FIXED")

    def test_condition_any_count_materializes_one_allowed_collection(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Payment", required=True, children=(
                field("Payment/Bank", repeatable=True, children=(
                    field("Payment/Bank/Id", required=True),
                )),
                field("Payment/System", repeatable=True, children=(
                    field("Payment/System/Id", required=True),
                )),
            )),
        ))
        rule = {
            "kind": "for_each",
            "selector": {"collection": "Payment"},
            "assertions": [{"kind": "condition", "condition": {"any": [
                {"count": {"collection": "Payment/Bank"}, "operator": "GE", "value": 1},
                {"count": {"collection": "Payment/System"}, "operator": "GE", "value": 1},
            ]}}],
            "applies_to_structure": "R",
        }
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=(rule,))
        self.assertIn("Payment/Bank", generated)
        self.assertIn("Payment/Bank/Id", generated)
        self.assertNotIn("Payment/System", generated)

    def test_for_each_in_comparison_materializes_selected_leaf(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Items", required=True, repeatable=True, children=(
                field("Items/Code"),
            )),
        ))
        rule = {
            "kind": "for_each",
            "selector": {"collection": "Items"},
            "assertions": [{
                "kind": "comparison",
                "left": {"field": "Code"},
                "operator": "IN",
                "right_value": ["10", "20"],
            }],
            "applies_to_structure": "R",
        }
        generated = TestDataGenerator().generate(form, structured_rules=(rule,))
        self.assertEqual(generated["Items/Code"], "10")

    def test_for_each_in_comparison_accepts_string_left(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Items", required=True, repeatable=True, children=(
                field("Items/Code"),
            )),
        ))
        rule = {
            "kind": "for_each",
            "selector": {"collection": "Items"},
            "assertions": [{
                "kind": "comparison",
                "left": "Code",
                "operator": "IN",
                "right_value": ["10", "20"],
            }],
            "applies_to_structure": "R",
        }
        generated = TestDataGenerator().generate(form, structured_rules=(rule,))
        self.assertEqual(generated["Items/Code"], "10")

    def test_for_each_any_condition_chooses_one_safe_non_null_branch(self):
        from dataclasses import replace

        safe_name = replace(field("Items/Name"), example_value="Example name")
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Items", required=True, repeatable=True, children=(
                field("Items/Code"),
                safe_name,
            )),
        ))
        rule = {
            "kind": "for_each",
            "selector": {"collection": "Items"},
            "assertions": [{
                "kind": "condition",
                "condition": {"any": [
                    {"field": "Code", "operator": "NE", "value": None},
                    {"field": "Name", "operator": "NE", "value": None},
                ]},
            }],
            "applies_to_structure": "R",
        }
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=(rule,))
        self.assertNotIn("Items/Code", generated)
        self.assertEqual(generated["Items/Name"], "Example name")

    def test_for_each_any_condition_can_materialize_complex_non_null_branch(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Payment", children=(
                field("Payment/Bank", children=(
                    field("Payment/Bank/Id", required=True),
                )),
                field("Payment/System", children=(
                    field("Payment/System/Id", required=True),
                )),
            )),
        ))
        rules = (
            {"kind": "presence", "target": "Payment", "state": "REQUIRED",
             "applies_to_structure": "R"},
            {
                "kind": "for_each",
                "selector": {"collection": "Payment"},
                "assertions": [{
                    "kind": "condition",
                    "condition": {"any": [
                        {"field": "Bank", "operator": "NE", "value": None},
                        {"field": "System", "operator": "NE", "value": None},
                    ]},
                }],
                "applies_to_structure": "R",
            },
        )
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=rules)
        self.assertEqual(generated["Payment"], "")
        self.assertEqual(generated["Payment/Bank"], "")
        self.assertEqual(generated["Payment/Bank/Id"], "TEST")
        self.assertNotIn("Payment/System", generated)

    def test_for_each_conditional_fixed_value_updates_only_matching_instances(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Items", repeatable=True, children=(
                field("Items/Status"),
                field("Items/Code"),
                field("Items/Name"),
            )),
        ))
        rules = (
            {"kind": "selection_cardinality", "selector": {"collection": "Items", "where": {
                "field": "Status", "operator": "EQ", "value": "A"}}, "min_occurs": 1},
            {"kind": "selection_cardinality", "selector": {"collection": "Items", "where": {
                "field": "Status", "operator": "EQ", "value": "B"}}, "min_occurs": 1},
            {"kind": "for_each", "selector": {"collection": "Items", "where": {
                "field": "Status", "operator": "EQ", "value": "A"}}, "assertions": ({
                    "kind": "conditional_fixed_value",
                    "condition": {"field": "Code", "operator": "EQ", "value": None},
                    "target": {"field": "Name"}, "value": "Name A",
                },)},
            {"kind": "for_each", "selector": {"collection": "Items", "where": {
                "field": "Status", "operator": "EQ", "value": "B"}}, "assertions": ({
                    "kind": "conditional_fixed_value",
                    "condition": {"field": "Code", "operator": "EQ", "value": None},
                    "target": {"field": "Name"}, "value": "Name B",
                },)},
        )
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=rules)
        self.assertEqual(generated["Items/Status"], ["A", "B"])
        self.assertEqual(generated["Items/Name"], ["Name A", "Name B"])
        self.assertNotIn("Items/Code", generated)

    def test_for_each_datetime_comparison_completes_selected_instances(self):
        from dataclasses import replace

        start = replace(field("Items/Period/Start"), datatype="DateTimeType",
                        example_value="2026-01-01T00:00:00")
        end = replace(field("Items/Period/End"), datatype="DateTimeType",
                      example_value="2026-01-01T00:00:00")
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Items", repeatable=True, children=(
                field("Items/Status"),
                field("Items/Period", children=(start, end)),
            )),
        ))
        rules = (
            {"kind": "selection_cardinality", "selector": {"collection": "Items", "where": {
                "field": "Status", "operator": "EQ", "value": "A"}}, "min_occurs": 1},
            {"kind": "for_each", "selector": {"collection": "Items", "where": {
                "field": "Status", "operator": "EQ", "value": "A"}}, "assertions": ({
                    "kind": "comparison", "left": {"field": "Period/End"}, "operator": "GT",
                    "right": {"field": "Period/Start"}, "value_type": "DATETIME",
                },)},
        )
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=rules)
        self.assertEqual(generated["Items/Period/Start"], ["2026-01-01T00:00:00"])
        self.assertEqual(generated["Items/Period/End"], ["2026-01-01T00:00:01"])

    def test_for_each_cross_selected_equality_completes_both_operands(self):
        from dataclasses import replace

        old_id = replace(field("Items/OldId"), example_value="ID-1")
        new_id = replace(field("Items/NewId"), example_value="ID-1")
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Items", repeatable=True, children=(
                field("Items/Status"), old_id, new_id,
            )),
        ))
        rules = (
            {"kind": "selection_cardinality", "selector": {"collection": "Items", "where": {
                "field": "Status", "operator": "EQ", "value": "OLD"}}, "min_occurs": 1},
            {"kind": "selection_cardinality", "selector": {"collection": "Items", "where": {
                "field": "Status", "operator": "EQ", "value": "NEW"}}, "min_occurs": 1},
            {"kind": "for_each", "selector": {"collection": "Items", "where": {
                "field": "Status", "operator": "EQ", "value": "NEW"}}, "assertions": ({
                    "kind": "comparison", "left": {"field": "NewId"}, "operator": "EQ",
                    "right": {"selector": {"collection": "Items", "where": {
                        "field": "Status", "operator": "EQ", "value": "OLD"}}, "field": "OldId"},
                },)},
        )
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=rules)
        self.assertEqual(generated["Items/OldId"], ["ID-1", None])
        self.assertEqual(generated["Items/NewId"], [None, "ID-1"])

    def test_selection_cardinality_in_chooses_first_allowed_value(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Items", repeatable=True, children=(field("Items/Kind"),)),
        ))
        rule = {
            "kind": "selection_cardinality",
            "selector": {"collection": "Items", "where": {
                "field": "Kind", "operator": "IN", "value": ["AP", "PA", "RE"]}},
            "min_occurs": 1,
            "max_occurs": 1,
        }
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=(rule,))
        self.assertEqual(generated["Items"], [None])
        self.assertEqual(generated["Items/Kind"], ["AP"])

    def test_for_each_required_target_accepts_absolute_field_path(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Owner", required=True, children=(
                field("Owner/Child", children=(field("Owner/Child/Value"),)),
            )),
        ))
        rule = {
            "kind": "for_each",
            "selector": {"collection": "Owner"},
            "assertions": [{
                "kind": "presence",
                "target": {"field": "Owner/Child"},
                "state": "REQUIRED",
            }],
        }
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=(rule,))
        self.assertIn("Owner/Child", generated)
        self.assertNotIn("Owner/Owner/Child", generated)

    def test_conditional_presence_required_treats_missing_condition_field_as_none(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Items", required=True, repeatable=True, children=(
                field("Items/Code"),
                field("Items/Name"),
            )),
        ))
        rule = {
            "kind": "conditional_presence",
            "scope": {"collection": "Items"},
            "condition": {"field": "Code", "operator": "EQ", "value": None},
            "target": {"field": "Name"},
            "state": "REQUIRED",
            "applies_to_structure": "R",
        }
        generated = TestDataGenerator().generate(form, structured_rules=(rule,))
        self.assertEqual(generated["Items"], [None])
        self.assertEqual(generated["Items/Name"], ["TEST"])

    def test_scoped_rule_can_target_top_level_field(self):
        from dataclasses import replace

        name = replace(field("Name"), example_value="Example")
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Header", required=True, children=(field("Header/Id", required=True),)),
            field("Code"),
            name,
        ))
        rules = (
            {"kind": "conditional_presence", "scope": {"collection": "Header"},
             "condition": {"field": "Code", "operator": "EQ", "value": None},
             "target": {"field": "Name"}, "state": "REQUIRED"},
            {"kind": "for_each", "selector": {"collection": "Header", "where": {
                "field": "Code", "operator": "EQ", "value": None}}, "assertions": ({
                    "kind": "comparison", "left": "Name", "operator": "IN",
                    "right_value": ["Allowed A", "Allowed B"],
                },)},
        )
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=rules)
        self.assertEqual(generated["Name"], "Allowed A")
        self.assertNotIn("Header/Name", generated)

    def test_scoped_forbidden_ne_null_does_not_create_missing_top_level_target(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Header", required=True, children=(field("Header/Id", required=True),)),
            field("Code"),
            field("OtherId"),
        ))
        rule = {
            "kind": "conditional_presence",
            "scope": {"collection": "Header"},
            "condition": {"field": "Code", "operator": "NE", "value": None},
            "target": {"field": "OtherId"},
            "state": "FORBIDDEN",
        }
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=(rule,))
        self.assertNotIn("Code", generated)
        self.assertNotIn("OtherId", generated)

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

    def test_for_each_fixed_value_updates_only_selected_repeatable_instance(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Group", repeatable=True, children=(field("Group/Type"),)),
        ))
        rules = (
            {"kind": "selection_cardinality", "selector": {"collection": "Group", "where": {
                "field": "Type", "operator": "EQ", "value": "A"}}, "min_occurs": 1, "max_occurs": 1},
            {"kind": "selection_cardinality", "selector": {"collection": "Group", "where": {
                "field": "Type", "operator": "EQ", "value": "B"}}, "min_occurs": 1, "max_occurs": 1},
            {"kind": "for_each", "selector": {"collection": "Group", "where": {
                "field": "Type", "operator": "EQ", "value": "A"}}, "assertions": (
                {"kind": "fixed_value", "target": {"field": "Type"}, "value": "A"},
            )},
        )
        generated = TestDataGenerator().generate(form, structured_rules=rules)
        self.assertEqual(generated["Group/Type"], ["A", "B"])

    def test_required_group_presence_is_aligned_to_each_selected_owner(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Party", repeatable=True, children=(
                field("Party/Role"),
                field("Party/Address", repeatable=True, children=(field("Party/Address/City"),)),
            )),
        ))
        rules = (
            {"kind": "selection_cardinality", "selector": {"collection": "Party", "where": {
                "field": "Role", "operator": "EQ", "value": "RH"}}, "min_occurs": 1},
            {"kind": "selection_cardinality", "selector": {"collection": "Party", "where": {
                "field": "Role", "operator": "EQ", "value": "UE"}}, "min_occurs": 1},
            {"kind": "for_each", "selector": {"collection": "Party"}, "assertions": (
                {"kind": "presence", "target": {"field": "Address"}, "state": "REQUIRED"},
            )},
        )
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=rules)
        self.assertEqual(generated["Party/Role"], ["RH", "UE"])
        self.assertEqual(generated["Party/Address"], ["", ""])

    def test_required_nested_groups_are_materialized_after_parent_contexts_appear(self):
        form = FormDefinition("P", "T", "M", "R", "1.0", "OK", None, (
            field("Party", repeatable=True, children=(
                field("Party/Role"),
                field("Party/Address", repeatable=True, children=(
                    field("Party/Address/Country", children=(field("Party/Address/Country/Code"),)),
                )),
            )),
        ))
        rules = (
            {"kind": "selection_cardinality", "selector": {"collection": "Party", "where": {
                "field": "Role", "operator": "EQ", "value": "RH"}}, "min_occurs": 1},
            {"kind": "selection_cardinality", "selector": {"collection": "Party", "where": {
                "field": "Role", "operator": "EQ", "value": "UE"}}, "min_occurs": 1},
            # Intentionally before the rule that creates the second Address context.
            {"kind": "for_each", "selector": {"collection": "Party/Address"}, "assertions": (
                {"kind": "presence", "target": {"field": "Country"}, "state": "REQUIRED"},
            )},
            {"kind": "for_each", "selector": {"collection": "Party"}, "assertions": (
                {"kind": "presence", "target": {"field": "Address"}, "state": "REQUIRED"},
            )},
        )
        generated = TestDataGenerator().generate(form, mode="required", structured_rules=rules)
        self.assertEqual(generated["Party/Address"], ["", ""])
        self.assertEqual(generated["Party/Address/Country"], ["", ""])

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
