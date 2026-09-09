from pathlib import Path
from random import Random
from uuid import UUID
from xml.etree import ElementTree as ET

from eaeu_xml.application.models import FieldView, FormDefinition, ProcessView
from eaeu_xml.core.errors import ProcessPackageError
from eaeu_xml.process_packages.loader import ProcessPackageLoader


class ProcessDiscoveryService:
    """Discovers valid packages below an explicit caller-owned root."""

    def discover_processes(self, root: Path) -> tuple[ProcessView, ...]:
        if not isinstance(root, Path):
            raise TypeError("processes_root must be pathlib.Path")
        if not root.is_dir():
            return ()
        results = []
        for path in sorted((item for item in root.iterdir() if item.is_dir()), key=lambda item: item.name):
            if not all((path / name).is_file() for name in ProcessPackageLoader.REQUIRED_FILES):
                continue
            try:
                package = ProcessPackageLoader.load(path)
            except ProcessPackageError:
                continue
            results.append(ProcessView(package.process.process_code, package.process.name,
                                       package.profile.process_version, package.process.status, package.path,
                                       package.process.normative_document_number))
        return tuple(results)


class TestDataGenerator:
    """Creates reproducible minimal values from a public FormDefinition."""

    def generate(self, form: FormDefinition, *, seed: int = 0) -> dict[str, object]:
        if form.generation_status == "NORMATIVE_CONFLICT":
            return {}
        random = Random(seed)
        result: dict[str, object] = {}

        def explicitly_required(field: FieldView) -> bool:
            return any(hint == "message_rule=REQUIRED" for hint in field.validation_hints)

        def should_include(field: FieldView) -> bool:
            return field.required or field.fixed_value is not None or any(
                explicitly_required(child) or child.fixed_value is not None or any_explicit_descendant(child)
                for child in field.children
            )

        def any_explicit_descendant(field: FieldView) -> bool:
            return any(explicitly_required(child) or child.fixed_value is not None or any_explicit_descendant(child)
                       for child in field.children)

        def visit(field: FieldView) -> None:
            if field.visibility == "HIDDEN" or not should_include(field):
                return
            if field.children:
                if field.ui_input_policy == "GROUP":
                    result[field.path] = [None] * field.min_occurs if field.repeatable and (field.min_occurs or 0) > 1 else None
                else:
                    value = field.fixed_value if field.fixed_value is not None else self._value(field, random)
                    result[field.path] = [value] * field.min_occurs if field.repeatable and (field.min_occurs or 0) > 1 else value
                for child in field.children:
                    visit(child)
                return
            value = field.fixed_value if field.fixed_value is not None else self._value(field, random)
            result[field.path] = [value] * field.min_occurs if field.repeatable and (field.min_occurs or 0) > 1 else value

        for field in form.fields:
            visit(field)
        for field in self._walk(form.fields):
            if field.path not in result:
                continue
            if field.xml_name == "InfEnvelopeCode": result[field.path] = form.message_code
            elif field.xml_name == "EDocCode": result[field.path] = form.structure_id
        return result

    @classmethod
    def _walk(cls, fields):
        for field in fields:
            yield field
            yield from cls._walk(field.children)

    @staticmethod
    def _value(field: FieldView, random: Random):
        if field.input_policy == "AUTO_GENERATED" and field.value_source == "GENERATED_UUID":
            return str(UUID(int=random.getrandbits(128), version=4))
        datatype = (field.datatype or "").lower()
        if datatype == "any_xml": return ET.Element("{urn:test:external}Payload")
        if "uuid" in datatype:return str(UUID(int=random.getrandbits(128),version=4))
        if "indicator" in datatype or "boolean" in datatype:return True
        if "datetime" in datatype:return "2026-08-24T00:00:00"
        if datatype.endswith("datetype") or datatype=="date":return "2026-08-24"
        local_type=datatype.rsplit(":",1)[-1]
        if "identifier" in datatype or "idtype" in datatype or (local_type.startswith("id") and local_type.endswith("type")):return "TEST"
        if "decimal" in datatype or "paymentamount" in datatype:return "10.50"
        if "quantity" in datatype or "integer" in datatype or "number" in datatype:return 1
        if field.classifier: return "TEST_CLASSIFIER_PLACEHOLDER"
        return "TEST"

    @staticmethod
    def example_value(*, datatype: str | None, xml_name: str | None, classifier: str | None = None):
        """Stable non-normative example used by presentation clients."""
        from eaeu_xml.application.examples import ExampleValueResolver
        return ExampleValueResolver().resolve(datatype=datatype,description=None,classifier=bool(classifier)).value
