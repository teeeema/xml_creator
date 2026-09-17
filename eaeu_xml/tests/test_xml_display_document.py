import unittest

from eaeu_xml.gui_qt.xml_display_document import (
    ENCODED_PAYLOAD_THRESHOLD,
    LARGE_TEXT_THRESHOLD,
    VISIBLE_PREFIX_LENGTH,
    CompactSyncError,
    ProtectedMarker,
    XmlDisplayDocument,
)


class XmlDisplayDocumentTests(unittest.TestCase):
    def test_threshold_is_character_count_and_large_payload_is_not_in_display(self):
        natural = ("обычный текст с пробелами и пунктуацией. " * 400)
        exact = (natural * 2)[:LARGE_TEXT_THRESHOLD]
        over = (natural * 2)[: LARGE_TEXT_THRESHOLD + 1]

        exact_document = XmlDisplayDocument(f"<root><data>{exact}</data></root>")
        self.assertFalse(exact_document.has_large_nodes)
        self.assertIn(exact, exact_document.compact_xml)

        over_document = XmlDisplayDocument(f"<root><data>{over}</data></root>")
        self.assertTrue(over_document.has_large_nodes)
        self.assertNotIn(over, over_document.compact_xml)
        self.assertIn(over[:VISIBLE_PREFIX_LENGTH] + "… ⟪скрыто 9 991 символов⟫", over_document.compact_xml)

    def test_encoded_payload_boundary_and_supported_alphabets(self):
        base64_pattern = "MIIGQAYJKoZIhvcNAQcCoIIGMTCCBi0CAQExDjAMBg+/="
        base64url_pattern = "AbCdEf0123456789-_"

        def payload(pattern: str, size: int) -> str:
            return (pattern * ((size // len(pattern)) + 1))[:size]

        below = payload(base64_pattern, ENCODED_PAYLOAD_THRESHOLD - 1)
        below_document = XmlDisplayDocument(f"<root><value>{below}</value></root>")
        self.assertFalse(below_document.has_large_nodes)
        self.assertIn(below, below_document.compact_xml)

        for size in (200, 500, 5_000, 10_000):
            encoded = payload(base64_pattern, size)
            document = XmlDisplayDocument(f"<root><value>{encoded}</value></root>")
            self.assertTrue(document.has_large_nodes, size)
            self.assertEqual(document.hidden_nodes[0].character_count, size)
            self.assertIn(
                encoded[:VISIBLE_PREFIX_LENGTH]
                + f"… ⟪скрыто {size - VISIBLE_PREFIX_LENGTH:,} символов⟫".replace(",", " "),
                document.compact_xml,
            )
            self.assertNotIn(encoded, document.compact_xml)

        url_encoded = payload(base64url_pattern, 500)
        url_document = XmlDisplayDocument(f"<root><value>{url_encoded}</value></root>")
        self.assertTrue(url_document.has_large_nodes)
        self.assertTrue(url_document.compact_xml.startswith("<root><value>AbCdEf0123…"))

    def test_certificate_like_payload_is_compacted_without_successful_decode_requirement(self):
        prefix = "MIIGQAYJKoZIhvcNAQcCoIIGMTCCBi0CAQExDjAMBg"
        payload = (prefix + ("AbCdEf0123456789+/=" * 20))[:257] + "..."
        document = XmlDisplayDocument(f"<root><anything>{payload}</anything></root>")

        self.assertTrue(document.has_large_nodes)
        self.assertIn("MIIGQAYJKo… ⟪скрыто 250 символов⟫", document.compact_xml)
        self.assertEqual(document.full_xml, f"<root><anything>{payload}</anything></root>")

    def test_natural_language_over_200_is_not_mistaken_for_encoded_payload(self):
        examples = (
            "Это обычное русское описание XML документа, содержащее слова, пробелы и пунктуацию. " * 5,
            "This is ordinary English prose describing an XML document with words, spaces, and punctuation. " * 5,
            "A normal sentence has spaces; commas, periods, questions? and other punctuation! " * 5,
            "XML description: this field contains a human-readable explanation of the document and its purpose. " * 5,
        )
        for text in examples:
            self.assertGreater(len(text), ENCODED_PAYLOAD_THRESHOLD)
            self.assertLessEqual(len(text), LARGE_TEXT_THRESHOLD)
            document = XmlDisplayDocument(f"<root><description>{text}</description></root>")
            self.assertFalse(document.has_large_nodes, text[:40])
            self.assertIn(text, document.compact_xml)

    def test_500k_and_1m_payloads_have_small_compact_representation(self):
        for size in (500_000, 1_000_000):
            payload = "X" * size
            full_xml = f"<Document><Code>123</Code><BinaryData>{payload}</BinaryData></Document>"
            document = XmlDisplayDocument(full_xml)

            self.assertEqual(document.full_xml, full_xml)
            self.assertEqual(len(document.hidden_nodes), 1)
            self.assertEqual(document.hidden_nodes[0].character_count, size)
            self.assertLess(len(document.compact_xml), 200)
            self.assertNotIn(payload[:1000], document.compact_xml)
            self.assertIn(
                "X" * VISIBLE_PREFIX_LENGTH
                + f"… ⟪скрыто {size - VISIBLE_PREFIX_LENGTH:,} символов⟫".replace(",", " "),
                document.compact_xml,
            )

    def test_multiple_same_named_and_namespace_nodes_keep_distinct_payloads(self):
        first = "A" * 12_000
        second = "Б" * 13_000
        source = (
            '<ns:root xmlns:ns="urn:test">'
            '<ns:BinaryData id="first">' + first + "</ns:BinaryData>"
            '<ns:BinaryData id="second">' + second + "</ns:BinaryData>"
            "<ns:Code>123</ns:Code>"
            "</ns:root>"
        )
        document = XmlDisplayDocument(source)
        self.assertEqual(len(document.hidden_nodes), 2)
        self.assertNotEqual(document.hidden_nodes[0].node_id, document.hidden_nodes[1].node_id)

        edited = document.compact_xml.replace("<ns:Code>123</ns:Code>", "<ns:Code>456</ns:Code>")
        full = document.commit_compact(edited, document.protected_markers())
        self.assertIn(first, full)
        self.assertIn(second, full)
        self.assertIn("<ns:Code>456</ns:Code>", full)
        self.assertNotIn("⟪скрыто", full)

    def test_comments_cdata_entities_unicode_whitespace_empty_and_attributes_survive(self):
        cdata_payload = ("строка 😀\n" * 1300) + "END"
        text_payload = ("A&amp;B" * 4000) + "TAIL"
        source = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<root xmlns="urn:test" attr="keep">\n'
            "  <!-- comment -->\n"
            "  <cdata><![CDATA[" + cdata_payload + "]]></cdata>\n"
            "  <encoded>" + text_payload + "</encoded>\n"
            "  <empty/>\n"
            "  <code>123 &amp; 456</code>\n"
            "</root>"
        )
        document = XmlDisplayDocument(source)
        self.assertEqual(len(document.hidden_nodes), 2)

        edited = document.compact_xml.replace("<code>123 &amp; 456</code>", "<code>789 &amp; 456</code>")
        full = document.commit_compact(edited, document.protected_markers())
        self.assertIn("<!-- comment -->", full)
        self.assertIn("<![CDATA[" + cdata_payload + "]]>", full)
        self.assertIn(text_payload, full)
        self.assertIn('<root xmlns="urn:test" attr="keep">', full)
        self.assertIn("<empty/>", full)
        self.assertIn("<code>789 &amp; 456</code>", full)

    def test_shifted_marker_can_commit_edit_before_hidden_node(self):
        payload = "Z" * 20_000
        document = XmlDisplayDocument(
            f"<root><Code>123</Code><BinaryData>{payload}</BinaryData></root>"
        )
        original_marker = document.protected_markers()[0]
        old_prefix = "<Code>123</Code>"
        new_prefix = "<Code>456789</Code>"
        edited = document.compact_xml.replace(old_prefix, new_prefix)
        delta = len(new_prefix) - len(old_prefix)
        shifted_marker = ProtectedMarker(
            original_marker.node_id,
            original_marker.start + delta,
            original_marker.end + delta,
        )

        full = document.commit_compact(edited, (shifted_marker,))
        self.assertIn(new_prefix, full)
        self.assertIn(payload, full)
        self.assertNotIn("⟪скрыто", full)

    def test_corrupt_or_missing_marker_is_fail_safe(self):
        payload = "P" * 20_000
        source = f"<root><BinaryData>{payload}</BinaryData></root>"
        document = XmlDisplayDocument(source)
        original_full = document.full_xml
        marker = document.protected_markers()[0]

        with self.assertRaises(CompactSyncError):
            document.commit_compact(document.compact_xml, ())
        self.assertEqual(document.full_xml, original_full)

        damaged = document.compact_xml[: marker.start] + "BROKEN" + document.compact_xml[marker.end :]
        damaged_marker = ProtectedMarker(marker.node_id, marker.start, marker.start + len("BROKEN"))
        with self.assertRaises(CompactSyncError):
            document.commit_compact(damaged, (damaged_marker,))
        self.assertEqual(document.full_xml, original_full)

        injected = document.compact_xml.replace(
            "</root>",
            "<note>⟪скрыто 99 999 символов⟫</note></root>",
        )
        with self.assertRaises(CompactSyncError):
            document.commit_compact(injected, document.protected_markers())
        self.assertEqual(document.full_xml, original_full)

    def test_diagnostic_inside_large_payload_maps_to_placeholder(self):
        payload = "A\n" * 6000
        source = "<root>\n  <before>1</before>\n  <data>" + payload + "</data>\n  <after>2</after>\n</root>"
        document = XmlDisplayDocument(source)
        node = document.hidden_nodes[0]

        hidden_line = source.count("\n", 0, node.full_start) + 100
        display_line, display_column = document.full_line_column_to_display(hidden_line, 1)
        placeholder_line = document.compact_xml.count("\n", 0, node.display_start) + 1
        self.assertEqual(display_line, placeholder_line)
        self.assertGreaterEqual(display_column, 1)

        after_full_line = source.count("\n", 0, source.index("<after>")) + 1
        after_display_line, _ = document.full_line_column_to_display(after_full_line, 1)
        expected_after_line = document.compact_xml.count("\n", 0, document.compact_xml.index("<after>")) + 1
        self.assertEqual(after_display_line, expected_after_line)

    def test_invalid_xml_stays_full_and_compaction_is_disabled(self):
        source = "<root><data>" + ("A" * 20_000)
        document = XmlDisplayDocument(source)
        self.assertFalse(document.has_large_nodes)
        self.assertEqual(document.full_xml, source)
        self.assertEqual(document.compact_xml, source)
        self.assertTrue(document.parse_error)


if __name__ == "__main__":
    unittest.main()
