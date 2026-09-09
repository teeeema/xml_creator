from eaeu_xml.decision5.models.transaction import TransactionInstance
from eaeu_xml.decision5.validation.correlation_validator import CorrelationValidator
from eaeu_xml.decision5.validation.procedure_validator import ProcedureValidator


class TransactionValidator:
    def validate(self, transaction: TransactionInstance) -> None:
        ProcedureValidator().validate(transaction.procedure_instance)
        CorrelationValidator().validate_history(transaction)
