from pathlib import Path
from datetime import date, datetime
from decimal import Decimal
import re
import unittest
from uuid import UUID

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.presentation.field_help import resolve_field_help


class FieldHelpAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = EaeuXmlApplication(Path(__file__).parents[2])
        cls.fields = []

        def walk(fields):
            for field in fields:
                if field.visibility != "HIDDEN":
                    yield field
                    yield from walk(field.children)

        for process in app.list_processes():
            for transaction in app.list_transactions(process.process_code):
                for message in app.list_messages(process.process_code, transaction.transaction_code):
                    form = app.get_form(process.process_code, transaction.transaction_code, message.message_code)
                    cls.fields.extend(walk(form.fields))

    def test_every_visible_field_has_human_help(self):
        self.assertGreater(len(self.fields), 20_000)
        for field in self.fields:
            with self.subTest(path=field.path):
                help_info = resolve_field_help(field, unconditionally_required=field.required)
                self.assertTrue(help_info.purpose.strip())
                self.assertTrue(help_info.what_to_enter.strip())
                self.assertTrue(help_info.example.strip())

    def test_no_generic_placeholder_examples(self):
        placeholder = re.compile(r"^\[(?:идентификатор|значение|код|текст|дата|номер)(?:\]|\s)", re.I)
        for field in self.fields:
            self.assertFalse(placeholder.match(str(field.example_value)), field.path)

    def test_available_examples_respect_local_patterns_and_enums(self):
        for field in self.fields:
            if field.example_value is None:
                continue
            with self.subTest(path=field.path):
                if field.pattern:
                    self.assertRegex(str(field.example_value), rf"\A(?:{field.pattern})\Z")
                if field.allowed_values and field.example_origin == "ALLOWED_VALUE":
                    self.assertIn(field.example_value, field.allowed_values)

    def test_datatype_examples_parse_as_their_declared_type(self):
        for field in self.fields:
            if field.example_origin != "DATATYPE_EXAMPLE" or field.example_value is None:
                continue
            datatype = (field.datatype or "").casefold()
            value = str(field.example_value)
            with self.subTest(path=field.path):
                if "uuid" in datatype or "universallyuniqueid" in datatype:
                    UUID(value)
                elif "datetime" in datatype:
                    datetime.fromisoformat(value)
                elif datatype.endswith("datetype") or datatype == "date":
                    date.fromisoformat(value)
                elif "decimal" in datatype:
                    Decimal(value)
                elif "indicator" in datatype or "boolean" in datatype:
                    self.assertIn(value, {"true", "false"})


if __name__ == "__main__":
    unittest.main()
