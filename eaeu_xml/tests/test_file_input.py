from base64 import b64encode
from pathlib import Path
import tempfile
import unittest

from eaeu_xml.application.file_input import FileInputService
from eaeu_xml.application import DraftService


class FileInputServiceTests(unittest.TestCase):
    def test_file_is_embedded_as_base64_without_local_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "document.txt"
            payload = "Документ".encode("utf-8")
            path.write_bytes(payload)
            result = FileInputService().load(path)
            self.assertEqual(result.value, b64encode(payload).decode("ascii"))
            self.assertEqual(result.filename, "document.txt")
            self.assertEqual(result.size, len(payload))
            self.assertEqual(result.media_type, "text/plain")
            self.assertNotIn(str(path), result.value)

    def test_unknown_mime_and_large_file_warning_are_presentation_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "content.unknown_extension"
            path.write_bytes(b"12345")
            result = FileInputService(warning_threshold=4).load(path)
            self.assertIsNone(result.media_type)
            self.assertTrue(result.exceeds_warning_threshold)

    def test_embedded_payload_survives_draft_without_source_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            encoded = b64encode(b"binary payload").decode("ascii")
            service = DraftService(root)
            document = service.new_document(
                process_code="P", process_version="1", transaction_code="T",
                message_code="M", structure_id="R", structure_version="1",
                generation_mode="TEST", values={"BinaryText": encoded},
            )
            path = root / "binary.eaeudraft.json"
            service.save_draft(document, path)
            restored = service.load_draft(path)
            self.assertEqual(restored.values["BinaryText"], encoded)
            metadata = FileInputService.restored(encoded)
            self.assertEqual(metadata.size, len(b"binary payload"))


if __name__ == "__main__":
    unittest.main()
