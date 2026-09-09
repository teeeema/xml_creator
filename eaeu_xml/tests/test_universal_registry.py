import json
from pathlib import Path
import shutil
import tempfile
import unittest

from eaeu_xml.core.errors import (
    DuplicateProcessCodeError,
    ProcessDefinitionNotFoundError,
    ProcessPackageValidationError,
    StructureResolutionError,
)
from eaeu_xml.process_packages import (
    MessageDefinition,
    ProcessPackageLoader,
    ProcessRegistry,
    StructureDefinition,
    StructureResolver,
)


FIXTURE = Path(__file__).parent / "fixtures" / "P.TEST.01"


def rewrite_json(path: Path, transform) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    transform(data)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def replace_tree_strings(value, old: str, new: str):
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [replace_tree_strings(item, old, new) for item in value]
    if isinstance(value, dict):
        return {key: replace_tree_strings(item, old, new) for key, item in value.items()}
    return value


class UniversalRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def add_process(self, directory: str, code: str) -> Path:
        target = self.root / directory
        shutil.copytree(FIXTURE, target)
        for manifest in target.rglob("*.yaml"):
            rewrite_json(manifest, lambda data, c=code: data.clear() or data.update(
                replace_tree_strings(json.loads(manifest.read_text(encoding="utf-8")), "P.TS.01", c)
            ))
        return target

    def make_shared_only(self, process: Path) -> None:
        messages = process / "messages.yaml"
        rewrite_json(messages, lambda data: [item.update(structure_id="R.TEST.001", structure_version="2.0.0")
                                              for item in data["messages"]])
        shutil.rmtree(process / "structures" / "R.TEST.001")

    def install_shared_structure(self) -> None:
        target = self.root / "shared" / "structures" / "R.TEST.001"
        target.mkdir(parents=True)
        shutil.copy2(FIXTURE / "structures" / "R.TEST.001" / "2.0.0.yaml", target / "2.0.0.yaml")

    def test_registry_loads_two_arbitrary_processes_and_versions(self):
        self.add_process("first", "P.ONE.01")
        self.add_process("second", "P.TWO.01")
        registry = ProcessRegistry(self.root)
        self.assertEqual([item.process.process_code for item in registry.list_processes()],
                         ["P.ONE.01", "P.TWO.01"])
        self.assertEqual(registry.get_process("P.TWO.01").process.process_code, "P.TWO.01")
        self.assertEqual(registry.get_process("P.ONE.01", version="1.0").profile.process_version, "1.0")
        with self.assertRaises(ProcessDefinitionNotFoundError):
            registry.get_process("P.UNKNOWN.01")
        with self.assertRaises(ProcessDefinitionNotFoundError):
            registry.get_process("P.ONE.01", version="9.9.9")

    def test_duplicate_process_code_is_rejected(self):
        self.add_process("first", "P.ONE.01")
        self.add_process("second", "P.ONE.01")
        with self.assertRaises(DuplicateProcessCodeError) as raised:
            ProcessRegistry(self.root)
        self.assertEqual(raised.exception.code, "DUPLICATE_PROCESS_CODE")

    def test_shared_structure_is_reused_by_two_processes(self):
        self.install_shared_structure()
        first = self.add_process("first", "P.ONE.01")
        second = self.add_process("second", "P.TWO.01")
        self.make_shared_only(first)
        self.make_shared_only(second)
        registry = ProcessRegistry(self.root)
        resolver = StructureResolver()
        a = resolver.resolve(process=registry.get_process("P.ONE.01"),
                             structure_code="R.TEST.001", version="2.0.0")
        b = resolver.resolve(process=registry.get_process("P.TWO.01"),
                             structure_code="R.TEST.001", version="2.0.0")
        self.assertIs(a, b)
        with self.assertRaises(StructureResolutionError):
            resolver.resolve(process=registry.get_process("P.ONE.01"),
                             structure_code="R.TEST.001", version="")

    def test_local_shared_collision_requires_explicit_source(self):
        self.install_shared_structure()
        process = self.add_process("first", "P.ONE.01")
        with self.assertRaises(ProcessPackageValidationError) as raised:
            ProcessRegistry(self.root)
        self.assertEqual(raised.exception.code, "AMBIGUOUS_STRUCTURE_SOURCE")
        profile = process / "version_profiles" / "current.yaml"
        rewrite_json(profile, lambda data: data["structures"]["R.TEST.001"].update(source="local"))
        package = ProcessRegistry(self.root).get_process("P.ONE.01")
        self.assertEqual(StructureResolver().resolve(process=package,
                         structure_code="R.TEST.001", version="2.0.0").namespace,
                         "urn:test:structure:v2.0.0")
        shared = self.root / "shared" / "structures" / "R.TEST.001" / "2.0.0.yaml"
        rewrite_json(shared, lambda data: data.update(namespace="urn:test:shared:v2.0.0"))
        rewrite_json(profile, lambda data: data["structures"]["R.TEST.001"].update(source="shared"))
        shared_package = ProcessRegistry(self.root).get_process("P.ONE.01")
        self.assertEqual(StructureResolver().resolve(process=shared_package,
                         structure_code="R.TEST.001", version="2.0.0").namespace,
                         "urn:test:shared:v2.0.0")

    def test_many_messages_share_one_definition_and_message_is_not_structure(self):
        process = self.add_process("first", "P.ONE.01")
        messages = process / "messages.yaml"
        rewrite_json(messages, lambda data: [item.update(structure_id="R.TEST.001", structure_version="2.0.0")
                                              for item in data["messages"]])
        package = ProcessPackageLoader.load(process)
        self.assertEqual(len(package.structures), 2)  # two versions, one normative structure code
        self.assertEqual({item.structure_id for item in package.messages.values()}, {"R.TEST.001"})
        self.assertFalse(issubclass(MessageDefinition, StructureDefinition))

    def test_one_response_message_can_be_used_by_two_transactions(self):
        process = self.add_process("first", "P.ONE.01")
        transactions = process / "transactions.yaml"
        def add_transaction(data):
            second = dict(data["transactions"][0])
            second["transaction_code"] = "P.ONE.01.TRN.002"
            data["transactions"].append(second)
        rewrite_json(transactions, add_transaction)
        package = ProcessPackageLoader.load(process)
        response = "P.ONE.01.MSG.002"
        self.assertEqual(sum(response in item.response_messages for item in package.transactions.values()), 2)
        self.assertFalse(hasattr(package.messages[response], "transaction_id"))


if __name__ == "__main__":
    unittest.main()
