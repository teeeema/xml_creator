import unittest

from eaeu_xml.presentation.text_sanitizer import (
    has_presentation_garbage,
    normalize_extracted_regex,
    sanitize_presentation_text,
)


class PresentationTextSanitizerTests(unittest.TestCase):
    def test_noncharacters_are_contextually_normalized_without_mutating_input(self):
        source = "A\ufdd0B\ufdefC\ufffeD\uffffE\U0001fffeF\U0010ffffG"
        self.assertEqual(sanitize_presentation_text(source), "A-B-C-D-E-F-G")
        self.assertTrue(has_presentation_garbage(source))
        self.assertFalse(has_presentation_garbage(sanitize_presentation_text(source)))

    def test_regex_and_russian_word_keep_intended_hyphen(self):
        self.assertEqual(sanitize_presentation_text("[0-9a-fA\ufffeF]{4}"), "[0-9a-fA-F]{4}")
        self.assertEqual(
            sanitize_presentation_text("административно\ufffeтерриториального"),
            "административно-территориального",
        )

    def test_replacement_control_separator_and_invisible_artifacts_are_not_rendered(self):
        source = "A\ufffdB\x00C\u00adD\u200bE\u2028F\u00a0G"
        rendered = sanitize_presentation_text(source)
        self.assertEqual(rendered, "A-B CDE\nF G")
        self.assertFalse(has_presentation_garbage(rendered))

    def test_parser_spillover_is_removed_from_presentation_only(self):
        source = "Нормативный текст <PARSED TEXT FOR PAGE: 100 / 200> debug spillover"
        self.assertEqual(sanitize_presentation_text(source), "Нормативный текст")
        self.assertIn("<PARSED TEXT FOR PAGE", source)

    def test_op22_regex_normalization_matches_readable_rtf_patterns(self):
        self.assertEqual(
            normalize_extracted_regex(
                "[0-9a-fA-F]{8}-[0-9a-fA\ufffeF]{4}-[0-9a-fA-F]{4}-"
                "[0-9a-fA-F]{4}- [0-9a-fA-F]{12}"
            ),
            "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
        )
        self.assertEqual(
            normalize_extracted_regex("[A-Z0-9][A-Z0-9 -]{1,8}[A\ufffeZ0-9]"),
            "[A-Z0-9][A-Z0-9-]{1,8}[A-Z0-9]",
        )
        self.assertEqual(
            normalize_extracted_regex(r"\d{4}/(AM|BY|KG|KZ|RU)- \d{6}"),
            r"\d{4}/(AM|BY|KG|KZ|RU)-\d{6}",
        )
        self.assertEqual(
            normalize_extracted_regex(r"P\.[A-Z]{2}\.[0- 9]{2}\.MSG\.[0-9]{3} 1"),
            r"P\.[A-Z]{2}\.[0-9]{2}\.MSG\.[0-9]{3}",
        )


if __name__ == "__main__":
    unittest.main()
