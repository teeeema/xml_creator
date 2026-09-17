from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

try:
    from PySide6.QtTest import QSignalSpy
    from PySide6.QtWidgets import QApplication
except (ImportError, ModuleNotFoundError):
    QApplication = None


@unittest.skipUnless(QApplication is not None, "PySide6 GUI extra is not installed")
class Base64UtilityModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        from eaeu_xml.gui_qt.base64_model import Base64UtilityModel

        self.model = Base64UtilityModel()

    def _wait(self, action, timeout=5000):
        spy = QSignalSpy(self.model.operationFinished)
        action()
        if spy.count() == 0:
            self.assertTrue(spy.wait(timeout))
        self.app.processEvents()

    def test_encode_preview_copy_save_decode_and_save_use_full_payload(self):
        source = (b"binary\x00\xff" * 200_000)[:1_000_000]
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / "source.bin"
            text_path = root / "encoded.txt"
            restored_path = root / "restored.bin"
            source_path.write_bytes(source)

            self._wait(lambda: self.model.encodeFile(str(source_path)))
            full = self.model.full_encoded_text()
            self.assertEqual(self.model.encodedFileName, "source.bin")
            self.assertTrue(self.model.canTogglePreview)
            self.assertTrue(self.model.encodedPreview.startswith(full[:10] + "… ⟪скрыто "))
            self.assertNotEqual(self.model.encodedPreview, full)

            self.model.copyBase64()
            self.assertEqual(QApplication.clipboard().text(), full)
            self._wait(lambda: self.model.saveBase64(str(text_path)))
            self.assertEqual(text_path.read_text(encoding="ascii"), full)

            self.model.setDecodeInput("\n".join((full[:100], full[100:])))
            self._wait(self.model.decode)
            self.assertEqual(self.model.decoded_bytes(), source)
            self._wait(lambda: self.model.saveDecoded(str(restored_path)))
            self.assertEqual(restored_path.read_bytes(), source)

    def test_invalid_decode_keeps_output_empty_and_reports_error(self):
        self.model.setDecodeInput("not valid !!!")
        self._wait(self.model.decode)
        self.assertEqual(self.model.decoded_bytes(), b"")
        self.assertFalse(self.model.hasDecodedResult)
        self.assertIn("Некорректный Base64", self.model.error)
        with TemporaryDirectory() as directory:
            output = Path(directory) / "should-not-exist.bin"
            self.model.saveDecoded(str(output))
            self.assertFalse(output.exists())

    def test_empty_file_roundtrip(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "empty.bin"
            path.write_bytes(b"")
            self._wait(lambda: self.model.encodeFile(str(path)))
            self.assertEqual(self.model.full_encoded_text(), "")
            self.model.setDecodeInput("")
            self._wait(self.model.decode)
            self.assertEqual(self.model.decoded_bytes(), b"")
            self.assertTrue(self.model.hasDecodedResult)


if __name__ == "__main__":
    unittest.main()
