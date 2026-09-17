import unittest

from eaeu_xml.application.xml_formatter import XmlFormatter


class XmlFormatterTests(unittest.TestCase):
    def setUp(self): self.formatter = XmlFormatter()

    def test_formatting_is_idempotent_and_preserves_xml_features(self):
        source = '<?xml version="1.0"?><x:root xmlns:x="urn:test"><!-- note --><x:item id="1"><![CDATA[a < b]]></x:item></x:root>'
        once = self.formatter.format(source)
        self.assertEqual(once, self.formatter.format(once))
        self.assertIn('xmlns:x="urn:test"', once)
        self.assertIn('id="1"', once)
        self.assertIn("<!-- note -->", once)
        self.assertIn("<![CDATA[a < b]]>", once)
        self.assertTrue(once.startswith("<?xml"))

    def test_invalid_xml_raises_without_a_replacement(self):
        with self.assertRaises(Exception): self.formatter.format("<root>")


if __name__ == "__main__": unittest.main()
