"""Regression tests for independently selectable OP26 normative versions."""
import unittest
from pathlib import Path

from eaeu_xml.core.errors import (
    ProcessDefinitionNotFoundError,
    ProcessPackageValidationError,
)
from eaeu_xml.process_packages import EaeuXmlEngine, ProcessPackageLoader, ProcessRegistry
from eaeu_xml.process_packages.versioning import load_process_version


PACKAGE = Path(__file__).resolve().parents[2] / "P.MM.01_OP_26"


class Op26VersionSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.legacy = ProcessPackageLoader.load(PACKAGE)

    def test_default_and_explicit_legacy_version(self):
        for requested in (None, "1.1.0"):
            with self.subTest(version=requested):
                selected = load_process_version(PACKAGE, version=requested)
                self.assertEqual(selected.profile.process_version, "1.1.0")
                self.assertEqual(len(selected.messages), 28)
                self.assertEqual(len(selected.transactions), 19)

    def test_engine_default_is_legacy(self):
        self.assertEqual(EaeuXmlEngine.load_process(PACKAGE).package.profile.process_version, "1.1.0")
        self.assertEqual(EaeuXmlEngine.load_process(PACKAGE, version="1.1.0").package.profile.process_version, "1.1.0")

    def test_unverified_130_is_blocked_in_every_selector(self):
        with self.assertRaises(ProcessPackageValidationError) as direct:
            load_process_version(PACKAGE, version="1.3.0")
        self.assertEqual(direct.exception.code, "PROCESS_VERSION_NOT_READY")
        with self.assertRaises(ProcessPackageValidationError) as engine:
            EaeuXmlEngine.load_process(PACKAGE, version="1.3.0")
        self.assertEqual(engine.exception.code, "PROCESS_VERSION_NOT_READY")
        registry = ProcessRegistry.__new__(ProcessRegistry)
        registry._packages = {"P.MM.01": self.legacy}
        registry._version_packages = {}
        registry.shared_structures = {}
        with self.assertRaises(ProcessPackageValidationError) as registry_result:
            registry.get_process("P.MM.01", version="1.3.0")
        self.assertEqual(registry_result.exception.code, "PROCESS_VERSION_NOT_READY")
        self.assertEqual(registry.get_process("P.MM.01").profile.process_version, "1.1.0")

    def test_unknown_or_unsafe_version_is_never_a_fallback(self):
        for requested in ("9.9.9", "../1.3.0", "current", "", "/tmp"):
            with self.subTest(version=requested):
                with self.assertRaises(ProcessDefinitionNotFoundError) as error:
                    load_process_version(PACKAGE, version=requested)
                self.assertEqual(error.exception.code, "PROCESS_VERSION_NOT_FOUND")


if __name__ == "__main__":
    unittest.main()
