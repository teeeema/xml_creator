class Decision5Error(ValueError):
    def __init__(self, *, code: str, message: str, rule_id: str | None = None) -> None:
        self.code = code
        self.rule_id = rule_id
        self.message = message
        super().__init__(message)


class AddressValidationError(Decision5Error): pass
class IdentifierValidationError(Decision5Error): pass
class ActionValidationError(Decision5Error): pass
class HeaderValidationError(Decision5Error): pass
class TransactionStateError(Decision5Error): pass
class ForbiddenHeaderFieldError(HeaderValidationError): pass
class MissingRequiredHeaderFieldError(HeaderValidationError): pass
class CorrelationError(Decision5Error): pass
class ProcedureIdError(IdentifierValidationError): pass
class SignalValidationError(Decision5Error): pass
class FaultValidationError(Decision5Error): pass
class IntegrationValidationError(Decision5Error): pass
class IntegrationOwnershipError(IntegrationValidationError): pass
class TransactionPatternError(Decision5Error): pass
class InvalidStateTransitionError(TransactionPatternError): pass
class RetryNotAllowedError(TransactionPatternError): pass
class TimeoutTransitionError(TransactionPatternError): pass
class FaultCorrelationError(FaultValidationError): pass
class ProcessPackageError(Decision5Error): pass
class ProcessPackagePathError(ProcessPackageError): pass
class ProcessPackageFormatError(ProcessPackageError): pass
class ProcessPackageValidationError(ProcessPackageError): pass
class ProcessDefinitionNotFoundError(ProcessPackageError): pass
class ProcessRegistryError(ProcessPackageError): pass
class DuplicateProcessCodeError(ProcessRegistryError): pass
class StructureResolutionError(ProcessPackageError): pass
class UnresolvedStructureVersionError(ProcessPackageError): pass
class ProcessBodyNotImplementedError(ProcessPackageError): pass
class BodyValidationError(ProcessPackageError):
    def __init__(self, *, code: str, message: str, issues=()) -> None:
        self.issues = tuple(issues)
        super().__init__(code=code, message=message)
