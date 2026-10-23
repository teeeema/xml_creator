"""Regression tests for independently selectable OP26 normative versions."""
import unittest
import json
import shutil
from tempfile import TemporaryDirectory
from pathlib import Path

from eaeu_xml.core.errors import (
    ProcessDefinitionNotFoundError,
    ProcessPackageFormatError,
    ProcessPackageValidationError,
)
from eaeu_xml.process_packages import EaeuXmlEngine, GenerationMode, ProcessPackageLoader, ProcessRegistry
from eaeu_xml.process_packages.versioning import load_process_version


PACKAGE = Path(__file__).resolve().parents[2] / "P.MM.01_OP_26"
FIXTURE = Path(__file__).parent / "fixtures" / "P.TEST.01"


class VersionGateRegressionTests(unittest.TestCase):
    """Synthetic editions prove infrastructure, never normative readiness."""

    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve() / "package"
        shutil.copytree(FIXTURE, self.root)
        self.selected = self.root / "versions" / "1.3.0"
        shutil.copytree(FIXTURE, self.selected)
        profile = self.selected / "version_profiles" / "current.yaml"
        data = json.loads(profile.read_text())
        data["process_version"] = "1.3.0"
        profile.write_text(json.dumps(data))
        self.metadata = {"process_code": "P.TS.01", "target_version": "1.3.0",
                         "state": "VERIFIED_READY", "promotion_allowed": True}
        self.write_status()

    def write_status(self):
        (self.selected / "migration_status.json").write_text(json.dumps(self.metadata))

    def test_verified_selection_is_independent_and_legacy_default_survives(self):
        legacy = load_process_version(self.root)
        selected = load_process_version(self.root, version="1.3.0")
        self.assertEqual(selected.path, self.selected)
        self.assertEqual(selected.profile.process_version, "1.3.0")
        self.assertNotEqual(legacy.path, selected.path)
        self.assertIsNot(legacy.messages, selected.messages)
        self.assertEqual(load_process_version(self.root).profile, legacy.profile)

    def test_registry_rechecks_revoked_cached_edition(self):
        registry = ProcessRegistry(self.root.parent)
        registry.get_process("P.TS.01", version="1.3.0")
        self.metadata["promotion_allowed"] = False
        self.write_status()
        with self.assertRaises(ProcessPackageValidationError):
            registry.get_process("P.TS.01", version="1.3.0")
        self.assertNotEqual(registry.get_process("P.TS.01").profile.process_version, "1.3.0")

    def test_directly_indexed_edition_cannot_bypass_revocation_as_default(self):
        registry = ProcessRegistry(self.root / "versions")
        selected = registry.get_process("P.TS.01")
        self.metadata["promotion_allowed"] = False
        self.write_status()
        with self.assertRaises(ProcessPackageValidationError):
            registry.get_process("P.TS.01")
        with self.assertRaises(ProcessPackageValidationError):
            load_process_version(self.selected, legacy_package=selected)

    def test_generation_uses_selected_structure_and_rules_without_legacy_leakage(self):
        structure_path = self.selected / "structures/R.TEST.001/2.0.0.yaml"
        structure = json.loads(structure_path.read_text())
        structure["namespace"] = "urn:test:selected-edition"
        structure_path.write_text(json.dumps(structure))
        rule_path = self.selected / "message_rules/P.TS.01.MSG.001.yaml"
        rules = json.loads(rule_path.read_text())
        rules["fixed_values"]["Items/@code"] = "SELECTED"
        rule_path.write_text(json.dumps(rules))
        for version, namespace, code in ((None, "urn:test:structure:v2.0.0", "FIXED"),
                                         ("1.3.0", "urn:test:selected-edition", "SELECTED"),
                                         (None, "urn:test:structure:v2.0.0", "FIXED")):
            with self.subTest(version=version):
                engine = EaeuXmlEngine.load_process(self.root, version=version)
                root = engine.build_body("P.TS.01.MSG.001", {"Items": {"Name": ["A", "B"]}},
                                         mode=GenerationMode.TEST).serialize_xml_element()
                self.assertEqual(root.tag, f"{{{namespace}}}TestPayload")
                self.assertEqual(list(root)[0].attrib["code"], code)

    def test_engine_rechecks_readiness_before_generation(self):
        engine = EaeuXmlEngine.load_process(self.root, version="1.3.0")
        self.metadata["state"] = "DRAFT_NOT_READY"
        self.write_status()
        with self.assertRaises(ProcessPackageValidationError) as error:
            engine.build_body("P.TS.01.MSG.001", {})
        self.assertEqual(error.exception.code, "PROCESS_VERSION_NOT_READY")

    def test_direct_loader_checks_passport_process_and_profile_identity(self):
        for key, value in (("process_code", "P.OTHER.01"), ("target_version", "9.9.9")):
            with self.subTest(key=key):
                original = self.metadata[key]
                self.metadata[key] = value
                self.write_status()
                with self.assertRaises(ProcessPackageValidationError):
                    ProcessPackageLoader.load(self.selected)
                self.metadata[key] = original
        self.write_status()
        profile = self.selected / "version_profiles" / "current.yaml"
        data = json.loads(profile.read_text())
        data["process_version"] = "1.1.0"
        profile.write_text(json.dumps(data))
        with self.assertRaises(ProcessPackageValidationError):
            ProcessPackageLoader.load(self.selected)

    def test_relocated_draft_with_passport_remains_blocked(self):
        target = Path(self.temporary.name) / "relocated"
        shutil.copytree(self.selected, target)
        status = target / "migration_status.json"
        data = json.loads(status.read_text())
        data["promotion_allowed"] = False
        status.write_text(json.dumps(data))
        with self.assertRaises(ProcessPackageValidationError):
            ProcessPackageLoader.load(target)

    def test_versioned_catalog_cannot_link_legacy_manifests(self):
        manifest = self.selected / "messages.yaml"
        manifest.unlink()
        manifest.symlink_to(self.root / "messages.yaml")
        with self.assertRaises(ProcessPackageValidationError):
            load_process_version(self.root, version="1.3.0")

    def test_malformed_passports_fail_closed(self):
        for value in ([], None, {**self.metadata, "promotion_allowed": "true"}):
            with self.subTest(value=value):
                (self.selected / "migration_status.json").write_text(json.dumps(value))
                with self.assertRaises(ProcessPackageValidationError):
                    ProcessPackageLoader.load(self.selected)

    def test_invalid_registry_version_has_domain_error(self):
        registry = ProcessRegistry(self.root.parent)
        for value in ([], {}, 130, True):
            with self.subTest(value=value):
                with self.assertRaises(ProcessDefinitionNotFoundError):
                    registry.get_process("P.TS.01", version=value)

    def test_profile_cannot_escape_catalog(self):
        manifest = self.selected / "process.yaml"
        data = json.loads(manifest.read_text())
        data["active_profile"] = "../../version_profiles/current"
        manifest.write_text(json.dumps(data))
        with self.assertRaises(ProcessPackageValidationError) as error:
            ProcessPackageLoader.load(self.selected)
        self.assertEqual(error.exception.code, "INVALID_ACTIVE_PROFILE")

    def test_malformed_selected_manifest_is_rejected(self):
        (self.selected / "messages.yaml").write_text("[]")
        with self.assertRaises(ProcessPackageFormatError) as error:
            load_process_version(self.root, version="1.3.0")
        self.assertEqual(error.exception.code, "MANIFEST_OBJECT_REQUIRED")

    def test_versions_root_cannot_be_redirected(self):
        versions = self.root / "versions"
        external = Path(self.temporary.name).resolve() / "external"
        versions.rename(external)
        versions.symlink_to(external, target_is_directory=True)
        with self.assertRaises(ProcessDefinitionNotFoundError):
            load_process_version(self.root, version="1.3.0")


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
        with self.assertRaises(ProcessPackageValidationError) as loader:
            ProcessPackageLoader.load(PACKAGE / "versions" / "1.3.0")
        self.assertEqual(loader.exception.code, "PROCESS_VERSION_NOT_READY")
        with self.assertRaises(ProcessPackageValidationError) as engine:
            EaeuXmlEngine.load_process(PACKAGE, version="1.3.0")
        self.assertEqual(engine.exception.code, "PROCESS_VERSION_NOT_READY")
        with self.assertRaises(ProcessPackageValidationError) as by_path:
            EaeuXmlEngine.load_process(PACKAGE / "versions" / "1.3.0")
        self.assertEqual(by_path.exception.code, "PROCESS_VERSION_NOT_READY")
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
