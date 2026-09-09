from eaeu_xml.decision5.models.procedure import ProcedureInstance
from eaeu_xml.decision5.validation.identifier_validator import IdentifierValidator


class ProcedureValidator:
    def validate(self, procedure: ProcedureInstance) -> None:
        IdentifierValidator().validate_procedure_id(procedure.procedure_id)
