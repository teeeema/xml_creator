from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from eaeu_xml.application.base64_service import Base64Service


class Base64ServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = Base64Service()

    def test_roundtrip_empty_binary_unicode_padding_and_whitespace(self):
        samples = (
            b"",
            bytes(range(256)),
            "Привет, Base64 😀".encode("utf-8"),
            b"padding-required",
        )
        for source in samples:
            with self.subTest(size=len(source)):
                encoded = self.service.encode_bytes(source)
                wrapped = f"  \n{encoded[:8]}\n{encoded[8:]}\t "
                self.assertEqual(self.service.decode_text(wrapped).data, source)

    def test_encode_file_reports_name_and_sizes(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "sample.bin"
            source = b"\x00\xff\x10example"
            path.write_bytes(source)
            result = self.service.encode_file(path)
        self.assertEqual(result.name, "sample.bin")
        self.assertEqual(result.source_size, len(source))
        self.assertEqual(result.encoded_size, len(result.text))
        self.assertEqual(self.service.decode_text(result.text).data, source)

    def test_invalid_base64_is_rejected_strictly(self):
        for value in ("%%%%", "abcd*efg", "YWJj===bad"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.service.decode_text(value)

    def test_common_format_hint_is_informational(self):
        encoded = self.service.encode_bytes(b"%PDF-1.7\nbody")
        self.assertEqual(self.service.decode_text(encoded).format_hint, "PDF")

    def test_large_payload_smoke_1mb_and_10mb(self):
        for size in (1_000_000, 10_000_000):
            source = (b"\x00\xffBase64-smoke" * ((size // 14) + 1))[:size]
            encoded = self.service.encode_bytes(source)
            self.assertEqual(self.service.decode_text(encoded).data, source)


if __name__ == "__main__":
    unittest.main()

