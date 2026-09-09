from dataclasses import replace
from pathlib import Path
import unittest

from eaeu_xml.application import (
    EaeuXmlApplication, FieldView, FieldVisibilityFilter, FormDefinition,
    FormDisplayMode, IssueView,
)
from eaeu_xml.gui.controller import GuiController


FIXTURES = Path(__file__).parent / "fixtures"


def field(path, *, required=False, policy="USER_INPUT", children=(), visibility="VISIBLE"):
    return FieldView(
        path, path.rsplit("/", 1)[-1], path.rsplit("/", 1)[-1],
        f"Описание {path}", "ELEMENT", "StringType", required, 1 if required else 0,
        1, False, False, ui_input_policy=policy, visibility=visibility,
        help_text=f"Справка {path}", children=tuple(children),
    )


class FormFilterTests(unittest.TestCase):
    def setUp(self):
        self.required = field("Root/Required", required=True)
        self.optional = field("Root/Optional")
        self.read_only = field("Root/Automatic", policy="READ_ONLY")
        self.unresolved = field("Root/Unknown", policy="UNRESOLVED_UI_POLICY")
        self.group = field("Root", policy="GROUP", children=(self.required, self.optional, self.read_only, self.unresolved))
        self.hidden = field("Hidden", visibility="HIDDEN")
        self.form = FormDefinition("P", "T", "M", "R", "1.0.0", "OK", None, (self.group, self.hidden))
        self.filter = FieldVisibilityFilter()

    def paths(self, result):
        return set(result.visible_paths)

    def test_all_mode_excludes_hidden(self):
        result = self.filter.apply(self.form)
        self.assertEqual(self.paths(result), {"Root", "Root/Required", "Root/Optional", "Root/Automatic", "Root/Unknown"})

    def test_required_mode_preserves_parent_group(self):
        result = self.filter.apply(self.form, mode=FormDisplayMode.REQUIRED)
        self.assertEqual(self.paths(result), {"Root", "Root/Required"})

    def test_user_fields_mode_includes_interactive_and_unresolved(self):
        result = self.filter.apply(self.form, mode=FormDisplayMode.USER_FIELDS)
        self.assertEqual(self.paths(result), {"Root", "Root/Required", "Root/Optional", "Root/Unknown"})

    def test_errors_mode_and_empty_message(self):
        empty = self.filter.apply(self.form, mode=FormDisplayMode.ERRORS)
        self.assertEqual(empty.empty_message, "Ошибок заполнения не обнаружено.")
        issue = IssueView("REQUIRED", "Root/Optional", "required", "ERROR")
        result = self.filter.apply(self.form, mode=FormDisplayMode.ERRORS, issues=(issue,))
        self.assertEqual(self.paths(result), {"Root", "Root/Optional"})

    def test_search_display_xml_path_description_and_help(self):
        for query in ("Optional", "Root/Optional", "Описание Root/Optional", "Справка Root/Optional"):
            with self.subTest(query=query):
                result = self.filter.apply(self.form, query=query)
                self.assertEqual(self.paths(result), {"Root", "Root/Optional"})

    def test_search_composes_with_mode(self):
        result = self.filter.apply(self.form, mode=FormDisplayMode.REQUIRED, query="Optional")
        self.assertFalse(result.fields)

    def test_filled_mode_preserves_parent(self):
        result = self.filter.apply(self.form, mode=FormDisplayMode.FILLED, values={"Root/Optional": "x"})
        self.assertEqual(self.paths(result), {"Root", "Root/Optional"})


class ControllerFilterStateTests(unittest.TestCase):
    def setUp(self):
        self.controller = GuiController(EaeuXmlApplication(FIXTURES))
        self.controller.select_process("P.TS.01")

    def test_field_values_and_repeatable_state_survive_filter_switch(self):
        original = {"Items": [None, None], "Items/Name": ["one", "two"], "Items/@code": ["FIXED", "FIXED"]}
        self.controller.set_values(original)
        self.controller.set_display_mode(FormDisplayMode.USER_FIELDS)
        self.controller.update_visible_values({"Items": [None, None], "Items/Name": ["one", "two"]})
        self.controller.set_display_mode(FormDisplayMode.ALL)
        self.assertEqual(self.controller.values, original)

    def test_validation_uses_hidden_by_filter_values(self):
        values = self.controller.apply_test_data()
        self.controller.set_display_mode(FormDisplayMode.USER_FIELDS)
        self.controller.update_visible_values({"Items": None, "Items/Name": values["Items/Name"]})
        self.assertEqual(self.controller.values["Items/@code"], "FIXED")
        self.assertTrue(self.controller.validate().is_valid)

    def test_nested_repeatable_control_roundtrip_does_not_wrap_unchanged_scalars(self):
        original={"Items":None,"Items/Name":"TEST","Items/@code":"FIXED"}
        self.controller.set_values(original)
        self.controller.update_visible_values({"Items":[None],"Items/Name":[["TEST"]],"Items/@code":[["FIXED"]]})
        self.assertEqual(self.controller.values,original)

    def test_error_navigation_reveals_field_without_changing_mode(self):
        self.controller.set_display_mode(FormDisplayMode.ERRORS)
        self.controller.set_values({})
        issue = self.controller.validate().errors[0]
        self.assertTrue(self.controller.reveal_error_field(issue.field_path))
        self.assertIn(issue.field_path, self.controller.form_presentation.visible_paths)
        self.assertEqual(self.controller.display_mode, FormDisplayMode.ERRORS)

    def test_summary_is_provided_by_facade(self):
        expected = self.controller.application.get_message_input_summary(
            self.controller.process_code, self.controller.transaction_code, self.controller.message_code)
        self.assertEqual(self.controller.message_input_summary, expected)


if __name__ == "__main__":
    unittest.main()
