from pathlib import Path

from eaeu_xml.core.errors import ProcessDefinitionNotFoundError
from eaeu_xml.decision5.models.action import ApplicationAction
from eaeu_xml.services.action_builder import ActionBuilder
from eaeu_xml.process_packages.body import GenerationMode, StructuredProcessBodyProvider, ProcessBodyProvider
from eaeu_xml.process_packages.loader import ProcessPackageLoader
from eaeu_xml.process_packages.models import MessageDefinition, ProcessPackage, StructureDefinition, TransactionDefinition
from eaeu_xml.process_packages.resolver import StructureVersionResolver


class EaeuXmlEngine:
    def __init__(self, package: ProcessPackage, body_provider: ProcessBodyProvider | None = None) -> None:
        self.package = package
        self.body_provider = body_provider or StructuredProcessBodyProvider(package)
        self.process = package.process
        self.procedures = package.procedures
        self.operations = package.operations
        self.participants = package.participants
        self.transactions = package.transactions
        self.messages = package.messages
        self.structures = package.structures
        self.rules = package.rules
        self.structure_version_resolver = StructureVersionResolver(package)

    @classmethod
    def load_process(cls, process_package_path: Path, *, body_provider: ProcessBodyProvider | None = None) -> "EaeuXmlEngine":
        return cls(ProcessPackageLoader.load(process_package_path), body_provider)

    def get_transaction(self, code: str) -> TransactionDefinition:
        try:
            return self.transactions[code]
        except KeyError as error:
            raise ProcessDefinitionNotFoundError(code="TRANSACTION_NOT_FOUND", message=f"Транзакция не найдена: {code}") from error

    def get_operation(self, code: str):
        try:
            return self.operations[code]
        except KeyError as error:
            raise ProcessDefinitionNotFoundError(code="OPERATION_NOT_FOUND", message=f"Операция не найдена: {code}") from error

    def get_message(self, code: str) -> MessageDefinition:
        try:
            return self.messages[code]
        except KeyError as error:
            raise ProcessDefinitionNotFoundError(code="MESSAGE_NOT_FOUND", message=f"Сообщение не найдено: {code}") from error

    def get_structure(self, message_code: str, *, mode: GenerationMode = GenerationMode.STRICT) -> StructureDefinition:
        message = self.get_message(message_code)
        if not message.structure_id:
            raise ProcessDefinitionNotFoundError(code="MESSAGE_STRUCTURE_UNDEFINED", message=f"Для {message_code} структура не задана.")
        return self.resolve_structure(message.structure_id,mode=mode).definition

    def resolve_structure(self, structure_id: str, *, mode: GenerationMode = GenerationMode.STRICT):
        return self.structure_version_resolver.resolve(structure_id,mode=mode)

    def get_active_structure_version(self, structure_id: str) -> StructureDefinition:
        return self.structure_version_resolver.get_active_structure_version(structure_id)

    def build_application_action(self, transaction_code: str, message_code: str) -> ApplicationAction:
        transaction = self.get_transaction(transaction_code)
        self.get_message(message_code)
        if not self.package.profile.process_version:
            raise ProcessDefinitionNotFoundError(code="PROCESS_VERSION_UNDEFINED", message="Active profile не задаёт process_version.")
        return ActionBuilder().build_application(
            process_code=self.process.process_code, process_version=self.package.profile.process_version,
            procedure_code=transaction.procedure_code, transaction_code=transaction.transaction_code,
            message_code=message_code,
        )

    def validate_body(self, message_code: str, values: dict, *, mode: GenerationMode = GenerationMode.STRICT):
        message = self.get_message(message_code)
        structure = self.get_structure(message_code,mode=mode)
        validator = getattr(self.body_provider, "validate_body", None)
        if validator is None:
            raise ProcessDefinitionNotFoundError(code="BODY_VALIDATION_NOT_SUPPORTED", message="Body provider не поддерживает validation.")
        return validator(message, structure, values, mode=mode)

    def build_body(self, message_code: str, values: dict, *, mode: GenerationMode = GenerationMode.STRICT):
        message = self.get_message(message_code)
        structure = self.get_structure(message_code,mode=mode)
        return self.body_provider.build_body(message, structure, values, mode=mode)
